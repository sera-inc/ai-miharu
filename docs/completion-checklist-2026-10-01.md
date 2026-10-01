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
