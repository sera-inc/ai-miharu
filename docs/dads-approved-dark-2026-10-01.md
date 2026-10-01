# 承認C: 暗色役割の整理とコントラスト測定（2026-10-01）

ユーザー承認「暗色表示：役割ごとに色を整理し、文字のコントラストを検証」の範囲を適用。共有DS原本・Layer 1・配布方式・資格情報は変更しない。製品ローカルLayer 2拡張として扱い、共有DSに既に暗色定義があるとは主張しない。A/B/D/Eの文字・余白・角丸・重なりは別担当。ガード最大z-index 2147483647は変更しない。

## 参照と変更

実際の `sera-inc/digital-design-system` commit `6051bceb67c60fb805b757c22bbd66f3318ea980` の `tokens/semantic.css`（面・境界・テキスト・意味色を用途で分離）と `vendor/dads/docs/foundations/color/index.md`（文字4.5:1、非文字3:1）を読んだ。公開DADS値は同梱 `portal/app/static/dads/dads.css` と照合した。

- portal暗色の境界をgray-300へ統一し、raised境界もstrongに関連づける。gray-500や600の境界はraised面gray-700上では3:1未満だった。
- 暗色補助文字をgray-200、成功色をgreen-200、チャート軸を補助文字役割、focusをblue-200にする。本文・面の既存階層は維持。
- demo本文のgray-50 fallbackを実値 #f2f2f2に一致。copy補助文字を#cccccc、境界を#b3b3b3に改善。選択境界を警告に見える橙からblue-200にし、成功色の欠落定義を追加。
- demo copy hover/activeとキーボードfocusを定義。入力に既存のoutline:noneがあったためfocus-visibleの明示枠を追加。
- 注入guardではdanger-on-dark、warning-on-dark、warning-action-bg、warning-action-textに用途分離。色そのものと挙動は維持。通知面・補助文字・境界・影も別役割のまま。二つのguardファイルはバイト同一。

## 実測

Chromium `/usr/bin/chromium` でDADSと製品CSSを読ませ、`getComputedStyle()` の色を取得。sRGB各成分を線形化し、相対輝度 `0.2126 R + 0.7152 G + 0.0722 B`、比率 `(Lmax + .05)/(Lmin + .05)` で計算した。11 role × canvas/panel/card/raisedの4面 + guard/demo7組 = **51組、閾値違反0**。文字は4.5、境界/focusは3を下限とした。全データは [JSON](evidence/2026-10-01/approved-dark-contrast.json)。下表は最も明るいraised面#4d4d4d上とguard/demoの主要組。

| 役割 | 前景・背景（computed） | 比率 |
|---|---|---:|
| text-primary | rgb(242, 242, 242), rgb(77, 77, 77) | 7.551 |
| text-secondary | rgb(204, 204, 204), rgb(77, 77, 77) | 5.264 |
| text-link | rgb(197, 215, 251), rgb(77, 77, 77) | 5.832 |
| danger | rgb(255, 187, 187), rgb(77, 77, 77) | 5.264 |
| warning | rgb(255, 212, 61), rgb(77, 77, 77) | 5.932 |
| success | rgb(155, 212, 181), rgb(77, 77, 77) | 5.023 |
| chart-axis | rgb(204, 204, 204), rgb(77, 77, 77) | 5.264 |
| text-on-dark-secondary | rgb(204, 204, 204), rgb(77, 77, 77) | 5.264 |
| border-subtle | rgb(179, 179, 179), rgb(77, 77, 77) | 4.032 |
| border-raised | rgb(179, 179, 179), rgb(77, 77, 77) | 4.032 |
| focus-ring | rgb(197, 215, 251), rgb(77, 77, 77) | 5.832 |
| guard-text | rgb(255, 255, 255), rgb(26, 26, 26) | 17.404 |
| guard-dismiss | rgb(179, 179, 179), rgb(26, 26, 26) | 8.301 |
| guard-danger | rgb(255, 187, 187), rgb(26, 26, 26) | 10.839 |
| guard-warning | rgb(255, 212, 61), rgb(26, 26, 26) | 12.214 |
| guard-action | rgb(26, 26, 26), rgb(255, 212, 61) | 12.214 |
| demo-copy | rgb(204, 204, 204), rgb(77, 77, 77) | 5.264 |
| demo-copy-border | rgb(179, 179, 179), rgb(77, 77, 77) | 4.032 |

デモcopy文字は従来#b3b3b3 / #4d4d4dの4.032:1から5.264:1へ改善。portal本文の最低比率は7.551:1、成功文字の最低は5.023:1。通知の危険・警告は本文に加え日本語のblock/検出文でも意味を示す。

`node --check extension/src/guard.js`、guard配布元/portalコピーのcmp、extension既存4テストファイルを実行済み。UI全体の回帰は他担当の総合検証と合わせる。

## 限界

この行列は基本面に対するrole値の測定であり、全画面・全半透明合成背景・全disabled状態のWCAG適合証明ではない。実画面のalpha合成、ホバー、drawer/popover、フォーカスの可視性は別途ブラウザ総合検証が必要。色覚特性を含む利用者試験・支援技術試験の合格を主張しない。第三者ページが独自にDADS変数を上書きする場合のguard配色は保証しない。配布境界の変更はFの対象なので行っていない。
