# DADS 製品適用の管理者試験（実行時の構成・検証・限界）

**状態**: 2026-09-30 更新。依頼者（管理者）の明示指示による**管理者試験**で、次のいずれでもない。
デザインシステムの正式な採用、Layer 2 の承認、全画面の移行、アクセシビリティの承認、標準手順の人間レビューの通過。
DeepSeek の仮対応（`mapping.md`）は提案であり、人間の承認は記録されていない。デザインシステムの配布方式（設計書の未決事項 U-03）は決まっておらず、この製品はそれを決めない。
デザインシステム側への PR は作成していない（ドラフト PR #2 は 2026-09-27 に閉じた）。

## 何がどう動くか

- **標準の起動で DADS の見た目になる。** クローンして `docker compose up -d --build` するだけでよく、デザインシステムのクローン、マウント、認証情報は要らない。
  以前は private のトークンをマウントしない限り従来の見た目に戻る構成だったが、公開トークンを同梱したため、通常の起動でも同じ見た目になる。
- `portal/app/static/index.html` は、`enterprise.css` の後に `/digital-design-system/tokens/index.css`（Layer 1）と `/dads-product.css`（製品アダプター）を読み込む。既存の DOM・JavaScript・旧変数名は保ち、
  アダプターが色・面・文字・境界・フォーカスなどの見た目を変える。ダーク表示は維持している。

### 同梱の Layer 1（`portal/app/static/dads/`）

