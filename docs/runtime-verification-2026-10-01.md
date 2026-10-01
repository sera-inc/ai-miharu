# 実行・回帰検証（2026-10-01）

この検証は保存済みクラウド環境だけで実施した。利用者のMac、実顧客データ、外部の実Microsoftテナントは使用していない。データは `demo/seed.sh` の合成データであり、ログイン情報も公開デモ値を用いた。

## 起動と検証条件

- portal/receiverはそれぞれ独立したPython 3.12 venvに各 `requirements.lock` をインストールし、uvicornで起動。healthzは両方HTTP 200。
- Docker ComposeのLoki/Grafana/Mailpitを利用。Docker内の依存取得はDNS制約で失敗したため、ホストvenvを実行に用いた。Dockerイメージ自体の再build成功を主張しない。
- 合成Microsoft Entraプロバイダーはホスト8092で起動。ブラウザーでMicrosoftサインイン→管理者選択→portal `#wizard` 復帰まで成功。PKCE・コード交換は製品の通常処理。
- 拡張デモのnginxはマウントしたクラウドcheckoutのファイル権限により403。製品ファイルを変更せず、同じextensionディレクトリーをPython HTTP server（8093）で配信して操作した。
- Chromium `/usr/bin/chromium`、既存 `tools/screenshots` のPlaywrightを利用。録画は既存 `/usr/bin/ffmpeg` をPlaywrightの実行パスへリンクした。専用ffmpeg CDNは403だった。
- portal URLはクラウド内部 `http://localhost:8091`。外部の人が開けるプレビューURLとは区別する。確認画像URLを共有して確認の機会を設けた後、引き継ぎ時に停止した。外部の対話プレビューは提供できていない。

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
- 改修後の最終検証: portal Python **731 passed, 24 warnings**（`/tmp/miharu-portal-final.log`、3.20秒） / portal Node 34 passed。receiverは変更なし、373 passedの結果を維持。extension Nodeは4 test files passed（各ファイル内のassertを含む）。
- portalは `PYTHONPATH=portal PORTAL_AUTH=none` で実行。異なるportal/receiver依存を同一venvへ混在させていない。
- ログは `artifacts/test-results/`。全リポジトリーCI、コンテナビルド、実端末収集、実Microsoftテナント、全OSの実ブラウザーをこの結果に含めない。

## Push後のGitHub Actions確認

Draft PR [#7](https://github.com/sera-inc/ai-miharu/pull/7)、対象commit `49aac41e14ff4d166570cedaf406a01aee40792c` をGitHub connectorで確認した。CLI認証失敗をCI失敗と混同せず、実際のworkflow/jobログを取得した。

- [ci run 36884192659](https://github.com/sera-inc/ai-miharu/actions/runs/36884192659): **success**。21ジョブ成功、公開用のbuild-images/publish-chart 2ジョブはskipped。compose-smokeとdemo-smokeも成功しているため、クラウドローカルで未完了だったDockerビルド・起動はGitHub runner上の別証拠として確認できた。
- [trivy run 36884192668](https://github.com/sera-inc/ai-miharu/actions/runs/36884192668): **failure**。repoのdependency gate（job 110443196941）とscanner image gate（job 110443197031）が失敗。両方のgateログは `urllib3 2.7.0` のHIGH `CVE-2026-97687` と `CVE-2026-97689` を検出し、Fixed Versionは `2.8.0` と報告している。対象は `scanner/requirements.lock` とscannerイメージ。
- portal/receiver/discoveryのimage gateと設定不備gateは成功。scanner依存ロックはこのUI改修で変更されていないが、セキュリティgate未達の状態を成功とは扱わない。その後scannerのurllib3下限を2.8.0へ更新し、同じDockerベースでlockを再生成した。変更はurllib3のバージョン・hash・由来と入力の下限だけ。修正commitのTrivy再実行はpush後に確認する。
- この確認結果は上記commit限定。後続commitのCI結果へ流用しない。mainへの統合・公開操作は行っていない。

## scanner依存修正と再現方法

公式[urllib3 2.8.0 release](https://github.com/urllib3/urllib3/releases/tag/2.8.0)、[HTTPS proxy TLS advisory](https://github.com/urllib3/urllib3/security/advisories/GHSA-8988-9cw3-xx77)、[無制限chunk-sizeバッファー advisory](https://github.com/urllib3/urllib3/security/advisories/GHSA-vxq7-64xx-v4gw) の修正版2.8.0をCIログと照合した。wheel/sdistのSHA-256も[PyPIの2.8.0 metadata](https://pypi.org/pypi/urllib3/2.8.0/json)と一致。

scanner回帰は **238 passed（45.61秒）**。監査ログのデフォルトHOMEがread-onlyのため、製品でサポートする `AIGUARD_AUDIT_LOG=/workspace/ai-miharu-runtime/scanner-audit.log` を指定して実行した。依存は `--require-hashes` で導入し、`pip check` も成功した。実行ログは `/tmp/miharu-scanner-final.log`。

lock生成には `python:3.12-slim`、`pip-tools==7.6.0`、`click==8.4.2` とMakefileと同じ `pip-compile --generate-hashes --strip-extras --output-file=requirements.lock requirements.in` を使用した。2回目の生成物は初回とバイト単位で一致。他コンポーネントのlockにはurllib3が存在しないため変更していない。

クラウド固有のネットワーク制約を解消するため、Docker実行時に既存の `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` / `NO_PROXY` を `-e 名前` で引き継ぎ、ホスト `/etc/hosts` と `/etc/ssl/certs/ca-certificates.crt` をread-only mountした。CAはコンテナー内 `/tmp/ca.crt` とし、`SSL_CERT_FILE` と `PIP_CERT` をこのパスへ設定した。プロキシ値を出力・コミットせず、TLS証明書検証も無効化していない。これによりDocker内で実際の正規lock生成が完了した。初回のDNS/build失敗はこの回避策適用前の記録として区別する。

## 残る制約

外部確認URL・指定画像モデル・正式な共有デザイントークンの承認など、親の要件チェックリストで未完了となる項目は、この実行検証によって解消したとは扱わない。Grafanaのダッシュボードは画面を開いたが、全パネルのデータ意味や第三者UIすべての日本語化は網羅検証していない。
