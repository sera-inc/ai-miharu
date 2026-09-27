# Copyright 2026 Aman Karir
# SPDX-License-Identifier: Apache-2.0
# Part of Shadow AI Guard, https://github.com/AmanSK5/shadow-ai-guard

"""Vendor user sync for the budget view.

Each provider here is a vendor whose admin API can list the members of a
paid workspace. The receiver holds the connection key (state.py, the same
recoverable-by-design trade as the log store password) and this module
spends it: one outward call per sync, against a URL hardcoded below -
never one the request supplies, so there is nothing here for a crafted
request to point somewhere else.

What a provider returns is a member list, not a judgement: email, name, the
vendor's own role string, a seat tier where the API exposes one, and any
usage counters the vendor reports. The reconciliation against what the
fleet actually does happens in the portal, against findings this module
never sees.

Providers are deliberately few and honest about what each can do:

  anthropic   Claude work orgs (Team / Enterprise). GET /v1/organizations/
              users with a scoped admin key (read:members is enough). The
              API paginates; seat tiers are not exposed, so tier stays
              blank and the operator records tiers on the subscription.
  fireflies   Fireflies.ai. One GraphQL query for the team's users, which
              also reports per-user usage (transcripts, minutes) - the
              rare vendor that hands over the usage half too.
  devin       Cognition, covering Devin and Devin Desktop (the IDE that
              was Codeium, then Windsurf). GET the org's members with a
              service-user key. Teams reaches this too, not just
              Enterprise - one of the few vendors here where that is
              true - so the wizard does not send a Teams admin to Import.

ChatGPT Business is the named absence: OpenAI exposes no admin API on
that plan (SCIM and the Compliance API are Enterprise-only), so it is a
guided CSV import in the portal, and the wizard says so rather than
pretending a connector could exist.
"""

import json
import re
import time

import httpx

# One bound for every provider: a member list bigger than this is either the
# wrong key (a reseller org?) or an API looping; both deserve a refusal
# that names the cap rather than an unbounded crawl.
MAX_MEMBERS = 5000
_TIMEOUT = 15.0

ANTHROPIC_URL = "https://api.anthropic.com/v1/organizations/users"
FIREFLIES_URL = "https://api.fireflies.ai/graphql"
OPENAI_URL = "https://api.openai.com/v1/organization/users"
CURSOR_URL = "https://api.cursor.com/teams/members"
CHATGPT_SCIM_URL = "https://api.openai.com/scim/v2"
NOTION_SCIM_URL = "https://api.notion.com/scim/v2"
GRAMMARLY_SCIM_URL = "https://app.grammarly.com/scim/v2"
# The only vendor here needing an id in the path. %s is filled from the
# operator's stored key, never from a request, and only after _DEVIN_ORG
# has passed it - so the host and path are as fixed as every other URL.
DEVIN_URL = "https://api.devin.ai/v3beta1/organizations/%s/members/users"
_DEVIN_ORG = re.compile(r"^org-[A-Za-z0-9_-]{1,64}$")

