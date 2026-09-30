# mapping.md — 実装値 → トークン対応表

**対象**: リポジトリ直下（Layer 1 の生成物 `portal/app/static/dads/`、`tools/`、`docs/`、`.scratch/`、`node_modules` は除く）　**再インベントリ**: 2026-09-30　**生成**: デザインシステムの `scripts/inventory.mjs`（測定にだけ使用。原本は複製していない）
**ステータス**: DeepSeek 4.1 Flash による仮対応（**人間レビュー未承認**、Phase 1 未完了）
**現行の実装値**: 14 ファイル・**143 種・2,180 出現**（色 17 種 36 出現／フォントサイズ 37 種 511 出現／余白 47 種 1,379 出現／角丸 28 種 230 出現／z-index 14 種 24 出現）
**現行の内訳**: AI仮対応 31・保留 65・除外 36・**未判定 11**（計 143）。判定は 2026-09-27 の値単位の DeepSeek 出力を引き継いだもので、現行の出現箇所での再判定は行っていない。

> この表は設計書 §6 Phase 1 の中核資産です。設計書は人間による対応トークンの決定とレビュー承認を要求します。
> 今回は依頼者の 2026-09-27 の明示指示により、DeepSeek 4.1 Flash（`deepseek-v4.1-flash:cloud`）単独で仮判定しました。
> **人間承認を受けたものとして扱いません。** 「AI仮対応」は提案であり、承認・確定ではありません。
> **未解決（保留・未判定）が残るため、Phase 1 / Phase 2 は完了していません。** 未解決を 0 と表示しません。

## 数字の読み方（旧版 352 種との関係）

- **旧版（2026-09-27）**: 14 ファイル・**352 種・2,452 出現**。AI仮対応 108・保留 208・除外 36。全文は [mapping-baseline-2026-09-27.md](mapping-baseline-2026-09-27.md) に、判定を書き換えずに保存している。
- **現行（2026-09-30）**: 上記のとおり **143 種・2,180 出現**。差は次の 2 点による。
  1. **色は 226 種 → 17 種。** 2026-09-28 のコミット `35f9771`（管理者試験の先行適用）が、`enterprise.css` と `index.html` の生の色をアダプター `dads-product.css` の `--app-sg-*`（未承認の製品ローカル案）への参照へ置き換えた。旧版の色 226 種のうち 220 種は現行のコードに残っていない。残る色 17 種は、旧版に無かった 11 種（拡張機能のガード通知とデモページの色）と、旧版にもあった 6 種（白、HTML 文字参照の誤検出、Microsoft ロゴの4色）。
  2. **フォントサイズ・余白・角丸・z-index の 126 種は旧版と同じ値のまま全て残っている**（未置換。出現回数だけが変わる）。
- **同じ「143」が 2 つある点に注意。** 旧版の色のうち保留だった **143 値**（`dads-held-colors-layer2-assessment.json`）と、現行インベントリ全体の **143 種** は、たまたま同数であって別の集合。前者は 2026-09-27 の色だけの数、後者は 2026-09-30 の全カテゴリの数。
- 生の色が減ったことは、色の対応が正しいこと・承認されたことを意味しない。置換は試験環境での先行適用で、ライト・ダーク両テーマの目視確認と自動テストの通過までを確認している。全画面の視覚回帰・WCAG・支援技術の確認は未実施（`dads-runtime-mount.md`）。
- `CLAUDE.md` 移行規則 1 は「未解決値が残る間は CSS 値を推測で置換しない」。色の先行適用はこの規則に対する、依頼者の明示指示による例外であり、他の値（余白・フォントサイズ・角丸・z-index）には広げていない。

## 判定の出どころ

| 資料 | 内容 | 位置づけ |
|---|---|---|
| `mapping-baseline-2026-09-27.md` | 旧版 352 種の値単位の DeepSeek 判定 | 現行表の「引き継ぎ元」。書き換えない |
| `dads-held-colors-layer2-assessment.json` | 旧版の色のうち保留 143 値を、未承認の `--app-sg-*` 31 トークン案で再判定（35 値に候補、108 値は継続保留） | 提案。現行表の集計には反映していない |
| `dads-held-hex-occurrences.json` | 保留 HEX の使用箇所 138 件の判定 | 提案 |
| `dads-held-hex-dark-proposal-assessment.json` | 使用箇所 92 件を `--app-sg-*` 案で再判定（追加候補 60・保留 32） | 提案 |
| `dads-inventory-2026-09-30.md` | 今回の再インベントリの生出力（判定なし） | 測定値 |

