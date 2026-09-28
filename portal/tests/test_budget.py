# Copyright 2026 Aman Karir
# SPDX-License-Identifier: Apache-2.0
# Part of Shadow AI Guard, https://github.com/AmanSK5/shadow-ai-guard

"""The budget proxies and the page that draws them. Same direct-call
harness as the suite: the receiver owns storage and validation, so what
the portal must hold is thinner and worth stating exactly - each route
forwards the right verb to the right receiver path with the operator's
own session, classic mode refuses with the message that names the fix,
and the page ships with the view wired into the shell."""

import os
from pathlib import Path

os.environ.setdefault("PORTAL_AUTH", "none")

import pytest
from fastapi import HTTPException

from app import main

INDEX = (Path(__file__).parent.parent / "app" / "static"
         / "index.html").read_text()


@pytest.fixture
def receiver_spy(monkeypatch):
    """Managed mode with the receiver replaced by a recorder."""
    calls = []

    def fake(base, method, path, token, body=None):
        calls.append({"method": method, "path": path, "token": token,
                      "body": body})
        return {"ok": True}

    monkeypatch.setattr(main, "RECEIVER_URL", "http://receiver:8080")
    monkeypatch.setattr(main.managed, "receiver_request", fake)
    return calls


class _Req:
    cookies = {"aiguard_session": "aigt_test"}


# ----------------------------------------------------------- the proxies --


def test_each_route_forwards_the_right_verb_and_path(receiver_spy):
    token = main._admin_forward(_Req())

    main.api_budget(token=token)
    sub = main.BudgetSubscriptionWrite(
        tool_id="claude", vendor="Anthropic", plan="Team",
        seat_tiers=[main.BudgetSeatTier(name="premium", seats=5,
                                        unit_price_monthly=100)])
    main.api_budget_subscription(sub, token=token)
    main.api_budget_members(main.BudgetMembersWrite(
        tool_id="claude", source="csv",
        members=[main.BudgetMemberWrite(email="a@corp.example")]),
        token=token)
    main.api_budget_connection(main.BudgetConnectionWrite(
        tool_id="claude", provider="anthropic",
        api_key="sk-ant-api01-test"), token=token)
    main.api_budget_sync(main.BudgetToolRef(tool_id="claude"), token=token)
    main.api_budget_connection_delete(main.BudgetToolRef(tool_id="claude"),
                                      token=token)
    main.api_budget_subscription_delete(main.BudgetToolRef(tool_id="claude"),
                                        token=token)
    main.api_budget_fx("GBP", token=token)

    got = [(c["method"], c["path"]) for c in receiver_spy]
    assert got == [
        ("GET", "/admin/budget"),
        ("PUT", "/admin/budget/subscription"),
        ("PUT", "/admin/budget/members"),
        ("PUT", "/admin/budget/connection"),
        ("POST", "/admin/budget/sync"),
        ("POST", "/admin/budget/connection/delete"),
        ("POST", "/admin/budget/subscription/delete"),
        ("GET", "/admin/budget/fx?to=GBP"),
    ]
    # The operator's own session rides every call - the portal holds no
    # credential of its own for this.
    assert all(c["token"] == "aigt_test" for c in receiver_spy)


def test_the_body_reaches_the_receiver_intact(receiver_spy):
    token = main._admin_forward(_Req())
    main.api_budget_connection(main.BudgetConnectionWrite(
        tool_id="fireflies", provider="fireflies",
        api_key="ff-key-123"), token=token)
    body = receiver_spy[-1]["body"]
    # plan_key rides along empty: the portal only carries it, and the
    # receiver decides what an empty one means (the tool's only
    # subscription, or a refusal when there are several).
    assert body == {"tool_id": "fireflies", "plan_key": "",
                    "provider": "fireflies",
                    "api_key": "ff-key-123"}


def test_classic_mode_refuses_and_names_the_fix(monkeypatch):
    monkeypatch.setattr(main, "RECEIVER_URL", "")
    with pytest.raises(HTTPException) as e:
        main._admin_forward(_Req())
    assert e.value.status_code == 503
    assert "RECEIVER_URL" in e.value.detail


