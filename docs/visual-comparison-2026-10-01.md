# 実画面の比較記録

指定された実参照は公開サイトcommit `af27978`のsumai-deskとsumai-sketch。AIミハルLPは同じSumaiLandingを使用し、製品の実装内容を当てはめた。Image2.5の新規コンセプト画像を生成したという主張はしない。

撮影: 1440×900、390×900、Chromium / Playwright。Browser/IAB専用ツールがないための代替。`?sera_internal=1` と `html[data-analytics-excluded=true]` を全ページで確認し、解析同意を拒否した。初期モバイルは共通MobilePageBodyの要約表示。全文撮影では「詳しい説明」を開いてから各sectionへスクロールした。撮影用の静的画面でUIを置換していない。

[evidence](evidence/2026-10-01/) に両参照と製品のhero画像、DOM順序、変更前後のポータル画像、レスポンシブ集計を保存。全ページ画像はクラウド `artifacts/lp-comparison/*-full.png`、全20製品画面は `assets/screenshots/`、実操作動画は `assets/videos/paste-guard-demo.webm`。

## 照合内容

| 比較点 | 確認内容・修正 | 限界 |
|---|---|---|
| LP構成 | 共通section順、機能/料金/FAQ/CTA導線、mobile要約→全文展開を維持 | AI詳細・料金出典等の補助sectionは意図的追加。構造DOMは参照14/製品20section |
| 見出し | 製品の長いコピーを7字×2行へ短縮しdesk同様の72px desktop文字サイズへ | sketchは9字行用の共通小サイズ。全製品同一文字幅という意味ではない |
| 色・余白 | 共通blue hero/白い下部境界、ヘッダ・CTA配置を比較 | ピクセル完全一致を主張しない |
| 実画面の扱い | ヒーロー比較画像をcontainにして切り抜きを減らし、最新20画面と実貼付動画へ差替え | 小さいhero内では詳細は読めない。拡大リンク・詳細説明で補う |
| 操作 | 業務絞込、全角検索、ゼロ件解除、予算ギャラリー切替をdesktop/mobileで確認 | 問い合わせ送信は行っていない |
| mobile | 幅390pxで3ページの初期要約と詳細展開を確認。文書横溢れ0 | すべての端末・ブラウザ幅の保証ではない |
| ポータル | 改修前後overview/toolsをview_imageで比較。ナビを白地・青選択へ、本文/表/入力/余白を実DS役割へ寄せた | DS未移行値・独自dark/chart役割が残る |
| 意味と表示 | 架空実績を追加せず、OSS提供中と商用未提供案を近接表示。政府公式でないFAQ追加 | Image2.5指定・商標調査・人間デザインレビュー未解決 |

`view_image`で参照desktop/mobileと最終製品のhero、ポータルbefore/afterを直接確認した。上部copyの英語補助文を日本語へ、情報システムの業界導線を修正したことは意図差。全section本文の一字一句/全pixelの完全一致や、スキルの全面10/10サインオフを主張しない。

公開site側の詳細対応表は `docs/ai-miharu-lp-parity-2026-10-01.md`。通常本番buildは外部カタログ照合APIへのfetchに失敗。`VITE_RESOURCE_CATALOG_API_URL='' npm run build` はcompile・4213ルートprerender・静的SEO等の検証に成功したが、外部catalog release gateの通過とは区別する。全site Nodeテスト392件、TypeScript検査は成功。