- 中身は `index.css` と `dads.css`。`tools/dads/build-dads-tokens.mjs` が、公開パッケージ
  [`@digital-go-jp/tailwind-theme-plugin`](https://github.com/digital-go-jp/tailwind-theme-plugin) **1.0.1**（デジタル庁、MIT ライセンス）の `dist/v4.css` から**機械的に生成**する。
  全値を `--dads-` 接頭辞のまま複製し、手では何も足さない（spacing とブレークポイントだけは DADS Foundation の定義値で補う）。**Layer 1 は改変しない。**
- 再生成と差分検査: `cd tools/dads && npm ci && npm run build`、検査は `npm run check`（同梱のファイルが生成結果と異なると失敗する）。パッケージのバージョンは `package.json` と `package-lock.json` で固定している。
- **private の `sera-inc/digital-design-system` の内容は、リポジトリにもイメージにも入れていない。** 同梱の `dads.css`（231 個の `--dads-*` 宣言）は、
  デザインシステムが自身の `tokens/dads.css` として持つファイルと、変数名・値がすべて一致することを 2026-09-30 に照合した（読み取りのみ。どちらの生成元も同じ公開パッケージ 1.0.1）。
- ライセンス全文は `licenses/dads-tailwind-theme-plugin-MIT.txt`、由来の表示は `NOTICE`。デジタル庁が提供・推奨するものではない。
- 同梱しないもの: デザインシステム側の Layer 2（`brand.css`、`semantic.css`）。そのため `/digital-design-system/tokens/brand.css` と `semantic.css` の 2 つのルートは、外部マウントがない限り 404 になる（ページはこの 2 つを読み込まない）。

### 製品アダプター（`portal/app/static/dads-product.css`）

- `--app-sg-*` は**この製品ローカルの Layer 2 拡張案**（未承認）。デザインシステムの Layer 2 の正典は変更していない。
- デザインシステムの Layer 2（`--app-*`）が外部にない標準構成でも同じ見た目になるよう、同名の代替値を `@layer sera-standalone-fallback` に持つ。外部の Layer 2 を読み込んだ環境では、
  レイヤーに入れていない外部の宣言が優先される。代替値がすべて Layer 1 の値を参照していること、アダプターが使う `--dads-*` の名前が同梱トークンにすべてあることは、テスト（`test_dads_css_routes.py`）で検査している。

### 任意: 組織のトークンディレクトリで置き換える

組織が自前の DADS トークン（例: private のデザインシステムの `tokens/`）を持つ場合だけ、読み取り専用でマウントして同梱分と置き換えられる。

```bash
cd deploy/compose   # デモは demo/ で -f demo/docker-compose.dads.yml
DADS_TOKENS_DIR=/absolute/path/to/tokens \
  docker compose -f docker-compose.yml -f docker-compose.dads-mount.yml up -d
```

- `index.css`、`dads.css`、`brand.css`、`semantic.css` の**4 ファイルすべて**が要る。1 つでも欠けるディレクトリは使わず、警告を出して同梱分を使う（半分だけ当たった見た目にならないようにするため）。
- ポータルは起動時に、どちらを使っているかをログに出す: `DADS tokens: bundled` または `DADS tokens: mounted`。不完全なマウントは `DADS_CSS_DIR=... is incomplete (missing: ...)` の警告が出る。
  システム状態画面の「デザイントークン」にも「同梱」または「外部マウント」と表示する。**「DADS になっている」と黙って主張しない。**
- private のデザインシステムを使う場合は、権限のある管理者が別に取得し、採用するコミットを固定する。製品のリポジトリ・イメージにはコピーしない。

### 認証の境界

ページと CSS は同じ `require_page_auth` の境界。管理モードではログインページも CSS を取得できる。CSS は表示用で、端末やツールなどのデータは含まない。API と利用者のデータは従来どおり `require_auth` で保護している。
CSS、アイコン、ロゴは名前付きの固定ルートで配信し、呼び出し側が与えたパスは解決しない。

## 通常のクローンでの確認

| 確認 | 結果（2026-09-30） |
|---|---|
| `demo/`（`docker compose up -d --build`）で起動し、ポータルのログを見る | `DADS tokens: bundled` |
| `deploy/compose/`（最小構成、`PORTAL_PORT=18091`）で起動し、ページと CSS を取得 | ページ・`/digital-design-system/tokens/index.css`・`dads.css`・`/dads-product.css`・ファビコン・ロゴがすべて 200 |
| システム状態画面 | 「デザイントークン: 同梱（デジタル庁デザインシステムの公開トークン）」 |
| `tools/dads` で `npm ci && npm run check` | `dads tokens are current (plugin v1.0.1, 215 variables, 55 text styles)` |
| `docker compose config`（デモ、最小構成、マウント用の重ね合わせ） | いずれも有効。既定のイメージはこのチェックアウトからビルドされる（`sera-ai-governance/*:local`） |

## 検証した範囲

- **自動テスト**: ポータル（Python）730 件、受信サービス 373 件、ブラウザー側のロジック（Node）31 件が通る。CSS ルート、同梱トークンの完全性、アダプターの参照、日本語表記、ブランド素材のルートを含む。
- **実ブラウザー（Chromium、サンプルデータの管理モード）**: 18 画面とウィザード、システム状態を、幅 1920・1440・1024・768・390px、ライト・ダークで開き、横はみ出しとコンソール・ネットワークのエラーがないことを確認した。
  サインイン画面もライト・ダークで確認した。
- **axe-core 4.13.0**（WCAG 2.0・2.1・2.2 の A・AA と best-practice のルール）: 20 画面 × ライト・ダークの 40 通りで、初回は 8 ルール（空の表見出し、名前のないセレクト、ランドマーク外の内容、見出しレベル、
  コントラスト、`dl` の構造、目標サイズ、見出し 1 の欠如）に違反があった。原因の修正後の再検査では**違反 0**。修正: 表示用トークンの取り違え（暗い面用の文字色を明るいカードに使っていた）、透過で薄めていた文字色、
  `dl` 内の注記、操作列の見出し、貼り付けガードモードのラベル、検索・バナーのランドマーク、ページ見出し、フッターのリンクの大きさ。
- **キーボード**: 概要画面で Tab を 60 回押し、59 個の停止位置すべてに、計算上の枠線または影による焦点表示があることを確認した。今回の変更で `outline: none` は追加していない。
  モバイルのナビ（`AppShell`）の焦点移動と循環は 2026-09-27 に確認した（下記）。

## 未実施・限界（完了と主張しない）

- 支援技術（VoiceOver・NVDA など）での確認、強制カラー（ハイコントラスト）表示、200%・400% 拡大時のリフロー、色覚シミュレーション、実機のタッチ操作。**axe は自動検査であり、WCAG への適合を保証しない。**
- ホバー・押下・無効などの全状態のコントラスト、全画面の視覚回帰（デザインシステムのコンポーネントとの比較）、デザインシステムの UI チェックリストの通しでの確認。
- `mapping.md` は、生の値 143 種・2,180 出現のうち AI 仮対応 31・保留 65・除外 36・未判定 11。**保留と未判定が残るため Phase 1 は完了していない。** 色は `--app-sg-*` への置換を先行適用したが、
  余白・フォントサイズ・角丸・z-index の 126 種は未置換。
- 拡張機能（`extension/src/guard.js` の通知）とそのデモページは、ポータルとは別の暗い見た目で、DADS 化していない。
- デザインシステムのコンポーネント（React）への置き換えはしていない。製品は単一の HTML と JavaScript のままで、理由は `deviations.md` に記録した。
- 同梱の Layer 1 は、公開パッケージ 1.0.1 に固定している。上げるときは `npm run build` の差分を人間がレビューする。

## AppShell モバイルナビの追加検証（2026-09-27）

- DeepSeek `deepseek-v4.1-flash:cloud` に DADS AppShell の要件と既存実装を渡し、焦点移動・フォーカス循環・Escape・開閉状態の修正を生成した。提案のハンバーガーボタンは DADS HTML 実装の SVG と視覚規則を `dads-product.css` に適応した。
  最初の提案はデスクトップでもボタンが表示されるため不採用とし、DeepSeek の修正版を適用した。
- 元の HTML コンポーネントは MIT。ライセンス全文を `licenses/dads-html-MIT.txt` に、由来を `NOTICE` に記録した。Layer 1 の原本は改変していない。製品の HTML・JavaScript 実装を維持する理由は `deviations.md` に記録した。
- 390px のブラウザーで、閉じたサイドバーが `inert`、開いた時の `aria-expanded=true` と焦点移動、Tab / Shift+Tab の循環、Escape で起動ボタンへ戻ること、メニューからのページ移動後に本文へ焦点が移ることを確認した。
  1440px ではメニューボタンが隠れ、サイドバーが操作可能な状態へ戻ることを確認した。画面幅による横はみ出しとブラウザーのコンソールエラーは観測されなかった。
