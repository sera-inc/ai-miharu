# 実行・回帰検証（2026-10-01）

この検証は保存済みクラウド環境だけで実施した。利用者のMac、実顧客データ、外部の実Microsoftテナントは使用していない。データは `demo/seed.sh` の合成データであり、ログイン情報も公開デモ値を用いた。

## 起動と検証条件

- portal/receiverはそれぞれ独立したPython 3.12 venvに各 `requirements.lock` をインストールし、uvicornで起動。healthzは両方HTTP 200。
- Docker ComposeのLoki/Grafana/Mailpitを利用。Docker内の依存取得はDNS制約で失敗したため、ホストvenvを実行に用いた。Dockerイメージ自体の再build成功を主張しない。
- 合成Microsoft Entraプロバイダーはホスト8092で起動。ブラウザーでMicrosoftサインイン→管理者選択→portal `#wizard` 復帰まで成功。PKCE・コード交換は製品の通常処理。
- 拡張デモのnginxはマウントしたクラウドcheckoutのファイル権限により403。製品ファイルを変更せず、同じextensionディレクトリーをPython HTTP server（8093）で配信して操作した。
- Chromium `/usr/bin/chromium`、既存 `tools/screenshots` のPlaywrightを利用。録画は既存 `/usr/bin/ffmpeg` をPlaywrightの実行パスへリンクした。専用ffmpeg CDNは403だった。
- portal URLはクラウド内部 `http://localhost:8091`。外部の人が開けるプレビューURLとは区別する。検証後も親の確認待ちとして起動を継続した。

## 画面・レスポンシブ

改修前20画面を `artifacts/baseline/` にPNG/WebP保存。改修後20画面は `artifacts/final-screens/`。`tools/screenshots/capture-portal.mjs` の20対象（overview, tools, people, devices, personal, mcp, register, registry, paste, iso, budget, agentic, setup, coverage, fleet, tokens, settings, dashboard, diagnostics, wizard）を実際に開いた。

設定を5タブに展開した24ルートを1440pxと390pxで検証し、48組のスクリーンショットと本文を `artifacts/regression-responsive/` に保存。JavaScript pageerror 0件、document全体の横はみ出し0件。表内部のスクロールは許容した。個々の全ボタンや全キーボード順序を網羅したという主張ではない。

axe-coreのWCAG 2 A/AA・2.1 AA検査は24ルートで実行。初回はsettings/accountの3つの役割selectのaccessible name欠落を検出し、UI担当へ報告した。対象selectへaria-labelを追加後、同じsettings/accountを再検査し違反0件を確認（artifacts/axe-final/results.json）。他23ルートの初回検査も違反0件。自動検査はアクセシビリティ全体の適合宣言ではない。

## 実ブラウザーの主要操作

| 操作 | 結果と復元 | 証拠 |
|---|---|---|
| 無効なパスワード | サインイン拒否の日本語表示 | operations/login-error.png |
| 設定エラー | 253文字を超える合成企業ドメインを保存し、422に対応する日本語メッセージを確認 | operations/settings-error.png |
| 設定保存 | example.com, synthetic.exampleを保存・再描画で値を確認し、元の値に戻した | operations/results.json |
| 空状態 | 存在しない合成ツール名で検索し、結果なしを確認 | operations/empty-search.png |
| 登録トークン | 1日有効のQA用トークンを発行し、全文表示を閉じてから失効。失効済み行を確認 | operations/token-revoked.png |
| 個人アカウント許容 | 合成理由を入力し許容済みを確認、その後未解決に戻した | operations/personal-accepted.png |
| AI台帳判断 | claude-codeをレビュー中として理由付きで保存、保存済み判断の削除によりガバナンス既定値へ復元 | operations/register-saved.png |
| SSO | モックMicrosoftサインイン→オーナー認証→#wizard復帰、ログインフォーム消失 | /tmp/miharu-sso-qa.log（ランタイムログ） |
| 貼り付け警告 | 合成AWSサンプルを実clipboard+Ctrl+Vで貼り付け、警告→それでも貼り付ける→報告 | final-screens/paste-guard-warn.webp, paste-guard-report.webp |
| 貼り付け遮断 | 合成カード番号4111 1111 1111 1111の貼り付けを遮断し、入力欄に番号が入らないことを画像確認 | final-screens/paste-guard-block.webp |

貼り付け操作は実際の `extension/src/guard.js` を変更せずに実行。録画 `final-screens/paste-guard-demo.webm` は14.64秒。撮影時に本物の秘密情報を使わなかった。トークン全文は撮影せず、公開に使う20画面も発行操作前に撮影した。

## 自動回帰

- 改修前: portal Python 730 passed / receiver Python 373 passed / portal Node 31 passed。
- 改修後: portal Python 730 passed / portal Node 34 passed。receiverは変更なし、373 passedの結果を維持。extension Nodeは4 test files passed（各ファイル内のassertを含む）。
- portalは `PYTHONPATH=portal PORTAL_AUTH=none` で実行。異なるportal/receiver依存を同一venvへ混在させていない。
- ログは `artifacts/test-results/`。全リポジトリーCI、コンテナビルド、実端末収集、実Microsoftテナント、全OSの実ブラウザーをこの結果に含めない。

## 残る制約

外部確認URL・指定画像モデル・正式な共有デザイントークンの承認など、親の要件チェックリストで未完了となる項目は、この実行検証によって解消したとは扱わない。Grafanaのダッシュボードは画面を開いたが、全パネルのデータ意味や第三者UIすべての日本語化は網羅検証していない。
