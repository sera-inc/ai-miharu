# DADS 製品適用の管理者試験

**状態**: 2026-09-27、`deepseek-v4.1-flash:cloud` の出力を使い、製品ブランチに共通画面の色・面・文字・境界・フォーカスの暫定アダプターを実装した。DADS Phase 1 の 352 値の完全な対応、全画面の移行、アクセシビリティ承認は未完了。管理者から製品への即時適用が指示されたため、未承認の `--app-sg-*` 案を試験環境で先行利用している。

## 構成

- `portal/app/static/index.html` は既存 `enterprise.css` の後に、DADS `tokens/index.css` と `dads-product.css` を読み込む。既存 DOM・JavaScript・旧変数名を保ち、アダプター CSS が色と共通部品の見た目を変更する。
- `dads-product.css` の `--app-sg-*` はこの製品の試験候補。`digital-design-system` の Layer 1 `tokens/dads.css` や Layer 2 正典を変更していない。ダーク表示は維持する。
- CSS の URL は固定パスのみ。DADS の4ファイルは `DADS_CSS_DIR` の読み取り専用マウントから配信し、製品ソースと Docker image に private デザインシステムの原本・認証情報をコピーしない。
- ページと CSS は同じ `require_page_auth` 境界。管理モードではログインページも CSS を取得できる。表示用 CSS はブラウザへ公開されるが、API や利用者データは従来どおり `require_auth` で保護する。
- `DADS_CSS_DIR` が無い場合、DADS トークンと製品アダプターは 404 となり、既存の `enterprise.css` で表示する。CSS の 404 がコンソールに出るため、正式移行時は依存の配布と条件付き読み込みを整える。

## 試験起動

権限のある管理者が `sera-inc/digital-design-system` を別途 clone し、採用する Git commit を固定する。製品リポジトリ直下から:

```bash
DADS_TOKENS_DIR=/absolute/path/to/digital-design-system/tokens \
  docker compose -f demo/docker-compose.yml -f demo/docker-compose.dads.yml up -d --build
```

`demo/docker-compose.dads.yml` は読み取り専用 bind mount。ログイン後にライト・ダークの切替、概要、検出ソース、チャート、フォーム、モーダルを確認する。

## 現時点の検証と残件

- 固定 CSS ルート、未設定時の404、ページ認証境界をテスト。サンプルデータの管理モードで CSS 200、概要と検出ソースへの遷移、ライト・ダーク切替、表・棒グラフ切替を実画面で確認した。
- Python Portal 全テスト、Node の既存テストが通過した。これは全画面の視覚回帰・機能同等性・WCAG 合格を示すものではない。
- `docs/mapping.md` は 108 仮対応／208 保留／36 除外のまま。未解決を0と偽らない。生値が残る既存 CSS と他画面・拡張機能は段階移行が必要。
- デザインシステム側のドラフト PR #2 は、製品適用優先の指示で閉じた。Layer 2 の正式承認や配布方式の決定とは別の管理者試験である。

## AppShell モバイルナビの追加検証（2026-09-27）

- DeepSeek `deepseek-v4.1-flash:cloud` に DADS AppShell の要件と既存実装を渡し、焦点移動・フォーカス循環・Escape・開閉状態の修正を生成した。提案のハンバーガーボタンは DADS HTML 実装の SVG と視覚規則を `dads-product.css` に適応した。最初の提案はデスクトップでもボタンが表示されるため不採用とし、DeepSeek の修正版を適用した。
- 元の HTML コンポーネントは MIT。ライセンス全文を `licenses/dads-html-MIT.txt` に、由来を `NOTICE` に記録した。Layer 1 の原本は改変していない。製品の HTML・JavaScript 実装を維持する理由は `docs/deviations.md` に記録した。
- 390px のブラウザで、閉じたサイドバーが `inert`、開いた時の `aria-expanded=true` と焦点移動、Tab / Shift+Tab の循環、Escape で起動ボタンへ戻ること、メニューからのページ移動後に本文へ焦点が移ることを確認。1440px ではメニューボタンが隠れ、サイドバーが操作可能な状態へ戻ることを確認。画面幅による横はみ出しとブラウザコンソールのエラーは観測されなかった。
- Portal Python 700 件と Node 描画・アクティベーション 23 件は 2026-09-28 時点で通過。支援技術、axe、全画面のデザイン比較はまだ未完了。`DADS-VERSION` はこの管理者試験の参照値であり、Phase 5 完了やデザインシステムの正式承認を示さない。
