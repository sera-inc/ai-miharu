# Codexによる役割別UI改修（2026-10-01）

本変更は `dads-product.css` の製品アダプター改修。実DS `6051bceb67c60fb805b757c22bbd66f3318ea980` の `tokens/semantic.css` と `tokens/brand.css` を読み取り、役割名と公開DADS primitiveの対応を照合した。private原本ファイルは同梱せず、必要な代替値を製品側で独立記述した。外部の完全トークンmount時には、既存 `@layer sera-standalone-fallback` の低優先度により実DSが優先する。

## 新たな対応提案と変更範囲

| 文脈 | 対応 | 変更理由 |
|---|---|---|
| ライトのcanvas/panel | `--app-surface-sunken` | 白いカードと画面背景を分ける |
| カード/raised/hover | `--app-surface` / `--app-surface-raised` / `--app-surface-hover` | 共通の意味役割に揃える |
| 境界/入力境界 | `--app-border` / `--app-border-strong` | 従来の薄いgray200を置換 |
| 本文/補助/リンク | `--app-text` / `--app-text-muted` / `--app-text-link` | 実semanticの役割へ統一 |
| 選択/主要操作 | `--app-primary` / `--app-primary-hover` / `--app-primary-bg` | DADS blueに揃える |
| ナビ、本文、フォーム | `--app-text-body-size` | 対象selectorのみ14pxへ。小字の値一括変換はしない |
| ページ/カード見出し | `--app-text-heading-lg-size` / `--app-text-heading-sm-size` | 24/18pxで情報階層を明確化 |
| テーブル本文 | `--app-text-table-size` | Dense14へ |
| 補足ラベル | `--app-text-body-sm-size` / `--app-text-label-size` | 12px補助情報を適用 |
| main/card/表の余白 | `--app-space-1/2/3/4` | 用途別に8/16/24/32pxを適用 |
| focus | 既存共有focusトークン | outline除去の高詳細度セレクタも上書き |

Codexによる実装提案であり、人間のmappingレビュー承認を示さない。旧mappingの未解決や誤判定を0と扱わない。製品独自ダーク/チャート役割は維持した。DOMやAPI・イベントは変更していない。プリミティブの全面移植（Phase 3）ではない。

白いナビ、青い選択表示、読みやすい表/フォーム、見出しと余白、44px相当の主要ボタンを導入。白いロゴはライト時のみ青い背景タイルを付けて視認性を保った。狭幅では見出し/操作群を折返し、ダーク時は暗いナビ面を維持。

## 検証

- Browser plugin not available。既存 `tools/screenshots/node_modules/playwright-core` と `/usr/bin/chromium` 使用。
- 対象: `http://localhost:8091` のデモサインイン→概要→ライト/ダーク→390pxモバイルナビ開く。
- 1440×900 / 390×844。タイトル「AIミハル」、有意味な内容、フレームワークエラー画面なし、pageerror 0。モバイルのdocument幅390px=viewport390px、ナビ開後 `aria-expanded=true`。
- 写真: `/tmp/miharu-design-after/overview.png`, `tools.png`, `dark.png`, `mobile.png`, `mobile-nav.png`。追加のロゴ背景・ダークナビ調整は全画面QA担当が再撮影する。
- `PYTHONPATH=portal PORTAL_AUTH=none /workspace/ai-miharu-portal-venv/bin/pytest portal/tests/test_dads_css_routes.py -q`: **16 passed**。public primitive存在とfallback定義充足を含む。
- 全画面/テーマaxe、全操作、外部DS mountとの計算値比較は別途QA担当。支援技術未検証。これらの前に全移行完了を宣言しない。

## 実DS外部mountの追加比較

別プロセス `127.0.0.1:8094` を `DADS_CSS_DIR=/workspace/digital-design-system/tokens` で起動（原本コピーなし）。起動ログは `DADS tokens: mounted`。通常8091のbundledと同じデモにサインインして比較した。

- light/dark × body / aside / main / .view-head h2 / .wcard / input / nav button.nav-child × color / backgroundColor / borderColor / fontSize / lineHeight / padding / minHeight の計算値: **差分0**。
- 比較結果・CSS応答一覧: `artifacts/dads-mount-comparison.json`。
- 通常ページ読込のCSS要求は両構成ともすべて200。
- axe実行後のみ、bundledで `/dads.css`、mountedで `/dads.css`・`/brand.css`・`/semantic.css` の404を再現。ブラウザの正規CSS importは `/digital-design-system/tokens/` 基準で成功している。
- 原因のソース証拠: インストール済みaxe-coreの `axe.js:19913` 付近 `parseSameOriginStylesheet` が `CSSImportRule.href`（相対URL）を取得して `parse_crossorigin_stylesheet_default(importUrl, ...)` に渡す。親stylesheetのURLへの解決がここにないため、axeによる再取得が文書ルートを参照する。製品の通常CSSロード障害と区別する。
- この比較は7 selectorの代表値に限定する。全画面全プロパティの同一性証明ではない。比較専用プロセスは検証後停止し、利用者確認用8091は維持。