# What the portal needs to offer the wizard: which providers exist, what
# each one's key looks like and where an admin creates it. Data, not
# secrets - served as-is by /admin/budget.
PROVIDERS = {
    "anthropic": {
        "label": 'Anthropic（Claude Enterprise / Console）',
        # What plan the admin API needs. Stated only where it is actually
        # known: Anthropic documents that Team has no admin keys, so that
        # one is a fact. Fireflies below does not get a guess.
        "plan": 'Enterprise、または Console 組織。Team プランには Admin API が一切ありません。',
        "key_hint": 'read:members スコープが付与された Admin API キー。組織のプライマリオーナーが claude.ai > Organization settings > API で作成します（Console 組織の場合: Settings > Admin keys）。読み取り専用スコープを選択してください。この同期は書き込みを一切行いません。Claude Team プランでは Admin キーが提供されません。API セクション自体が存在しません。そのため Team ワークスペースでは代わりに インポート 経路を使用し、Organization settings > Members から実行します。',
        "syncs": 'メンバーとロール。シートティアは API に含まれません。サブスクリプションに記録してください。',
    },
    "chatgpt": {
        "label": 'ChatGPT ワークスペース（Enterprise または Edu）',
        "plan": 'Enterprise または Edu。Business（2025 年に Team から名称変更されたプラン）には SSO がありますが SCIM はないため、インポート を使用します。',
        "key_hint": 'SCIM API トークンはワークスペース管理コンソールの Settings > Security > SCIM Provisioning から取得します。これは ID プロバイダーではなく OpenAI によって発行され、IdP が書き込むのと同じエンドポイントを読み取ります。使用するのに IdP は必要ありません。Codex CLI には独自のメンバー一覧がありません。「他に対象」でチェックを入れてください。',
        "syncs": 'メンバーとアカウントが有効かどうか。SCIM にはシートティアや使用状況が含まれません。ティアはサブスクリプションに記録してください。',
        "unverified": True,
    },
    "notion": {
        "label": 'Notion（Enterprise）',
        "plan": 'Enterprise のみ。Free、Plus、Business では SCIM トークンを一切発行できません。',
        "key_hint": 'SCIM API トークンは組織のオーナーが Manage organization で作成します。発行するのは Notion であり、ID プロバイダーではありません。これは IdP が書き込むのと同じエンドポイントを読み取ります。',
        "syncs": 'メンバーとアカウントが有効かどうか。シートティアや使用状況はありません。ティアはサブスクリプションに記録してください。',
        "unverified": True,
    },
    "grammarly": {
        "label": 'Grammarly（Pro または Enterprise）',
        "plan": 'Pro または Enterprise。また、先に SAML SSO を設定する必要があります。設定するまで Grammarly はトークンを発行しません。',
        "key_hint": 'SCIM トークンは Admin Panel の Settings > SSO & Provisioning から取得します。',
        "syncs": 'メンバーとアカウントが有効かどうか。',
        "unverified": True,
    },
    "openai": {
        "label": 'OpenAI（APIプラットフォーム組織）',
        "plan": '任意の組織（Admin APIキーが必要）。これはAPIプラットフォーム組織です。ChatGPTワークスペースはSCIM専用で、インポートを使用します。',
        "key_hint": 'Admin APIキー。オーナーが platform.openai.com > Settings > Organization > Admin keys で作成します。通常のプロジェクトAPIキーは機能しません。組織エンドポイントが受け付けるのはAdminキーだけです。',
        "syncs": 'メンバーとその組織ロール。シート階層はAPIには含まれません。シート階層はサブスクリプションに記録してください。',
        # Written from OpenAI's documented endpoint and NOT yet run against a
        # real organisation. The first operator to point it at one is the
        # test; a refusal here names the vendor and the status rather than
        # failing silently.
        "unverified": True,
    },
    "cursor": {
        "label": 'Cursor（TeamまたはEnterprise）',
        "plan": 'Team と Enterprise の両方で管理 API を利用できます。',
        "key_hint": 'Team APIキー。cursor.com > Settings > Cursor Admin API で取得します。HTTP Basicとして、キーをユーザー名として、パスワードなしで送信します。これは同社のcurl例のとおりです。',
        "syncs": 'メンバーとそのチームロール。削除済みメンバーはシートとしてカウントされず、除外されます。',
        "unverified": True,
    },
    "fireflies": {
        "label": 'Fireflies.ai',
        # Fireflies' own knowledge base says API access is available on every
        # plan level, and neither the `users` query nor the API-key article
        # names a tier or an admin role. The "Business or higher" gate people
        # quote is on the separate `analytics` query, which this connector
        # does not use: the per-user counters it reports are fields on
        # `users` itself.
        "plan": '任意のプラン。FirefliesはすべてのプランレベルでAPIアクセスを文書化しており、team-usersクエリは階層を指定していません。',
        "key_hint": 'APIキー。fireflies.ai > Integrations > Fireflies API で取得します。チーム管理者のキーはチーム全体を一覧表示します。',
        "syncs": 'メンバー、管理者フラグ、ユーザーごとの使用量（文字起こし、分数）。',
    },
    "devin": {
        "label": 'Devin / Devin Desktop（Cognition）',
        # Teams genuinely reaches this - the docs give Teams its own API
        # quick start, and a Teams org admin can mint a service user. That
        # is worth stating plainly, because the assumption in this file
        # everywhere else is that a member list means Enterprise.
        "plan": 'TeamsまたはEnterprise。どちらもサービスユーザーを作成し、自組織のメンバーを読み取れます。Enterpriseはさらに、この同期では使用しないクロス組織エンドポイントにもアクセスできます。',
        "key_hint": 'サービスユーザーAPIキー（cog_で始まる）と組織IDを、org-xxxx:cog_xxxx のように1つの値として入力します。組織管理者は同じ場所（Settings > Service Users）で両方を作成します。ここに組織IDが表示され、Create service user がキーを発行します。キーは一度だけ表示されます。メンバーロールで十分です。この同期は読み取りのみを行います。CognitionがWindsurfをDevinに統合したため、Windsurfライセンスもここにあります。',
        "syncs": 'メンバーとそのロール名。シート階層と使用量はこのエンドポイントにはありません。シート階層はサブスクリプションに記録してください。',
    },
}


