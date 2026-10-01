# 日本語UI監査（2026-10-01）

## 対象と現状証拠

`CLAUDE.md`、`README.md`、既存の `docs/ja-ui-copy-review.md` と日本語テストを読み、表示文言と機械用の識別子を区別した。基準画面20件の撮影完了を待ってから `index.html` を変更した。撮影と全画面動作確認は別の実行時QA記録を参照。

| 対象 | 変更前に確認した状態 | 今回の対応 |
|---|---|---|
| ポータル各画面・空状態 | ナビゲーション、設定、空状態は既に日本語。未知のAPIエラーは「処理できませんでした」のみ | 実際の受信サービス・ポータルのエラーに合わせ、設定、権限、ログ保存先、端末・トークン、承認の案内を追加 |
| 設定フォーム | 勤務時間、SMTPポート、機密表示、URL、SSOの制約違反が一般エラーになっていた | 入力形式、文字数、必要な権限と次の操作を日本語で案内 |
| 構造化された検証エラー | FastAPIの配列形式を文字列化して一般エラーにしていた | 入力内容・秘密情報を表示せず、日本語で入力形式と必須項目の確認を促す |
| システム状態 | `registry_error`、`loki_last_error` は例外の型名だけ表示 | 日本語の説明に「診断コード」として併記。生の例外本文は引き続き表示しない |
| SSO専用画面 | 本文は日本語、会社と問い合わせ先も正しいが文書言語が未指定 | `html lang="ja"` を追加 |
| 拡張機能 | manifest、guard、管理設定スキーマは日本語。popup/optionsの専用画面は実装されていない | 二つの配布元コピーの同一性を既存テストで確認。原著authorは保持 |
| 拡張機能デモ | 警告/ブロック/オフと空状態は日本語。クリップボード拒否時は未通知 | 日本語のコピー失敗通知、読み上げ通知、viewport、株式会社世良と問い合わせ先を追加 |
| Grafana | 自作ダッシュボードのタイトル・説明・凡例・表示フィルターは日本語。Composeに `GF_USERS_DEFAULT_LANGUAGE: ja-JP` が設定済み | 機械用クエリ、Lokiラベル名、固有製品名は変更しない |
| 会社・帰属 | ポータルの問い合わせは `info@sera-inc.co.jp`。原著Nyxusは第三者製品と明記済み | 原著の著作権・ライセンス・製品帰属は維持 |

## 変更箇所

- `portal/app/static/index.html`: エラー表示層のみで英語のAPI契約を日本語へ変換。ネットワーク障害やログ未設定を、検出結果ゼロと区別して表示する。
- `portal/app/main.py`: SSO専用文書の言語指定。
- `extension/demo/index.html`: コピー失敗の日本語通知、サンプルデータの案内、連絡先、viewport。
- `portal/tests/error_text.test.cjs`: 設定/権限の復旧案内、ログ未接続、検証エラーに含まれる秘密情報を露出しないことを検証。

APIキー、JSONキー、URL、環境変数、SMTPの応答原文、CLIコマンド、外部サービスの画面固有名は、連携・診断に必要な原表記を維持した。独自CSSには変更を加えていない。

## 検証

- `node --test portal/tests/*.test.cjs`: **34 passed**（追加3件を含む）。
- `PYTHONPATH=portal PORTAL_AUTH=none /workspace/ai-miharu-portal-venv/bin/pytest portal/tests/test_ja_terminology.py portal/tests/test_login.py portal/tests/test_error_disclosure.py -q`: **55 passed**。FastAPI `on_event` の既存非推奨警告6件。
- 上記は表示関数と認証・秘匿・表記の回帰検証。全ブラウザー・外部IDプロバイダー・Grafana本体のすべての翻訳まで確認したものではない。

## 残る範囲と限界

- Grafana本体は第三者アプリの日本語ロケールに依存する。全ての内部画面の完全翻訳はこのリポジトリの自作ダッシュボードとは別の範囲。
- 外部サービスの製品名や応答原文、管理者が登録した自由入力、技術識別子は翻訳対象ではない。
- 未知のAPIエラーは日本語の汎用メッセージへフォールバックする。今回で全APIエラーの個別訳を網羅したという主張はしない。

## axe検査に基づく追補

実行時QAの `artifacts/axe/results.json` で設定／アカウント画面の `select-name` 違反を確認した。既存アカウントのロール、新規アカウントのロール、SSO再認証間隔の3種類に日本語の `aria-label` を追加。既存アカウントはユーザー名をHTMLエスケープして含め、対象を区別できるようにした。`test_account_email_and_preferences.py` に回帰検査を追加し **22 passed**。ブラウザー上のaxe再検査は実行時QA担当へ依頼済み。

## 承認待ち期間の追加監査・独立修正（同日）

ポータルと拡張機能の固定HTML・動的表示（英語だけのボタン、placeholder、title、aria-label、通知・確認文）を再検索した。確認した一致は製品名・規格・コード例が中心で、今回それらを翻訳する変更は行っていない。これは全ブラウザー状態の再検証ではない。一方、これまで対象表から漏れていた `scanner/ai_guard/cli.py` と端末レポートに、利用者向けの英語が残っていた。

