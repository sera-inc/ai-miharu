> **最新追記（2026-10-01）:** A〜Eと細部選定の委任を受領し、実装・再検査を進めた。旧「選択待ち」「画像生成未許可」「停止済み」はその記録時点の状態。[最新適用と検証](approved-migration-verification-2026-10-01.md) および[現行決定表](dads-current-decisions-2026-10-01.md)を優先。

# AIミハル 改善・検証チェックリスト

開始: 2026-10-01。クラウド `/workspace` のみ使用。初期commit `a33af44`、初期作業ツリーclean、実行中コンテナなし。
作業branch: `codex/ai-miharu-complete-20261001`。公開サイト別branch: `codex/ai-miharu-lp-20261001`。
参照DS: `6051bceb67c60fb805b757c22bbd66f3318ea980`。参照サイト: `af27978d59957a3bbe17fbe08bb93257bb03f159`。
本repo内AGENTS.mdなし。CLAUDE.md、README.md、TESTING.md、docs/feature-coverage.md、mapping.mdを参照。公開サイトAGENTS.mdの内部アクセス除外に従う。

| 要件 | 開始時の証拠・問題 | 完了基準／状況 |
|---|---|---|
| 1 再起動・baseline・branch | 停止中、READMEにDockerデモ手順 | branch作成済。デモ起動・画面baseline準備中 |
| 2 実DS移行 | READMEにPhase1未完了。143値の保留と誤除外あり | 実DSをclone済。`design-audit-2026-10-01.md`参照。機能/視覚/アクセシビリティ検証を要す |
| 3 全UI日本語・会社 | 日本語UI既存、第三者著作表示あり | error/empty/settingsと周辺UIを再検証。ライセンス保持 |
| 4 合成データ主要操作 | feature-coverageは保存操作を未実施と明記 | デモの合成fixtureだけで保存・発行・失効を含む操作を検証 |
| 5 Image2.5・ブランド | AIミハル既存ロゴあり | Image Gen callableだが指定モデルの選択/確認不可。Image2.5使用を主張しない。新規生成は保留 |
| 6 repo名 | `ai-miharu`へ改名済、名称はAI利用の見守りに適合 | 維持案。追加変更によるリンク/CI影響なし |
| 7 sumai LP・料金・実画面 | 公開サイトclone成功。既存SumaiLandingを共有 | desk/sketchとの順序・CTA対応表、desktop/mobile比較、一次料金、実UI画像/動画 |
| 8 基盤費用 | Compose既存、負荷推奨は未確立 | 公式出典、条件付き5基盤比較、構成図作成中 |
| 9 公開site組込 | AI LP既存、情報システム掲載あり | 個別branchのみ。main統合/push直前は親との調整が必須 |
| 10 main/push/CI | 未変更 | 全完了後のみ。force push/既存変更破棄を行わない |
| 11 人が見られるURL・停止 | 起動前 | URL共有・確認機会後に停止。localhostを外部確認URLとは扱わない |

## 環境上の問題（初期）

- ホームは書込不可。Docker/npm cacheをworkspaceへ移すことで回避。
- Docker bridge内DNS失敗により通常のimage buildが失敗。ホスト環境起動等を検討中。
- Playwright browser downloadはcdn.playwright.dev 403。既存 `/usr/bin/chromium` で検証する。
- Browser/IAB専用toolはカタログにないため、Playwrightへフォールバック。
- Image Gen tool schemaにmodel指定がない。要求のImage2.5は未検証・未使用。

この文書の項目が未完了の間は「全要件完了」「100%一致」と報告しない。

## 実装・検証後の状態

- 実施: 作業branch、実DS監査、役割別CSS/日本語エラー/SSO・アクセシブル名の修正。原著ライセンス保持。
- 実施: 基準20画面、改修後20画面、24ルート×2幅、合成データの保存/復元・発行/失効操作、実貼付動画。詳細は `runtime-verification-2026-10-01.md`。
- 実施: 公開site別branchにLP/料金/検索改善、sumaiの実DOM/画像比較、全392テスト、型検査、外部release確認を除くbuild。
- 実施: 国内外料金・5基盤コスト・条件付き試算・構成図。名称はAIミハルを維持。
- 未完了: DS全Phase移行（未解決値/Primitive全面移植/支援技術レビュー）、全第三者UI日本語の網羅検査、Image2.5指定、新規アイコン/画像生成。
- 未完了: 通常Docker build（Docker内DNS）、通常site release gate（外部API fetch）、外部対話プレビューURL（Cloudflare endpointへのDNS失敗/プロキシ403）。自己判断で制限を回避しない。
- main反映条件を満たしていないため、main統合/push・本番公開は実行しない。公開siteはendpoint-operationsとの親調整も未了。レビュー可能な個別branchに保持する。
- ポータル内部URLは http://localhost:8091、LP内部URLは http://localhost:5173/information-systems/products/ai-miharu/ 。いずれも利用者が外部から開けるURLとは主張しない。人が確認する機会の確保と停止手順を親へ引き継ぐ。
- 追加検証: 実DS外部mountと同梱fallbackをlight/dark×7要素×7属性で比較し差分0。網羅的な全値移行完了とは区別する。`/dads.css` 404はaxeによる相対importの再取得に限られ、通常ブラウザ読み込みでは再現せず。

## 保存・停止の最終記録

- 製品ドラフトPR: https://github.com/sera-inc/ai-miharu/pull/7 。公開済コードhead `db775f8bc15994753b902aec2d492dbe2260a304`。通常CI / Trivy両方成功。
- 公開siteドラフトPR: https://github.com/sera-inc/sera-inc-public-site/pull/74 。remote head `26cc48530ab78262fb7660f0733065f0fd67fa13`。CLI write認証がなかったためGitHub connectorで保存。local `677d4d01` とremoteのtree SHA `c726daa4b25802aa1af65aed0d0fc1e6bc8502e4` が一致することを検証。対象commitのGitHub Actions実行は0件（CI成功とは表現しない）。
- siteのmain統合は未実施。endpoint-operationsと競合し得る共有ファイルはrouteSeo.ts、生成llms文書、package-lock.json。最新remoteで比較し、統合時にllmsを再生成する。
- 画面確認用GitHub画像URLを途中共有済み。インタラクティブな外部URLは未提供という制約を明示した。
- 最終停止: 今回のportal/receiver/mock/extension HTTP/Vite、demo Composeを通常停止。8080/8091/8092/8093/8094/5173/3000/3100/8025は待受なし、起動中Dockerコンテナ0。volume削除はしていない。
- 対応表は実在z-index9値を未判定へ訂正し、未解決85種。機械再抽出は143種/2,186出現。人間による対応決定や承認を捏造しない。
- 最後の文書訂正はクラウド内の追加commit/patchとして保持する。動作コードを変えていないため既済みの検証を再利用し、文書だけを理由にCI一式を再起動しない。次の実装・統合時にまとめて反映する。

## 継続調査

親からの再開指示に従い、[通常build・SEO変更・画像モデル・操作プレビュー](remaining-environment-checks-2026-10-01.md)を再調査した。通常buildの必須catalog APIは環境プロキシがCONNECT403を返す。最新mainのSEO修正と今回branchを照合、関連6ファイル同一・履歴baseline変更なし、計測テスト21件成功。地域料金の追加一次情報と再取得条件を費用比較に追記。外部操作URLとImage2.5の指定手段は引き続き未達。main公開は保留する。