いずれも DeepSeek の出力であり、人間による承認ではない。`--app-sg-*` は `dads-product.css` にある製品ローカルの Layer 2 拡張案で、デザインシステムの Layer 1・Layer 2 には反映していない（上流への PR も作成していない）。

## 再現手順

```bash
# 権限のある担当者が、デザインシステムのリポジトリ（private）を別に clone して実行する。測定にだけ使い、出力に原本の内容は含まれない。
rsync -a --exclude=.git --exclude=.scratch --exclude=tools --exclude=node_modules \
      --exclude=portal/app/static/dads --exclude=docs ./ /tmp/inv-target/
node /path/to/digital-design-system/scripts/inventory.mjs /tmp/inv-target --out /tmp/inventory.md
```

`portal/app/static/dads/`（Layer 1 の生成物）と `docs/` を除くのは、製品の実装値ではないため。除かずに測ると Layer 1 の全トークンが実装値として数えられる。

## 色

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `#b3b3b3` | 6 | — | 未判定 | `extension/demo/index.html` 他2件。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#1a1a1a` | 5 | — | 未判定 | `extension/demo/index.html` 他2件。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#ffffff` | 4 | --app-surface | AI仮対応 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: --sf はサーフェス色の定義で、白は基底 surface に相当する。--app-surface-raised も白だが、変数名と用途から generic な surface と判断。 |
| `#000000` | 3 | — | 未判定 | `extension/demo/index.html` 他2件。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#10003` | 3 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: HTMLエンティティ &#10003; の一部として抽出されたもので、CSS色ではないため。 |
| `#333333` | 2 | — | 未判定 | `extension/demo/index.html`。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#ffbbbb` | 2 | — | 未判定 | `extension/src/guard.js` 他1件。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#ffd43d` | 2 | — | 未判定 | `extension/src/guard.js` 他1件。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#00a4ef` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `#4d4d4d` | 1 | — | 未判定 | `extension/demo/index.html`。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#7f7f7f` | 1 | — | 未判定 | `extension/demo/index.html`。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#7fba00` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `#cccccc` | 1 | — | 未判定 | `extension/demo/index.html`。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#f25022` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `#f9f9f9` | 1 | — | 未判定 | `extension/demo/index.html`。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#ff8d44` | 1 | — | 未判定 | `extension/demo/index.html`。2026-09-27 のインベントリに無かった値で、DeepSeek は未判定。 |
| `#ffb900` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |

## フォントサイズ

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `12px` | 80 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 12px は --app-text-body-sm-size と --app-text-label-size の両方に一致し、ソース文脈もテーブル本文・ナビ・メタラベル・フォーム部品など複数用途にまたがるため一意に決められない。 |
| `10px` | 71 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 10px に一致する候補トークンがない。近い 0.75rem（12px）等へ意味を変えて寄せることもできない。 |
| `11px` | 59 | --app-text-label-size | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: .card-section の font-size:11px は大文字化された小さなラベル見出しであり、ラベル用途と判断できる。値は 11px だが DADS のラベルサイズ (0.75rem=12px) に寄せる。 |
| `13px` | 41 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 13px に一致する候補トークンがない。本文・見出し・強調など用途も混在し、14px や 12px への近似置換は不適切。 |
| `11.5px` | 36 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 11.5px に一致する候補トークンがない。テーブル本文や補足に使われるが 0.75rem（12px）や table-size（14px）とは一致しない。 |
| `12.5px` | 30 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 12.5px に一致する候補トークンがない。ナビ・本文・見出し補助など用途が広く、12px トークンへの近似は不適切。 |
| `10.5px` | 27 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 10.5px に一致する候補トークンがない。メタ情報や補足本文用だが、0.75rem（12px）等とは値が異なる。 |
| `9px` | 27 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 9px に一致する候補トークンがない。小型ラベルやメタ情報用だが、該当サイズのトークンが候補にない。 |
| `9.5px` | 23 | --app-text-label-size | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: nav .count のバッジ、.ag-node b の大文字ラベルはいずれも小さな UI ラベル/バッジ用途。DADS の最小ラベルサイズ (0.75rem=12px) に寄せる。 |
| `8.5px` | 19 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 8.5px に一致する候補トークンがない。極小ラベルや補足用だが、候補に該当サイズがない。 |
| `22px` | 10 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 22px に一致する候補トークンがない。見出しと数値表示にまたがり、20px/24px/32px の候補へ近似で寄せるのは不適切。 |
| `8px` | 10 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 8px に一致する候補トークンがない。大文字ラベルやキャプション用だが、候補に該当サイズがない。 |
| `13.5px` | 7 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: table、本文パラグラフ、タブ、注記など複数用途で使われ、table-sizeとbody-sizeの両方が考えられ一意に決められないため。 |
| `14px` | 7 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: h3見出し、strong、summaryなど複数用途で使われ、body-size・heading-sm-size・label-sizeのどれに一意対応するか決められないため。 |
| `15px` | 6 | --app-text-heading-sm-size | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: すべてh3/h4の小見出しで用途が一致しており、候補では小見出し用トークンが対応するため。 |
| `16px` | 6 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: h2/h4見出し、数値・強調値、アイコン用フォントサイズが混在し、heading-sm-sizeやnumeric-sizeに一意対応しないため。 |
| `17px` | 5 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 数値・強調値とアイコン用フォントサイズが混在し、numeric-sizeなど候補トークンに一意対応しないため。 |
| `19px` | 5 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: chevronアイコン、見出し、数値・金額が混在し、heading-sizeやnumeric-sizeに一意対応しないため。 |
| `20px` | 4 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 出現箇所はいずれもmin-width、box-shadow、paddingで、フォントサイズ指定ではないため。 |
| `26px` | 4 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: KPI/statsの数値とh2見出しが混在し、heading-lg-sizeやdisplay-sm-sizeに一意対応しないため。 |
| `0.92em` | 3 | 保留 | 保留 | `extension/demo/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: .muted、table、codeで用途が混在し、相対em指定で候補の固定トークンに一意対応しないため。 |
| `18px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: padding、height、box-shadow などの寸法として使われており、font-size 指定ではないため除外。 |
| `21px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 出現箇所はいずれもmarginやpaddingで、フォントサイズ指定ではないため。 |
| `24px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: box-shadow、padding、gap の寸法として使われており、font-size 指定ではないためフォントサイズ抽出の誤検知として除外。 |
| `28px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: box-shadow、padding、width/height の寸法として使われており、font-size 指定ではないため除外。 |
| `30px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 430pxや130pxの一部としての誤検出で、独立したフォントサイズ指定ではないため。 |
| `7.5px` | 3 | --app-text-label-size | AI仮対応 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: すべて小さなラベル／テーブルヘッダのラベル用途で一致しており、label-sizeが対応するため。 |
| `0.85em` | 2 | 保留 | 保留 | `extension/demo/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: ボタンとコード/等幅表示の両方で使われており用途が異なる。また0.85emは候補トークンのどのサイズとも一致せず、一意に決められない。 |
| `25px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 見出し(h2)と統計値(dt)で使われ用途が異なる。統計値には25pxに対応する候補トークンがなく、一意に決められない。 |
| `27px` | 2 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: flex-basis、min-height の寸法として使われており、font-size 指定ではないため除外。 |
| `.9em` | 1 | --app-text-numeric-size | AI仮対応 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: codeや.monoの等幅表示で、等幅用のnumericサイズ（14px monospace）に対応する。.9em（約14.4px）も近い。 |
| `1.05em` | 1 | --app-text-heading-sm-size | AI仮対応 | `extension/demo/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: h2の見出しで、h1より小さい見出し。1.05em（約16.8px）は18pxの小見出しトークンに最も近く、役割も一致する。 |
| `1.4em` | 1 | --app-text-heading-lg-size | AI仮対応 | `extension/demo/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: h1の見出しで、見出し大サイズに相当する。1.4em（約22.4px）は24pxの見出し大トークンに最も近く、役割も一致する。 |
| `14.5px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: CSSのfont-sizeとして使われている有効な値だが、候補トークンには14.5pxに対応する値がなく、近い14px系トークンへ置き換えると意味・見た目が変わる可能性があるため。 |
| `15.5px` | 1 | --app-text-heading-sm-size | AI仮対応 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: カード名でfont-weight:650の見出し的テキスト。DADSの小見出し（18B）に対応し、太字用途も一致する。 |
| `29px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: width、height、flex-basis の寸法として使われており、font-size 指定ではないため除外。 |
| `32px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: width/height、margin、または 232px の部分一致として現れており、font-size 指定ではないため除外。 |

## 余白

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `10px` | 138 | 保留 | 保留 | `extension/demo/index.html` 他4件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに10px相当がなく、近い8px/16pxへ置換すると余白寸法が変わるため保留。 |
| `8px` | 115 | --app-space-2 | AI仮対応 | `extension/demo/index.html` 他4件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 8px は DADS の spacing-2 に一致し、提示文脈の厳密な 8px は gap/padding/top/bottom などの余白用途に使われているため。 |
| `12px` | 114 | 保留 | 保留 | `extension/demo/index.html` 他4件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに12px相当がなく、近い8px/16pxとは値が異なるため保留。 |
| `14px` | 109 | 保留 | 保留 | `extension/demo/index.html` 他4件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに14px相当がなく、近い16pxとは値が異なるため保留。 |
| `6px` | 106 | 保留 | 保留 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに6px相当がなく、4px/8pxとは値が異なるため保留。 |
| `16px` | 85 | --app-space-2 | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークン --app-space-2 が16pxと一致し、padding/gap等の余白用途で使われているため。 |
| `4px` | 74 | --app-space-05 | AI仮対応 | `extension/src/guard.js` 他3件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークン --app-space-05 が4pxと一致し、margin/padding等の余白用途で使われているため。 |
| `2px` | 68 | 保留 | 保留 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに2px相当がなく、0px/4pxとは値が異なるため保留。 |
| `20px` | 60 | 保留 | 保留 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに20px相当がなく、16px/24pxとは値が異なるため保留。 |
| `5px` | 59 | 保留 | 保留 | `extension/src/guard.js` 他3件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに5px相当がなく、4px/8pxとは値が異なるため保留。 |
| `7px` | 55 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに7px相当がなく、8pxとは値が異なるため保留。 |
| `9px` | 55 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに9px相当がなく、8px/16pxとは値が異なるため保留。 |
| `18px` | 51 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: DADSの余白トークンに18pxは存在せず、近い16px/24pxとは値も意味も異なるため。 |
| `11px` | 42 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに11pxがなく、8px/16pxなどへ置換すると値が変わるため。 |
| `17px` | 42 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに17pxがなく、16pxでは値も用途が異なるため。 |
| `15px` | 32 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに15pxがなく、16pxとは値も意味も一致しないため。 |
| `3px` | 32 | 保留 | 保留 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに3pxがなく、4pxや0pxとは異なる値のため。 |
| `13px` | 26 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに13pxがなく、8px/16pxでは置換できないため。 |
| `1px` | 23 | 保留 | 保留 | `portal/app/static/dads-product.css` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに1pxがなく、0pxとは異なる余白値のため。 |
| `22px` | 16 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに22pxがなく、24pxとは値も用途も異なるため。 |
| `24px` | 12 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: --app-space-3と--app-gutterの両方が24pxで、ソースではgap/グリッド間隔とpadding/marginに混在し用途が一意に決められないため。 |
| `19px` | 10 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに19pxがなく、16px/24pxでは値が異なるため。 |
| `21px` | 6 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークンに21pxがなく、24pxとは値も意味も一致しないため。 |
| `45px` | 6 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: max-width:145pxの部分文字列として抽出された誤検知であり、box-shadowのぼかし値でもあるため余白値ではない。 |
| `26px` | 4 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 26px に対応する値がないため。 |
| `28px` | 4 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 28px に対応する値がないため。 |
| `32px` | 4 | --app-space-4 | AI仮対応 | `extension/demo/index.html` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークン --app-space-4 が 32px に対応し、gap・padding-left・margin などの余白用途で使われているため。 |
| `30px` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 30px に対応する値がないため。 |
| `38px` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 38px に対応する値がないため。 |
| `23px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 23px に対応する値がないため。 |
| `25px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 25px に対応する値がないため。 |
| `35px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 35px に対応する値がないため。 |
| `4.5px` | 2 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補の --app-space-05 は 4px であり 4.5px とは一致しないため。 |
| `40px` | 2 | --app-space-5 | AI仮対応 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークン --app-space-5 が 40px に対応し、padding などの余白用途で使われているため。 |
| `55px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 余白として使われているが、候補トークンに 55px に対応する値がないため。 |
| `64px` | 2 | --app-space-8 | AI仮対応 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 候補トークン --app-space-8 が 64px に対応し、padding・margin などの余白用途で使われているため。 |
| `1.5px` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: font-size:11.5px の一部を誤抽出したもので、独立した余白値ではないため。 |
| `1.6em` | 1 | 保留 | 保留 | `extension/demo/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: margin-top の余白値だが、em は要素のフォントサイズに依存する相対値であり、候補の px 固定 spacing トークンと同一意味にならないため。 |
| `223px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: padding-left の余白値だが、候補に 223px がなく、任意のレイアウト値として spacing トークンへ一意に対応できないため。 |
| `27px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: flex-basis と min-height の寸法指定で、余白カテゴリの値ではないため。 |
| `36px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: height/min-height の寸法指定で、余白カテゴリの値ではないため。 |
| `44px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: padding-top の余白値だが、候補に 44px がなく、40px や 48px への近似置換はできないため。 |
| `48px` | 1 | --app-space-6 | AI仮対応 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: main の padding-bottom 48px は DADS spacing-6 (48px) に対応する余白値のため。 |
| `50px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: box-shadow の blur radius で、余白ではないため。 |
| `56px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: padding-bottom の余白値だが、候補に 56px がなく、48px や 64px とは値も意味も一致しないため。 |
| `58px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: margin-left の余白値だが、候補トークンの 4/8/16/24/32/40/48/64px のいずれにも一致せず、近い値への置換も意味が異なるため。 |
| `60px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: padding-bottom の余白値だが、候補に 60px がなく、64px とは値が異なるため。 |

