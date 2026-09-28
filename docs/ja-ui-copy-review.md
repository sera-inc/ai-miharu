# 製品UIの日本語レビュー記録

**対象**: `portal/app/static/index.html` ほか、ポータル・拡張機能・デモで利用者が読む文言（JavaScript が生成するメッセージ、ダイアログ、空・エラー・読み込み中の表示、表、グラフ、メニュー、フォーム、ツールチップを含む）
**実施日**: 2026-09-28　**実施**: Claude Opus 5.5（最終品質レビュー。人間のレビュー承認ではない）

## 方法

1. 各文言について、`main` ブランチ（原著 Shadow AI Guard の英語版）の該当箇所を突き合わせ、画面上で利用者に伝えるべき**実際の意味**を先に確認した。下表の「実際の意味（原文）」列がその記録。
2. 直訳調・不自然・意味の誤り・用語の不統一がある文言だけを修正した。自然に読める既存訳は変更していない。
3. 製品名・プロトコル名・規格名・略語は、訳すと意味が伝わりにくくなるものは原語のまま残し、必要な箇所で日本語の説明を添えた（例: `MCP（Model Context Protocol）`、`ISO/IEC 42001`、`Codex CLI`、`Grafana`、`Entra`）。
4. 変更後にポータルの Python テスト、Node の描画テスト、ブラウザーでの主要画面確認を行った（結果はコミットと引き継ぎに記録）。

## 用語の統一方針

| 原語 | 統一後 | 補足 |
|---|---|---|
| Paste guard | 貼り付けガード | 機能名。LP と同じ表記。「ペーストガード」「ペースト ガード」を置き換え |
| AI register | AI台帳 | 利用判断（承認・責任者・レビュー期限）の記録 |
| Tool registry / registry | ツールレジストリ／レジストリ | 検出に使うツール定義。AI台帳とは別機能 |
| decision（AI register） | 判断 | 「決定」「意思決定」「判定」を統一 |
| System health | システム状態 | 「システム正常性」「システム検出状況」を統一 |
| Detection sources | 検出ソース | 「検出元」「ソース」単独を統一 |
| device | 端末 | 画面内で「デバイス」「端末」「マシン」が混在していたため統一。OAuth の「デバイスコード」など技術用語は除く |
| collector | 収集エージェント | 「コレクタ」を統一 |
| Collector coverage | 収集エージェントのカバー率 | 「確認率」は誤訳 |
| open（個人アカウント） | 未解決 | 「確認済み」を含み、「許容済み」だけが外れる件数 |
| accepted（個人アカウント） | 許容済み | ツールの「承認済み」と区別 |
| overridden（貼り付けガード） | 警告後に続行 | 「上書き」は誤訳 |
| MCP / CLI / IDE | MCP / CLI / IDE | 略語のまま。MCP は初出で日本語の説明を付ける |
| browser | ブラウザー | 表記ゆれ（ブラウザ／ブラウザー）を統一 |

## 意味・動作の誤りとして修正したもの（31 件）