# What each SHIPPED registry tool's vendor can tell an administrator about who
# holds a seat. PROVIDERS above is the subset this receiver has actually
# implemented; this is the wider map, so the portal can answer the operator's
# real question - "why is my tool not in the Automatic list?" - with either
# "its vendor offers nothing" or "its vendor does, and we have not built it
# yet", which is a far more useful thing to open an issue about.
#
# `api` is what the VENDOR offers, not what we support:
#   rest      a REST/GraphQL admin endpoint that lists members
#   scim      SCIM 2.0 only, which means provisioning through an IdP
#   none      no organisation or seat list exists to read
#   unknown   not documented publicly, or not established
#
# `plan` records the tier, and says so honestly where a tier is not documented.
# Checked against vendor documentation in August 2026. Vendors move these gates
# often - anything here that starts costing an operator a wasted afternoon
# should be re-checked rather than trusted because it is written down.
MEMBER_APIS = {
    "claude": {
        "api": "rest", "connector": "anthropic",
        "plan": 'Enterprise、またはConsole 組織。Teamプランには管理APIがありません。',
        "how": 'Admin API、GET /v1/organizations/users。',
    },
    "claude-code": {
        "api": "rest", "connector": "anthropic",
        "plan": 'Enterprise、またはConsole 組織。',
        "how": 'Claudeと同じAnthropic 組織です。ライセンスは1つ、メンバーリストも1つです。',
    },
    "chatgpt": {
        "api": "scim", "connector": "chatgpt",
        "plan": 'EnterpriseまたはEduのみ。Business（2025年にTeamから改称）にはSSOがありますが、SCIMはありません。',
        "how": 'SCIM 2.0はapi.openai.com/scim/v2です。トークンはOpenAI自身の管理コンソールから発行されるため、IdPは関与しません。',
    },
    "codex-cli": {
        "api": "rest", "connector": "chatgpt",
        "plan": '費用を負担しているプランであれば何でも。',
        "how": '独自のメンバーリストはありません。ChatGPTワークスペースまたはAPI プラットフォーム組織に紐づきます。「他に対象」の項目にチェックを入れてください。',
    },
    "openai-api-platform": {
        "api": "rest", "connector": "openai",
        "plan": 'Admin APIキーがあれば、どの組織でも可。',
        "how": 'GET /v1/organization/users。',
    },
    "gemini": {
        "api": "rest",
        "plan": 'GeminiにはGoogle WorkspaceのBusiness Standard以上。',
        "how": 'ライセンスはWorkspaceで割り当てられます。Admin SDK Directory APIとEnterprise License Manager APIで、誰がライセンスを保有しているかを一覧表示できます。',
    },
    "gemini-cli": {
        "api": "rest",
        "plan": 'Google Workspace、またはCode Assist用のGoogle Cloudプロジェクト。',
        "how": 'Geminiと同じWorkspaceライセンス割り当てです。',
    },
    "github-copilot": {
        "api": "rest",
        "plan": 'Copilot BusinessまたはCopilot Enterprise。',
        "how": 'GET /orgs/{org}/copilot/billing/seats。組織オーナーが、manage_billing:copilotとread:orgを持つトークンを使用します。',
    },
    "cursor": {
        "api": "rest", "connector": "cursor",
        "plan": 'Team と Enterprise の両方で利用できます。',
        "how": 'Admin API、Team API キーを使用した GET /teams/members。',
    },
    "codeium": {
        "api": "rest", "connector": "devin",
        # This entry used to say Enterprise-only, which was true of the old
        # Windsurf analytics API and stopped being true when Cognition moved
        # the product onto Devin's platform: Teams has its own API quick
        # start and can mint a service user. An operator on Teams was being
        # told to go and do a CSV import they did not need.
        "plan": 'Teams または Enterprise。Cognition の Devin API 経由で、Windsurf 買収以降ライセンスは同一です。',
        "how": 'サービスユーザーキーを使用した GET /v3beta1/organizations/{org}/members/users。',
    },
    "tabnine": {
        "api": "rest",
        "plan": 'Enterprise、SaaS コンソールまたはセルフホスト。',
        "how": 'チームとユーザー向けの Admin API、および SCIM IdP 同期。',
    },
    "warp": {
        "api": "unknown", "plan": '',
        "how": 'Warp Teams と Enterprise では、メンバーを Warp ダッシュボードで管理します。公開されたメンバー用 API は文書化されていません。存在しないと断定できず、公開情報では未確認です。',
    },
    "cline": {
        "api": "unknown",
        "plan": 'Enterprise。',
        "how": 'Cline Enterprise はメンバーを独自のダッシュボードで管理します。公開されたメンバー API は文書化されていません。',
    },
    "roo-code": {
        "api": "none", "plan": '',
        "how": '独自のモデルキーを使用するオープンソース拡張機能です。ベンダーアカウントが存在しないため、読み取れるシート一覧もありません。',
    },
    "continue": {
        "api": "none", "plan": '',
        "how": '独自のモデルキーを使用するオープンソース拡張機能です。ベンダーのシート一覧はありません。',
    },
    "otter": {
        "api": "rest",
        "plan": 'Enterprise。SCIM Directory Sync には追加で 100 シート以上が必要です。',
        "how": '公開 API は Enterprise 専用で、Bearer 認証です。',
    },
    "grammarly": {
        "api": "scim", "connector": "grammarly",
        "plan": 'Pro または Enterprise で、先に SAML SSO を有効にする必要があります。',
        "how": 'SCIM 2.0（app.grammarly.com/scim/v2）。',
    },
    "wispr-flow": {
        "api": "scim",
        "plan": 'Enterprise。',
        "how": 'admin.wisprflow.ai の管理ポータルで SCIM プロビジョニングに対応しています。Enterprise API が対象とするのはメンバー一覧ではなく監査ログです。',
    },
    "perplexity": {
        "api": "scim",
        "plan": 'Enterprise Pro（50 シート以上）、または Enterprise Max（シート数不問）。',
        "how": 'SCIM は IdP 経由のみです。管理用 REST API は存在せず、SCIM トークンはセルフサービスではなく、オンボーディング時に発行されます。',
    },
    "mistral": {
        "api": "rest",
        "plan": 'Enterprise。Admin API はプレビュー中です。',
        "how": 'console.mistral.ai/api/admin、x-api-key。',
    },
    "grok": {
        "api": "rest",
        "plan": 'Grok Business、または xAI 組織。',
        "how": 'Management API（management-api.x.ai）で management key を使用します。',
    },
    "microsoft-copilot": {
        "api": "rest",
        "plan": 'Microsoft 365 管理者がいる任意のテナント。',
        "how": 'Microsoft Graph: subscribedSkus とユーザーごとの licenseDetails で、誰がアドオンを保有しているかを確認できます。',
    },
    "microsoft-365-copilot": {
        "api": "rest",
        "plan": 'M365 E3/E5 または Business Standard/Premium へのアドオン。',
        "how": 'Microsoft Graph。他の M365 サービスと同じライセンス割り当てです。',
    },
    "atlassian-rovo": {
        "api": "rest",
        "plan": 'ドキュメント化されていません。必要なのは組織の API キーです。どのプランで発行できるかは公開されていません。',
        "how": 'Organizations REST API、GET /v2/orgs/{orgId}/directories/{directoryId}/users。',
    },
    "notion-ai": {
        "api": "scim", "connector": "notion",
        "plan": 'Enterpriseのみ - Free、Plus、BusinessではSCIMを使用できません。',
        "how": 'プロビジョニングにはSCIMを使用します。通常のNotion APIの /v1/users も、インテグレーショントークンを使ってワークスペースメンバーを一覧表示できます。',
    },
    "fireflies": {
        "api": "rest", "connector": "fireflies",
        "plan": 'すべてのプラン - APIアクセスはすべてのプランレベルで文書化されています。',
        "how": 'チームのユーザーを対象とする1つのGraphQLクエリで、ユーザーごとの使用量を取得できます。別の分析クエリにはBusiness以上が必要ですが、この方法ではそのクエリを使用しません。',
    },
    "hugging-face": {
        "api": "rest",
        "plan": 'メンバー一覧は任意の組織で利用できます。SCIMには、SSOを有効にしたEnterprise Hubが必要です。',
        "how": 'GET /api/organizations/{org}/members.',
    },
    "deepseek": {
        "api": "unknown", "plan": '',
        "how": 'オープンプラットフォームはAPIキーを発行します。組織メンバー用のエンドポイントは公開されたドキュメントに記載されていません。',
    },
    "midjourney": {
        "api": "none", "plan": '',
        "how": '個人向けサブスクリプションです。組織が存在しないため、シート一覧も存在しません。',
    },
    "ollama": {
        "api": "none", "plan": '',
        "how": 'アカウントなしでローカルで実行されます - 一覧表示する対象が存在しません。',
    },
    "lm-studio": {
        "api": "none", "plan": '',
        "how": 'アカウントを持たないローカルデスクトップアプリです。',
    },
}