## 角丸

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `8px` | 26 | --app-radius-md | AI仮対応 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 8px は角丸の基本スケールで、--app-radius-md（DADS radius-8）に対応。ソース上でも border-radius:8px の用途がある。 |
| `12px` | 22 | --app-radius-lg | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: dialog の border-radius:12px など角丸に使用され、--app-radius-lg（DADS radius-12）に対応。 |
| `7px` | 20 | --app-radius-sm | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: ナビボタン、アバター、チップ、小アイコンボタン、ツールチップなど小〜中規模の部品で使われており、小さい角丸トークン --app-radius-sm（DADS 6px）の用途階層に対応するため。 |
| `10px` | 19 | --app-radius-lg | AI仮対応 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: カード、設定パネル、ドロップ領域、メニューなど大きめの面・パネルで使われており、大きい角丸トークン --app-radius-lg（DADS 12px）の用途階層に対応するため。 |
| `4px` | 19 | --app-radius-xs | AI仮対応 | `extension/demo/index.html` 他4件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius:4px として使用され、--app-radius-xs（DADS radius-4）に対応。 |
| `6px` | 19 | --app-radius-sm | AI仮対応 | `extension/src/guard.js` 他3件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius:6px として使用され、--app-radius-sm（DADS radius-6）に対応。 |
| `9px` | 15 | --app-radius-md | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: タブ、セットバー、検索結果、ノート、統計カードなど中規模の容器で使われており、中角丸トークン --app-radius-md（DADS 8px）の用途階層に対応するため。 |
| `50%` | 14 | --app-radius-full | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius:50% は円形・完全な角丸の用途で、--app-radius-full に対応。 |
| `99px` | 13 | --app-radius-full | AI仮対応 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius:99px はピル形状・完全な角丸の用途で、--app-radius-full に対応。 |
| `0` | 10 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: ソース文脈が著作権表記の「2026」等であり、角丸の CSS 値として抽出された誤検知。 |
| `3px` | 9 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: ソース文脈では margin/padding/box-shadow などの値で、border-radius:3px の使用が確認できず、角丸カテゴリの抽出誤検知。 |
| `5px` | 9 | --app-radius-xs | AI仮対応 | `extension/demo/index.html` 他2件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 入力欄、ボタン、ピル、テーブル、小さいトラックなど小さい操作要素で使われており、最小角丸トークン --app-radius-xs（DADS 4px）の用途階層に対応するため。 |
| `var(--app-radius-md)` | 7 | 除外 | 除外 | `portal/app/static/dads-product.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: `portal/app/static/dads-product.css`。公式インベントリが CSS カスタムプロパティ参照を生値と誤検出。値は既存トークンを参照している。 |
| `2px` | 6 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: margin/padding/width/shadow/outline 内の値や 12px などの部分一致で、border-radius 値として使われていないため。 |
| `var(--radius-sm)` | 4 | --app-radius-sm | AI仮対応 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius に既存の small 用変数が使われており、候補の --app-radius-sm に対応する。 |
| `11px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: gap/font-size/margin の値で、border-radius 値として使われていないため。 |
| `var(--app-radius-sm)` | 3 | 除外 | 除外 | `portal/app/static/dads-product.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: `portal/app/static/dads-product.css` 他1件。公式インベントリが CSS カスタムプロパティ参照を生値と誤検出。値は既存トークンを参照している。 |
| `0 0 10px 10px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 下左右のみ10pxの非一様な角丸指定で、候補トークン（4/6/8/12px/full）に一致する値がなく、近い値に置換すると意味が変わるため。 |
| `0 0 7px 7px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 下左右のみ7pxの非一様な角丸指定で、候補トークンに7px相当がなく、近い値に置換すると意味が変わるため。 |
| `0!important` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: !importantを除くと0は有効なborder-radius値だが、候補トークンに0相当がなく、一意に対応できないため。 |
| `14px!important` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: !importantを除いても14pxは候補トークンに存在せず、近い--app-radius-lg等に置換すると値が異なるため。 |
| `1px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border/outline の太さやコメント中の 1px で、border-radius 値として使われていないため。 |
| `2px 4px 4px 2px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius の4値指定で角ごとに異なる非対称な角丸であり、候補トークンは単一の角丸スケールのみです。単一トークンに置き換えると意味が変わるため対応不可です。 |
| `4px 4px 0 0` | 1 | --app-radius-xs | AI仮対応 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 上角のみ 4px の角丸で、4px は --app-radius-xs（dads-radius-4）に対応する。 |
| `999px` | 1 | --app-radius-full | AI仮対応 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: ピル状の完全な角丸で、--app-radius-full（dads-radius-full）に対応する。 |
| `inherit` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: border-radius:inheritはCSS値だが、継承元の半径値が不明で候補トークンに一意に対応できないため。 |
| `var(--app-radius-sm) var(--app-radius-sm` | 1 | 除外 | 除外 | `portal/app/static/dads-product.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: `portal/app/static/dads-product.css`。公式インベントリの40文字切り取りで shorthand が途中まで抽出された誤検出。 |
| `var(--radius)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 既存カスタムプロパティ参照であり、解決後の半径値がソース文脈から特定できず、候補トークンに一意に対応できないため。 |

## z-index

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `1` | 5 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: ソース文脈に z-index:1 が確認できず、v1.1.0 や -1、initial-scale=1 など非 z-index の数値・コード内出現のみ。抽出誤検知と判断。 |
| `60` | 4 | --app-z-popover | AI仮対応 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: #navtip の z-index:60 として使用され、ツールチップ/ポップオーバーの用途。候補トークンの --app-z-popover に対応。 |
| `2` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 著作権年 2026 や SVG の points 値などに含まれる数値で、z-index としての使用が確認できない。抽出誤検知。 |
| `2147483647` | 2 | --app-z-toast | AI仮対応 | `extension/src/guard.js` 他1件。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: guard.js の固定通知（position:fixed; top:16px; right:16px; z-index:2147483647）で最大値を使用。トースト/通知の用途なので --app-z-toast に対応。 |
| `19` | 1 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: .posture-mark の z-index:19 として使用されているが、装飾マーク用途に合う候補トークンがなく一意に決められない。 |
| `20` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 著作権年 2026 に含まれる数値で、z-index:20 は確認できない。抽出誤検知。 |
| `3` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: カテゴリは z-index だが、文脈では margin-top:3px や色値・JS コメント内の数字などであり、z-index 宣言ではない抽出誤検知と判断できるため。 |
| `4` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: box-shadow の 0 4px 14px などに出現し、z-index:4 は確認できない。抽出誤検知。 |
| `40` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: minmax(400px,1fr) や SVG パス座標などに出現し、z-index:40 は確認できない。抽出誤検知。 |
| `5` | 1 | 除外 | 除外 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: URL の AmanSK5 や行番号などに出現し、z-index:5 は確認できない。抽出誤検知。 |
| `70` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: box-shadow の 70px や 70% などに出現し、z-index:70 は確認できない。抽出誤検知。 |
| `75` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: #setupbell .bcount の z-index:75（バッジ）と推測されるが、バッジ用途に合う候補トークンがなく一意に決められない。 |
| `90` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: 90deg や right:-90px、rotate(-90deg) など角度・位置指定として出現し、z-index:90 は確認できない。抽出誤検知。 |
| `9000` | 1 | 保留 | 保留 | `portal/app/static/index.html`。2026-09-27 の DeepSeek 判定（現行の出現箇所での再判定は未実施）: #tour の固定全画面オーバーレイ用 z-index であり、候補の modal/popover/toast とは用途が異なる。9000 に対応する専用の z-index トークンが候補にないため。 |

---

検査ファイル数: 14 / 抽出値: 143 種・2,180 出現（AI仮対応 31、保留 65、除外 36、未判定 11）
