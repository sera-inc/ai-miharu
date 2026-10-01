# 承認E: 重なり順とフォーカスの適用記録

ユーザー承認: 固定バー・ドロワー・モーダル・ポップアップの順序を統一する（2026-10-01、親伝達）。実DS `6051bce` のsemantic役割を参照。共通DS原本や新しい認証設定は変更しない。

| 対象 | 適用 | 動作上の扱い |
|---|---|---|
| `.topbar`, `.setbar` | `--app-z-sticky` = 100 | 上部バーと下部保存バー。包含する検索結果は親stacking context内 |
| `.overlay` | `calc(var(--app-z-drawer) - 1)` = 199 | 詳細drawerより下、固定バーより上 |
| `.drawer`, mobile `aside` | `--app-z-drawer` = 200 | mobile navと詳細drawerを同時に開かない |
| `#tour` | `--app-z-modal` = 300 | 開始時に既存drawer/nav/popoverを閉じる。native dialogのtop layerはブラウザー標準を維持 |
| 検索、navflyout、navtip、usermenu、setuppanel、chart tooltip | `--app-z-popover` = 400 | 一時表示。詳細drawerまたはtour開始時に閉じ、背景のpopupが前に残ることを防ぐ |
| 図表・編集領域の局所1〜4 | 保持 | global roleへ機械昇格させない |
| 注入ガード最大z、skip link | 保持 | Fの外部ページ境界と、キーボードで本文へ移る既存優先度を維持 |

詳細drawerは閉じた状態でinert/aria-hidden、開いた状態でdialogとして認識できるようにした。開くと閉じるボタンへフォーカスし、背景shellをinertにする。Tab/Shift+Tabをdrawer内で循環させ、Escapeまたは閉じる操作で背景のinertを解除し、元の操作要素が残っていればフォーカスを戻す。画面遷移/サインアウトによるdrawer解除も同期する。

これらは単にz値を変更して終わらせず、相互表示・キーボード操作を維持するための変更。最終実測は承認後QA資料に記録する。値を変えたことだけを操作性の合格とは扱わない。