# ---------------------------------------------------------------- the page --


def test_the_shell_ships_the_budget_view():
    # The nav entry, the view function, and the fragment round trip: a view
    # reachable only by typing its fragment is a view nobody finds.
    assert "['budget','予算']" in INDEX
    assert "async function budget()" in INDEX
    assert "view === 'budget'" in INDEX


def test_the_wizard_names_the_honest_provider_set():
    # ChatGPT Business gets the guided import and the page says why - the
    # absence of an admin API on that plan is OpenAI's, and presenting it
    # as ai-guard's gap (or hiding it) would both be wrong.
    assert "自動同期にはベンダーの管理APIが必要" in INDEX
    # Requests for automatic setup now go to the Sera support address.
    assert "mailto:info@sera-inc.co.jp" in INDEX


# ---------------------------------------------------------- the report --


def test_the_shell_ships_the_share_view():
    # Reachable from the page and by fragment, and rendered by its own
    # function - a report nobody can link to is a report nobody sends.
    assert "'budget-report'" in INDEX
    assert "function budgetReport()" in INDEX
    assert "data-act=\"b-report\"" in INDEX


def test_the_report_can_withhold_names_and_guards_the_csv():
    # The page names individuals and their personal account domains, so
    # withholding them is one control, in the page and in the export.
    assert "BRNAMES" in INDEX and "名前を伏せる" in INDEX
    assert "-anonymised.csv" in INDEX or "'-anonymised'" in INDEX
    # An exported address starting with = is a live formula in Excel.
    assert "B_FORMULA_LEAD" in INDEX and "function bCsvCell" in INDEX


def test_printing_drops_the_furniture():
    assert "@media print" in INDEX
    for hidden in ("aside", ".topbar", ".drawer", "[data-act]"):
        assert hidden in INDEX.split("@media print")[1][:600], hidden


def test_linking_a_tool_is_four_steps_with_a_review():
    """The budget wizard was already three steps; what it lacked was the
    language. Its only progress marker was the italic text "step 1 of 3", the
    seat tiers were three inputs whose only labels were placeholders that
    vanish once anything is typed, and it committed straight from the last
    step with nothing showing the licence, its covered tools and the cost
    together."""
    for needle in ("function bwRail(", "function bwBodyReview(",
                   "const BW_STEPS", "確認してリンク",
                   'class="tiers"', "<th>プラン</th>", "ライセンス単価",
                   "bw-tsum", "bw-money"):
        assert needle in INDEX, needle
    # The rail summary carries the money, not a step count: this is the one
    # wizard whose subject is a number.
    assert "月間支出" in INDEX
    assert "function bwLive()" in INDEX
    # Currency is read off the screen too, or every figure renders unitless
    # until the step is left.
    assert "function bWizCur()" in INDEX
    assert "step 1 of 3" not in INDEX and "step ${w.step} of 3" not in INDEX


def test_the_rail_does_not_tick_a_step_nobody_has_visited():
    """Both the tool and the member source are prefilled when the wizard
    opens, so keying "done" off the value alone ticked steps 1 and 2 green
    before the operator had looked at either."""
    assert "const passed = w.editing || w.step > st.k;" in INDEX


def test_linking_does_not_open_on_an_already_linked_tool():
    """b-open picked the first OBSERVED tool whichever it was, so on a
    deployment whose busiest tool is already linked it opened on that one -
    and pressing through to the end overwrote the subscription that existed,
    with nothing on screen saying so. Caught by driving the wizard and reading
    the review step, which named a tool the Budget view already listed."""
    assert "const taken = new Set();" in INDEX
    assert "const free = (REGTOOLS || []).slice()" in INDEX
    assert "filter(t => !taken.has(t.id));" in INDEX