class SyncError(Exception):
    """A failed sync, carrying what the operator should hear. Never the
    key, and never a raw vendor body - those are logged nowhere and
    echoed nowhere.

    The message lives in .detail, assigned from this module's own
    templates at each raise site. The route reads that field rather than
    str()-ing the caught exception, so nothing exception-shaped flows
    into a response body - the property CodeQL's stack-trace-exposure
    query checks for, held structurally instead of by convention."""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


def _refusal(status: int, vendor: str) -> SyncError:
    if status == 401:
        return SyncError("%s answered 401: the key is wrong, expired or "
                         "revoked" % vendor)
    if status == 403:
        return SyncError("%s answered 403: the key lacks the scope this "
                         "sync needs (read:members for Anthropic)" % vendor)
    if status == 429:
        return SyncError("%s answered 429 (rate limited): try again in a "
                         "minute" % vendor)
    return SyncError("%s answered HTTP %d" % (vendor, status))


async def sync_anthropic(api_key: str) -> list[dict]:
    """The org's members via the Anthropic Admin API, all pages.

    Pagination is id-based: page with after_id until has_more is false.
    The page cap backs MAX_MEMBERS - the loop cannot run away even if the
    API misbehaves.
    """
    members: list[dict] = []
    after = ""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for _ in range(MAX_MEMBERS // 100 + 1):
            params = {"limit": "100"}
            if after:
                params["after_id"] = after
            try:
                r = await client.get(
                    ANTHROPIC_URL, params=params,
                    headers={"x-api-key": api_key,
                             "anthropic-version": "2023-06-01"})
            except httpx.HTTPError as e:
                raise SyncError("could not reach the Anthropic API (%s)"
                                % type(e).__name__)
            if r.status_code != 200:
                raise _refusal(r.status_code, "the Anthropic API")
            try:
                body = r.json()
            except json.JSONDecodeError:
                raise SyncError("the Anthropic API answered 200, but not "
                                "with JSON")
            for u in body.get("data") or []:
                email = str(u.get("email") or "").strip().lower()
                if not email:
                    continue
                members.append({
                    "email": email,
                    "name": str(u.get("name") or "")[:200],
                    "role": str(u.get("role") or "")[:64],
                    "seat_tier": "",
                    "usage": {},
                })
                if len(members) > MAX_MEMBERS:
                    raise SyncError("more than %d members: refusing rather "
                                    "than store a partial member list as if it "
                                    "were complete" % MAX_MEMBERS)
            if not body.get("has_more"):
                return members
            after = str(body.get("last_id") or "")
            if not after:
                # has_more with no cursor would loop on page one forever.
                return members
    raise SyncError("the Anthropic API kept paginating past %d members"
                    % MAX_MEMBERS)


_FIREFLIES_QUERY = ("{ users { name email is_admin num_transcripts "
                    "minutes_consumed } }")


async def sync_fireflies(api_key: str) -> list[dict]:
    """The team's users via the Fireflies GraphQL API, usage included."""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            r = await client.post(
                FIREFLIES_URL, json={"query": _FIREFLIES_QUERY},
                headers={"Authorization": "Bearer " + api_key})
        except httpx.HTTPError as e:
            raise SyncError("could not reach the Fireflies API (%s)"
                            % type(e).__name__)
    if r.status_code != 200:
        raise _refusal(r.status_code, "the Fireflies API")
    try:
        body = r.json()
    except json.JSONDecodeError:
        raise SyncError("the Fireflies API answered 200, but not with JSON")
    if body.get("errors"):
        # GraphQL reports refusals in-band. The first message is the story
        # ("Invalid API key", "not authorized"); the rest repeat it.
        msg = str((body["errors"][0] or {}).get("message") or "error")[:200]
        raise SyncError("the Fireflies API refused the query: %s" % msg)
    users = (body.get("data") or {}).get("users") or []
    if len(users) > MAX_MEMBERS:
        raise SyncError("more than %d members: refusing rather than store "
                        "a partial member list as if it were complete"
                        % MAX_MEMBERS)
    members = []
    for u in users:
        email = str(u.get("email") or "").strip().lower()
        if not email:
            continue
        usage = {}
        if u.get("num_transcripts") is not None:
            usage["transcripts"] = int(u["num_transcripts"] or 0)
        if u.get("minutes_consumed") is not None:
            usage["minutes"] = round(float(u["minutes_consumed"] or 0))
        members.append({
            "email": email,
            "name": str(u.get("name") or "")[:200],
            "role": "admin" if u.get("is_admin") else "member",
            "seat_tier": "",
            "usage": usage,
        })
    return members


async def sync_openai(api_key: str) -> list[dict]:
    """The organisation's members via the OpenAI Admin API, all pages.

    This is the API PLATFORM organisation - the one that owns API keys and
    projects - not a ChatGPT workspace. ChatGPT's member list is SCIM-only
    and Enterprise-only, which is an identity-provider integration rather
    than a vendor endpoint this could call, so it stays on the Import path.

    Pagination is cursor-based: page with `after` until has_more is false.
    """
    members: list[dict] = []
    after = ""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for _ in range(MAX_MEMBERS // 100 + 1):
            params = {"limit": "100"}
            if after:
                params["after"] = after
            try:
                r = await client.get(
                    OPENAI_URL, params=params,
                    headers={"Authorization": "Bearer " + api_key})
            except httpx.HTTPError as e:
                raise SyncError("could not reach the OpenAI API (%s)"
                                % type(e).__name__)
            if r.status_code != 200:
                raise _refusal(r.status_code, "the OpenAI API")
            try:
                body = r.json()
            except json.JSONDecodeError:
                raise SyncError("the OpenAI API answered 200, but not with "
                                "JSON")
            page = body.get("data") or []
            for u in page:
                email = str(u.get("email") or "").strip().lower()
                if not email:
                    continue
                members.append({
                    "email": email,
                    "name": str(u.get("name") or "")[:200],
                    "role": str(u.get("role") or "")[:64],
                    "seat_tier": "",
                    "usage": {},
                })
                if len(members) > MAX_MEMBERS:
                    raise SyncError("more than %d members: refusing rather "
                                    "than store a partial member list as if "
                                    "it were complete" % MAX_MEMBERS)
            if not body.get("has_more"):
                return members
            after = str(body.get("last_id") or "")
            if not after and page:
                after = str(page[-1].get("id") or "")
            if not after:
                # has_more with no cursor would loop on page one forever.
                return members
    raise SyncError("the OpenAI API kept paginating past %d members"
                    % MAX_MEMBERS)


async def sync_cursor(api_key: str) -> list[dict]:
    """The team's members via the Cursor Admin API.

    One unpaginated call. Authentication is HTTP Basic with the API key as
    the USERNAME and an empty password - the shape their docs show as
    `curl -u YOUR_API_KEY:` - not a bearer token.

    Removed members keep appearing with isRemoved set; they are dropped
    here, because a seat that has been taken away is not a seat somebody
    holds and counting it would overstate what the licence is paying for.
    """
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            r = await client.get(CURSOR_URL, auth=(api_key, ""))
        except httpx.HTTPError as e:
            raise SyncError("could not reach the Cursor API (%s)"
                            % type(e).__name__)
    if r.status_code != 200:
        raise _refusal(r.status_code, "the Cursor API")
    try:
        body = r.json()
    except json.JSONDecodeError:
        raise SyncError("the Cursor API answered 200, but not with JSON")
    # Their docs show a bare array; a wrapped object would be a kindness to
    # accept too rather than a reason to fail the whole sync.
    rows = body if isinstance(body, list) else (body.get("teamMembers")
                                                or body.get("members") or [])
    if not isinstance(rows, list):
        raise SyncError("the Cursor API answered with JSON this does not "
                        "recognise as a member list")
    if len(rows) > MAX_MEMBERS:
        raise SyncError("more than %d members: refusing rather than store a "
                        "partial member list as if it were complete"
                        % MAX_MEMBERS)
    members = []
    for u in rows:
        if not isinstance(u, dict) or u.get("isRemoved"):
            continue
        email = str(u.get("email") or "").strip().lower()
        if not email:
            continue
        members.append({
            "email": email,
            "name": str(u.get("name") or "")[:200],
            "role": str(u.get("role") or "")[:64],
            "seat_tier": "",
            "usage": {},
        })
    return members

async def _scim_users(base_url: str, token: str, vendor: str) -> list[dict]:
    """Members from any SCIM 2.0 /Users endpoint.

    SCIM was ruled out here at first as "an identity-provider integration
    rather than a vendor API". That is wrong wherever the VENDOR issues the
    token from its own admin console and the endpoint answers a plain GET -
    which is a bearer key like any other, and no IdP is involved. What stays
    ruled out is a vendor whose token is issued by its support team during
    onboarding, because there is nothing an operator can paste.

    Pagination is SCIM's own: 1-based startIndex, and totalResults says when
    to stop. Written once because the three vendors that qualify differ only
    in their base URL.
    """
    members: list[dict] = []
    start = 1
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for _ in range(MAX_MEMBERS // 100 + 1):
            try:
                r = await client.get(
                    base_url.rstrip("/") + "/Users",
                    params={"startIndex": str(start), "count": "100"},
                    headers={"Authorization": "Bearer " + token,
                             "Accept": "application/scim+json"})
            except httpx.HTTPError as e:
                raise SyncError("could not reach %s (%s)"
                                % (vendor, type(e).__name__))
            if r.status_code != 200:
                raise _refusal(r.status_code, vendor)
            try:
                body = r.json()
            except json.JSONDecodeError:
                raise SyncError("%s answered 200, but not with JSON" % vendor)
            page = body.get("Resources")
            if page is None:
                raise SyncError("%s answered without a SCIM Resources list - "
                                "check the base URL is the SCIM one" % vendor)
            for u in page:
                if not isinstance(u, dict):
                    continue
                # userName is the email on every vendor here, but the emails
                # array is the spec's own answer, so prefer it and fall back.
                email = ""
                for e in (u.get("emails") or []):
                    if isinstance(e, dict) and e.get("value"):
                        email = str(e["value"])
                        if e.get("primary"):
                            break
                email = (email or str(u.get("userName") or "")).strip().lower()
                if not email or "@" not in email:
                    continue
                nm = u.get("name") or {}
                name = str(nm.get("formatted") or
                           " ".join(x for x in [nm.get("givenName"),
                                                nm.get("familyName")] if x) or
                           u.get("displayName") or "")
                # A deactivated SCIM user is not holding a seat. Counting one
                # would overstate what the licence pays for, the same way a
                # removed Cursor member would.
                if u.get("active") is False:
                    continue
                members.append({
                    "email": email,
                    "name": name[:200],
                    "role": "",
                    "seat_tier": "",
                    "usage": {},
                })
                if len(members) > MAX_MEMBERS:
                    raise SyncError("more than %d members: refusing rather "
                                    "than store a partial member list as if "
                                    "it were complete" % MAX_MEMBERS)
            total = body.get("totalResults")
            got = start - 1 + len(page)
            if not page or (isinstance(total, int) and got >= total):
                return members
            start = got + 1
    raise SyncError("%s kept paginating past %d members"
                    % (vendor, MAX_MEMBERS))


async def sync_chatgpt(api_key: str) -> list[dict]:
    """The ChatGPT workspace's members, via its SCIM 2.0 endpoint.

    Enterprise and Edu only - Business (renamed from Team in 2025) has SSO
    but no SCIM, and so stays on the Import path. The token comes from the
    workspace's own admin console, Settings > Security > SCIM Provisioning,
    not from an identity provider.

    Codex CLI has no member list of its own: it rides whichever workspace
    pays for it, so tick it under "also covers" rather than looking for a
    connector of its own.
    """
    return await _scim_users(CHATGPT_SCIM_URL, api_key, "the ChatGPT SCIM API")


async def sync_notion(api_key: str) -> list[dict]:
    """The workspace's members via Notion's SCIM endpoint.

    Enterprise only - Free, Plus and Business cannot mint a SCIM token at
    all. An organisation owner creates it under Manage organization, so it
    is a vendor-issued key even though an IdP is the usual consumer.
    """
    return await _scim_users(NOTION_SCIM_URL, api_key, "the Notion SCIM API")


async def sync_grammarly(api_key: str) -> list[dict]:
    """The account's members via Grammarly's SCIM endpoint.

    Pro and Enterprise, and SAML SSO has to be configured first - Grammarly
    will not issue the token before it is. The token comes from the Admin
    Panel, Settings > SSO & Provisioning.
    """
    return await _scim_users(GRAMMARLY_SCIM_URL, api_key,
                             "the Grammarly SCIM API")


async def sync_devin(api_key: str) -> list[dict]:
    """The organisation's members via Cognition's Devin API, all pages.

    Covers Devin and Devin Desktop - the IDE that shipped as Codeium, then
    as Windsurf - because Cognition folded them onto one platform and one
    licence. That is why the registry keeps them as one tool, and why this
    is the connector the `codeium` id links to.

    Teams reaches this, not only Enterprise: an org admin creates a service
    user under Settings > Service Users and generates a `cog_` key. Member
    role is enough, since this only reads.

    The stored key is "org-xxxx:cog_xxxx" - the org id and the key, both
    shown on that same settings page. Devin has no endpoint that resolves a
    key to its own organisation, so the id has to be carried; it is checked
    against _DEVIN_ORG before it goes anywhere near a URL.

    Pagination is cursor-based: page with `after` until has_next_page is
    false. Seat tiers and usage are not on this endpoint, so both stay
    blank and tiers are recorded on the subscription.
    """
    org, _, key = api_key.partition(":")
    org, key = org.strip(), key.strip()
    if not key:
        raise SyncError("the Devin key needs the organisation id with it, as "
                        "org-xxxx:cog_xxxx - both are on Settings > Service "
                        "Users")
    if not _DEVIN_ORG.match(org):
        raise SyncError("%r is not a Devin organisation id: it should look "
                        "like org-xxxx, from Settings > Service Users"
                        % org[:40])

    members: list[dict] = []
    after = ""
    url = DEVIN_URL % org
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for _ in range(MAX_MEMBERS // 100 + 1):
            params = {"first": "100"}
            if after:
                params["after"] = after
            try:
                r = await client.get(
                    url, params=params,
                    headers={"Authorization": "Bearer " + key})
            except httpx.HTTPError as e:
                raise SyncError("could not reach the Devin API (%s)"
                                % type(e).__name__)
            if r.status_code == 403:
                # The generic 403 names an Anthropic scope, which would send
                # a Devin operator looking in the wrong console.
                raise SyncError("the Devin API answered 403: the service "
                                "user needs the ViewOrgMembership permission "
                                "on this organisation")
            if r.status_code == 404:
                raise SyncError("the Devin API answered 404: no organisation "
                                "%s - check the id on Settings > Service "
                                "Users" % org)
            if r.status_code != 200:
                raise _refusal(r.status_code, "the Devin API")
            try:
                body = r.json()
            except json.JSONDecodeError:
                raise SyncError("the Devin API answered 200, but not with "
                                "JSON")
            page = body.get("items") or []
            for u in page:
                email = str(u.get("email") or "").strip().lower()
                if not email:
                    # Service users are members of the org and have no
                    # address. They hold no paid seat, so skipping them
                    # keeps the count to people.
                    continue
                # Roles are assignments, not a field: a member can hold more
                # than one. Join them so the portal shows what the vendor
                # actually says rather than an arbitrary first pick.
                roles = []
                for a in u.get("role_assignments") or []:
                    nm = str(((a or {}).get("role") or {}).get("role_name")
                             or "").strip()
                    if nm and nm not in roles:
                        roles.append(nm)
                members.append({
                    "email": email,
                    "name": str(u.get("name") or "")[:200],
                    "role": ", ".join(roles)[:64],
                    "seat_tier": "",
                    "usage": {},
                })
                if len(members) > MAX_MEMBERS:
                    raise SyncError("more than %d members: refusing rather "
                                    "than store a partial member list as if "
                                    "it were complete" % MAX_MEMBERS)
            if not page or not body.get("has_next_page"):
                return members
            after = str(body.get("end_cursor") or "")
            if not after:
                # has_next_page with no cursor would loop on page one.
                return members
    raise SyncError("the Devin API kept paginating past %d members"
                    % MAX_MEMBERS)

SYNCERS = {"anthropic": sync_anthropic, "fireflies": sync_fireflies,
           "openai": sync_openai, "cursor": sync_cursor,
           "chatgpt": sync_chatgpt, "notion": sync_notion,
           "grammarly": sync_grammarly, "devin": sync_devin}


# ----------------------------------------------------------------- fx --
# Daily ECB reference rates via the Frankfurter API: keyless, free, one
# fixed host - the same no-request-supplied-URL rule as the vendor syncs.
# The portal uses them to show the Budget headline in the preferred
# currency, always naming the rate's date inline, and falls back to
# per-currency figures when this cannot answer. ECB publishes once per
# working day around 16:00 CET, so a half-day cache never serves a rate
# the source itself has moved past.

FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"
_FX_TTL = 12 * 3600
_fx_cache: dict = {}


async def fx_rates(base: str) -> dict:
    """{"base", "date", "rates"} - units of each currency per one `base`,
    per the ECB's latest daily reference fixing. Cached per base."""
    now = time.time()
    hit = _fx_cache.get(base)
    if hit and now - hit[0] < _FX_TTL:
        return hit[1]
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(FRANKFURTER_URL, params={"base": base})
        except httpx.HTTPError as e:
            raise SyncError("could not reach the exchange-rate source (%s)"
                            % type(e).__name__)
    if r.status_code == 404:
        # Frankfurter answers 404 for a currency the ECB does not fix.
        raise SyncError("the ECB publishes no reference rate for %s" % base)
    if r.status_code != 200:
        raise _refusal(r.status_code, "the exchange-rate source")
    try:
        body = r.json()
    except json.JSONDecodeError:
        raise SyncError("the exchange-rate source answered 200, but not "
                        "with JSON")
    rates = {}
    for k, v in (body.get("rates") or {}).items():
        if isinstance(k, str) and len(k) == 3 and isinstance(v, (int, float)) \
                and v > 0 and len(rates) < 64:
            rates[k.upper()] = float(v)
    out = {"base": base, "date": str(body.get("date") or "")[:10],
           "rates": rates}
    _fx_cache[base] = (now, out)
    return out
