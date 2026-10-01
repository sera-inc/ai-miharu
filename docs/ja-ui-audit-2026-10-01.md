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