def test_the_member_step_names_every_connector_and_its_plan():
    """Automatic sync exists for two of the thirty tools the registry ships,
    and the only way to find that out was to open the dropdown and not see
    yours. The step now lists the connectors with the plan each needs.

    The general note replaced a ChatGPT-specific one: naming a single absence
    made it look like the only one, when every tool without a connector is in
    exactly the same position."""
    assert "プラン、およびその方法" in INDEX
    # There used to be a SECOND table listing only the built connectors,
    # directly above a dropdown containing exactly those same connectors. It
    # said nothing the full table does not, and having both invited the
    # reading that the dropdown was the list of vendors rather than the list
    # of ones with code behind them.
    assert "The complete list of vendors" not in INDEX
    assert "plan it needs" not in INDEX
    assert "一覧にないツールはCSVで取り込むか" in INDEX
    assert "手動で登録してください" in INDEX
    # The old copy spoke only about ChatGPT in the general slot.
    assert "const BPROVIDER_NONE = `ChatGPT Business" not in INDEX


def test_a_tool_with_no_licence_mates_says_so():
    """Atlassian Rovo shares a licence group with nothing, so "Also covers"
    rendered an empty chip row and a bare "more tools..." - which reads as a
    control that failed to load rather than one with nothing to offer."""
    assert "レジストリ内に、このツールとライセンスグループまたはベンダーを共有するものはない" in INDEX
    assert "すべてのツールから選択" in INDEX


def test_the_member_step_answers_why_a_tool_is_missing():
    """Naming only the two built connectors left the operator of the other
    twenty-eight with no answer. The step now separates "the vendor offers
    nothing" from "the vendor offers something nobody has connected", which is
    the only one of the two worth opening an issue about."""
    for needle in ("member_apis", "管理APIあり・自動同期未対応",
                   "シート一覧がありません", "未記載",
                   "管理APIあり・未接続",
                   "自動同期に対応済みのツール"):
        assert needle in INDEX, needle
    # A connector written from a docs page is not a connector anybody has
    # run. Being in the dropdown reads as "this works", so the ones that have
    # never touched a real tenant say so where the key gets pasted.
    assert "unverified" in INDEX
    assert "実際の組織に対して実行されたことはありません" in INDEX


def test_import_and_manual_speak_about_the_tool_being_linked():
    """Import and Manual carried a paragraph about ChatGPT whichever tool you
    were linking. It went stale the moment a ChatGPT connector existed: it
    told an Enterprise workspace to use Import when Automatic had just started
    working for it. The answer is per-tool and already in member_apis, so the
    note is built from that instead of from one vendor's example."""
    assert "BPROVIDER_CHATGPT" not in INDEX
    assert "ChatGPT Business (Team) is the usual surprise" not in INDEX
    for needle in ("は自動で同期できます",
                   "のベンダーはメンバーAPIを提供しています",
                   "読み取れる組織またはシート一覧がありません",
                   "メンバーAPIを文書化していません"):
        assert needle in INDEX, needle


def test_a_tool_you_defined_is_not_reported_as_undocumented():
    """member_apis covers the tools this release ships with. A tool the
    operator defined has no row, and an absent row is not a finding - falling
    through to the "not documented" branch made the page state, about a tool
    invented five minutes earlier, that its vendor documents no members API.
    Nobody had looked. "We have no record" and "we looked and there is
    nothing" are different sentences."""
    assert "はあなたが定義したツールです" in INDEX
    assert "ここにはそのベンダーが提供する内容の記録はありません" in INDEX
    # And the table says which tools it is actually about.
    assert "今回のリリースに同梱されるツール" in INDEX
    assert "独自に追加したツールは含まれません" in INDEX


def test_the_budget_page_lists_providers_as_a_list_not_a_chain():
    """The empty state joined every provider with " and ". At two vendors that
    read fine; at seven it was one breathless sentence. The trailing line
    about ChatGPT Business went with it - it is one plan of one vendor, it
    stopped being the only notable absence, and the wizard's own step now says
    what applies to the tool being linked."""
    assert "ChatGPT Business has no admin API on that plan" not in INDEX
    assert "labels.slice(0, -1).join('、')" in INDEX


