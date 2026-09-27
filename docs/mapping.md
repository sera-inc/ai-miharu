# mapping.md — 実装値 → トークン対応表

**対象**: `.`　**生成日**: 2026-09-27　**生成**: `scripts/inventory.mjs`
**ステータス**: DeepSeek 4.1 Flash による仮対応（人間レビュー未承認、Phase 1 未完了）

> この表は設計書 §6 Phase 1 の中核資産です。設計書は人間による対応トークン決定・レビューを要求します。
> 今回は依頼者の明示指示により DeepSeek 4.1 Flash 単独で仮判定しました。人間承認を受けたものとして扱いません。
> `保留` は用途が曖昧で値だけでは置換できず、`除外` は抽出誤検知等です。**未解決が残るため Phase 2 への一括移行は不可です。**

## 色

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `#fff` | 21 | 保留 | 保留 | `extension/demo/index.html` 他4件。DeepSeek 判定: 白はページ/ポップオーバー背景、暗色背景上の文字色など複数用途で使われ、--app-surface と --app-text-inverse 等のどれか一意に決められないため。 |
| `#111` | 6 | --app-text | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 本文やオプションの主要文字色として使われており、--app-text の用途に一致するため。 |
| `#f5a524` | 5 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: 警告色として罫線とボタン背景の両方に使われ、--app-warning と --app-warning-border を一意に決められないため。 |
| `#ddd` | 4 | 保留 | 保留 | `extension/demo/index.html` 他3件。DeepSeek 判定: 暗色背景上の文字色と罫線の両方に使われ、候補の border/text 系トークンに一意に対応しないため。 |
| `#1f2430` | 4 | 保留 | 保留 | `extension/src/guard.js` 他1件。DeepSeek 判定: ガード通知の暗色背景で、候補に一致する暗色 surface 用トークンがないため。 |
| `#555` | 4 | 保留 | 保留 | `extension/src/guard.js` 他3件。DeepSeek 判定: 罫線色と補助文字色の両方に使われ、--app-border-strong と --app-text-muted を一意に決められないため。 |
| `#55d9bd` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: アクティブ表示の背景とフォーカスアウトラインの両方に使われ、--app-primary と --app-focus-ring のどちらか一意に決められないため。 |
| `#102e27` | 3 | --app-primary-text | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマのプライマリボタン文字色として使われており、--app-primary-text の用途に一致するため。 |
| `rgba(255,255,255,.07)` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 半透明の白で暗色背景上の背景・罫線に使われるが、候補に半透明の surface/border トークンがなく一意に決められないため。 |
| `#10003` | 3 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: HTMLエンティティ &#10003; の一部として抽出されたもので、CSS色ではないため。 |
| `#9aa0ab` | 2 | --app-text-muted | AI仮対応 | `extension/demo/index.html`。DeepSeek 判定: `.muted` の補助文字色として使われており、--app-text-muted の用途に一致するため。 |
| `#333` | 2 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: 暗色背景上の入力欄などの罫線色で、候補の --app-border / --app-border-strong と値・用途が一致せず一意に決められないため。 |
| `#1e222b` | 2 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: ダークな背景色だが、候補の --app-surface 系は白または明るいグレーであり、用途・値とも一致しないため。 |
| `#262a33` | 2 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: ダークなボーダー色だが、候補の --app-border 系は明るいグレーであり、一致しないため。 |
| `#3a3f4a` | 2 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: ダークなボーダー色だが、候補の --app-border 系と値が一致しないため。 |
| `#e5484d` | 2 | 保留 | 保留 | `extension/src/guard.js` 他1件。DeepSeek 判定: ブロック時の色だが、プロパティが不明で --app-danger / --app-danger-text / --app-danger-border のどれか一意に決められないため。 |
| `rgba(0,0,0,.35)` | 2 | 保留 | 保留 | `extension/src/guard.js` 他1件。DeepSeek 判定: box-shadow 用の色で、対応する影のトークンが候補にないため。 |
| `#39bda6` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: primary ボタンの背景と境界線の両方に使われており、--app-primary と --app-primary-border のどちらか一意に決められないため。 |
| `#1a2940` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマのホバー背景色だが、候補の --app-surface-hover は明るいグレーで一致しないため。 |
| `#edf9f6` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: グラデーション背景の明るい緑だが、success 用途ではなく対応するトークンがないため。 |
| `#f7fbfa` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: グラデーション背景の明るい色だが、対応するトークンがないため。 |
| `#123236` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマのグラデーション背景色で、success 用途ではなく対応するトークンがないため。 |
| `#102a36` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマのグラデーション背景色で、info 用途ではなく対応するトークンがないため。 |
| `#112138` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマのグラデーション背景色で、対応するトークンがないため。 |
| `#f2bd5b` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビのピン固定・ホバー用の強調色として使われており、候補の警告色やフォーカス色とは用途が異なるため、一意に対応するトークンを決められない。 |
| `#bbb` | 2 | --app-border | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: border-color として使用される汎用の境界線色であり、--app-border の用途に一致する。 |
| `#bdccda` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: register-score-head 内の淡いテキスト色で、暗背景上のミュートテキストと推測される。候補の --app-text-muted や --app-text-inverse とはテーマ・用途が一致しないため保留。 |
| `#22313e` | 2 | --app-text | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: :root の --fg として定義される基本前景色であり、--app-text の用途に一致する。 |
| `#5c6c7c` | 2 | --app-text-muted | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: :root の --mut として定義されるミュートテキスト色であり、--app-text-muted の用途に一致する。 |
| `#d6dfe5` | 2 | --app-border | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: :root の --bd として定義される境界線色であり、--app-border の用途に一致する。 |
| `#14735f` | 2 | --app-primary | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: :root の --pri として定義されるプライマリ色であり、--app-primary の用途に一致する。 |
| `#e8eef3` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: [data-theme=dark] の --fg として定義されるダークテーマ用前景色であり、候補のライトテーマ向け基本テキスト・反転テキストとは一意に対応しない。 |
| `#18232f` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: [data-theme=dark] の --sf2 として定義されるダークテーマ用二次サーフェス色であり、候補のサーフェストークンはライトテーマ向けのため対応しない。 |
| `#95a6b6` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: [data-theme=dark] の --mut として定義されるダークテーマ用ミュートテキスト色であり、候補の --app-text-muted とはテーマ・値が異なるため対応しない。 |
| `#263340` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: [data-theme=dark] の --bd として定義されるダークテーマ用境界線色であり、候補の --app-border とはテーマ・値が異なるため対応しない。 |
| `#7bdfc4` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: [data-theme=dark] の --pri として定義されるダークテーマ用プライマリ色であり、候補の --app-primary はライトテーマ/ブランド定義のため一意に対応しない。 |
| `rgba(0,0,0,.62)` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: box-shadow の影色として使われており、候補には shadow/overlay 用トークンがない。surface/text 等の色トークンに置き換えると用途が異なるため保留。 |
| `rgba(255,255,255,.1)` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: border-color と progress 背景の両方に使われる半透明白で、候補の border/surface トークンは不透明色。用途を一意に決められないため保留。 |
| `rgba(255,255,255,.12)` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: hover 背景と navflyout の border に使われる半透明白。surface-hover や border のどれか一つに確定できず、候補に対応する半透明トークンもないため保留。 |
| `rgba(255,255,255,.06)` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 暗色テーマの hover 背景として使われる半透明白。候補の surface-hover は solid-gray-50 で、ダークテーマの overlay 用とは意味が異なるため保留。 |
| `#ffffff` | 2 | --app-surface | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --sf はサーフェス色の定義で、白は基底 surface に相当する。--app-surface-raised も白だが、変数名と用途から generic な surface と判断。 |
| `rgba(20,24,28,.05)` | 2 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: box-shadow の影色。候補に shadow 用トークンがなく、色トークンでは代替できないため保留。 |
| `rgba(0,0,0,.28)` | 2 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: box-shadow の影色。候補に shadow 用トークンがないため保留。 |
| `rgba(15,18,20,.45)` | 2 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: dialog の backdrop 背景色。候補に scrim/backdrop 用トークンがないため保留。 |
| `rgba(14,110,140,0)` | 2 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: CSS の色値だがソース文脈がなく、候補トークンにも透明な teal 系の用途がないため一意に判断できない。 |
| `#14161c` | 1 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: body の暗色背景。候補の surface 系は白/薄灰で、暗色 inverse surface 用トークンがないため保留。 |
| `#e8e8e8` | 1 | --app-text-inverse | AI仮対応 | `extension/demo/index.html`。DeepSeek 判定: 暗色背景 #14161c 上の本文色で、inverse text の用途。候補の --app-text-inverse が該当する。 |
| `#6b7280` | 1 | --app-text-muted | AI仮対応 | `extension/demo/index.html`。DeepSeek 判定: placeholder の文字色で、muted text の用途。候補の --app-text-muted が該当する。 |
| `#262b36` | 1 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: button.copy の背景色だが、この暗色に対応する背景用トークンが候補にない。--app-text は同系色でもテキスト用途のため選ばない。 |
| `#101318` | 1 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: #report の背景色で、候補に該当する暗色サーフェストークンがない。 |
| `#4ade80` | 1 | --app-success-text | AI仮対応 | `extension/demo/index.html`。DeepSeek 判定: `.ok` の文字色で成功状態を表すため、成功テキスト用トークンが適切。 |
| `#cbd5e2` | 1 | --app-border | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ポップアップの境界線色（--pop-bd）で、標準ボーダー用途に相当。 |
| `#118b80` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: --chart のグラフ用色で、候補にチャート/データ可視化用トークンがない。 |
| `#118b801c` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: --chart-soft の半透明グラフ用色で、候補に該当するトークンがない。 |
| `#4cddbc` | 1 | --app-primary | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビのアクティブ表示インジケータのアクセント背景で、ブランド主色（primary）に相当。 |
| `#472631` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: nav .count のバッジ背景色だが、候補のdanger系は背景/文字の用途・明度が合わず一意に決められない。 |
| `#ffb2ba` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: nav .count の文字色だが、候補のdanger-textは濃色で用途・色調が一致しない。 |
| `#eaf0ff` | 1 | --app-primary-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: --acc-soft の淡いアクセント背景で、primaryの背景トークンに相当。 |
| `#fff4dc` | 1 | --app-warning-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: --warn-soft の警告用淡色背景で、warning背景トークンに相当。 |
| `#feebed` | 1 | --app-danger-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: --dstr-soft の破壊的/危険用淡色背景で、danger背景トークンに相当。 |
| `#182c59` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--acc-soft` はアクセントの淡色背景を意図するが、候補の --app-primary-bg と --app-surface-selected が同じ値・類似用途で、どちらに対応するか一意に決められないため。 |
| `#392c13` | 1 | --app-warning-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--warn-soft` は警告の淡い背景色を定義しており、警告背景トークン --app-warning-bg の用途に一致するため。 |
| `#422229` | 1 | --app-danger-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--dstr-soft` は危険・エラーの淡い背景色を定義しており、危険背景トークン --app-danger-bg の用途に一致するため。 |
| `#46d59e` | 1 | --app-success | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.estate-dot` のアクティブ状態を示す緑色のドット背景で、成功の基本色トークン --app-success の用途に一致するため。 |
| `#8a97a8` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.estate-dot.off` のオフ状態ドット背景で、候補には中立・無効状態のトークンがなく、text/border/surface の用途とも一致しないため。 |
| `#f0a840` | 1 | --app-warning | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.estate-dot.warn` の警告状態を示すドット背景で、警告の基本色トークン --app-warning の用途に一致するため。 |
| `#8090a7` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビゲーションのSVGアイコン色で、muted なアイコン・テキスト色として --app-text-muted が妥当なため。 |
| `#66768e` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビゲーションのシェブロン色で、muted なアイコン色として --app-text-muted が妥当なため。 |
| `#d9e0e9` | 1 | --app-border | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.search` の border-color で、標準の境界線トークン --app-border の用途に一致するため。 |
| `#13283f` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.overview-posture` の装飾グラデーションの一部で、単一の意味トークンに対応せず、どの状態・面かを一意に決められないため。 |
| `#102034` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.overview-posture` の装飾グラデーションの一部で、単一の意味トークンに対応せず、どの状態・面かを一意に決められないため。 |
| `#12283e` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: `.overview-posture` の装飾グラデーションの一部で、単一の意味トークンに対応せず、どの状態・面かを一意に決められないため。 |
| `#102c34` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色グラデーション背景の一部で、候補にあるサーフェストークン（白/薄灰）とは用途・明度が異なり、対応するトークンが一意に決まらない。 |
| `#10252d` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色グラデーション背景の一部で、候補トークンには該当する暗色サーフェス用途がなく一意に決まらない。 |
| `#112a34` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色グラデーション背景の一部で、候補トークンには該当する暗色サーフェス用途がなく一意に決まらない。 |
| `#ff9ba2` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色背景上の危険色インジケータ文字色。候補の--app-danger-textはred-900（暗い赤）で、前提背景が異なり一意に対応しない。 |
| `#79e5c2` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色背景上の成功色インジケータ文字色。候補の--app-success-textはgreen-800（暗い緑）で、前提背景が異なり一意に対応しない。 |
| `#8fa1b7` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色背景上の補助テキスト色。--app-text-mutedはsolid-gray-600（明色背景向け）で、暗色背景用のミュートテキストトークンがないため保留。 |
| `#aab7c8` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色背景上の本文テキスト色。--app-textはsolid-gray-800で暗色背景には合わず、対応するトークンがない。 |
| `#94a5b9` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色背景上の補助テキスト色。--app-text-mutedの用途と背景が異なり一意に決まらない。 |
| `#e9f0f7` | 1 | --app-text-inverse | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗色背景上のボタン文字色として、反転テキスト用トークンの用途に一致。値も白色系で近い。 |
| `#071c21` | 1 | --app-primary-text | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: primaryボタンの文字色として、ブランドのprimary-text用途に一致。 |
| `#f8fafc` | 1 | --app-surface-sunken | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: テーブルヘッダーの背景色で、沈んだサーフェス用トークンの用途に一致。 |
| `#183e5e` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: アバター背景のグラデーション端点で、単一のブランド/サーフェストークンには対応せず保留。 |
| `#087b72` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: アバターの装飾グラデーション用で、特定の意味トークンに対応しないため。 |
| `#4fd3b8` | 1 | --app-primary | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: 登録進捗バーの塗り色で、主色（ブランド主色）として使われているため。 |
| `#eaf0f7` | 1 | --app-text-inverse | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマ上のボタン文字色で、反転テキスト色として扱えるため。 |
| `#f1faf8` | 1 | --app-surface-selected | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: チェック状態のウィジェット背景色で、選択面の色として使われているため。 |
| `#142a2e` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマ用の選択背景色で、対応するトークンがないため。 |
| `#27504f` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマ用の選択境界色で、対応するトークンがないため。 |
| `#718097` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビの見出しラベルの文字色で、補助テキスト色として使われているため。 |
| `#64748c` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の提示範囲に値が現れず、用途（color/background/border）が判別できないため。 |
| `#91a0b6` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: フライアウトの見出し文字色で、補助テキスト色として使われているため。 |
| `#778398` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: テーブルヘッダの文字色で、補助テキスト色として使われているため。 |
| `#fff7e9` | 1 | --app-warning-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: 注意サマリの背景グラデーション開始色で、警告背景色として使われているため。 |
| `#fcfaf5` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 注意サマリの背景グラデーション中間色で、特定の意味トークンに一致しないため。 |
| `#352b19` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: [data-theme=dark] の attention 背景グラデーション用の濃茶。warning/danger の背景トークンとは明度・用途が異なり、候補に対応する暗色背景トークンがない。 |
| `#29231a` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 同じ暗色グラデーションの中間色。対応する暗色背景トークンがない。 |
| `#172134` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 同じ暗色グラデーションの濃紺。対応する暗色背景トークンがない。 |
| `#999` | 1 | --app-border | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: .pill の border に使用される中性グレーの境界線色。用途が border であり、候補の --app-border が対応する。 |
| `#d7dbe2` | 1 | --app-border | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: main#app * の border-color に使用される境界線色。用途が border であり、候補の --app-border が対応する。 |
| `#101a2a` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: dark テーマの budget-card-head 背景。候補に暗色 surface トークンがない。 |
| `#111d2e` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: dark テーマの budget-kpis 背景。候補に暗色 surface トークンがない。 |
| `#111c2c` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: dark テーマの note 背景。候補に暗色 surface トークンがない。 |
| `#a7b5c8` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: tenant-chev の chevron 色。muted text に近いが、--app-text-muted は solid-gray-600 で明度・色味が一致せず、他に適切なテキスト/アイコン色トークンがない。 |
| `#7d90aa` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: nav-child の nav-dot 背景。青灰系で primary/info などの用途が特定できず、適切なトークンがない。 |
| `#172d40` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: register-score の背景。暗色背景用トークンがなく、--app-primary 等の意味も特定できない。 |
| `#082d28` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: evidence-print の文字色。濃緑で success-text の可能性はあるが、文脈が success を示さず、dark テーマでの用途も不明瞭なため保留。 |
| `#f4f6f8` | 1 | --app-surface-sunken | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--bg` としてページ背景に使われる淡いグレー。DADS の sunken surface（solid-gray-50）に対応する。 |
| `#edf2f5` | 1 | --app-surface-sunken | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--sf2` として二次サーフェスに使われる淡いグレー。surface-sunken の用途に合致する。 |
| `#e1f2ed` | 1 | --app-primary-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--pri-soft` はプライマリの淡い背景色。primary-bg（brand-selected）に対応する。 |
| `#486fbd` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--acc` はアクセント色で、リンク（--app-text-link）と情報（--app-info）のどちらにも解釈でき、ソース行だけでは一意に決められない。 |
| `#b93b51` | 1 | --app-danger | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--dstr` は危険色の基本色。danger に対応する。 |
| `#8d601b` | 1 | --app-warning | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--warn` は警告色の基本色。warning に対応する。 |
| `#eef2f5` | 1 | --app-warning-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--warn-soft` と推定される警告の淡い背景色。warning-bg に対応する。 |
| `#deeee8` | 1 | --app-success-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--ok-soft` と推定される成功の淡い背景色。success-bg に対応する。 |
| `#edf4f4` | 1 | --app-info-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--info-soft` と推定される情報の淡い背景色。info-bg に対応する。 |
| `#bdd7cd` | 1 | --app-success-border | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: `--ok-border` と推定される成功の境界線色。success-border に対応する。 |
| `#17334a03` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 影用の半透明色と推定され、候補トークンに shadow 系がないため対応不可。 |
| `#0b1017` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマの `--bg` で、候補トークンはライトテーマ用のため対応する surface 系トークンがない。 |
| `#111a24` | 1 | --app-surface | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソースで --sf（サーフェス）として定義されているため、ベースサーフェスの --app-surface が対応する。 |
| `#153831` | 1 | --app-primary-bg | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソースで --pri-soft（プライマリの淡色背景）として定義されているため、--app-primary-bg が対応する。 |
| `#a7b8e4` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソースで --acc（アクセント）として定義されているが、リンク（--app-text-link）や情報（--app-info）など複数の用途が想定され、一意に決められない。 |
| `#ff8e9b` | 1 | --app-danger | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソースで --dstr（危険色）として定義されているため、基本の危険色トークン --app-danger が対応する。 |
| `#eac078` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#0e141c` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#1c332f` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#14232b` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#34504d` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#63c8b0` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#63c8b01a` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#354756` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース行の文脈に値が現れず、変数名や用途を特定できない。 |
| `#00000013` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 8桁HEXの半透明黒でCSS色だが、候補トークンに黒の透過色や影・オーバーレイ用途に対応するものがない。ソース文脈から一意な用途も判別できないため保留。 |
| `rgba(12,24,46,.2)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: --pop-shadow の影色として使われる半透明色。候補トークンに影用の色トークンがなく、surface/border/text などへ意味を寄せると用途が異なるため保留。 |
| `rgba(12,24,46,.1)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: --pop-shadow の影色として使われる半透明色。候補トークンに影用の色トークンがなく、同じ値でも単独の意味に一意対応できないため保留。 |
| `rgba(0,0,0,.45)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマの --pop-shadow に使う半透明黒の影色。候補トークンに shadow/overlay 用の色がなく、値が近いだけのトークン選択は避けるべきため保留。 |
| `rgba(255,255,255,.055)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: aside の border-right 色として使う半透明白。--app-border は不透明の gray-420 であり、ダーク背景上の透過ボーダーとは意味が異なるため保留。 |
| `rgba(255,255,255,.05)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: nav button:hover の背景色として使う半透明白。--app-surface-hover は solid-gray-50 の不透明背景で、透過ホバーとは用途・意味が異なるため保留。 |
| `rgba(255,255,255,.02)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .fold の背景に使う極薄の半透明白。候補トークンに透過背景用のものや同義の surface がなく、一意対応できないため保留。 |
| `rgba(7,15,28,.42)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .overlay の背景色として使う半透明ダーク色。候補トークンに overlay/scrim 用トークンがなく、surface 等では意味が異なるため保留。 |
| `rgba(70,213,158,.12)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .estate-dot の box-shadow リングに使う半透明グリーン。--app-success は不透明の green-800 で、影用の透過色とは用途が異なるため保留。 |
| `rgba(138,151,168,.14)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .estate-dot.off の box-shadow リングに使う半透明グレー。--app-text-muted 等はテキスト色で、影用の透過色とは意味が異なるため保留。 |
| `rgba(240,168,64,.16)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .estate-dot.warn の box-shadow リングに使う半透明オレンジ。--app-warning は不透明の警告色で、影用の透過色とは用途が異なるため保留。 |
| `rgba(85,217,189,.09)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .nav-child.on .nav-dot の box-shadow リングに使う半透明色。候補トークンに影用の透過色がなく、primary 等へ寄せると意味が異なるため保留。 |
| `rgba(255,255,255,.025)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビのアクティブ時に使う半透明白のインセット影で、候補の不透明な surface/border/text トークンとは用途が異なるため。 |
| `rgba(16,24,40,.015)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: トップバー下の極薄い影用の半透明色で、対応する影トークンが候補にないため。 |
| `rgba(16,24,40,.02)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: メタチップのドロップシャドウ用の半透明色で、対応する影トークンが候補にないため。 |
| `rgba(11,20,36,.12)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: オーバーレイ/影系の半透明濃色で、候補の surface/border トークンとは意味が異なるため。 |
| `rgba(88,220,190,.12)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 装飾用の半透明アクセント境界色で、候補に対応するトークンがないため。 |
| `rgba(88,220,190,.025)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 装飾用の半透明アクセント色で、候補に対応するトークンがないため。 |
| `rgba(88,220,190,.018)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 装飾用の半透明アクセント色で、候補に対応するトークンがないため。 |
| `rgba(255,164,173,.26)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗背景上のステータス装飾に使う半透明ピンク境界色で、候補の danger 系トークンとは値・用途が異なるため。 |
| `rgba(196,50,60,.18)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗背景上のステータス装飾に使う半透明赤背景で、候補の danger-bg とは意味が異なるため。 |
| `rgba(100,236,195,.2)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗背景上の良好ステータス装飾に使う半透明緑境界色で、候補の success 系トークンとは値・用途が異なるため。 |
| `rgba(49,178,138,.16)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗背景上の良好ステータス装飾に使う半透明緑背景で、候補の success-bg とは意味が異なるため。 |
| `rgba(255,255,255,.15)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 暗背景上のミニボタン境界に使う半透明白で、候補の不透明な border/text トークンとは意味が異なるため。 |
| `rgba(16,24,40,.07)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow用の半透明ニュートラル影色。候補トークンはsurface/border/text等の不透明色で、影色に対応する用途のトークンがないため保留。 |
| `rgba(8,85,79,.18)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: button.mini.priのbox-shadow用の半透明プライマリ系影色。--app-primary等は塗り・文字色用で、影色として意味が一致しないため保留。 |
| `rgba(16,24,40,.025)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: input/select等のbox-shadow用の極薄ニュートラル影色。候補に対応する影トークンがなく、surface/border等とも用途が異なるため保留。 |
| `rgba(16,24,40,.06)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ステップ選択状態のbox-shadow用の半透明影色。候補トークンに影用の値・用途がなく一致しないため保留。 |
| `rgba(16,24,40,.12)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 固定バー付近のbox-shadow用の半透明ニュートラル影色。候補は不透明な色トークンで、影色用途に合うものがないため保留。 |
| `rgba(10,21,38,.18)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: カードの強いbox-shadow用の半透明ダーク影色。DADS候補トークンは面・境界・文字色で、影色トークンではないため保留。 |
| `rgba(104,224,199,.24)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: tenant-switchホバー時の半透明ボーダー色。候補のborder/primary系トークンは不透明色で、値と用途が一致しないため保留。 |
| `rgba(79,211,184,.25)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: プログレスバーのグロー用box-shadow色。--app-focus-ring等の候補トークンとは意味・値が異なるため保留。 |
| `rgba(255,255,255,.14)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマ時の半透明ボーダー色。--app-text-inverse等の白トークンは不透明な文字色用で、境界用途と一致しないため保留。 |
| `rgba(255,255,255,.11)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマ時のホバー背景用の半透明白。--app-surface-hoverは不透明なgray系で、値と用途が一致しないため保留。 |
| `rgba(10,20,38,.22)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: スイッチノブのbox-shadow用の半透明ダーク影色。候補に対応する影トークンがなく、他用途とも一致しないため保留。 |
| `rgba(242,189,91,.1)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ナビピンホバー背景用の半透明黄色。--app-warning-bg等の警告系トークンとは用途・値が異なるため保留。 |
| `rgba(2,8,20,.38)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow の影色として使われる半透明色であり、候補トークンにシャドウ用の色がないため、一意に対応付けできない。 |
| `rgba(255,255,255,.012)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: ダークテーマ時の偶数行背景に使われる半透明の白であり、候補トークンはライトテーマの固定色を想定しているため、対応するトークンがない。 |
| `#f6f6f3` | 1 | --app-surface | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --bg はページの基本背景色を定義しており、既定のサーフェスを表す --app-surface に対応する。 |
| `#1c2024` | 1 | --app-text | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --fg は前景色（本文テキスト）を定義しており、基本テキスト色の --app-text に対応する。 |
| `#eef0ec` | 1 | --app-surface-sunken | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --sf2 は二次的なサーフェス色を定義しており、一段沈んだ背景を表す --app-surface-sunken に対応する。 |
| `#177245` | 1 | --app-primary | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --pri はブランドの主要色を定義しており、--app-primary に対応する。 |
| `#0e6e8c` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --acc はアクセント色を定義しているが、候補トークンにアクセント用のものがなく、info とは用途が異なるため一意に決められない。 |
| `#8a5b00` | 1 | --app-warning | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --warn は警告色を定義しており、--app-warning に対応する。 |
| `#b3261e` | 1 | --app-danger | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --dstr は危険・エラー色を定義しており、--app-danger に対応する。 |
| `#5c636e` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --mut は補助テキスト色を定義しており、--app-text-muted に対応する。 |
| `#e4e5e0` | 1 | --app-border | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --bd は境界線色を定義しており、--app-border に対応する。 |
| `#e7f3ec` | 1 | --app-primary-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: 変数 --pri-soft は主要色の淡い背景を定義しており、--app-primary-bg に対応する。 |
| `#e3f0f5` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--acc-soft` はアクセント用の淡色背景だが、候補にアクセント用途のトークンがなく、info/primary/selected のどれに相当するか文脈だけでは一意に決められないため。 |
| `#fdf0d3` | 1 | --app-warning-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: `--warn-soft` は警告用の淡色背景であり、DADS の警告背景トークンに対応するため。 |
| `#fbeae9` | 1 | --app-danger-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: `--dstr-soft` は危険・災害用の淡色背景であり、DADS の危険背景トークンに対応するため。 |
| `#c9ccc4` | 1 | --app-border | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: `--pop-bd` はポップアップの境界線色であり、通常のボーダー用途のトークンに対応するため。 |
| `#0a7ea4` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--chart` はグラフ用の色であり、候補にチャート用トークンがないため。 |
| `#0a7ea41f` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--chart-soft` はグラフ用の半透明色であり、候補にチャート用トークンがないため。 |
| `#131b29` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--side` は暗色サイドバー背景だが、候補に暗色背景用サーフェストークンがないため。 |
| `#e1e7ef` | 1 | --app-text-inverse | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: `--side-ink` は暗色サイドバー上の主要テキスト色であり、暗背景上のテキスト用トークンに対応するため。 |
| `#8d99ab` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--side-mut` は暗色サイドバー上の補助テキスト色だが、暗背景用の補助テキストトークンが候補にないため。 |
| `#7cd4e6` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--side-on-ink` はサイドバーの選択・アクティブ時の文字色だが、対応する候補トークンが一意に決まらないため。 |
| `#14171b` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: `--bg` はダークテーマの背景色だが、候補に暗色背景用サーフェストークンがないため。 |
| `#e8eaed` | 1 | --app-text-inverse | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: `--fg` は暗色背景上の前景テキスト色であり、暗背景上のテキスト用トークンに対応するため。 |
| `#1d2126` | 1 | --app-surface | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: ソースの --sf は基準となる面の背景色（surface）を表すため。 |
| `#262b31` | 1 | --app-surface-raised | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --sf2 は --sf より一段明るい副次的な面で、持ち上がった surface（raised）に相当するため。 |
| `#46c07f` | 1 | --app-primary | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --pri は主色（primary）を表すため。緑色だが success ではなく primary の用途と判断。 |
| `#67c1dd` | 1 | --app-info | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --acc は --warn/--dstr と並ぶ情報系アクセント色で、DADS の info に対応するため。 |
| `#e3b341` | 1 | --app-warning | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --warn は警告色（warning）を表すため。 |
| `#f28b82` | 1 | --app-danger | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --dstr は破壊的・危険色（danger）を表すため。 |
| `#9aa3ad` | 1 | --app-text-muted | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --mut は補助テキスト色（muted text）を表すため。 |
| `#2b313a` | 1 | --app-border | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --bd は標準の境界線色（border）を表すため。 |
| `#1c3328` | 1 | --app-primary-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --pri-soft は primary の淡い背景色で、primary の背景トークンに対応するため。 |
| `#12303a` | 1 | --app-info-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --acc-soft は info 系アクセントの淡い背景色に対応するため。 |
| `#33290f` | 1 | --app-warning-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --warn-soft は warning の淡い背景色に対応するため。 |
| `#3a1f1d` | 1 | --app-danger-bg | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --dstr-soft は danger の淡い背景色に対応するため。 |
| `#2c323a` | 1 | --app-surface-raised | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --pop はポップオーバー背景用。ポップオーバーは浮き上がった面なので --app-surface-raised が対応する。 |
| `#454d58` | 1 | --app-border | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --pop-bd はポップオーバーの境界線用。既定の境界線トークン --app-border が対応する。 |
| `#2b9ec4` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: --chart はグラフ専用色。候補にチャート用トークンがなく、info 等の意味とは異なるため一意に決められない。 |
| `#2b9ec42e` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: --chart-soft はグラフの淡色・半透明色。候補に対応するチャート用トークンがない。 |
| `#0f1520` | 1 | --app-surface-sunken | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --side はサイドバー背景用。サイドバーは沈んだ面として --app-surface-sunken が対応する。 |
| `#f25022` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `#7fba00` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `#00a4ef` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `#ffb900` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: SVG の fill 属性内の色で、CSS 宣言の値ではないため抽出誤検知。 |
| `rgba(20,23,27,.20)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: --pop-shadow の影色。候補にシャドウ用トークンがなく対応先を決められない。 |
| `rgba(20,23,27,.12)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: --pop-shadow の影色。候補にシャドウ用トークンがなく対応先を決められない。 |
| `rgba(255,255,255,.08)` | 1 | --app-border | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: --side-line はサイドバーの境界線用。既定の境界線トークン --app-border が対応する。 |
| `rgba(94,199,222,.13)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: サイドバーのアクティブ背景用と思われる半透明アクセント色。選択背景系の候補はあるが、半透明の独自色で用途もサイド専用のため一意に対応するトークンを決められない。 |
| `rgba(0,0,0,.5)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: box-shadow の影色として使われている。候補に影用トークンがなく、対応先を一意に決められない。 |
| `rgba(124,212,230,.4)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: フッターリンク hover の border-bottom-color に使われる半透明アクセント色。候補の文字色・ボーダー色トークンとは用途が異なり、対応先を決められない。 |
| `rgba(0,0,0,.18)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: box-shadow の影色として使われている。候補に影用トークンがなく、対応先を一意に決められない。 |
| `rgba(15,18,20,.35)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: オーバーレイ背景色として使われている。候補にオーバーレイ用トークンがなく、対応先を決められない。 |
| `rgba(15,18,20,.18)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: box-shadow の影色として使われている。候補に影用トークンがなく、対応先を一意に決められない。 |
| `rgba(8,12,18,.62)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: ソース文脈がなく、半透明の暗色は影やオーバーレイなどの独自用途と推測される。候補に一致する用途のトークンがないため保留。 |
| `rgba(8,12,18,.72)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: ソース文脈がなく、半透明の暗色は影やオーバーレイなどの独自用途と推測される。候補に一致する用途のトークンがないため保留。 |
| `rgba(14,110,140,.45)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: ソース文脈がなく、半透明の独自アクセント色と推測される。候補トークンの中に一致する用途が見いだせないため保留。 |
| `rgba(8,12,18,.28)` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: ソース文脈がなく、半透明の暗色は影やオーバーレイなどの独自用途と推測される。候補に一致する用途のトークンがないため保留。 |

## フォントサイズ

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `12px` | 80 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: ソース行の文脈では padding、margin、border-radius、box-shadow、gradient などに使われており、フォントサイズ用途が確認できない。また候補には body-sm と label の両方が 0.75rem(12px) で存在し、用途を一意に特定できないため。 |
| `10px` | 71 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 文脈は margin、border-radius、box-shadow、padding などで、フォントサイズ用途が確認できない。候補トークンにも一致するサイズがないため。 |
| `11px` | 60 | --app-text-label-size | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: .card-section の font-size:11px は大文字化された小さなラベル見出しであり、ラベル用途と判断できる。値は 11px だが DADS のラベルサイズ (0.75rem=12px) に寄せる。 |
| `13px` | 41 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: .card h3 や .evidence-review-copy h3 の見出し、font:13px/1.45 の本文、button のラベルなど、見出し・本文・ラベルが混在しており一意に決められない。 |
| `11.5px` | 36 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: .note、.src-note、.qr-none は小さな本文/注記、select はラベル/コントロールで、body-sm と label のどちらに寄せるか一意に決められない。 |
| `12.5px` | 30 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: nav button はラベル/ボタン、index.html の font-size:12.5px はポップオーバー本文の可能性があり、body-sm と label が混在している。 |
| `9px` | 27 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 文脈は border-radius、gap などでフォントサイズ用途が確認できず、候補トークンにも一致するサイズがないため。 |
| `10.5px` | 27 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: ユーザー名、タグ、段落、メタチップ、select など本文とラベルが混在しており、一意に決められない。 |
| `9.5px` | 23 | --app-text-label-size | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: nav .count のバッジ、.ag-node b の大文字ラベルはいずれも小さな UI ラベル/バッジ用途。DADS の最小ラベルサイズ (0.75rem=12px) に寄せる。 |
| `8.5px` | 19 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: .posture-copy span の小さなテキストで、ラベルか本文小のどちらか判断できず、候補トークンともサイズが離れている。 |
| `8px` | 10 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 文脈は gap、border-radius、box-shadow、padding などでフォントサイズ用途が確認できない。 |
| `22px` | 9 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 文脈は margin、width、padding などでフォントサイズ用途が確認できない。 |
| `14px` | 7 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: フォントサイズとしての14pxがある一方、padding/gap等の用途も混在し、フォントサイズ用途でもbody/table/numericの14px候補があり一意に決められないため。 |
| `13.5px` | 7 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: タブボタンのfont-size指定だが、候補トークンに13.5px相当がなく、近い値の14pxへ置換すると意味が異なるため。 |
| `16px` | 6 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: nav-chevronのfont-size:16pxがある一方、top/blur/shadow等の用途も混在し、候補に16px相当がないため。 |
| `17px` | 5 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: font-size:17pxの用途がある一方、margin/padding等も混在し、候補に17px相当がないため。 |
| `19px` | 5 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: font-size:19pxの用途がある一方、gap等も混在し、候補に19px相当がないため。 |
| `15px` | 5 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: bodyや見出しにfont-size:15pxがある一方、margin/padding/gap等も混在し、候補に15px相当がないため。 |
| `20px` | 4 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 出現箇所はいずれもmin-width、box-shadow、paddingで、フォントサイズ指定ではないため。 |
| `26px` | 4 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: budget-kpis strongにfont-size:26pxがある一方、width/padding等も混在し、候補に26px相当がないため。 |
| `0.92em` | 3 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: muted/tableのfont-size指定だが、候補は0.75rem等で0.92em相当がなく、近い値へ置換できないため。 |
| `21px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: 出現箇所はいずれもmarginやpaddingで、フォントサイズ指定ではないため。 |
| `30px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: 430pxや130pxの一部としての誤検出で、独立したフォントサイズ指定ではないため。 |
| `7.5px` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: budget-kpis em/table thのfont-size指定だが、候補に7.5px相当がないため。 |
| `24px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow、padding、gap の寸法として使われており、font-size 指定ではないためフォントサイズ抽出の誤検知として除外。 |
| `28px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow、padding、width/height の寸法として使われており、font-size 指定ではないため除外。 |
| `18px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: padding、height、box-shadow などの寸法として使われており、font-size 指定ではないため除外。 |
| `0.85em` | 2 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: font-size:0.85em の実指定はあるが、0.85em に一致する候補トークンがなく、相対 em で用途も一意に決められないため保留。 |
| `27px` | 2 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: flex-basis、min-height の寸法として使われており、font-size 指定ではないため除外。 |
| `25px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: font-size:25px の実指定があるが、候補トークンに 25px 相当がなく、24px や 32px とは値も用途も異なるため保留。 |
| `1.4em` | 1 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: h1 の font-size:1.4em として使われているが、一致する候補トークンがなく、相対 em のため一意に決められない。 |
| `1.05em` | 1 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: h2 の font-size:1.05em として使われているが、一致する候補トークンがなく、相対 em のため一意に決められない。 |
| `32px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: width/height、margin、または 232px の部分一致として現れており、font-size 指定ではないため除外。 |
| `29px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: width、height、flex-basis の寸法として使われており、font-size 指定ではないため除外。 |
| `.9em` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: code/.mono の font-size:.9em として使われているが、一致する候補トークンがなく、mono 用トークンとも値が異なるため保留。 |
| `15.5px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: card-name の font-size:15.5px として使われているが、一致する候補トークンがなく、近い値のトークンに寄せるのは適切でないため保留。 |
| `14.5px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: CSSのfont-size指定であり抽出誤検知ではないが、候補トークンに14.5pxに対応する値が存在しない。body/tableの14px系やlabel/body-smの0.75remは値が近いだけで用途・値が異なるため、一意に対応付けできない。 |

## 余白

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `10px` | 138 | 保留 | 保留 | `extension/demo/index.html` 他4件。DeepSeek 判定: DADS の余白スケールに 10px 対応のトークンがなく、border-radius や font-size など余白以外の用途も混在しているため一意に決められない。 |
| `8px` | 114 | --app-space-2 | AI仮対応 | `extension/demo/index.html` 他4件。DeepSeek 判定: 8px は DADS の spacing-2 に一致し、提示文脈の厳密な 8px は gap/padding/top/bottom などの余白用途に使われているため。 |
| `12px` | 113 | 保留 | 保留 | `extension/demo/index.html` 他4件。DeepSeek 判定: 12px は DADS の spacing-3 に一致するが、padding/margin の余白用途と border-radius/box-shadow の用途が混在し、値単体では一意に決められない。 |
| `14px` | 109 | 保留 | 保留 | `extension/demo/index.html` 他4件。DeepSeek 判定: DADS の余白スケールに 14px 対応のトークンがなく、padding/gap の余白と font-size/box-shadow の用途が混在しているため。 |
| `6px` | 106 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: DADS の余白スケールに 6px 対応のトークンがなく、margin/padding の余白と border-radius の用途が混在しているため。 |
| `16px` | 85 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 16px は DADS の spacing-4 に一致するが、top/right/gap の余白と font-size/blur/box-shadow の用途が混在し一意に決められない。 |
| `4px` | 74 | 保留 | 保留 | `extension/src/guard.js` 他3件。DeepSeek 判定: 4px は DADS の spacing-1 に一致するが、提示文脈では border/box-shadow/outline-offset など余白以外の用途が中心で、余白トークンに対応させる根拠が一意でない。 |
| `2px` | 68 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: 2px は DADS の spacing-05 に一致するが、margin の余白と outline/width/box-shadow の用途が混在し一意に決められない。 |
| `20px` | 60 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: 20px は DADS の spacing-5 に一致するが、padding の余白と min-width/box-shadow の用途が混在し一意に決められない。 |
| `5px` | 59 | 保留 | 保留 | `extension/src/guard.js` 他3件。DeepSeek 判定: DADS の余白スケールに 5px 対応のトークンがなく、padding/margin の余白と border-radius の用途が混在しているため。 |
| `9px` | 55 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: DADS の余白スケールに 9px 対応のトークンがなく、gap の余白と border-radius の用途が混在しているため。 |
| `7px` | 55 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: DADS の余白スケールに 7px 対応のトークンがなく、margin の余白と border-radius/stroke-width の用途が混在しているため。 |
| `18px` | 51 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: paddingの余白として使われる一方、box-shadowのYオフセットやheightにも同じ18pxがあり用途が一意でない。またDADS spacingに18pxはない。 |
| `11px` | 42 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: gap/marginの余白とfont-sizeの両方で使われ、用途が一意でない。DADS spacingに11pxはない。 |
| `17px` | 42 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: margin/paddingの余白とfont-sizeの両方で使われ、用途が一意でない。DADS spacingに17pxはない。 |
| `3px` | 32 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: margin/paddingの余白とbox-shadowのoffset/spreadの両方で使われ、用途が一意でない。DADS spacingに3pxはない。 |
| `15px` | 32 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: margin/padding/gapの余白とfont-size/fontの両方で使われ、用途が一意でない。DADS spacingに15pxはない。 |
| `13px` | 26 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: marginの余白とfont-sizeの両方で使われ、用途が一意でない。DADS spacingに13pxはない。 |
| `1px` | 22 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: border幅としての使用が多く、marginの余白にも同じ1pxがあり用途が一意でない。DADS spacingに1pxはない。 |
| `22px` | 16 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: paddingの余白とwidth:calc()内の計算値の両方で使われ、用途が一意でない。DADS spacingに22pxはない。 |
| `24px` | 12 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: gap/paddingの余白では--app-space-6に一致するが、box-shadowのぼかし値にも同じ24pxがあり用途が一意でない。 |
| `19px` | 10 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: gapの余白とfont-sizeの両方で使われ、用途が一意でない。DADS spacingに19pxはない。 |
| `21px` | 6 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: margin/paddingの余白だが、DADS spacingに21pxはなく、近い20pxとは意味が異なる。 |
| `45px` | 6 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: max-width:145pxの部分文字列として抽出された誤検知であり、box-shadowのぼかし値でもあるため余白値ではない。 |
| `32px` | 4 | 保留 | 保留 | `extension/demo/index.html` 他1件。DeepSeek 判定: 32pxはmarginの余白として使われる一方、width/heightのサイズ指定や232pxの部分文字列にも出現し、用途が一意でない。候補の--app-space-5は32pxだが、サイズ用途に誤適用されるため保留。 |
| `28px` | 4 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 28pxに一致する候補トークンがない。paddingの余白、width/height、box-shadowのオフセットなど用途が混在している。 |
| `26px` | 4 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 26pxに一致する候補トークンがない。paddingの余白、font-size、width/heightなど用途が混在している。 |
| `30px` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 30pxに一致する候補トークンがない。430pxや130pxの部分文字列、box-shadowのオフセットとしての出現が主で、余白用途として一意に扱えない。 |
| `38px` | 3 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 38pxに一致する候補トークンがない。min-heightのサイズ指定やコメント内の文字列であり、余白用途ではない。 |
| `55px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 55pxに一致する候補トークンがない。paddingの余白だが、候補に55px相当のトークンがない。 |
| `40px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 40pxは--app-space-6に一致するが、paddingの余白とmin-heightのサイズ指定、340pxの部分文字列が混在し、一意に決められない。 |
| `25px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 25pxに一致する候補トークンがない。font-sizeやwidth/heightのサイズ指定が主で、余白用途ではない。 |
| `64px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 64pxは--app-space-8に一致するが、paddingの余白とmin-heightのサイズ指定が混在し、一意に決められない。 |
| `35px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 35pxに一致する候補トークンがない。min-heightのサイズ指定であり、余白用途ではない。 |
| `23px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 23pxに一致する候補トークンがない。paddingの余白とline-height、コメント内の文字列が混在している。 |
| `4.5px` | 2 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: 4.5pxに一致する候補トークンがない。paddingの余白だが、候補に4.5px相当のトークンがない。 |
| `1.6em` | 1 | 保留 | 保留 | `extension/demo/index.html`。DeepSeek 判定: margin-top の余白だが、1.6em は相対単位で DADS spacing の候補値に一致しないため。 |
| `27px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: flex-basis と min-height の寸法指定で、余白カテゴリの値ではないため。 |
| `58px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: margin-left と min-height で用途が混在し、候補トークンにも 58px 対応がないため。 |
| `56px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: padding-bottom の余白だが、56px に対応する候補トークンがないため。 |
| `48px` | 1 | --app-space-6 | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: main の padding-bottom 48px は DADS spacing-6 (48px) に対応する余白値のため。 |
| `36px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: height/min-height の寸法指定で、余白カテゴリの値ではないため。 |
| `50px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow の blur radius で、余白ではないため。 |
| `44px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: padding と box-shadow の blur で用途が混在し、候補トークンにも 44px 対応がないため。 |
| `60px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: padding-bottom と min-height で用途が混在し、候補トークンにも 60px 対応がないため。 |
| `1.5px` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: font-size:11.5px の一部を誤抽出したもので、独立した余白値ではないため。 |
| `223px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: padding-left の余白だが、223px に対応する候補トークンがないため。 |

## 角丸

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `8px` | 26 | --app-radius-md | AI仮対応 | `extension/demo/index.html` 他2件。DeepSeek 判定: 8px は角丸の基本スケールで、--app-radius-md（DADS radius-8）に対応。ソース上でも border-radius:8px の用途がある。 |
| `12px` | 22 | --app-radius-lg | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: dialog の border-radius:12px など角丸に使用され、--app-radius-lg（DADS radius-12）に対応。 |
| `7px` | 20 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: border-radius:7px として角丸に使用されているが、候補に 7px 相当のトークンがない。sm=6px・md=8px に近いが値が異なるため選ばない。 |
| `10px` | 19 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: border-radius:10px や --radius:10px として角丸に使用されているが、候補に 10px 相当のトークンがない。 |
| `4px` | 19 | --app-radius-xs | AI仮対応 | `extension/demo/index.html` 他4件。DeepSeek 判定: border-radius:4px として使用され、--app-radius-xs（DADS radius-4）に対応。 |
| `6px` | 19 | --app-radius-sm | AI仮対応 | `extension/src/guard.js` 他3件。DeepSeek 判定: border-radius:6px として使用され、--app-radius-sm（DADS radius-6）に対応。 |
| `9px` | 15 | 保留 | 保留 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: border-radius:9px として使用されているが、候補に 9px 相当のトークンがない。 |
| `50%` | 14 | --app-radius-full | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: border-radius:50% は円形・完全な角丸の用途で、--app-radius-full に対応。 |
| `99px` | 13 | --app-radius-full | AI仮対応 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: border-radius:99px はピル形状・完全な角丸の用途で、--app-radius-full に対応。 |
| `0` | 10 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース文脈が著作権表記の「2026」等であり、角丸の CSS 値として抽出された誤検知。 |
| `5px` | 9 | 保留 | 保留 | `extension/demo/index.html` 他2件。DeepSeek 判定: border-radius:5px として使用されているが、候補に 5px 相当のトークンがない。 |
| `3px` | 9 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: ソース文脈では margin/padding/box-shadow などの値で、border-radius:3px の使用が確認できず、角丸カテゴリの抽出誤検知。 |
| `2px` | 6 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: margin/padding/width/shadow/outline 内の値や 12px などの部分一致で、border-radius 値として使われていないため。 |
| `var(--radius-sm)` | 4 | --app-radius-sm | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: border-radius に既存の small 用変数が使われており、候補の --app-radius-sm に対応する。 |
| `11px` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: gap/font-size/margin の値で、border-radius 値として使われていないため。 |
| `0 0 10px 10px` | 2 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 下部のみ 10px の角丸で、候補トークンに一致する半径がなく、部分指定のため単純置換できない。 |
| `4px 4px 0 0` | 1 | --app-radius-xs | AI仮対応 | `portal/app/static/enterprise.css`。DeepSeek 判定: 上角のみ 4px の角丸で、4px は --app-radius-xs（dads-radius-4）に対応する。 |
| `var(--radius)` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 既存の汎用 radius 変数の実値が文脈から分からず、md/lg など候補のどれに対応するか一意に決められない。 |
| `14px!important` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 14px の角丸は候補の半径スケールに一致せず、近い lg への置換はできない。 |
| `0!important` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: border-radius:0!important として使われる有効な値だが、0 用の候補トークンがなく対応を一意に決められない。 |
| `0 0 7px 7px` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: 下部のみ 7px の角丸で、候補トークンに一致する半径がなく、部分指定のため単純置換できない。 |
| `inherit` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: border-radius:inherit として使われる有効な値だが、継承を表す候補トークンがない。 |
| `1px` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: border/outline の太さやコメント中の 1px で、border-radius 値として使われていないため。 |
| `999px` | 1 | --app-radius-full | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: ピル状の完全な角丸で、--app-radius-full（dads-radius-full）に対応する。 |
| `2px 4px 4px 2px` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: border-radius の4値一括指定であり、各角で異なる半径を指定している。候補トークンは単一の角丸値に対応するため一意に置換できず、2px に一致する候補トークンも存在しない。 |

## z-index

| 実装値 | 出現回数 | 対応トークン | 状態 | 備考（代表ファイル） |
|---|---|---|---|---|
| `1` | 5 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: ソース文脈に z-index:1 が確認できず、v1.1.0 や -1、initial-scale=1 など非 z-index の数値・コード内出現のみ。抽出誤検知と判断。 |
| `60` | 4 | --app-z-popover | AI仮対応 | `portal/app/static/index.html`。DeepSeek 判定: #navtip の z-index:60 として使用され、ツールチップ/ポップオーバーの用途。候補トークンの --app-z-popover に対応。 |
| `2` | 3 | 除外 | 除外 | `portal/app/static/enterprise.css` 他1件。DeepSeek 判定: 著作権年 2026 や SVG の points 値などに含まれる数値で、z-index としての使用が確認できない。抽出誤検知。 |
| `2147483647` | 2 | --app-z-toast | AI仮対応 | `extension/src/guard.js` 他1件。DeepSeek 判定: guard.js の固定通知（position:fixed; top:16px; right:16px; z-index:2147483647）で最大値を使用。トースト/通知の用途なので --app-z-toast に対応。 |
| `90` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: 90deg や right:-90px、rotate(-90deg) など角度・位置指定として出現し、z-index:90 は確認できない。抽出誤検知。 |
| `75` | 1 | 保留 | 保留 | `portal/app/static/enterprise.css`。DeepSeek 判定: #setupbell .bcount の z-index:75（バッジ）と推測されるが、バッジ用途に合う候補トークンがなく一意に決められない。 |
| `70` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow の 70px や 70% などに出現し、z-index:70 は確認できない。抽出誤検知。 |
| `4` | 1 | 除外 | 除外 | `portal/app/static/enterprise.css`。DeepSeek 判定: box-shadow の 0 4px 14px などに出現し、z-index:4 は確認できない。抽出誤検知。 |
| `5` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: URL の AmanSK5 や行番号などに出現し、z-index:5 は確認できない。抽出誤検知。 |
| `40` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: minmax(400px,1fr) や SVG パス座標などに出現し、z-index:40 は確認できない。抽出誤検知。 |
| `19` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: .posture-mark の z-index:19 として使用されているが、装飾マーク用途に合う候補トークンがなく一意に決められない。 |
| `20` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: 著作権年 2026 に含まれる数値で、z-index:20 は確認できない。抽出誤検知。 |
| `9000` | 1 | 保留 | 保留 | `portal/app/static/index.html`。DeepSeek 判定: #tour の固定全画面オーバーレイ用 z-index であり、候補の modal/popover/toast とは用途が異なる。9000 に対応する専用の z-index トークンが候補にないため。 |
| `3` | 1 | 除外 | 除外 | `portal/app/static/index.html`。DeepSeek 判定: カテゴリは z-index だが、文脈では margin-top:3px や色値・JS コメント内の数字などであり、z-index 宣言ではない抽出誤検知と判断できるため。 |

---

検査ファイル数: 13 / 抽出値: 349 種（AI仮対応 93、保留 223、除外 33）