- CLIの自作コマンド説明、オプション説明、進捗、件数、初期設定の案内、探索の空状態、MCP評価の固定見出し・リスク表示を日本語にした。CLIのコマンド名、オプション名、設定ファイル名、環境変数、検出ソース識別子は維持。
- 端末レポートの見出し、表ラベル、重大度、機密表示、月表記、禁止ツール・アプリ連携の対応案内を日本語化。検出ゼロの場合にも検出ソースの状態を確認する案内を加え、正常に検査した保証と誤解しない表現にした。
- `[BLOCKED]` / `[APPROVED]` はポリシー集計にも使う識別子なので維持。JSON/CSVのキー・enum・検出本文、Confluence出力、原著copyright/SPDX/帰属、DSのmapping・CSSには変更していない。
- 実出力: [CLIヘルプ](evidence/2026-10-01/scanner-help-ja.txt)、[合成データ9件の端末レポート](evidence/2026-10-01/scanner-demo-ja.txt)。後者の機密表示は製品の固定表示であり、実際の証拠データは同梱fixtureの合成データだけを使用した。CLIは完了終了し、常駐サービスは再起動していない。

### 残る日本語化作業（承認・外部条件なしで実装可能）

1. **Clickが生成する文言**: `Usage` / `Options` / `Commands`、自動の `--help` / `--version` 説明、引数検証の `Error` / `Invalid value` 等。今回の自作ヘルプとは別に、ライブラリ互換性を保持する日本語化方式の設計・テストが必要。今回の証拠にも英語が見える。
2. **scanner動的な検出・評価本文**: `scanners/*.py` にある説明・前提条件失敗理由、MCPリスクの分類・タイトル・推奨、fixtureの説明、認証ユーティリティの失敗・権限警告。これらはCLIだけでなく機械出力に含まれるため、JSON契約を変えず表示層で訳す方式が必要。外部サービスの応答原文は日本語の診断案内と区別して扱う。
3. **Confluenceレポート、運用スクリプト**: `report._generate_confluence()` は固定文言も英語。`entrypoint.py` / `schedule.py` と配布スクリプトの管理者向けログ・CLIヘルプは今回未変更で、利用者向け画面とは分けた残件として残す。
4. **第三者画面・ブラウザー標準文言**: Grafana本体、SSO提供元、ブラウザーの標準フォーム検証はロケール・外部製品に依存する。コード検索のみで日本語網羅済みとは言えない。

従って、この追加修正をもって「ユーザー向け全UI日本語化完了」とはしていない。承認待ちのDS判断とは独立した残作業がある。

### 追加修正の検証

- `AIGUARD_AUDIT_LOG=/tmp/ai-miharu-ja-qa/audit.log PYTHONPATH=scanner /workspace/ai-miharu-scanner-venv/bin/python -m pytest scanner/tests -q`: **238 passed（45.63秒）**。既存demoテストに日本語の主要表示と、JSON側の英語risk enum・ポリシー識別子を維持する確認を追加した。
- CLI `--help` と `scan --demo` の実行はいずれも終了コード0、成果物を上記へ保存。APIを使う本番探索や初期設定による認証ファイル生成は実行していない。
- 初回demoテストは既定監査ログ先 `/home/agent/.ai-guard` が読取り専用で失敗したため、既存の `AIGUARD_AUDIT_LOG` オプションで書込み可能な一時ディレクトリへ変更。HOMEの変更・新しい永続認証の設定はしていない。変更中に発見したf-string構文エラーも修正後、上記全件が成功した。
- `git diff --check` 成功。表示層のみのためポータル全テスト・画面撮影は再実行せず既存証拠を維持。

## 設定反映の誤説明訂正とConfluence追補（同日）

- ウィザードの「再配布なしですぐに反映」と、設定冒頭の「再起動なしで各端末と受信サービスに反映」は、ブラウザー拡張機能の実装と矛盾していたため訂正した。`extension/src/guard.js` は `storage.managed` から動作設定を読み、ポータルの中央設定を直接購読しない。貼り付けガードの変更は**ポリシーの再生成・端末への再配布**、拡張機能の報告先URL変更は**パッケージの再生成・再配布**が必要と、既存の拡張機能セットアップ手順に揃えた。`docs/feature-coverage.md` の設定・貼り付けガード行も訂正。画像は再撮影していないため、既存画像の説明文は訂正前の可能性がある。
- 前節で未変更としたConfluence出力の**固定文言**も追加で日本語化した。見出し、表、重大度、対応案内、空状態を端末レポートと揃え、wikiマークアップと機械用ポリシー識別子を維持。動的検出本文・外部応答の未翻訳は依然として残る。前節の「Confluence固定文言が未翻訳」はこの追補で解消。
- 検証: `node --test portal/tests/*.test.cjs` **34 passed**、`portal/tests/test_wizard.py portal/tests/test_ja_terminology.py` **47 passed**（既存FastAPI警告6件）。変更に無関係な全238件は再実行していない。
- Confluenceも合成fixtureのCLI実行が終了コード0。[実出力](evidence/2026-10-01/scanner-confluence-ja.txt)の日本語見出し・対応パネル・合成利用者・`[BLOCKED]` を確認。`_generate_json` / `_generate_csv` はHEADとのPython AST比較で完全一致。`git diff --check` 成功。