def test_a_new_plan_hands_its_key_to_what_follows():
    """Linking a second plan on a tool with "CSV" as the source opened the
    import with no plan key: the wizard passed on its own empty one, and the
    receiver - rightly - refuses to guess between two plans. The wizard now
    reads the key the receiver derived back from the save's answer and hands
    it to the connection, the first sync and the import alike."""
    html = (main.STATIC / "index.html").read_text()
    save = html.split("if (act === 'b-save') {", 1)[1].split("if (act === 'b-sync')", 1)[0]
    assert "const mine = (saved.subscriptions || []).find(x => x.tool_id === w.tool_id" in save
    assert "if (mine) pk = mine.plan_key || 'default';" in save
    assert "plan_key: w.plan_key || ''" not in save.split("let pk =", 1)[1]
    assert save.count("plan_key: pk") == 3


def test_the_import_asks_which_plan_when_it_does_not_know():
    """The screen names the plan it is importing into, and when it has no key
    on a tool with several plans it asks rather than letting the import fail
    with the receiver's refusal after the paste."""
    html = (main.STATIC / "index.html").read_text()
    view = html.split("function budgetImport() {", 1)[1].split("\nfunction ", 1)[0]
    assert "const askPlan = !BCSV.plan_key && plans.length > 1;" in view
    assert 'id="b-csv-plan"' in view
    assert "parsed.members.length && !askPlan" in view
    assert "e.target.id === 'b-csv-plan' && BCSV" in html


def test_a_headerless_paste_keeps_the_role_and_seat_it_plainly_carries():
    """"jane@corp.example,member,max 5" is the common paste. With no header
    line the parser kept only the address and dropped the other two, which
    reads as a broken import. It now names a column from its values - all
    role words is the role, account states are a status and ignored, the
    one column left is the seat tier - and only says a column is unread
    when it genuinely cannot name it."""
    html = (main.STATIC / "index.html").read_text()
    fn = html.split("function parseUsersCsv(text) {", 1)[1].split("\n}\n", 1)[0]
    assert "const isRole = /^(owner|admin|administrator|member|members|user|users|viewer|guest|billing|manager|editor)$/i;" in fn
    assert "const isStatus = /^(active|inactive|invited|pending|suspended|deactivated|disabled|enabled)$/i;" in fn
    assert "if (spare.length === 1) iTier = spare[0];" in fn
    assert "guessed = iRole >= 0 || iTier >= 0;" in fn
    assert "&& i !== iRole && i !== iTier && !ignored.includes(i)).length" in fn
    assert "'ヘッダー行なし、列名は値から生成'" in html


def test_a_subscription_record_is_collapsible_and_remembers_being_open():
    """Each subscription is a native <details> record: collapsed by default,
    keyboard-openable, its summary carrying commitment, allocation, observed
    use and review count. Every action on the page ends in a render that
    rebuilds the cards, so open state is kept per record for the session,
    and a record just linked or imported into opens itself."""
    html = (main.STATIC / "index.html").read_text()
    card = html.split("function budgetCard(sub) {", 1)[1].split("\nfunction budgetImport()", 1)[0]
    assert 'return `<details class="budget-card${reviewCount ? \' has-review\' : \'\'}" data-bkey="${esc(bKey(sub))}"${BOPEN.has(bKey(sub)) ? \' open\' : \'\'}>' in card
    assert '<summary class="budget-card-summary">' in card
    for act in ("b-sync", "b-edit", "b-import", "b-unlink", "b-madd"):
        assert f'data-act="{act}"' in card, act
    assert "let BOPEN = new Set();" in html
    assert "app.addEventListener('toggle', e => {" in html
    # three places open a record on purpose, plus the toggle listener itself
    assert html.count("BOPEN.add(") == 4
    css = (main.STATIC / "enterprise.css").read_text()
    assert ".budget-card>summary{display:block;list-style:none;cursor:pointer}" in css
    assert ".budget-card-summary:focus-visible{outline:2px solid var(--acc)" in css
    assert "var(--ok)" not in css