| 画面・箇所 | 実際の意味（原文） | 修正後 | 理由 |
|---|---|---|---|
| 未完了のセットアップ | "A log store: Findings stay in container logs, so no page here can count them." | 未設定だと検出結果はコンテナのログに残るだけで、 ／ このポータルのどのページでも集計できません。 | 【意味の誤り】原文は「どのページでも数えられない」。訳が逆の意味になっていた。 |
| 未完了のセットアップ | "The required ones are not about it refusing to run. They are about it running <b>wrong</b>." / "Nothing here is broken. These are the parts that are not earning their keep yet." | 必須項目が未設定でも動作は止まりません。ただし、誤った結果を表示します。 ／ 不具合ではありません。設定すると、まだ使っていない機能が役立つようになります。 | 【意味の誤り】強調が「正しく動作する」になり、原文（誤って動作する）と逆だった。 |
| 概要・対応事項 | "Close the collector coverage gaps" / "Review detection coverage" | 収集エージェント未導入の端末を解消 ／ 検出カバレッジを確認 | 【意味の誤り】coverage gap は「未導入の端末」であり「確認率」ではない。 |
| 判断待ちキュー | button "Add to registry" (opens the tool registry form) | data-act="cand-add" data-key="…">レジストリに追加 | 【意味の誤り】このボタンはツールレジストリ（検出定義）の登録フォームを開く。AI台帳（利用判断）とは別機能。 |
| 判断待ちキュー | pill "not in registry" / "new today" | レジストリ未登録 ／ 本日新規 | 【意味の誤り】in_registry はツールレジストリへの登録有無。AI台帳ではない。 |
| 概要・自律AI | columns "Device" / "Runs" / "Schedule" / "Reaches" / "Answers to" | 端末 ／ 実行内容 ／ スケジュール ／ 接続先 ／ 責任者 | 【意味の誤り】"Answers to" は責任者。「報告先」ではない。 |
| 概要・主要件数 | "Open personal accounts" / "N first seen in the last 7 days · N accepted" | 過去 … の初検出 … 件${ open.length !== f.personal.length ? ／ 検出結果を取得できません | 【意味の誤り】Open は「未解決」の件数で、「開く」ではない。語順も崩れていた。accepted はツールの承認と区別して「許容済み」。 |
| 概要・主要件数 | "Collector coverage" / "N of M observed devices" | 観測した端末 … 台中 … 台 ／ 検出結果を取得できません | 【意味の誤り】coverage を「確認率」と訳していた。 |
| 概要・AI支出 | badges "N idle" / "N unseated" / "Nothing flagged" | 指摘なし | 【意味の誤り】unseated は「シートを持たずに使っている人」。「未割り当て」では逆の意味に読める。 |
| 概要・検出カバレッジ | caption "Collector coverage" | 収集エージェントのカバー率 | 【意味の誤り】「確認率」ではない。 |
| 概要・貼り付けガード | "Running on N device(s)[ across V versions], so low numbers here genuinely mean few risky pastes." | … 台の端末で動作しています${versions > 1 ? ／ : ''}。件数が少ないのは、これらの端末で危険な貼り付けが実際に少ないことを示します。 | 【意味の誤り】訳文が原文と逆の主張（件数だけでは判断できない）になっていた。導入済み端末に限った原文の意味に戻した。 |
| 概要のカード説明 | detection_coverage "Collector coverage and which sources report" | 収集エージェントのカバー率と、報告中の検出ソース | 【意味の誤り】「確認率」を修正。 |
| 端末 | summary "N devices" / "N AI tools observed" / "N with personal accounts" / "N unattributed" | 端末一覧の概要 ／ aria-label="端末一覧の概要"> … 台の端末 … 種類のAIツール … 台で個人アカウントを利用 … 台は利用者が未登録 | 【意味の誤り】personal は端末の台数で「件の個人利用」ではない。単位を明示。 |
| 利用者対応表 | placeholder "key,identity / C02XXXX,jo.bloggs / jo.bloggs,Jo Bloggs" | key,identity / C02XXXX,taro.yamada / taro.yamada,山田太郎 ／ placeholder="key,identity / C02XXXX,taro.yamada / taro.yamada,山田太郎" | 【不具合】取り込み処理が見出し行として読み飛ばすのは英語の key 行だけ。訳した見出しをそのまま使うと「キー→人物」という誤った対応が保存される。 |
| ツール | title "Of the devices this tool was found on, how many show the AI actually being used." / "N using" | このツールが検出された端末のうち、AIが実際に使われた形跡がある端末の数です。 ／ title="このツールが検出された端末のうち、AIが実際に使われた形跡がある端末の数です。">うち … 台で利用 | 【誤訳】説明文が疑問文になっていた。 |
| MCPサーバーの詳細 | "N device(s) · configured by X · first seen D (unknown) · last seen D (unknown)" | 不明 | 【未翻訳】unknown が英語のまま表示されていた。ツールは内部IDではなく表示名にした。 |
| ツールレジストリの登録 | "This tool is already in the registry. Change what you need here; its identifiers are on the next step." / "Name the tool and identifiers will be proposed for it. Nothing is saved until you have confirmed them." | このツールはすでにレジストリに登録されています。必要な項目をここで変更してください。識別子は次の手順で編集できます。 ／ ツール名を入力すると、識別子の候補を提案します。確認するまで何も保存されません。 | 【意味の誤り】登録先は AI台帳 ではなくレジストリ。改行で空白も入っていた。 |
| ツールレジストリの登録 | "Seen on N devices" | 検出端末 ／ … 台 | 【誤訳】"Seen on" を「確認日」としていたが、中身は端末の台数。 |
| ツールレジストリの登録 | category options (raw English values) | … | 【未翻訳】カテゴリが coding などの英語のまま表示されていた。保存する値は英語のまま value に残した。 |
| ツールレジストリの登録 | "Name, vendor, id and category are all required: the registry refuses an entry without them." | 名前、提供元、識別子、カテゴリはすべて必須です。未入力の項目があるとレジストリに登録できません。 | 【意味の誤り】登録を拒否するのはレジストリ。 |
| ツールレジストリの登録 | derived suggestion pill "low confidence" | 信頼度 … | 【未翻訳】low が英語のまま表示されていた。 |
| ツールレジストリの登録 | review statuses "unseen" / "already matching" / "watching" | 検出できない ／ 一致あり ／ 一致待ち | 【意味の誤り】unseen は識別子が無くこの利用環境では検出できない状態で、「未検出」ではない。 |
| ツールレジストリ | columns "id" / "name" / "vendor" / "identifiers" (a count) / "updated" | 識別子 ／ 名前 ／ 提供元 ／ 検出用識別子の数 ／ 更新日時 | 【誤訳】identifiers 列は検出用の識別子の件数で、「ベンダー識別子」ではない。 |
| AI台帳 | status pill "not in registry" | レジストリ未登録 | 【意味の誤り】AI台帳の画面上で「AI台帳に未登録」と表示していた。未登録なのはレジストリ。 |
| AI台帳 | metric "not in registry" | … ／ レジストリ未登録 | 【意味の誤り】observed_not_in_registry はレジストリ未登録の件数。 |
| AI台帳 | "… name tools the registry does not know:" | レジストリにないツールを指定した…が…件あります： | 【意味の誤り】原文は the registry。 |
| AI台帳 | button "Add to registry" | data-key="…">レジストリに追加 | 【意味の誤り】AI台帳の画面上のツールに「AI台帳に追加」と表示していた。追加先はレジストリ。 |
| ISO/IEC 42001 証跡 | "N tools in use, N watched for, N not in the registry" | 、… 件はレジストリ未登録 | 【意味の誤り】not in the registry を「台帳に登録されていません」としていた。 |
| ISO/IEC 42001 証跡 | "Monitoring coverage: N of M expected sources reporting" (link "Setup") | 検出ソースの報告状況 ／ 想定される検出ソース … 件のうち、… 件から報告があります ／ 検出ソース | 【誤訳】リンク先は「検出ソース」画面で「初期設定」ではない。 |
| ISO/IEC 42001 証跡 | review input "N tool(s) in use and not in the registry" / "N decision(s) with no owner" | 利用中のツール … 件がレジストリに未登録です ／ 責任者が未設定の判断が … 件あります | 【意味の誤り】not in the registry を「AI台帳に登録されていません」としていた。owner は責任者。 |
| ISO/IEC 42001 証跡 | "The JSON identifies registry and governance files by hash. It may not be reproduced identically after log retention changes; its checksum detects accidental changes, not deliberate modification." | JSONには、レジストリとガバナンスファイルを識別するハッシュ値が含まれます。 | 【意味の誤り】ハッシュ値で識別するのはレジストリのファイル。AI台帳ではない。 |

## `portal/app/static/index.html`（291 件）

| 画面・箇所 | 実際の意味（原文） | 修正前 | 修正後 | 理由 |
|---|---|---|---|---|
| サイドバー | aria-label "Go to Workspace overview" | ワークスペース概要へ移動 ／ aria-label="ワークスペース概要へ移動" | 概要へ移動 ／ aria-label="概要へ移動" | 「ワークスペース」は画面上に存在しない呼称。移動先の画面名だけにした。 |
| サイドバー | aria-label "Open System health" | システム検出状況を開く ／ aria-label="システム検出状況を開く"> | システム状態を開く ／ aria-label="システム状態を開く"> | 移動先の画面名は「システム状態」。別名の「システム検出状況」を使わない。 |
| サイドバー | "Checking sources…" (estate status while loading) | ソースを確認中… | 検出ソースを確認中… | 何の「ソース」かを明示。 |
| サイドバー | chevron text "System health" | システム検出状況 | システム状態 | 画面名に合わせて統一。 |
| ヘッダー | "Checking sources…" | ソースを確認中… | 検出ソースを確認中… | 何の「ソース」かを明示。 |
| ヘッダー検索 | placeholder "Search this view, or jump to a page, tool or device…" | このビューを検索、またはページ、ツール、端末へ移動… ／ placeholder="このビューを検索、またはページ、ツール、端末へ移動…" | この画面内を検索、またはページ・ツール・端末へ移動… ／ placeholder="この画面内を検索、またはページ・ツール・端末へ移動…" | 「ビュー」は開発者用語。利用者には「画面」。 |
| ヘッダー | title "Checking which detection sources have reported" | どの検出ソースが報告済みか確認中 ／ title="どの検出ソースが報告済みか確認中" | 報告済みの検出ソースを確認しています ／ title="報告済みの検出ソースを確認しています" | 直訳調の語順を自然な文にした。 |
| ヘッダー | "Checking sources…" (trust state) | ソースを確認中… | 検出ソースを確認中… | 何の「ソース」かを明示。 |
| ヘッダー | title "light / dark" | ライト / ダーク ／ title="ライト / ダーク">◐ | ライト / ダーク表示を切り替え ／ title="ライト / ダーク表示を切り替え" aria-label="ライト / ダーク表示を切り替え">◐ | 記号だけのボタンに操作内容の名前を付けた（読み上げ時に「◐」だけにならない）。 |
| ツアー終了ダイアログ | "You can take it again whenever you like, under Settings › Getting started - along with the setup wizard." | いつでも、次の場所からもう一度実行できます: 設定 › はじめに — セットアップウィザードと併せて | ツアーは設定 › はじめにからいつでも再開できます。セットアップウィザードも同じ場所にあります。 | 英語の語順をなぞった分断文を1文にした。 |
| セットアップのスキップ確認 | "Nothing is collected until two things are set." | 2つの項目が設定されるまで、何も収集されません。 | 次の2項目を設定するまで、検出結果は正しく集まりません。 | 本文の趣旨（止まるのではなく誤った内容になる）と矛盾しない表現にした。 |
| セットアップのスキップ確認 | "The receiver address is all a collector download bakes in, and with no corporate domains every account reads as a personal one - so the Overview headline, Personal accounts and the ISO evidence would all report the wrong thing rather than report nothing." | 収集エージェントのダウンロードに組み込まれるのは受信サービスアドレスだけであり、企業ドメインが設定されていないと、すべてのアカウントが個人用として認識されます。そのため、概要の見出し、個人アカウント、ISO証跡はいずれも、何も報告しないのではなく、誤った内容を報告することになります。 | 収集エージェントのダウンロードには受信サービスのアドレスが埋め込まれます。また、企業ドメインが未設定だと、すべてのアカウントが個人アカウントとして扱われます。その結果、概要の見出し・個人アカウント・ISO/IEC 42001 の証跡は「何も表示しない」のではなく、誤った内容を表示します。 | 直訳の長文を2文に分け、規格名を正式表記にした。 |
| セットアップのスキップ確認 | "You can pick this up again whenever you like, under Settings › Getting started." | いつでも、次の場所から再開できます: 設定 › はじめに. | 設定 › はじめにからいつでも再開できます。 | 英語の句読点「.」が残っていた。 |
| パスワード変更 | "Every other session is signed out with the old password; this one stays." | 他のすべてのセッションは古いパスワードでサインアウトされ、このセッションは維持されます。 | ほかの端末やブラウザーのセッションはすべてサインアウトされます。この画面のセッションはそのまま使えます。 | 「古いパスワードでサインアウト」は誤読を招く直訳。 |
| サインイン | "No admin account exists yet. The receiver printed a one-time setup code to its log when it started - find it with … or …. The code works once; if you lose it, restart the receiver for a fresh one." | 管理者アカウントがまだ存在しません。受信サービスは起動時に1回限りのセットアップ コードをログに出力しました - 次のコマンドで確認できます: kubectl logs deploy/&lt;release&gt;-ai-guard \| grep setup_code または docker compose logs receiver。コードは1回のみ有効です。 紛失した場合は、受信サービスを再起動して新しいコードを発行してください。 | 管理者アカウントはまだありません。受信サービスが起動時に1回限りのセットアップコードをログへ出力しています。kubectl logs deploy/&lt;release&gt;-ai-guard \| grep setup_code または docker compose logs receiver で確認してください。コードは1回だけ使えます。分からなくなった場合は、受信サービスを再起動すると新しいコードが発行されます。 | 行の折り返しで「セットアップ コード」に空白が入っていた。ダッシュ区切りの直訳を解消。 |
| サインイン | "Uses your work email." (SSO required) | 職場のメールアドレスを使用します。 | 仕事用のメールアドレスでサインインします。 | 何に使うのかを明示。 |
| サインイン | "Single sign-on is required here, so a password only works for the break-glass account - the one this deployment was set up with. It is the way back in if the identity provider is unreachable." | ここではシングルサインオンが必須のため、パスワードは緊急用アカウント（この環境のセットアップに使用したアカウント）でのみ使えます。IDプロバイダーに接続できない場合の復旧手段です。 | この環境ではシングルサインオンが必須です。パスワードでサインインできるのは、セットアップ時に作成した緊急用アカウントだけです。IDプロバイダーに接続できないときの復旧用に使います。 | 括弧書きの補足を文に組み込み読みやすくした。 |
| サインイン | "Uses your work email." (SSO optional) | 職場のメールアドレスを使用します。 | 仕事用のメールアドレスでサインインします。 | 何に使うのかを明示。 |
| セッション切れ | "Signed out - the session expired or was revoked. Sign in again." | サインアウトしました - セッションが期限切れまたは無効化されました。もう一度サインインしてください。 | セッションの有効期限が切れたか、無効になったためサインアウトしました。もう一度サインインしてください。 | ダッシュ区切りの直訳を因果が分かる1文にした。 |
| 設定変更の通知 | "Settings were changed by <b>X</b> N minutes ago. This page was loaded before that, so what you are looking at may be out of date. [Reload] Saving here changes only the fields you edit, so you will not overwrite theirs by accident." | 設定を変更したユーザー: … … 分前。このページはそれより前に読み込まれたため、表示内容が古い可能性があります。 | … さんが … 分前に設定を変更しました。このページはそれより前に読み込まれたため、表示が古い可能性があります。 | 「変更したユーザー: X N分前」という項目名の羅列を文にした。 |
| 設定変更の通知 | same (second sentence) | ここで保存すると、編集したフィールドだけが変更されるため、他のユーザーの変更を誤って上書きすることはありません。 | ここで保存して変更されるのは、編集した項目だけです。ほかの人の変更を誤って上書きすることはありません。 | 「フィールド」を利用者向けの「項目」にし、長い因果文を分けた。 |
| 未完了のセットアップ | "The receiver address: Nothing can deploy without it: every collector download bakes this in." | これがないと何もデプロイできません。どの ／ 収集エージェントのダウンロードにもこれが組み込まれます。 | 未設定だと何も展開できません。収集エージェントのダウンロードには ／ 必ずこのアドレスが埋め込まれます。 | 英語の単語区切りの空白が「どの 収集」と文中に残っていた。 |
| 未完了のセットアップ | "Corporate domains: Without them every account reads as a personal one, and the Overview headline inherits that." | これらがないと、すべてのアカウントが ／ 個人アカウントとして扱われ、概要の見出しもそれを引き継ぎます。 | 未設定だと、すべてのアカウントが個人アカウントとして ／ 扱われ、概要の見出しもその前提で表示されます。 | 文中の余分な空白を除き、「引き継ぐ」の直訳を言い換えた。 |
| 未完了のセットアップ | "A log store: Findings stay in container logs, so no page here can count them." | 検出結果はコンテナログに残るため、ここにあるどのページでも ／ それらを数えられます。 | 未設定だと検出結果はコンテナのログに残るだけで、 ／ このポータルのどのページでも集計できません。 | 【意味の誤り】原文は「どのページでも数えられない」。訳が逆の意味になっていた。 |
| 未完了のセットアップ | "Email: N person has / people have an account here and has/have never been told." / "Nobody can be told an account was made for them." | 人がここにアカウントを持っており、まだ通知されていません。 ／ 自分のアカウントが作成されたことを誰にも伝えられません。 | アカウントを作成済みで、まだ案内メールを受け取っていない人が ／ 人います。 ／ アカウントを作成しても、本人に案内メールを送れません。 | 「自分のアカウントが…誰にも伝えられません」は主語が逆転した誤訳。 |
| 未完了のセットアップ | "Single sign-on: People sign in with a portal password rather than their work account." | ユーザーはポータルのパスワードでサインインしており、 ／ 職場のアカウントではありません。 | 利用者は仕事用アカウントではなく、このポータル専用の ／ パスワードでサインインしています。 | 文中の余分な空白と、否定が後ろに来る直訳を解消。 |
| 未完了のセットアップ | "Update available: X" / "System health has the release notes and the commands for this deployment." / "See how" | 更新があります: ／ システム状態には、リリースノートと、このデプロイメント用のコマンドがあります。 ／ 方法を見る | 新しいリリースがあります: ／ リリースノートと、この環境向けの更新コマンドをシステム状態で確認できます。 ／ 確認する | 「方法を見る」は操作名として不自然。 |
| 未完了のセットアップ | heading "Some of this deployment is not set up" / "A few things are still worth doing" | このデプロイメントの一部が未設定です ／ まだいくつか対処すべき点があります | この環境には未設定の項目があります ／ 設定しておくとよい項目があります | 「デプロイメント」は開発者用語。 |
| 未完了のセットアップ | "The required ones are not about it refusing to run. They are about it running <b>wrong</b>." / "Nothing here is broken. These are the parts that are not earning their keep yet." | 必須項目は、動作を拒否することではなく、正しく動作することに関係します。 ／ ここに壊れているものはありません。まだ十分に活用されていない部分です。 | 必須項目が未設定でも動作は止まりません。ただし、誤った結果を表示します。 ／ 不具合ではありません。設定すると、まだ使っていない機能が役立つようになります。 | 【意味の誤り】強調が「正しく動作する」になり、原文（誤って動作する）と逆だった。 |
| 未完了のセットアップ | "Shown because setup was skipped or left part-done. It never blocks anything." | 設定がスキップされたか、一部のみ完了したため表示されています。何もブロックしません。 | セットアップをスキップしたか、途中で終えたため表示しています。操作が制限されることはありません。 | 「何もブロックしません」は何が何を止めないのか分かりにくい直訳。 |
| 概要・対応事項 | "Findings are unavailable. Check System health before interpreting these counts." | 検出結果を利用できません。これらの数値を解釈する前に、システム正常性を確認してください。 | 検出結果を取得できません。数値を判断する前に、システム状態を確認してください。 | 画面名は「システム状態」。「利用できません」より原因が伝わる「取得できません」に統一。 |
| 概要・対応事項 | "Follow up on activity in accounts outside your corporate domains." | 企業ドメイン外のアカウントのアクティビティを確認してください。 | 企業ドメイン以外のアカウントでの利用を確認してください。 | 「アクティビティ」は直訳。 |
| 概要・対応事項 | "View findings and recorded outcomes" | 検出結果と記録された結果を表示 | 検出結果と対応記録を見る | 「結果と結果」の重複を解消。 |
| 概要・対応事項 | "Close the collector coverage gaps" / "Review detection coverage" | 収集エージェントの確認率を改善 ／ 検出カバレッジを確認 | 収集エージェント未導入の端末を解消 ／ 検出カバレッジを確認 | 【意味の誤り】coverage gap は「未導入の端末」であり「確認率」ではない。 |
| 概要・対応事項 | "N scanner-observed device(s) without a collector signal." / "N gaps" / "Verify enrollment and reporting" | …台のスキャナで観測されたデバイス（コレクタ信号なし）。 ／ …件のギャップ ／ 登録と報告を確認 | スキャナーでは観測されたものの、収集エージェントから報告がない端末が … 台あります。 ／ 未導入 … 台 ／ 端末の登録と報告状況を確認 | 括弧書きの直訳と、「コレクタ」「ギャップ」の用語不統一を解消。 |
| 概要・対応事項 | "Complete the AI register" / "Register data is unavailable; open the register to check it." / "N discovered tool(s) without a recorded decision." / "Not read" / "N overdue review(s)" / "N decisions" / "Confirm ownership and permitted use" | AI台帳を完成させる ／ 台帳データを利用できません。台帳を開いて確認してください。 ／ …件の検出されたツール（記録された決定なし）。 ／ 未読み取り ／ …件の期限超過レビュー ／ …件の決定 ／ 所有権と許可された用途を確認 | AI台帳に判断を記録 ／ AI台帳のデータを取得できません。AI台帳を開いて確認してください。 ／ 判断が未記録の検出ツールが … 件あります。 ／ 未取得 ／ レビュー期限超過 … 件 ／ 判断記録 … 件 ／ 責任者と利用範囲を確認 | 「所有権」は ownership（担当者）の誤訳。括弧書きの直訳を文にした。 |
| 概要・検出ツール表 | column headers "Observed surfaces" / "Devices ↓" / "Activity" | AIツール ／ 観測された利用環境 ／ デバイス ↓ ／ クラウドID ／ 個人アカウント ／ アクティビティ | AIツール ／ 利用環境 ／ 端末数 ↓ ／ クラウドID ／ 個人アカウント ／ 検出件数 | 列の中身（件数の推移）に合う見出しにした。 |
| 概要・検出ツール表 | personal accounts cell "N open" / "None observed" | …件未対応 ／ 観測なし | …件未対応 ／ なし | 個人アカウント列の「観測なし」は、ツール自体が観測されていないと誤読される。 |
| 概要・検出ツール表 | aria-label "Inspect X" | …を検査 ／ aria-label="…を検査"> | …の詳細を開く ／ aria-label="…の詳細を開く"> | 「検査」は操作内容と合わない。 |
| 概要・検出ツール | list item "devices" / "cloud" | …デバイス …クラウド | …端末 …クラウドID | 数えている対象（端末・クラウドID）を明示。 |
| 判断待ちキュー | button "Names nothing" (title "Record that this signal identifies no program.") | このシグナルがどのプログラムも特定しないことを記録します。 ／ title="このシグナルがどのプログラムも特定しないことを記録します。">何も特定しない | このシグナルがどのプログラムにも当てはまらないことを記録します。 ／ title="このシグナルがどのプログラムにも当てはまらないことを記録します。">該当ツールなし | 「何も特定しない」は操作名として意味が通らない。 |
| 判断待ちキュー | button "Add to registry" (opens the tool registry form) | data-act="cand-add" data-key="…">AI台帳に追加 | data-act="cand-add" data-key="…">レジストリに追加 | 【意味の誤り】このボタンはツールレジストリ（検出定義）の登録フォームを開く。AI台帳（利用判断）とは別機能。 |
| 判断待ちキュー | "Awaiting a decision" lede "Discovery and governance work that still needs an owner." | 判断待ち ／ まだオーナーが必要な検出結果とガバナンス作業。 | 判断待ち ／ 担当者の判断がまだ必要な検出結果とガバナンス作業です。 | 「オーナー」はロール名と紛らわしい。 |
| 判断待ちキュー | "Observed, no decision recorded" / "Known tools currently in use without an explicit outcome" | 観測済み、意思決定は未記録 明示的な結果が記録されていない、現在使用中の既知のツール | 利用を確認済み・判断は未記録 利用中の既知のツールのうち、判断が記録されていないもの | 「意思決定」「明示的な結果」は直訳。画面全体で「判断」に統一。 |
| 判断待ちキュー | pill "not in registry" / "new today" | AI台帳に未登録 ／ 今日の新規 | レジストリ未登録 ／ 本日新規 | 【意味の誤り】in_registry はツールレジストリへの登録有無。AI台帳ではない。 |
| 判断待ちキュー | "Recording a decision clears the tool from this queue." | 意思決定を記録すると、ツールはこのキューから削除されます。 | 判断を記録すると、このキューから外れます。 | 「削除」はデータが消えると誤解される。 |
| 概要・自律AI | "Not read yet. Open Agentic AI." | 未読です。エージェント型AIを開いてください。 | まだ読み込んでいません。「エージェント型AI」を開いてください。 | 「未読」はメッセージの既読と紛らわしい。 |
| 概要・自律AI | button "Open Agentic AI →" | エージェント型AI … を開く | エージェント型AIを開く … | 矢印アイコンが文の途中に入り「エージェント型AI → を開く」と表示されていた。 |
| 概要・自律AI | "Nothing reported starting itself. [N process(es) reached a model unrecognised, which is a different question.] That is either true or the collectors have not been updated to look. System health says which." | ／ 自己起動したという報告はありません。${ c.unrecognised ? ／ : ''} それは、 本当であるか、収集側が確認するように更新されていないかのどちらかです。システム状態がどちらかを示します。 ／ | ／ 自動で起動するAIの報告はありません。${ c.unrecognised ? ／ : ''}本当に存在しないのか、収集エージェントがまだ確認に対応していないのかは、システム状態で確認できます。 ／ | 改行で文が分断され、「それは、本当であるか…」という直訳になっていた。 |
| 概要・自律AI | "<b>N</b> of M answer to nobody: a credential with no person behind it, so revoking a sign-on does not stop them." / "All of them run under an identity somebody can be asked about." | …（… 中）は誰にも説明責任を負いません。背後に人がいない資格情報のため、サインオンを取り消しても止められません。 ／ いずれも、責任を問える ID で実行されています。 | 全 … 件のうち … 件は責任者がいません。人に紐づかない認証情報で動くため、誰かのサインオンを取り消しても止まりません。 ／ すべて、責任者を確認できるIDで実行されています。 | 「説明責任を負いません」「背後に人がいない資格情報」は直訳。 |
| 概要・自律AI | columns "Device" / "Runs" / "Schedule" / "Reaches" / "Answers to" | デバイス ／ 実行 ／ スケジュール ／ 到達先 ／ 報告先 | 端末 ／ 実行内容 ／ スケジュール ／ 接続先 ／ 責任者 | 【意味の誤り】"Answers to" は責任者。「報告先」ではない。 |
| 概要・自律AI | "nothing configured" | 何も設定されていません | 設定なし | 表のセルとして簡潔にした。 |
| 概要・自律AI | badges "no tool we know" / "a person" / "unattributed" | 既知のツールはありません ／ ある人物 ／ 未帰属 | 既知のツールなし ／ 担当者あり ／ 責任者不明 | 「ある人物」「未帰属」は直訳。 |
| 概要・自律AI | footer "N unrecognised process(es) reached a model" | … 件の未認識プロセスがモデルに到達 | 未登録のプロセス … 件がモデルに接続 | 「到達」は直訳。 |
| 概要・全体状況 | "Your estate at a glance" / "N observed devices · last 7 days" / "Findings unavailable" | … 台の観測済みデバイス · 最終 … ／ 検出結果を利用できません | 観測した端末 … 台 · 過去 … ／ 検出結果を取得できません | 「最終 7日」は期間の意味が伝わらない。 |
| 概要・全体状況 | "Data unavailable" (posture) | データを利用できません | データを取得できません | 原因が伝わる表現に統一。 |
| 概要・全体状況 | "No detection source reported in this window. These counts are missing data, not a clean result." / "N open personal account(s) · N coverage gap(s)" | この期間に報告した検出ソースはありません。これらのカウントはデータ不足であり、問題なしという結果ではありません。 ／ … 件の未対応の個人アカウント · … 件のカバレッジギャップ | この期間に報告した検出ソースはありません。件数が0なのはデータがないためで、問題がないという意味ではありません。 ／ 未解決の個人アカウント … 件 · 収集エージェント未導入の端末 … 台 | 「カウント」「カバレッジギャップ」を利用者向けの語にした。open は確認済みを含むため「未解決」。 |
| 概要・全体状況 | "N people named in personal-account findings · N unnamed devices" / "Do not interpret unavailable data as a clean result." | 個人アカウントの検出記録がある利用者 … 名${f.unnamed ? ／ 利用できないデータを問題なしと解釈しないでください。 | 個人アカウントで検出された利用者 … 名${f.unnamed ? ／ 取得できないデータを「問題なし」と見なさないでください。 | 「名称不明デバイス」は端末名が無いと誤読される（実際は利用者名が不明）。 |
| 概要・主要件数 | "Open personal accounts" / "N first seen in the last 7 days · N accepted" | … 件が過去 …${ open.length !== f.personal.length ? ／ : ''} 以内に初検出 ／ 検出結果を利用できません | 過去 … の初検出 … 件${ open.length !== f.personal.length ? ／ 検出結果を取得できません | 【意味の誤り】Open は「未解決」の件数で、「開く」ではない。語順も崩れていた。accepted はツールの承認と区別して「許容済み」。 |
| 概要・主要件数 | "Collector coverage" / "N of M observed devices" | … / … 台の観測デバイス ／ 検出結果を利用できません | 観測した端末 … 台中 … 台 ／ 検出結果を取得できません | 【意味の誤り】coverage を「確認率」と訳していた。 |
| 概要・主要件数 | "Register decisions" / "Register data unavailable" / "N tools without a recorded decision" | AI台帳データを利用できません ／ … 件の判断が記録されていないツール | AI台帳のデータを取得できません ／ 判断が未記録のツール … 件 | 数値の単位（ツール）が文末に来て読みにくかった。 |
| 概要・AI支出 | "Nothing linked yet. The Budget view records what each AI tool costs and joins it against observed use." | まだ何もリンクされていません。予算ビューでは、各AIツールのコストを記録し、観測された利用状況と突き合わせます。 | まだ契約が登録されていません。予算画面で各AIツールの費用を登録すると、実際の利用状況と照合できます。 | 「リンク」「ビュー」は開発者用語。 |
| 概要・AI支出 | tiles "tracked per month" / "tools linked" / "paid seats never observed" | 毎月追跡${conv | 月額合計${conv | 数値は月額の合計。「毎月追跡」は直訳。 |
| 概要・AI支出 | "paid seats never observed" | 一度も観測されていない有償ライセンス | 利用が確認されていない有償シート | 他の表と同じ「シート」に統一。 |
| 概要・AI支出 | column "Review" (flags) | 更新日 ／ レビュー | 更新日 ／ 要確認 | 列の中身は注意喚起のバッジ。 |
| 概要・AI支出 | badges "N idle" / "N unseated" / "Nothing flagged" | フラグ付きの項目はありません | 指摘なし | 【意味の誤り】unseated は「シートを持たずに使っている人」。「未割り当て」では逆の意味に読める。 |
| 概要・検出ツール | "Findings are unavailable." | ／ 検出結果を利用できません。 ／ | ／ 検出結果を取得できません。 ／ | 表現の統一。 |
| 概要・検出ツール | "No tools match this view." / "N of M discovered tools" / "No data available" | ／ この表示に一致するツールはありません。 ／ ／ … / … 件の検出されたツール ／ 利用可能なデータがありません | ／ この条件に一致するツールはありません。 ／ ／ 検出ツール … 件中 … 件 ／ データがありません | 分数表記の直訳を解消。 |
| 概要・検出ツール | "Observed devices per tool. Cloud-only tools may have zero associated devices." / "One bar per day for the last X, written as a total when the window holds fewer than three days. Devices and cloud identities are counted separately." | ツールごとの観測デバイス。クラウド専用ツールでは関連デバイスが 0 台の場合があります。 ／ 直近 ／ 、1 日あたり 1 本のバーです。期間が 3 日未満の場合は合計で表示されます。デバイスとクラウド ID は別々にカウントされます。 | ツールごとの観測端末数です。クラウドだけで使われるツールは、端末数が0台になることがあります。 ／ 過去 ／ の件数を1日1本の棒で示します（期間が3日未満の場合は合計を表示）。端末とクラウドIDは別々に数えています。 | 文の区切りと数字前後の空白を整理。 |
| 概要・最近の個人アカウント | columns "Person" / "Source" | 人物 ／ アカウント ／ AIツール ／ デバイス ／ 利用環境 ／ ソース ／ 最終確認日時 | 利用者 ／ アカウント ／ AIツール ／ 端末 ／ 利用環境 ／ 検出ソース ／ 最終確認日時 | 「人物」は直訳。 |
| 概要・最近の個人アカウント | "None seen. That is a result, not an absence of one." | 何も観測されていません。それも結果であり、結果がないわけではありません。 | 個人アカウントの利用は観測されていません。データを取得できたうえでの結果です。 | 直訳で意味が取りにくかった。 |
| 概要・最近の個人アカウント | "Latest activity in accounts outside your corporate domains" | 企業ドメイン外のアカウントにおける最新のアクティビティ | 企業ドメイン以外のアカウントでの最近の利用 | 「アクティビティ」は直訳。 |
| 概要・最近の個人アカウント | footer "N in this window" | この期間内の … | この期間に … 件 | 助数詞が無く意味が通らなかった。 |
| 概要・検出カバレッジ | "No status available." | 検出カバレッジ ／ 利用可能なステータスがありません。 | 検出カバレッジ ／ 状態を取得できません。 | 直訳。 |
| 概要・検出カバレッジ | "Visibility across your estate" / "Collector signals across observed devices" | 自社環境全体の可視性 ／ 観測されたデバイスにおける収集エージェントからの報告 | 環境全体の可視化状況 ／ 観測した端末のうち、収集エージェントが報告している割合 | 「可視性」は直訳。 |
| 概要・検出カバレッジ | ring aria-label "N of M devices have a collector signal" | …／… 台のデバイスに収集エージェントからの報告があります ／ 収集エージェントの確認状況を表示できません | 観測した端末 … 台中 … 台で収集エージェントが報告しています ／ 収集エージェントのカバー率を表示できません | 用語を「カバー率」に統一。 |
| 概要・検出カバレッジ | caption "Collector coverage" | 収集エージェントの確認率 | 収集エージェントのカバー率 | 【意味の誤り】「確認率」ではない。 |
| 概要・検出カバレッジ | "Of devices seen by any source in this window." | この期間にいずれかのソースで観測されたデバイスの内訳です。 | この期間にいずれかの検出ソースで観測された端末の内訳です。 | 用語の統一。 |
| 概要・検出カバレッジ | "N/M reporting" | reduce((n,g) => n + g.total, 0)} レポート中 | reduce((n,g) => n + g.total, 0)} 報告中 | 「レポート中」は直訳。 |
| 概要・検出カバレッジ | tooltip "X · N of M dedicated sources reporting" | の専用ソースがレポート中 | ：専用の検出ソース ／ 件中 ／ 件が報告中 | 分数と「レポート中」の直訳を解消。 |
| 概要・検出カバレッジ | title "Dedicated sources for the X surface that are reporting. Other sources can still produce findings for it." | … 利用環境について報告している専用ソースです。他のソースもこの利用環境の検出事項を生成できます。 ／ title="… 利用環境について報告している専用ソースです。他のソースもこの利用環境の検出事項を生成できます。" | …専用の検出ソースのうち、報告しているものです。ほかの検出ソースからも、この利用環境の検出結果が届くことがあります。 ／ title="…専用の検出ソースのうち、報告しているものです。ほかの検出ソースからも、この利用環境の検出結果が届くことがあります。" | 「検出事項を生成できます」は直訳。 |
| 概要・検出カバレッジ | "Latest report by surface" / "findings · devices in this window" | 利用環境別の最新レポート ／ 検出結果 · この期間内のデバイス | 利用環境ごとの最新の報告 ／ 検出件数 · この期間の端末数 | 数値の意味（件数・端末数）を明示。 |
| 概要・検出カバレッジ | "Source catalogue, not configured integrations" / "Review sources" | ソースカタログであり、設定済みの統合ではありません ／ ソースを確認 … | 検出ソースの一覧です（設定済みの連携とは限りません） ／ 検出ソースを確認 … | 「統合」は integration の直訳。 |
| 概要・検出カバレッジ | "Collector coverage uses devices observed by any source, not your entire company fleet. An unobserved source may be unconfigured or inapplicable. These are dedicated sources per surface; other sources can also produce findings for it." | 収集エージェントカバレッジは、全社のデバイス群ではなく、いずれかのソースによって観測されたデバイスを使用します。観測されていないソースは、未設定または適用対象外である可能性があります。これらは利用環境ごとの専用ソースです。他のソースもその利用環境の検出結果を生成できます。 | 収集エージェントのカバー率は、全社のすべての端末ではなく、いずれかの検出ソースで観測された端末を母数にしています。報告のない検出ソースは、未設定か、この環境では使わないものかもしれません。表示しているのは利用環境ごとの専用ソースで、ほかのソースからもその利用環境の検出結果が届くことがあります。 | 「デバイスを使用します」は母数の説明として誤読される直訳。 |
| 概要・個人アカウントの推移 | "Personal-account exposure" / "Not enough days in the window to draw a trend yet." | 個人アカウントの露出 ／ この期間には、まだ傾向を描くのに十分な日数がありません。 | 個人アカウントの利用推移 ／ 推移を表示するには、期間内の日数が足りません。 | 「露出」は exposure の直訳で意味が伝わらない。 |
| 概要・個人アカウントの推移 | "Personal-account exposure" / "Daily detections against reporting coverage" | 個人アカウントの露出 ／ 報告カバレッジに対する日次検出数 | 個人アカウントの利用推移 ／ 1日ごとの検出件数と、報告した端末数 | 直訳。 |
| 概要・報告のない検出ソース | "Silent sources" / "In the catalogue, nothing reported in this window" | 沈黙しているソース … ／ カタログ内で、この期間に報告がなかったもの | 報告のない検出ソース … ／ 一覧にある検出ソースのうち、この期間に報告がなかったもの | 「沈黙」は silent の直訳。 |
| 概要・報告のない検出ソース | columns "Silent" / "Sources" | 利用環境 ／ 沈黙 ／ ソース | 利用環境 ／ 報告なし ／ 検出ソース | 同上。 |
| 概要・報告のない検出ソース | "never" (last seen) | 未確認 | 報告実績なし | 「未確認」では誰が確認していないのか不明。 |
| 概要・報告のない検出ソース | "Unconfigured or not applicable, not necessarily broken" | 未設定または適用対象外であり、必ずしも故障しているわけではありません | 未設定か、この環境では使わないソースです。故障とは限りません | 直訳調の文末を整理。 |
| 概要・貼り付けガード | "Browser extension, on the devices it reached" | ブラウザ拡張機能、到達したデバイス上で | ブラウザー拡張機能を導入した端末での記録 | 「到達したデバイス上で」は直訳。 |
| 概要・貼り付けガード | tile "devices running the guard" | ペーストガードを実行しているデバイス ／ <dt${over | 貼り付けガードが動作中の端末 ／ <dt${over | 用語の統一。 |
| 概要・貼り付けガード | "In block mode, N warned paste(s) would have been stopped outright." | ブロックモードでは、… 件の警告が表示された貼り付けは、ブロックモードではすべて停止されたはずです。 | ブロックモードであれば、警告を表示した … 件の貼り付けはすべて止められていました。 | 「ブロックモードでは」が1文に2回あった。 |
| 概要・貼り付けガード | "Running on N device(s)[ across V versions], so low numbers here genuinely mean few risky pastes." | … 台のデバイスで${versions > 1 ? ／ : ''}実行中です。この件数だけでは、他の端末を含む全体の状況は判断できません。 | … 台の端末で動作しています${versions > 1 ? ／ : ''}。件数が少ないのは、これらの端末で危険な貼り付けが実際に少ないことを示します。 | 【意味の誤り】訳文が原文と逆の主張（件数だけでは判断できない）になっていた。導入済み端末に限った原文の意味に戻した。 |
| 概要・貼り付けガード | "No device has checked in yet, so zero here means \"not deployed\", not \"nobody pasted anything\"." | まだ報告があったデバイスがないため、ここでのゼロは「未展開」を意味し、「誰も何も貼り付けなかった」という意味ではありません。 | まだ報告した端末がないため、0件は「未導入」を意味します。「誰も貼り付けていない」という意味ではありません。 | 直訳調の長文を整理。 |
| 概要・貼り付けガード | columns "Where pastes went" / "Warned" / "Overridden" / "Blocked" / "Detectors" | ペースト先 ／ 警告表示数 ／ 警告後の続行数 ／ ブロック数 ／ 検出機能 | 貼り付け先 ／ 警告 ／ 警告後に続行 ／ ブロック ／ 検出ルール | 「検出機能」は detector の直訳。実際は検出ルール（AWSキー、カード番号など）。 |
| 概要・優先して確認すること | "Where to focus" / "Follow-ups across your AI estate" / "Action queue" | 注目すべきポイント ／ AI資産全体にわたるフォローアップ ／ アクションキュー | 優先して確認すること ／ AI利用全体で対応が必要な事項 ／ 対応キュー | 「フォローアップ」「アクションキュー」は直訳。 |
| 概要・優先して確認すること | "Register not read" / "N awaiting a decision" | AI台帳未読み取り ／ … 件が判定待ち | AI台帳を取得できません ／ 判断待ち … 件 | 「判定」と「判断」の混在を解消。 |
| 概要・Grafana | "No Grafana configured." | Grafanaが構成されていません。 | Grafana が設定されていません。 | 設定画面の語に合わせた。 |
| 概要・Grafana | "No panel in GRAFANA_PANELS matches \"X\". Named here but not defined there, so there is nothing to draw." | GRAFANA_PANELS 内に "…" と一致するパネルはありません。ここで名前は挙がっていますが、そこで定義されていないため、 描画するものがありません。 | GRAFANA_PANELS に「…」と一致するパネルがありません。概要のウィジェットとして指定されていますが、パネルが定義されていないため表示できません。 | 「ここ」「そこ」が何を指すか分からない直訳。 |
| 概要・ウィジェットの失敗 | "Widget not drawn" | ウィジェットが描画されていません | ウィジェットを表示できませんでした | 直訳。 |
| 概要・ウィジェットの失敗 | "Shown so you know this widget failed, instead of it quietly not appearing." | このウィジェットが失敗したことを知らせるために表示しています。何も表示されずに黙って消えるのを避けるためです。 | 表示に失敗したことが分かるよう、このカードを残しています。 | 直訳の2文を簡潔にした。 |
| 読み取り上限の注意 | "Only the newest findings in this window were fetched (the read hit its safety cap): every count here is a floor, not a total. Narrow the window, or raise LOKI_MAX_FINDINGS." | この期間内の最新の検出結果のみを取得しました（読み取りが安全上限に達しました）。ここに表示される件数はすべて下限値であり、合計ではありません。対象期間を短くするか、上限を引き上げてください LOKI_MAX_FINDINGS. | 読み込み件数が安全上限に達したため、この期間の新しい検出結果だけを取得しました。表示している件数は下限値で、実際はこれより多い可能性があります。期間を短くするか、LOKI_MAX_FINDINGS の上限を引き上げてください。 | 英語のピリオドが残り、設定名の位置も崩れていた。 |
| 概要のカード名 | WIDGET_TITLES review_queue "Where to focus" / detection_coverage "Visibility across your estate" | 注力すべき項目 ／ 環境全体の可視性 | 優先して確認すること ／ 環境全体の可視化状況 | カード見出しとカード選択の名称を一致させた。 |
| 概要のカード名 | source_health "Silent sources" | 貼り付けガード ／ 無報告のソース | 貼り付けガード ／ 報告のない検出ソース | 同上。 |
| 概要のカード名 | activity_trend "Personal-account exposure" / agentic "Running on its own" | 個人アカウントの露出 ／ 自律的に動作 | 個人アカウントの利用推移 ／ 自律的に動作中のAI | 同上。 |
| 概要のカード説明 | WIDGET_BLURB stat_row "Posture and the four headline counts" | 態勢と 4 つの主要件数 | 全体状況と4つの主要件数 | 「態勢」は posture の直訳。 |
| 概要のカード説明 | review_queue "The follow-ups, and the decision and discovery queue" | フォローアップと、意思決定・検出結果のキュー | 対応事項と、判断・検出結果のキュー | 用語の統一。 |
| 概要のカード説明 | detection_coverage "Collector coverage and which sources report" | 収集エージェントの確認率と報告しているソース | 収集エージェントのカバー率と、報告中の検出ソース | 【意味の誤り】「確認率」を修正。 |
| 概要のカード説明 | recent_personal_accounts / budget / paste / source_health / activity_trend | ドメイン外のアカウントにおける最新アクティビティ ／ 観測された利用に対する契約 ／ 到達したデバイス上のブラウザ拡張機能 ／ 何も報告していないカタログソース ／ 日次検出数と報告カバレッジ | 企業ドメイン以外のアカウントでの最近の利用 ／ 契約と実際の利用状況の比較 ／ ブラウザー拡張機能を導入した端末での記録 ／ 一覧のうち報告のない検出ソース ／ 1日ごとの検出件数と報告した端末数 | 直訳の解消と用語統一。 |
| 概要の並べ替え | SIZE_LABEL "Half" / "Full" | 半分 ／ 全体 | 半幅 ／ 全幅 | 「全体」は幅の指定として意味が通らない。 |
| 概要の並べ替え | error "no renderer for X" | レンダラーがありません: | このカードの表示方法が定義されていません: | 「レンダラー」は開発者用語。 |
| 概要の並べ替え | button "Unstack" (title "give this card a column of its own again") | このカードに再び専用の列を割り当てる ／ title="このカードに再び専用の列を割り当てる" >スタック解除 | このカードを独立した列に戻します ／ title="このカードを独立した列に戻します" >重ねを解除 | 「スタック」は開発者用語。 |
| 概要の並べ替え | drop zone "Stack beneath" | 下にスタック | この下に重ねる | 同上。 |
| 概要の並べ替え | tray "Not on the page. Drag one into place, or add it at the end." / "Every card is on the page." | ページ上にありません。ドラッグして配置するか、末尾に追加してください。 ／ すべてのカードがページ上にあります。 | 表示していないカードです。ドラッグして配置するか、「追加」で末尾に置けます。 ／ すべてのカードを表示しています。 | 主語のない直訳を解消。 |
| 概要 | lede "Your AI estate. The exposure, the coverage, the next action." | 概要 ／ あなたのAI利用。検出状況、対象範囲、次の対応。 | 概要 ／ 組織内のAI利用状況、検出できている範囲、次に行う対応をまとめて確認できます。 | 体言止めの羅列を文にした。 |
| 概要の並べ替え | "Each card is shown as its name and size. Drag one to move it: the line shows where it lands. Drop it on the strip beneath another card to stack the two in one column. Cards not on the page wait in the tray below. This is your own view and changes nothing for anyone else - the widgets a deployment offers are set under Settings." | - デプロイで提供されるウィジェットは設定で構成されます | （表示できるカードの種類は「設定」で決まります） | 改行位置に空白が入り、「何も変更しません」は主語が不明な直訳だった。 |
| 概要の並べ替え | button "Clear canvas" (title "Move every card to the tray and start from nothing") / "Reset to default" | すべてのカードをトレイに移動し、何もない状態から開始する ／ キャンバスをクリア ／ デフォルトにリセット | すべてのカードをトレイに戻し、空の状態から配置します ／ すべて外す ／ 既定の配置に戻す | 「キャンバス」「デフォルト」は開発者用語。 |
| 概要の並べ替え | "<b>Previewing your arrangement.</b> This is how the page will read with today's data. Nothing is saved until you say so." | 配置をプレビューしています。 今日のデータでは、ページはこのように表示されます。保存を指示するまで、何も保存されません。 | 配置をプレビュー中です。現在のデータで表示するとこのようになります。「保存」を押すまで変更は保存されません。 | 「保存を指示するまで」は直訳。 |
| 概要の並べ替え | "The canvas is empty. Drag cards in from the tray." | キャンバスは空です。トレイからカードをドラッグして追加してください。 | カードがありません。トレイからカードをドラッグして追加してください。 | 「キャンバス」は開発者用語。 |
| 端末 | "Devices" / "N device(s) in this window. Each is keyed by the most stable identifier its source could get, usually a serial. Click one for detail." | デバイス ／ この期間内の … 台のデバイス。各デバイスは、ソースが取得できた最も安定した識別子（通常はシリアル）でキー付けされています。1つをクリックすると詳細が表示されます。 | 端末 ／ この期間に観測した端末は … 台です。端末は、検出ソースが取得できた最も安定した識別子（通常はシリアル番号）で区別しています。行をクリックすると詳細を表示します。 | 「キー付け」は直訳。 |
| 端末 | summary "N devices" / "N AI tools observed" / "N with personal accounts" / "N unattributed" | デバイスインベントリの概要 ／ aria-label="デバイスインベントリの概要"> … デバイス … 観測されたAIツール …件の個人利用あり … 未紐付け | 端末一覧の概要 ／ aria-label="端末一覧の概要"> … 台の端末 … 種類のAIツール … 台で個人アカウントを利用 … 台は利用者が未登録 | 【意味の誤り】personal は端末の台数で「件の個人利用」ではない。単位を明示。 |
| 端末 | columns "Device" / "Person" / "AI tools" / "Personal accounts" / "Local users" | デバイス ／ 人物 ／ AIツール ／ 個人アカウント ／ ローカルユーザー | 端末 ／ 利用者 ／ AIツール ／ 個人アカウント ／ 端末内のユーザー | 「人物」「ローカルユーザー」は直訳。 |
| 端末 | cells "Unattributed" / "None observed" | 未紐付け ／ 観測なし | 未登録 ／ なし | 列見出し（利用者・AIツール）と組み合わせて意味が通る語にした。 |
| 利用者対応表 | classic mode "Identity map: the map is the file at IDENTITY_MAP. One is configured. / None is configured." | 構成されています。 ／ 構成されていません。 | 設定済みです。 ／ 未設定です。 | 語順が英語のままだった。 |
| 利用者対応表 | "N device(s) still has/have no person attached." | … 台のデバイスにはまだ誰も紐付いていません。 | 利用者が未登録の端末が … 台あります。 | 直訳。 |
| 利用者対応表 | button "Clear the saved map" | 保存された対応表をクリア | 保存した対応表を削除 | 「クリア」より操作結果が明確。 |
| 利用者対応表 | "Saved rows (N)" / columns "key" "person" "changed" "by" | 保存された行 (…) ／ キー ／ 人物 ／ 変更 ／ 実行者 | 保存した行（…） ／ キー ／ 利用者 ／ 変更日時 ／ 変更者 | 列の中身に合わせた。 |
| 利用者対応表 | placeholder "key,identity / C02XXXX,jo.bloggs / jo.bloggs,Jo Bloggs" | キー,人物 / C02XXXX,taro.yamada / taro.yamada,山田太郎 ／ placeholder="キー,人物 / C02XXXX,taro.yamada / taro.yamada,山田太郎" | key,identity / C02XXXX,taro.yamada / taro.yamada,山田太郎 ／ placeholder="key,identity / C02XXXX,taro.yamada / taro.yamada,山田太郎" | 【不具合】取り込み処理が見出し行として読み飛ばすのは英語の key 行だけ。訳した見出しをそのまま使うと「キー→人物」という誤った対応が保存される。 |
| 利用者対応表 | "N rows understood, N skipped. Saving REPLACES the map saved here; a mounted file is untouched." | 件をスキップ | 行は対象外） | 原文の強調（REPLACES）が失われ、改行で空白も入っていた。 |
| 利用者対応表 | "N key(s) match no device or local user in the current window - kept, in case the machine reports later." | … 件のキーは現在の対象期間に含まれるデバイスやローカルユーザーと一致しません - 後でマシンが報告する場合に備えて保持されます。 | … 件のキーは、この期間に観測した端末や端末内のユーザーと一致しません。あとで報告される可能性があるため、そのまま保存します。 | 改行で数字と「件」の間に空白が入り、ダッシュ区切りの直訳だった。 |
| 利用者対応表 | "N commented row(s) carry a name and are not saved - the download writes proposals and blanks commented out, so remove the leading # from any you meant to keep:" | … 行にコメントアウトされた名前が含まれており、保存されません。ダウンロードでは 提案と空白がコメントアウトされて書き出されるため、保存するつもりのものから先頭の # を削除してください: | … 行はコメント行のため保存されません（名前は入っています）。ダウンロードしたファイルでは候補と空欄がコメント行になっているので、残したい行は先頭の # を削除してください： | 直訳の長文を整理し、改行による空白を除いた。 |
| 利用者対応表 | preview table header "key" / "person" | ${p.rows.length ? ` ／ キー ／ 人物 | ${p.rows.length ? ` ／ キー ／ 利用者 | 用語の統一。 |
| 利用者対応表 | pills "matches" / "not seen yet" | 一致 ／ まだ検出されていません | 観測あり ／ 未観測 | 何と一致したのかが分からなかった。 |
| 利用者対応表 | skip reason "no person" | 人物なし | 利用者名なし | 用語の統一。 |
| 利用者対応表 | skip reason "same key as line N" | 同じキー: 行 | 行目と同じキー | 語順が英語のままだった。 |
| 利用者 | "People" / "People named by cloud sources, which see accounts rather than machines. A device shows against a person only where the identity map links them." | 人物 ／ この一覧には、クラウドの検出ソースが特定したユーザーを表示します。クラウドソースはユーザーアカウントを検出し、端末は利用者対応表で紐づいた場合に表示されます。 | 利用者 ／ クラウドの検出ソースが特定した利用者を表示します。クラウドのソースは端末ではなくアカウントを検出するため、端末は利用者対応表で紐付けた場合にだけ表示されます。 | 見出し「人物」とナビ「ユーザー」が不一致だった。 |
| 利用者 | columns "Identity" / "AI tools" / "Devices" | 利用者識別子 ／ AIツール ／ デバイス | 利用者 ／ AIツール ／ 端末 | 用語の統一。 |
| 利用者 | cell "Unmapped" | 未紐付け | 端末の紐付けなし | 何が紐付いていないのかを明示。 |
| ツール・要注意の要因 | factors "N personal account(s)" / "wide spread (N devices)" / "installed, never used" | …件の個人利用 ／ 広く拡散 (… デバイス) ／ インストール済みだが未使用 | 個人アカウント … 件 ／ 利用が広い（… 台） ／ インストール済み・利用の形跡なし | 「拡散」は危険の拡大を連想させる直訳。未使用と断定せず観測の範囲で表現。 |
| ツール・要注意の要因 | factor "new in the last 2 days" | 過去2日以内の新規 | 直近2日以内に初検出 | 何が新規なのかを明示。 |
| ツール | pill "watch" | ">監視` | ">要観察` | 「監視」は監視機能と紛らわしい。 |
| ツール | lede text mentions pills "attention" / "watch" | 「要注意」は複数の懸念が重なっている場合、「監視」は確認すべき要因がある場合に表示されます。 | 「要注意」は複数の懸念が重なっている場合、「要観察」は確認すべき要因がある場合に表示されます。 | ピルの表記変更に合わせた。 |
| ツール | lede "…the AI register also counts people linked through a device…" | AI台帳にはデバイス情報から利用者を紐づけた人数も含まれるため、数値が異なる場合があります。 | AI台帳には端末から利用者を紐付けた人数も含まれるため、数値が異なる場合があります。 | 用語の統一。 |
| ツール | columns "AI tool" / "Status" / "Devices" | AIツール ／ ステータス ／ デバイス ／ <th title= | AIツール ／ 状態 ／ 端末数 ／ <th title= | 用語の統一。 |
| ツール | column title "People a SOURCE named on this tool. A cloud sign-in carries a person; an endpoint finding carries a machine, and the person behind it comes from the identity map - so this is lower than the register's user count for tools found on endpoints." | 検出ソースがこのツールについて特定した人物。クラウドのサインインは人物を伴い、エンドポイントの検出結果はマシンを伴います。その背後にいる人物は利用者対応表から取得されるため、エンドポイントで検出されたツールでは、これはAI台帳のユーザー数より少なくなります。 ／ title="検出ソースがこのツールについて特定した人物。クラウドのサインインは人物を伴い、エンドポイントの検出結果はマシンを伴います。その背後にいる人物は利用者対応表から取得されるため、エンドポイントで検出されたツールでは、これはAI台帳のユーザー数より少なくなります。" | 検出ソースがこのツールについて直接特定した利用者の数です。クラウドのサインインには利用者の情報が含まれますが、端末での検出結果には端末の情報しか含まれません。端末の利用者は利用者対応表から求めるため、端末で検出されたツールでは、この数がAI台帳の利用者数より少なくなります。 ／ title="検出ソースがこのツールについて直接特定した利用者の数です。クラウドのサインインには利用者の情報が含まれますが、端末での検出結果には端末の情報しか含まれません。端末の利用者は利用者対応表から求めるため、端末で検出されたツールでは、この数がAI台帳の利用者数より少なくなります。" | 「人物を伴い」「マシンを伴います」は直訳。 |
| ツール | pill "installed only" title "Found installed, but nothing has shown a model actually running - no account, no sign-in, and no traffic to the completion backend. Editors that bundle AI (Cursor, Windsurf/Devin Desktop) are useful all day without it." | インストール済みとして検出されましたが、モデルが実際に動作していることを示すものはありません - アカウントもサインインも、コード補完サービスへの通信もありません。AI機能を組み込んだエディター（Cursor、Windsurf/Devin Desktop）は、AIが実際に動作していなくても一日中役立ちます。 ／ title="インストール済みとして検出されましたが、モデルが実際に動作していることを示すものはありません - アカウントもサインインも、コード補完サービスへの通信もありません。AI機能を組み込んだエディター（Cursor、Windsurf/Devin Desktop）は、AIが実際に動作していなくても一日中役立ちます。" | インストールは検出されましたが、AIモデルが実際に使われた形跡（アカウント、サインイン、AIサービスへの通信）はありません。AI機能を内蔵したエディター（Cursor、Windsurf／Devinデスクトップ版）は、AIを使わなくてもエディターとして日常的に使われます。 ／ title="インストールは検出されましたが、AIモデルが実際に使われた形跡（アカウント、サインイン、AIサービスへの通信）はありません。AI機能を内蔵したエディター（Cursor、Windsurf／Devinデスクトップ版）は、AIを使わなくてもエディターとして日常的に使われます。" | 「一日中役立ちます」は直訳。 |
| ツール | title "Of the devices this tool was found on, how many show the AI actually being used." / "N using" | このツールが検出されたデバイスのうち、AIが実際に使用されていることを示すものはいくつありますか。 ／ title="このツールが検出されたデバイスのうち、AIが実際に使用されていることを示すものはいくつありますか。">… 使用中 | このツールが検出された端末のうち、AIが実際に使われた形跡がある端末の数です。 ／ title="このツールが検出された端末のうち、AIが実際に使われた形跡がある端末の数です。">うち … 台で利用 | 【誤訳】説明文が疑問文になっていた。 |
| ツール | "seen in cloud sign-ins only - no device attribution" | クラウドのサインインでのみ検出 - デバイスへの紐づけなし | クラウドのサインインでのみ検出（端末との紐付けなし） | ダッシュ区切りの直訳。 |
| ツール・接続先 | column "Devices" | 接続先のサービス ／ デバイス | 接続先のサービス ／ 端末数 | 列の中身は台数。 |
| 収集エージェント未導入の端末 | "Coverage" / "Machines an inventory or telemetry source knows about, but no endpoint collector has reported from. Usually the collector is not installed there yet." | カバレッジ ／ インベントリまたはテレメトリのソースが把握しているものの、エンドポイント収集エージェントから報告がないマシン。通常、そこにはまだ収集エージェントがインストールされていません。 | 収集エージェント未導入の端末 ／ 資産管理やテレメトリの検出ソースでは把握されているものの、収集エージェントから報告がない端末です。多くの場合、その端末にはまだ収集エージェントが導入されていません。 | ナビ名（検出対象外端末）と見出し（カバレッジ）が不一致で、どちらも内容を表していなかった。 |
| 収集エージェント未導入の端末 | columns "Device" / "Seen by" / "AI tools seen" (a count) | デバイス ／ 検出元 ／ 検出されたAIツール | 端末 ／ 検出したソース ／ AIツール数 | 列の中身は件数。 |
| 収集エージェント未導入の端末 | "Every device with a scanner finding also has a collector reporting." / "Nothing to compare: the findings could not be read." | ／ スキャナーの検出結果があるすべてのデバイスには、収集エージェントからの報告もあります。 ／ ／ ／ 比較できるものがありません: 検出結果を読み取れませんでした。 ／ | ／ スキャナーで検出されたすべての端末から、収集エージェントの報告も届いています。 ／ ／ ／ 検出結果を読み込めなかったため、比較できません。 ／ | 直訳。 |
| 端末の詳細 | "k · os · N findings" / "os unknown" | OS不明 | OS不明 | 語順が英語のままだった。 |
| 端末の詳細 | "Also reported as X — one machine, merged here because sources key it differently." | また、 … としても報告されています — ソースによって識別方法が異なるため、ここでは1台のマシンとして統合されています。 | 別の識別子 … でも報告されています。検出ソースによって識別子が異なるため、1台の端末としてまとめて表示しています。 | 改行で文が分断されていた。 |
| 端末の詳細 | rows "person" / "local users" (cell "unattributed") | 未紐付け | 未登録 | 用語の統一。 |
| 端末の詳細 | row "sources" (raw source ids) | ソース ／ … | 検出ソース ／ … | 内部ID（collector-macos など）がそのまま表示されていた。他画面と同じ表示名にした。 |
| ツールの詳細 | heading (raw tool id) | const series = ((G.trends \|\| {}).tools \|\| {})[k]; return ` ／ … | const series = ((G.trends \|\| {}).tools \|\| {})[k]; return ` ／ … | 見出しに内部ID（claude-code など）が出ていた。一覧と同じ表示名にした。 |
| ツールの詳細 | "N devices · N identities · N findings" | … デバイス · … アイデンティティ · … 検出結果 | 端末 … 台 · ID … 件 · 検出結果 … 件 · … | 単位を付け、見出しから外した内部IDをここに残した。 |
| ツールの詳細 | "daily activity, oldest to newest" | 日次のアクティビティ、古いものから新しいものへ | 1日ごとの検出件数（左が古い日付） | 直訳。 |
| ツールの詳細 | "Needs attention: … ." / "Worth watching: … ." | 対応が必要 ／ 注視が必要 | 要注意 ／ 要観察 | 英語のピリオドが残っていた。一覧のピルと同じ語にした。 |
| ツールの詳細 | row "installed vs used" (title "Installed says the product is on the machine. Used says something proved a model ran: an account, a sign-in, an MCP config, or traffic to the completion backend rather than to the update and telemetry hosts the editor reaches on launch anyway.") / "N installed · N where the AI ran" | インストール済みは、製品がマシン上にあることを示します。使用は、モデルが実行された証拠があることを示します：アカウント、サインイン、モデルコンテキストプロトコル設定、またはエディターが起動時にいずれにせよ接続する更新ホストやテレメトリホストではなく、コード補完サービスへの通信です。 ／ インストール済み vs 使用済み ／ … インストール済み · … AIが実行された場所${ | 「インストール済み」は製品が端末にあることを示します。「AIの利用あり」は、アカウント、サインイン、MCP設定、AIサービスへの通信など、モデルが実際に動いた証拠があることを示します（エディターが起動時に行う更新確認やテレメトリ通信は含みません）。 ／ インストールと利用 ／ インストール済み … 台 · AIの利用あり … 台${ | 「vs」「AIが実行された場所」は直訳。 |
| ツールの詳細 | "nothing has shown this one being used as an AI tool" | これがAIツールとして使用されていることを示すものはありません | AIツールとして使われた形跡はありません | 直訳。 |
| ツールの詳細 | heading "Devices" | デバイス | 検出された端末 | 用語の統一。 |
| MCPサーバー | heading "MCP servers" / "Integrations that AI tools are set up to use. Each holds its own credentials and can reach whatever it was pointed at, even when the tool that configured it is closed. That is why they get their own page." | モデルコンテキストプロトコルサーバー ／ AIツールが使用するように設定されている統合。それぞれが独自の認証情報を保持し、設定したツールが閉じられていても、指定された先に到達できます。そのため、これらには専用のページがあります。 | MCPサーバー ／ MCP（Model Context Protocol）サーバーは、AIツールが外部のサービスやデータに接続するために設定する連携です。それぞれが独自の認証情報を持ち、設定したツールを閉じていても接続先にアクセスできます。そのため専用の画面で確認します。 | 規格名は略語のまま使い、初出で日本語の説明を付けた。「統合」は直訳。 |
| MCPサーバー | tile "devices" | … ／ デバイス | … ／ 端末 | 用語の統一。 |
| MCPサーバー | columns "Server" / "Devices" / "Configured by" | サーバー ／ デバイス ／ 設定元 | サーバー ／ 端末数 ／ 設定したツール | 列の中身に合わせた。 |
| MCPサーバー | "Click a server to see which machines it's configured on. Widest reach is listed first." | サーバーをクリックすると、どのマシンに設定されているかを確認できます。到達範囲が最も広いものから表示されます。 | サーバーをクリックすると、設定されている端末を確認できます。設定端末の多い順に表示しています。 | 「到達範囲」は直訳。 |
| MCPサーバー | "No MCP servers found. Check the Setup page first: MCP findings come from the endpoint collectors, so if no collector is reporting, this page can't see anything either." | モデルコンテキストプロトコルサーバーが見つかりません。まずセットアップページを確認してください。モデルコンテキストプロトコルの検出結果はエンドポイント収集エージェントから送られるため、収集エージェントが報告していなければ、このページでも何も表示できません。 | MCPサーバーは見つかりませんでした。先に「検出ソース」画面を確認してください。MCPの検出結果は収集エージェントから届くため、収集エージェントが報告していなければ、この画面にも表示されません。 | 移動先の画面名を実際の名称にした。 |
| MCPサーバーの詳細 | "N device(s) · configured by X · first seen D (unknown) · last seen D (unknown)" | … デバイス · 設定者: … · 初回検出: … · 最終検出: … | 不明 | 【未翻訳】unknown が英語のまま表示されていた。ツールは内部IDではなく表示名にした。 |
| MCPサーバーの詳細 | "Whatever this server was pointed at is reachable from these machines without the configuring tool being open. What it can actually do there depends on the credentials it holds, which are not visible from here." | このサーバーの接続先は、設定ツールを開いていなくても、これらのマシンから到達可能です。そこで実際にできることは、サーバーが保持する認証情報に依存しており、ここからは見えません。 | このサーバーの接続先には、設定したツールを開いていなくても、これらの端末からアクセスできます。接続先で何ができるかはサーバーが持つ認証情報によって決まり、この画面からは確認できません。 | 直訳。 |
| MCPサーバーの詳細 | "No other findings from this device in the window, so there is nothing else to show about it." | この期間内にこのデバイスからの他の検出結果はないため、これについて他に表示できるものはありません。 | この期間、この端末からほかの検出結果はありません。 | 冗長な直訳。 |
| MCPサーバーの詳細 | "No device recorded against it." | ／ これに紐づくデバイスは記録されていません。 ／ | ／ このサーバーが設定された端末は記録されていません。 ／ | 「これ」が何か不明。 |
| 個人アカウント | button "Reopen" | data-act="pa-reopen" data-key="…">再オープン | data-act="pa-reopen" data-key="…">未解決に戻す | 「再オープン」は直訳。 |
| 個人アカウント | placeholder "why this is acceptable" / button "Accept" | これが許容される理由 ／ placeholder="これが許容される理由" autocomplete="off"> ／ 承認 | 許容する理由 ／ placeholder="許容する理由" autocomplete="off"> ／ 許容する | ツールの「承認」（AI台帳の判断）と区別するため「許容」にした。 |
| 個人アカウント | button "Ack" (title "spoken to - stays visible, stops being new") / "Accept…" (title "accepted with a reason - drops out of the open count") | 声かけ済み - 表示されたまま、新規ではなくなります ／ 理由付きで承認済み - オープン件数から外れます ／ title="声かけ済み - 表示されたまま、新規ではなくなります">確認 ／ 承認… | 本人に確認済みにします。表示は残り、新規扱いではなくなります ／ 理由を記録して許容します。未解決の件数から外れます ／ title="本人に確認済みにします。表示は残り、新規扱いではなくなります">確認済みにする ／ 許容… | 「オープン件数」は直訳。「確認」だけでは押した結果が分からない。 |
| 個人アカウント | status pill "accepted" | (st.at\|\|'').slice(0,10))}">承認済み` | (st.at\|\|'').slice(0,10))}">許容済み` | ツールの「承認済み」と区別。 |
| 個人アカウント | summary "N open" / "N acknowledged" / "N accepted" / "N people named" / "N AI tool(s) involved" | … 確認済み… 承認済み | … 件を確認済み… 件を許容済み | 「オープン」は直訳。数字の単位を明示。 |
| 個人アカウント | lede "…record where it got to: acknowledged keeps it visible, accepted needs a reason and takes it out of the open count" | 。対応状況を記録できます。確認済みの項目は表示に残ります。承認する場合は理由が必要で、承認済みの項目は未対応件数に含まれません | 。対応状況も記録できます。「確認済み」にした項目は表示に残ります。「許容」するには理由が必要で、許容済みの項目は未解決の件数に含まれません | 用語の統一。 |
| 個人アカウント | columns "Person" / "Device" / "Source" / "Status" | ／ ステータス ／ | ／ 対応状況 ／ | 用語の統一。 |
| 個人アカウント | pill "via device" (title "This source reported no account name. The person is the one the identity map attaches to this machine.") / "no identity" | このソースはアカウント名を報告していません。人物は、利用者対応表がこのマシンに紐付ける人物です。 ／ 識別情報なし | この検出ソースはアカウント名を報告していません。表示している利用者は、利用者対応表でこの端末に紐付けた人です。 ／ 利用者不明 | 直訳。 |
| 個人アカウント | "None seen in the last N hours. Worth trusting only if the sources on the Setup page are reporting." | 過去 … 時間に検出はありません。 セットアップページのソースが報告している場合にのみ信頼できます。 | 過去 … 時間に検出はありません。この結果は、「検出ソース」画面で各ソースが報告していることを確認したうえで判断してください。 | 移動先の画面名を実際の名称にした。 |
| AI台帳の判断フォーム | placeholder "owner, e.g. Security" | オーナー、例: セキュリティ ／ placeholder="オーナー、例: セキュリティ" | 責任者（例: 情報セキュリティ部） ／ placeholder="責任者（例: 情報セキュリティ部）" | 「オーナー」はポータルのロール名と紛らわしい。 |
| AI台帳の判断フォーム | placeholder "review due (YYYY-MM-DD, required for approved)" | レビュー期限 (YYYY-MM-DD、承認済みの場合は必須) ／ placeholder="レビュー期限 (YYYY-MM-DD、承認済みの場合は必須)" | レビュー期限（YYYY-MM-DD、承認済みの場合は必須） ／ placeholder="レビュー期限（YYYY-MM-DD、承認済みの場合は必須）" | 括弧を全角に統一。 |
| 概要・対応事項 | "N open" (personal accounts) | …件未対応 | 未解決 … 件 | 未解決の件数には「確認済み」も含まれるため「未対応」ではない。 |
| 概要・検出ツール表 | badge "N open" | …件未対応 | 未解決 … 件 | 同上。 |
| 概要・検出ツール | badge "N open" (list form) | … 件未対応 | 未解決 … 件 | 同上。 |
| ツールレジストリの登録 | surfaces "Browser" / "Desktop apps" / "CLI and IDE" / "MCP" / "Email" | ブラウザ ／ デスクトップアプリ ／ コマンドラインと統合開発環境 ／ モデルコンテキストプロトコル | ブラウザー ／ デスクトップアプリ ／ CLI・IDE | CLI・IDE・MCP は技術者に通じる略語のまま使う。長い展開形は見出しとして読みにくい。 |
| ツールレジストリの登録 | field labels "browser domain" / "cli binary" / "cli config path" / "mcp identifier" / "mcp config path" / "email sender domain" | ブラウザドメイン ／ macOSアプリ ／ macOSバンドルID ／ Windows実行ファイル ／ コマンドライン実行ファイル ／ コマンドライン設定パス ／ VS Code拡張機能 ／ モデルコンテキストプロトコル識別子 ／ モデルコンテキストプロトコル設定パス ／ メール送信者ドメイン | ブラウザーで開くドメイン ／ macOSアプリ名 ／ macOSバンドルID ／ Windows実行ファイル名 ／ CLIの実行ファイル名 ／ CLIの設定ファイルパス ／ VS Code拡張機能ID ／ MCPサーバー名 ／ MCPの設定ファイルパス ／ メールの送信元ドメイン | 入力する値の種類（名前・ID・パス）が分かる表記にした。 |
| ツールレジストリの登録 | reason "you added" | あなたが追加 | 手動で追加 | 「あなたが」は直訳。 |
| ツールレジストリの登録 | steps "What we found / This tool / Which tool" · "Discovered on your network / Name it to get proposals" · "How else to spot it / Confirm what to watch for" · "Review and save / What the fleet will watch" | 検出結果 ／ このツール ／ どのツール ／ ネットワーク上で検出 ／ 名前を入力して候補を取得 ／ 他に識別する方法 ／ 監視対象を確認 ／ 確認して保存 ／ 端末群が監視する内容 | 見つかったもの ／ このツール ／ ツールの指定 ／ ネットワーク上で検出 ／ 名前を入力すると識別子の候補を表示 ／ 識別子の確認 ／ 検出に使う識別子を選ぶ ／ 確認して保存 ／ 各端末で検出する内容 | 「どのツール」「他に識別する方法」は手順名として不自然。 |
| ツールレジストリの登録 | "N confirmed across S surface(s)" / "nothing confirmed yet" | 件が ／ 利用環境で確認されました ／ まだ何も確認されていません | 種類の利用環境で ／ 件を選択済み ／ 識別子がまだ選ばれていません | 選択（チェック）した件数であり、検出の確認ではない。 |
| ツールレジストリの登録 | "N of M surfaces covered" / "A surface with no identifier is not a gap in your estate - it is a place this tool would go unseen." | … / … 対応済み利用環境 | 利用環境 … 種類中 … 種類に識別子あり | 分数と名詞の直訳を解消。 |
| ツールレジストリの登録 | "A surface with no identifier is not a gap in your estate - it is a place this tool would go unseen." | 識別子のない利用環境は、自社環境の抜けではありません。そこは、このツールが見えないままになる場所です。 | 識別子がない利用環境は、自社環境の不備ではありません。その利用環境ではこのツールを検出できない、という意味です。 | 「見えないままになる場所」は直訳。 |
| ツールレジストリの登録 | heading "What we found" / "Which tool" | 検出結果 ／ どのツール | 見つかったもの ／ 登録するツール | 見出しとして自然な語にした。 |
| ツールレジストリの登録 | "Discovery saw this on your network and the classifier read it as an AI service. Confirm it is what you think it is - everything after this hangs off the name." | 検出処理がネットワーク上でこれを検出し、分類器がAIサービスと判定しました。想定どおりか確認してください。以降の設定は名称に基づいて処理されます。 | 検出処理がネットワーク上でこの通信を見つけ、分類器がAIサービスと判定しました。想定どおりのツールか確認してください。以降の手順はすべてこの名前をもとに進みます。 | 「これを検出し」は何を指すか曖昧。 |
| ツールレジストリの登録 | "This tool is already in the registry. Change what you need here; its identifiers are on the next step." / "Name the tool and identifiers will be proposed for it. Nothing is saved until you have confirmed them." | このツールはすでにAI台帳に登録されています。必要な箇所をここで変更してください。その 識別子は次のステップにあります。 ／ ツールに名前を付けると、その識別子が提案されます。確認するまで 何も保存されません。 | このツールはすでにレジストリに登録されています。必要な項目をここで変更してください。識別子は次の手順で編集できます。 ／ ツール名を入力すると、識別子の候補を提案します。確認するまで何も保存されません。 | 【意味の誤り】登録先は AI台帳 ではなくレジストリ。改行で空白も入っていた。 |
| ツールレジストリの登録 | evidence box "Evidence" / "Seen on N devices" / "Read as X (confidence)" / "Source: Discovery run" | 証跡 | 検出の根拠 | 監査用の「証跡」ではなく、検出された根拠。 |
| ツールレジストリの登録 | "Seen on N devices" | 確認日 ／ … デバイス | 検出端末 ／ … 台 | 【誤訳】"Seen on" を「確認日」としていたが、中身は端末の台数。 |
| ツールレジストリの登録 | "Read as X · confidence" / "Source: Discovery run" | ／ 読み取り結果 ／ … … 信頼度 ／ | ／ 判定 ／ … 信頼度 … ／ | 「高 信頼度」の語順と、カテゴリの英語表示を修正。 |
| ツールレジストリの登録 | category options (raw English values) | … | … | 【未翻訳】カテゴリが coding などの英語のまま表示されていた。保存する値は英語のまま value に残した。 |
| ツールレジストリの登録 | "Name, vendor, id and category are all required: the registry refuses an entry without them." | 名前、提供元、識別子、カテゴリはすべて必須です。未入力の項目があるとAI台帳に登録できません。 | 名前、提供元、識別子、カテゴリはすべて必須です。未入力の項目があるとレジストリに登録できません。 | 【意味の誤り】登録を拒否するのはレジストリ。 |
| ツールレジストリの登録 | "The id is how every other page refers to this tool, so it cannot change." | 識別子は他のすべてのページがこのツールを参照するために使うため、変更できません。 | 識別子は、ほかのすべての画面でこのツールを指すために使うため、変更できません。 | 直訳。 |
| ツールレジストリの登録 | "Dismissing instead? That is the Dismiss button on the review queue - it records that a person decided, so the same domain does not come back next week." | 代わりに却下しますか？それはレビューキューの「却下」ボタンです。人が判断したことが記録されるため、同じドメインが来週再び表示されることはありません。 | 登録せずに除外する場合は、判断待ちキューの「対象外にする」ボタンを使います。人が判断したことが記録されるため、同じドメインが翌週また表示されることはありません。 | キューのボタン名（無視）と説明（却下）が一致していなかった。ボタン名も「対象外にする」に揃えた。 |
| 判断待ちキュー | button "Dismiss" | 無視 | 対象外にする | 「無視」では判断を記録する操作だと伝わらない。 |
| ツールレジストリの登録 | "The id is how every other page refers to this tool and cannot change later." | 識別子は他のすべてのページがこのツールを参照するために使うため、後から変更できません。 | 識別子は、ほかのすべての画面でこのツールを指すために使うため、後から変更できません。 | 直訳。 |
| ツールレジストリの登録 | derived suggestion pill "low confidence" | … 信頼度 | 信頼度 … | 【未翻訳】low が英語のまま表示されていた。 |
| ツールレジストリの登録 | heading "How else to spot it" / "Name the tool on the first step and proposals appear here." | ／ 他に見つける方法 ／ 最初のステップでツールに名前を付けると、ここに提案が表示されます。 ／ | ／ 識別子の確認 ／ 最初の手順でツール名を入力すると、ここに識別子の候補が表示されます。 ／ | 手順名に合わせた。 |
| ツールレジストリの登録 | "What was already seen is ticked. Everything else is a proposal derived from the name - left off, and labelled - because a wrong identifier is worse than a missing one: a blank leaves this tool unseen on a surface, a wrong one hangs somebody else's findings on it. Tick only what you recognise." / "Nothing here has been seen in your estate yet - you are defining this tool before anything found it, so every line below is a guess until a finding matches it." | ／ 他に見つける方法 ／ すでに検出されているものにはチェックが入っています。それ以外は名前から導き出された提案で、チェックは外されたままラベルが付いています。誤った識別子は欠落している識別子より悪いためです。空欄のままにすると、このツールはある利用環境上で見えないままになりますが、誤った識別子は他人の検出結果をこのツールに紐づけてしまいます。認識できるものだけにチェックを入れてください。 ／ ${anyEv ? '' : | ／ 識別子の確認 ／ すでに検出されている識別子にはチェックが入っています。それ以外は名前から推定した候補で、チェックを外した状態で表示しています。誤った識別子は、識別子がないよりも問題になるためです。空欄なら、その利用環境でこのツールが検出されないだけですが、誤った識別子は別のツールの検出結果をこのツールに結び付けてしまいます。確かだと分かるものだけにチェックを入れてください。 ／ ${anyEv ? '' : | 「他人の検出結果」は誤訳（別ツールの検出結果）。直訳の長文を整理。 |
| ツールレジストリの登録 | group count "N confirmed" / "none confirmed" / "Add your own" / placeholder "an identifier you know, e.g. Acme.app" | 件確定 ／ 確定なし | 件を選択 ／ 未選択 | チェックした件数であり「確定」ではない。 |
| ツールレジストリの登録 | "Add your own" / placeholder | 自分で追加 | 識別子を追加 | 何を追加するのかを明示。 |
| ツールレジストリの登録 | placeholder "an identifier you know, e.g. Acme.app" | 既知の識別子、例: Acme.app ／ placeholder="既知の識別子、例: Acme.app" | 分かっている識別子（例: Acme.app） ／ placeholder="分かっている識別子（例: Acme.app）" | 自然な表現にした。 |
| ツールレジストリの登録 | "A confirmed identifier is still only a guess until something matches it. The next step says which is which." | 確認済みの識別子も、何かが一致するまでは単なる推測です。次のステップで、どれがどれかが示されます。 | 選択した識別子も、検出結果と一致するまでは推測にすぎません。一致しているかどうかは次の手順で確認できます。 | 「どれがどれか」は直訳。 |
| ツールレジストリの登録 | review statuses "unseen" / "already matching" / "watching" | 未検出 ／ 一致済み ／ 監視中 | 検出できない ／ 一致あり ／ 一致待ち | 【意味の誤り】unseen は識別子が無くこの利用環境では検出できない状態で、「未検出」ではない。 |
| ツールレジストリの登録 | column "status" | 利用環境 ／ 識別子 ／ ステータス ／ … | 利用環境 ／ 識別子 ／ 状態 ／ … | 用語の統一。 |
| ツールレジストリの登録 | "<b>Already matching</b> means findings exist for it today. <b>Watching</b> means the identifier is live but nothing has matched yet - which may mean nobody uses it that way, or may mean the identifier is wrong. The tool page keeps that split visible rather than reporting a confident zero." | 一致済み 今日時点でそれに対する検出結果が存在することを意味します。 監視中 識別子は有効だが、まだ何も一致していないことを意味します。これは、誰もそのようには使用していないことを意味する場合もあれば、識別子が誤っていることを意味する場合もあります。ツールページでは、断定的なゼロを報告するのではなく、その内訳を可視化したままにします。 | 一致ありは、現在その識別子に一致する検出結果があることを示します。一致待ちは、識別子は有効ですが、まだ一致する検出結果がないことを示します。そのような使い方をしている人がいないのか、識別子が誤っているのかは、この時点では区別できません。ツールの画面では、0件と断定せずにこの内訳を表示し続けます。 | 改行による空白と直訳を解消。 |
| ツールレジストリの登録 | button "Save and watch" | 変更を保存 ／ 保存して監視 | 変更を保存 ／ 保存して検出を開始 | 保存後に起きること（検出の開始）を明示。 |
| ツールレジストリ | button "Define a tool" | data-act="reg-add">ツールを定義 | data-act="reg-add">ツールを追加 | 操作名として一般的な表現にした。 |
| ツールレジストリ | "Your tools (N)" | あなたのツール (…) | この環境で追加したツール（…） | 「あなたの」は直訳。組織で追加した定義を指す。 |
| ツールレジストリ | columns "id" / "name" / "vendor" / "identifiers" (a count) / "updated" | 内部識別子 ／ 名前 ／ ベンダー ／ ベンダー識別子 ／ 更新日時 | 識別子 ／ 名前 ／ 提供元 ／ 検出用識別子の数 ／ 更新日時 | 【誤訳】identifiers 列は検出用の識別子の件数で、「ベンダー識別子」ではない。 |
| ツールレジストリ | pill "shadowed by a release - delete this copy" | リリースによって上書きされています - このコピーを削除 | 同梱版と重複しています（この定義は削除してください） | 「上書き」では何が起きているか分からない。 |
| ツールレジストリ | "None yet. A tool observed on the register that the registry does not know has an \"add to registry\" button - or define one here before it ever appears." | まだありません。AI台帳で観測されたツールをレジストリが認識していない場合、そのツールには「レジストリに追加」ボタンがあります。または、ツールが表示される前にここで定義することもできます。 | まだありません。AI台帳に表示されたツールがレジストリ未登録の場合は、そのツールの「レジストリに追加」ボタンから登録できます。検出される前に、ここで定義しておくこともできます。 | 直訳の長文を整理。 |
| ツールレジストリ | "Shipped registry (N) — read-only, updates with releases" / columns | 同梱レジストリ (…) — 読み取り専用、リリースに合わせて更新 ／ 識別子 ／ 名前 ／ ベンダー | 製品に同梱のツール定義（…）— 読み取り専用・リリースごとに更新 ／ 識別子 ／ 名前 ／ 提供元 | 「同梱レジストリ」は直訳。 |
| AI台帳・未検出のツール | "Watchlist — known, not observed (N, M without a decision)" / "Decisions recorded here apply the moment a tool first appears. Approvals carry the review date below." | , … は未判断 | 、うち判断なし … 件 | 「ウォッチリスト」は画面上の他の語と対応しない直訳。 |
| AI台帳・未検出のツール | placeholder "owner for these decisions, e.g. Security" / columns "tool" "vendor" "decision" / "no decision" / buttons "Approve" "Not approved" | これらの決定のオーナー、例: セキュリティ ／ placeholder="これらの決定のオーナー、例: セキュリティ"> | これらの判断の責任者（例: 情報セキュリティ部） ／ placeholder="これらの判断の責任者（例: 情報セキュリティ部）"> | 「オーナー」はロール名と紛らわしい。 |
| AI台帳・未検出のツール | columns "tool" / "vendor" / "decision" | ツール ／ ベンダー ／ 決定 | ツール ／ 提供元 ／ 判断 | 用語の統一。 |
| AI台帳・未検出のツール | "no decision" / buttons "Approve" / "Not approved" | 決定なし | 判断なし | 用語の統一。 |
| AI台帳・未検出のツール | buttons "Approve" / "Not approved" | data-act="wiz-approve" data-key="…">承認 ／ 未承認 | data-act="wiz-approve" data-key="…">承認する ／ 承認しない | ボタンは状態ではなく操作なので動詞にした。 |
| AI台帳 | "Could not build the register: X" | AI台帳を構築できませんでした: | AI台帳を作成できませんでした: | 「構築」はシステム構築と紛らわしい。 |
| AI台帳 | status pill "not in registry" | AI台帳に未登録 | レジストリ未登録 | 【意味の誤り】AI台帳の画面上で「AI台帳に未登録」と表示していた。未登録なのはレジストリ。 |
| AI台帳 | "was X" (stored status before expiry) | 以前は … | 期限切れ前: … | 承認期限切れで表示が変わったことを明示。 |
| AI台帳 | "approved · from the registry" | レジストリから | レジストリの設定 | 「レジストリから」は途中で切れた直訳。 |
| AI台帳 | "no decision" | 決定なし | 判断なし | 用語の統一。 |
| AI台帳 | "Nd overdue" / "in Nd" | …日超過` : (days >= 0 ? `あと …日` : ''); | 期限を…日超過` : (days >= 0 ? `あと…日` : ''); | 何を超過したのかを明示。 |
| AI台帳 | "The AI tools actually in use, from findings in the last X. Tools the registry watches for but nobody uses are counted below, not listed. Tools in use that the registry doesn't know are flagged - those are the ones to act on." | 実際に使用中のAIツール（直近 … の検出結果）。監視対象でも使用が確認されていないツールは、件数のみを示し、この一覧には表示しません。使用中でもレジストリが把握していないツールにはフラグを付けています。これらのツールが対応対象です。 | 直近…の検出結果から、実際に使われているAIツールを表示します。レジストリに登録済みでも利用が確認されていないツールは、一覧に出さず下の件数だけを示します。使われているのにレジストリに未登録のツールには印を付けています。優先して対応すべきなのはこれらのツールです。 | 体言止めの直訳を解消。 |
| AI台帳 | score "Governance decision coverage" / "Decision coverage" / "N of M observed tools have a recorded governance decision." | ガバナンス決定カバレッジ ／ 決定カバレッジ | 判断の記録率 | 「決定カバレッジ」は直訳。 |
| AI台帳 | "N of M observed tools have a recorded governance decision." | …件（…件の検出済みツール中）で、ガバナンス判断が記録されています。 | 検出済みツール … 件のうち … 件で判断を記録済みです。 | 括弧書きの直訳を解消。 |
| AI台帳 | metrics "awaiting decision" / "not in registry" | … ／ 決定待ち | … ／ 判断待ち | 用語の統一。 |
| AI台帳 | metric "not in registry" | … ／ AI台帳に未登録 | … ／ レジストリ未登録 | 【意味の誤り】observed_not_in_registry はレジストリ未登録の件数。 |
| AI台帳 | "No decisions recorded yet, so every tool shows the registry's shipped default (not approved). That's a default, not a decision anyone made. Click <b>edit</b> on any card to record a real one." | まだ決定が記録されていないため、すべてのツールにはレジストリの出荷時既定値（未承認）が表示されます。これは既定値であり、誰かが下した決定ではありません。実際の決定を記録するには、任意のカードで 編集 をクリックしてください。 | まだ判断が記録されていないため、すべてのツールにレジストリの初期値（未承認）を表示しています。これは初期値で、誰かが判断した結果ではありません。判断を記録するには、各カードの判断を編集を押してください。 | ボタン名（判断を編集）と説明の語を一致させた。 |
| AI台帳 | "No governance file is configured, so every tool shows the registry's shipped default (not approved). … Set GOVERNANCE_PATH to record approvals, owners and review dates." | ガバナンスファイルが設定されていないため、すべてのツールにはレジストリの出荷時既定値（未承認）が表示されます。これは既定値であり、誰かが下した決定ではありません。承認、所有者、レビュー日を記録するには、 GOVERNANCE_PATH を設定してください。 | ガバナンスファイルが設定されていないため、すべてのツールにレジストリの初期値（未承認）を表示しています。これは初期値で、誰かが判断した結果ではありません。承認・責任者・レビュー期限を記録するには GOVERNANCE_PATH を設定してください。 | 用語の統一。 |
| AI台帳 | "N record(s)/decision(s)/exception(s) name tools the registry does not know:" | 記録 ／ 決定 ／ 例外 | 記録 ／ 判断 ／ 例外 | 用語の統一。 |
| AI台帳 | "… name tools the registry does not know:" | 台帳にないツールを指定した…が…件あります： | レジストリにないツールを指定した…が…件あります： | 【意味の誤り】原文は the registry。 |
| AI台帳 | "This is fine if you recorded a decision ahead of registering the tool - but it's also what a typo looks like. Either way the record isn't being applied to anything right now." | ツールを登録する前に決定を記録している場合は問題ありませんが、タイプミスのようにも見えます。いずれにしても、この記録は現在何にも適用されていません。 | ツールをレジストリに登録する前に判断を記録したのであれば問題ありません。ただし、入力ミスの可能性もあります。いずれの場合も、この記録は現在どのツールにも適用されていません。 | 直訳。 |
| AI台帳 | "Governance queue" / "N of M observed tools · undecided tools appear first" / "needs a decision" | ガバナンスキュー…件（…件の検出済みツール中）· 未判断のツールが先に表示されます ／ 決定が必要 | ツールごとの判断検出済みツール … 件中 … 件 · 判断が未記録のツールを先に表示 ／ 判断が必要 | 括弧書きの直訳と用語を統一。 |
| AI台帳 | pill "new today" / vendor fallback | 今日の新規 ／ 開発元未設定 | 本日新規 ／ 提供元未設定 | 「開発元」と「提供元」の混在を解消。 |
| AI台帳 | cells "Decision" / "Exposure: N devices, N users" | 決定… ／ 露出… デバイス… ユーザー | 判断… ／ 利用規模… 台… 人 | 「露出」は exposure の直訳。 |
| AI台帳 | cell "Owner" / "Unassigned" | 未割り当て | 未設定 | owner はツールの責任者。所有者（財産の持ち主）ではない。 |
| AI台帳 | "Accounts N corporate · N personal" | アカウント… 法人 · … 個人 | アカウント会社 … · 個人 … | 「法人」は契約形態と紛らわしい。数字の前にラベルを置いた。 |
| AI台帳 | buttons "Edit decision" / "Clear decision" / "Add to registry" | data-act="gov-edit" data-key="…">決定を編集 | data-act="gov-edit" data-key="…">判断を編集 | 用語の統一。 |
| AI台帳 | button "Clear decision" | data-key="…">決定をクリア | data-key="…">判断を取り消す | 「クリア」より結果が明確。 |
| AI台帳 | button "Add to registry" | data-key="…">AI台帳に追加 | data-key="…">レジストリに追加 | 【意味の誤り】AI台帳の画面上のツールに「AI台帳に追加」と表示していた。追加先はレジストリ。 |
| AI台帳 | "Record governance decision" / "Set the outcome, accountable owner and next review." | ガバナンス決定を記録結果、責任者、次回レビューを設定します。 | 判断を記録判断の内容、責任者、次回のレビュー期限を設定します。 | 用語の統一。 |
| AI台帳 | "No AI tools to show: the findings could not be read. This is not an empty estate." / "No AI tools observed in the last X. That is a real answer for a small estate, and it is also what a fleet with no collectors deployed looks like: check Setup before reading it as a clean one." | 表示するAIツールがありません: 検出結果を読み取れませんでした。これは空の環境ではありません。 ／ ` : ` ／ 過去 … の間に AI ツールは検出されませんでした。 小規模な環境では実際にあり得る結果ですが、収集エージェントが配備されていない端末群も同じように見えます。クリーンな結果と判断する前にセットアップを確認してください。 | 検出結果を読み込めなかったため、表示できるAIツールがありません。AIツールが存在しないという意味ではありません。 ／ ` : ` ／ 過去…にAIツールは検出されませんでした。小規模な環境では実際にあり得る結果ですが、収集エージェントを導入していない場合も同じ表示になります。問題なしと判断する前に「検出ソース」画面を確認してください。 | 「クリーンな結果」「セットアップ」は直訳。移動先の画面名を示した。 |
| 貼り付けガード | "Could not read paste guard activity: X" | ペーストガード ／ ペーストガードのアクティビティを読み取れませんでした: | 貼り付けガード ／ 貼り付けガードの記録を読み込めませんでした: | 「アクティビティ」は直訳。 |
| 貼り付けガード | "What the paste guard stopped, on which tool, and how often. Only metadata is kept: the guard checks clipboard content on the device and reports which detector fired, so the text itself is never sent or stored. A heeded warning is the guard doing its job. An override is someone who saw the warning and pasted anyway, which is the row worth following up." | この画面では、ペーストガードが停止または警告した内容、対象ツール、発生件数を確認できます。保存されるのは検出結果などのメタデータのみです。ガードは端末上のクリップボード内容を検査して検出理由を報告しますが、貼り付けた文章そのものは送信も保存もされません。警告に従って貼り付けを中止した記録も確認できます。「警告後の続行」は、警告を確認した利用者が貼り付けを続けた件数です。 | 貼り付けガードが止めた内容、対象のツール、件数を確認できます。保存するのはメタデータだけです。ガードは端末上でクリップボードの内容を検査し、どの検出ルールに一致したかだけを報告するため、貼り付けた文章そのものは送信も保存もされません。警告を見て貼り付けをやめた場合は、ガードが役割を果たしたことを示します。「警告後に続行」は警告を見たうえで貼り付けた件数で、フォローアップが必要なのはこの行です。 | 原文の要点（警告に従えば成功、続行した行が要フォロー）が抜けていた。 |
| 貼り付けガード | stats "devices running the guard" / "warned" / "overridden" / "blocked" / "devices with an event" | ペーストガードを実行しているデバイス ／ … ／ 警告表示数 ／ … ／ 警告後の続行数 ／ … ／ ブロック済み ／ … ／ イベントのあったデバイス | 貼り付けガードが動作中の端末 ／ … ／ 警告 ／ … ／ 警告後に続行 ／ … ／ ブロック ／ … ／ 記録があった端末 | 概要カードと同じ語にそろえた。 |
| 貼り付けガード | "Running [version on N] in [mode on N]. A fleet split across versions is a rollout that stalled, and a device in warn mode where policy says block is a policy that is not in force. Neither is visible in a count of what was stopped." | ).join('')} を ${PG.guard_modes.map(m => ／ ).join('')} で実行中です。端末群内でバージョンが混在している場合、更新が行き渡っていない可能性があります。ブロックモードを設定していても、警告モードで動作中の端末では貼り付けを停止できません。この状態はブロック件数には含まれません。 ／ | ／ 動作状況: ${PG.guard_versions.map(v => ／ ).join('')}。端末間でバージョンが混在している場合は、更新の展開が止まっている可能性があります。また、ポリシーでブロックを指定しているのに警告モードで動作している端末では、そのポリシーが効いていません。どちらも、止めた件数には表れません。 ／ | 「〜を〜で実行中」の語順と、ポリシーが効いていない状態の説明を原文どおりにした。 |
| 貼り付けガード | "If block mode were on" | ブロックモードがオンだった場合 | ブロックモードにした場合 | 仮定の表現を自然にした。 |
| 貼り付けガード | "Every warned paste in this window would have been stopped outright instead of asked about - the same events, replayed under the stricter policy. What warn cannot stop is the override column: block has no \"paste anyway\"." | 警告が表示された貼り付けは、ブロックモードでは確認を求めずに停止されます。この表示は、同じイベントにブロックモードを適用した場合の推定です。警告を無視して続行した件数は「警告後の続行」列で確認できます。ブロックモードでは、そのまま貼り付ける選択肢はありません。 | この期間に警告した貼り付けは、ブロックモードなら確認を求めずにすべて止められていました。同じ記録にブロックモードを当てはめた試算です。警告モードで止められないのは「警告後に続行」の件数で、ブロックモードには「そのまま貼り付ける」選択肢がありません。 | 列名の表記を統一し、試算であることを明確にした。 |
| 貼り付けガード | "N stopped + N override(s) prevented" | + … 件の警告後の続行を防止 | （うち警告後の続行 … 件を防止） | 「+」でつないだ直訳を解消。 |
| 貼り付けガード | columns "Warned" / "Overridden" / "Blocked" / "Devices" / "Detectors" | AIツール ／ 警告表示数 ／ 警告後の続行数 ／ ブロック済み ／ デバイス ／ 検出機能 | AIツール ／ 警告 ／ 警告後に続行 ／ ブロック ／ 端末数 ／ 検出ルール | 概要カードと同じ語にそろえた。 |
| 貼り付けガード | "No paste events in this window. That is a real answer, and it is also what an estate with the extension not deployed looks like: check Setup before reading it as nobody having tried." | この期間にペーストイベントはありません。これは実際の回答であり、拡張機能が展開されていない環境も同じように見えます。誰も試していないと解釈する前に、セットアップを確認してください。 | この期間に貼り付けの記録はありません。本当に記録がない場合もありますが、拡張機能を導入していない環境でも同じ表示になります。誰も貼り付けていないと判断する前に「検出ソース」画面を確認してください。 | 「実際の回答」は直訳。移動先の画面名を示した。 |
| ISO/IEC 42001 証跡 | "Could not build the evidence index: X" | ISO/IEC 42001証跡 ／ 証跡インデックスを構築できませんでした: | ISO/IEC 42001 証跡 ／ 証跡の一覧を作成できませんでした: | 画面名を統一。 |
| ISO/IEC 42001 証跡 | "N tools in use, N watched for, N not in the registry" | 、… 件が台帳に登録されていません | 、… 件はレジストリ未登録 | 【意味の誤り】not in the registry を「台帳に登録されていません」としていた。 |
| ISO/IEC 42001 証跡 | "Monitoring coverage: N of M expected sources reporting" (link "Setup") | 検出元の報告状況 ／ 想定される検出元は … 件あり、そのうち … 件から報告があります ／ 初期設定 | 検出ソースの報告状況 ／ 想定される検出ソース … 件のうち、… 件から報告があります ／ 検出ソース | 【誤訳】リンク先は「検出ソース」画面で「初期設定」ではない。 |
| ISO/IEC 42001 証跡 | "Account governance: N personal accounts across N tools" | …件の個人アカウントを確認。対象ツールは ／ … 件です | 個人アカウント … 件を確認（対象ツール ／ … 件） | 1行の記録として簡潔にした。 |
| ISO/IEC 42001 証跡 | "Integrations: N MCP servers observed" / "Third parties" | 統合 ／ …件のMCPサーバーを確認 | 外部連携 ／ MCPサーバー … 件を確認 | 「統合」は integration の直訳。 |
| ISO/IEC 42001 証跡 | "Third parties: N providers observed across the tools in use" | 外部サービス ／ 利用中のAIツールで … 件の提供元が確認されました | 外部の提供元 ／ 利用中のAIツールの提供元 … 社を確認 | 数えているのは提供元（事業者）。 |
| ISO/IEC 42001 証跡 | review input "N tool(s) in use and not in the registry" / "N decision(s) with no owner" | …件の利用中ツールがAI台帳に登録されていません ／ 所有者のいない決定が…件あります | 利用中のツール … 件がレジストリに未登録です ／ 責任者が未設定の判断が … 件あります | 【意味の誤り】not in the registry を「AI台帳に登録されていません」としていた。owner は責任者。 |
| ISO/IEC 42001 証跡 | review input "N expected source(s) not reporting" | …件の検出元から報告がありません | 想定される検出ソースのうち … 件から報告がありません | 用語の統一。 |
| ISO/IEC 42001 証跡 | heading "ISO/IEC 42001 evidence" | ISO/IEC 42001の記録 | ISO/IEC 42001 証跡 | ナビ・エラー表示と画面名を統一。 |
| ISO/IEC 42001 証跡 | "source coverage · N of M reporting" | 検出元の報告率… / … 件が報告中 | 検出ソースの報告率… 件中 … 件が報告中 | 用語の統一。 |
| ISO/IEC 42001 証跡 | "Findings could not be read, so no clean-state conclusion is shown." | 検出結果を読み取れなかったため、クリーンな状態という結論は表示されません。 | 検出結果を読み込めなかったため、「問題なし」とは判断していません。 | 「クリーンな状態という結論」は直訳。 |
| ISO/IEC 42001 証跡 | "Nothing outstanding in this window. N of M expected sources are reporting; zero reporting is never treated as a clean estate." | 想定される検出元 … 件のうち … 件が報告中です。報告がゼロでも、問題がない環境とは判断できません。 | 想定される検出ソース … 件のうち … 件が報告中です。報告が0件の状態を「問題なし」とは扱いません。 | 用語の統一。 |
| ISO/IEC 42001 証跡 | "The JSON identifies registry and governance files by hash. It may not be reproduced identically after log retention changes; its checksum detects accidental changes, not deliberate modification." | JSONには、AI台帳とガバナンスファイルを識別するハッシュ値が含まれます。 | JSONには、レジストリとガバナンスファイルを識別するハッシュ値が含まれます。 | 【意味の誤り】ハッシュ値で識別するのはレジストリのファイル。AI台帳ではない。 |
| 設定の行 | pills "saved here" / "from deployment" | ここに保存済み ／ 環境変数から | ポータルに保存済み ／ 環境変数の値 | 「ここ」「〜から」だけでは状態が分からない。 |
| 設定の行 | "Saved in the portal (overriding the deployment's value; clear to fall back to it)." / "Saved in the portal." / "Currently from the deployment's environment; saving here overrides it." | ポータルに保存済み（環境変数の値を上書きしています。クリアすると環境変数の値に戻ります）。 ／ ポータルに保存済み。 ／ 現在は環境変数から取得されています。ここで保存すると、その値を上書きします。 | ポータルに保存した値を使っています（環境変数の値より優先）。値を消して保存すると環境変数の値に戻ります。 ／ ポータルに保存した値を使っています。 ／ 現在は環境変数の値を使っています。ここで保存すると、保存した値が優先されます。 | 「上書き」は環境変数が書き換わると誤解される。実際は優先順位の話。 |
| 設定の行 | "A value is set (never shown). Leave blank and save to CLEAR it; type and save to replace it." / "Not set." | 値が設定されています（表示されません）。消去するには空欄のまま保存し、置き換えるには入力して保存してください。 | 値は設定済みです（画面には表示しません）。空欄のまま保存すると値が削除されます。変更する場合は新しい値を入力して保存してください。 | 原文が強調する「空欄で保存すると消える」を先に伝える語順にした。 |
| 概要のカード選択 | widget titles and descriptions (WIDGET_JA) | const WIDGET_JA = {"stat_row":{"title":"主要数値","desc":"環境全体の主要件数"},"top_tools":{"title":"上位ツール","desc":"デバイス数別のツール"},"recent_personal_accounts":{"title":"最近の個人アカウント","desc":"最近確認された個人アカウント"},"detection_coverage":{"title":"検出カバレッジ","desc":"各利用環境のレポート率"},"source_health":{"title":"ソース健全性","desc":"レポート中のソースと停止中のソース"},"paste_guard":{"title":"ペーストガード","desc":"警告表示、警告後の続行、ブロックされた貼り付け"},"review_queue":{"title":"レビューキュー","desc":"ガバナンス判断待ちの観測ツール"},"budget_spend":{"title":"予算支出","desc":"観測された使用量に対する追跡AI支出（管理モード）"},"activity_trend":{"title":"アクティビティ推移","desc":"期間内の日別個人アカウント数とデバイス数"},"agentic":{"title":"エージェント型","desc":"人の介在なしに実行されるもの"}}; | const WIDGET_JA = {"stat_row":{"title":"主要な数値","desc":"全体状況と4つの主要件数"},"top_tools":{"title":"検出されたAIツール","desc":"観測したすべてのツール（端末数・ID・個人アカウント）"},"recent_personal_accounts":{"title":"最近の個人アカウント","desc":"企業ドメイン以外のアカウントでの最近の利用"},"detection_coverage":{"title":"環境全体の可視化状況","desc":"収集エージェントのカバー率と、報告中の検出ソース"},"source_health":{"title":"報告のない検出ソース","desc":"一覧のうち、この期間に報告がなかった検出ソース"},"paste_guard":{"title":"貼り付けガード","desc":"警告、警告後の続行、ブロックした貼り付け"},"review_queue":{"title":"優先して確認すること","desc":"対応事項と、判断・検出結果のキュー"},"budget_spend":{"title":"AI支出","desc":"契約と実際の利用状況の比較（管理モードのみ）"},"activity_trend":{"title":"個人アカウントの利用推移","desc":"1日ごとの検出件数と報告した端末数"},"agentic":{"title":"自律的に動作中のAI","desc":"人の操作なしに起動するAIと、その責任者"}}; | カード選択の名前が、概要に表示されるカード見出しと食い違っていた（例: 上位ツール／検出されたAIツール）。 |
| 概要のカード選択 | "Overview widgets" / "Overview catalogue" / "Choose which modules are available to people in this estate." / "N enabled" | 概要ウィジェット… ／ 概要カタログこの環境のユーザーが利用できるモジュールを選択します。 | 概要のカード… ／ 概要に配置できるカードこの環境の利用者が概要に配置できるカードを選びます。 | 「ウィジェット」「モジュール」「カタログ」が混在していた。画面上の呼び名は「カード」。 |
| 概要のカード選択 | "Embedded Grafana panel" | 埋め込み Grafana パネル | Grafana パネルを埋め込み表示 | 語順を自然にした。 |
| 概要のカード選択 | meta "Native · token" (source label) | 標準 | 標準の ／ の | 「標準ウィジェット」「Grafanaパネル」と続けて読めるようにした。 |
| 概要のカード選択 | meta suffix | パネル ／ ウィジェット | パネル ／ カード | 同上。 |
| 概要のカード選択 | "Deployment availability" / "People can still arrange or hide these modules from Overview → Edit." / "Restore N hidden widget(s)" / "Save catalogue" | ／ … 件の非表示 ウィジェット を復元 ／ | ／ 非表示にしたカード … 件を再表示 ／ | 英語の単語区切りの空白（「非表示 ウィジェット を」）が残っていた。 |
| 貼り付けガードの設定 | mode "warn (default)" | 警告（デフォルト） | 警告（既定） | 「デフォルト」より一般的な「既定」。 |
| 貼り付けガードの設定 | "What happens when someone pastes marked content into an AI tool: warn asks them first, block stops it. Baked into the policy downloads." | AIツールにマークされたコンテンツを貼り付けたときの動作: 警告は最初にユーザーに確認し、ブロックはそれを停止します。ポリシーのダウンロードに組み込まれます。 | 機密表示のある内容をAIツールに貼り付けたときの動作です。「警告」は貼り付ける前に本人に確認し、「ブロック」は貼り付けを止めます。設定はポリシーのダウンロードファイルに組み込まれます。 | 「マークされたコンテンツ」は直訳。 |
| 貼り付けガードの設定 | "Classification markings" / placeholder "one marking per line (empty = the default set)" / "Clear (default set)" | 分類マーキング… | 機密表示の文言… | 「分類マーキング」は直訳で、社外秘などの表示を指すと伝わらない。 |
| 貼り付けガードの設定 | placeholder "one marking per line (empty = the default set)" | 1行に1つのマーキング（空欄 = 既定のセット） ／ placeholder="1行に1つのマーキング（空欄 = 既定のセット）" | 1行に1つ入力（未設定の場合は既定の文言） ／ placeholder="1行に1つ入力（未設定の場合は既定の文言）" | 同上。 |
| 貼り付けガードの設定 | button "Clear (default set)" | ／ クリア（デフォルトセット） ／ | ／ 既定の文言に戻す ／ | 押した結果を名前にした。 |
| 貼り付けガードの設定 | "Document phrases the guard looks for in pastes, one per line. Save an empty box to use no markings; clear to go back to the default five. What people paste never leaves their device - only which detector matched gets reported." | ガードがペースト内で探す文書フレーズを1行に1つずつ入力します。マークなしにするには空欄を保存し、デフォルトの5つに戻すにはクリアします。ユーザーが貼り付けた内容がデバイスから出ることはなく、一致した検出器だけが報告されます。 | 貼り付けた内容に含まれていたら検出する文言（「社外秘」など）を1行に1つずつ入力します。空欄で保存すると機密表示の検出を行いません。「既定の文言に戻す」で既定の5つに戻ります。貼り付けた内容が端末の外に送られることはなく、一致した検出ルールだけが報告されます。 | 直訳と用語（ペースト・検出器）の不統一を解消。 |
