# CLAUDE.md — AIミハル 移行

このリポジトリは `sera-inc/digital-design-system`（DADS v2.17.1 基盤）への段階移行中。現在は **Phase 1**。正典はデザインシステムの `docs/01_SaaS向けデザインシステム拡張_設計書.md` §6 と `docs/03_移行手順チェックリスト.md`。

## 移行の必須規則

1. 原則では `docs/mapping.md` の「対応トークン」列を人間が決定・承認する。今回の管理者試験は依頼者の 2026-09-27 の明示指示により **DeepSeek 4.1 Flash がマッピングする例外**とし、モデル・根拠・未解決値を記録する。標準手順の人間レビューを通過したとは記載しない。未解決値が残る間は CSS 値を推測で置換しない。初回抽出は 349 種（2026-09-30 の再インベントリは 143 種・2,180 出現。`docs/mapping.md`）。
2. デザインシステムの Layer 1（`vendor/dads/` と `--dads-*`）は改変しない。スタイルの判断根拠は `tokens/semantic.css` と `vendor/dads/docs/` に置く。
3. Phase 2 は承認済みマッピングに従い、既存 CSS 変数の参照先だけを変更する。機能テストと主要画面の視覚比較を通す。
4. Phase 3 は **1 PR = 1 コンポーネント**。Button、Input、Select、Checkbox/Radio、Textarea の順に進め、各 PR で既存テストを通す。
5. Phase 4 の自前実装には `docs/deviations.md` に理由を記録する。Phase 5 は axe、キーボード、支援技術の確認を行う。`outline: none` を追加しない。
6. Apache-2.0 の `LICENSE` と `NOTICE`、元著作者表示を保持する。元プロジェクトによる支持を示唆しない。

## Worker での現行テスト

リポジトリ直下から実行する。Python の依存は CI と同じロックファイルから親ディレクトリの `.venv` に導入済み。

```bash
PYTHONPATH=portal PORTAL_AUTH=none ../.venv/bin/pytest portal/ -q
(cd receiver && PYTHONPATH=. ../../.venv/bin/pytest tests -q)
node --test portal/tests/*.test.cjs
(cd tools/dads && npm ci && npm run check)   # 同梱の DADS トークンが公開パッケージの生成結果と一致するか
```

変更後はテスト結果を記録し、サンプルデータ入りデモの主要画面をブラウザで確認する。

## 2026-09-27 管理者試験の例外（2026-09-30 更新）

管理者の明示指示で、Phase 1 の保留解消前に DeepSeek の `dads-product.css`（`--app-sg-*`）を製品に適用した。**標準の起動でこの見た目になる。**
DADS の Layer 1 は、公開パッケージ `@digital-go-jp/tailwind-theme-plugin` 1.0.1（MIT）から `tools/dads` で生成して `portal/app/static/dads/` に同梱している。private のデザインシステムの内容は製品にもイメージにも入れない。
`DADS_CSS_DIR`（`deploy/compose/docker-compose.dads-mount.yml`、`demo/docker-compose.dads.yml`）は、組織が自前の**完全な**トークンで置き換えるための任意のマウントで、不完全なら警告して同梱分を使う。
これは全画面移行・標準レビュー承認・Layer 2 正式採用ではない。デザインシステム側の配布方式（U-03）は未決で、この製品は決めない。続きは、製品 UI の機能と視覚差分の検証（支援技術、全画面の視覚回帰）と、保留・未判定の値の人間レビュー。
詳細は `docs/dads-runtime-mount.md`、対応表は `docs/mapping.md`、逸脱は `docs/deviations.md`。
