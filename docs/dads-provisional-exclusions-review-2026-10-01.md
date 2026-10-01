# DS仮対応31・除外27の追加照合（未承認）

> 現行状態の追記: 本文は承認前の調査baselineとして保持。ユーザーの細部選定の明示委任後の確定判断・適用/未適用区分は[現行決定表](dads-current-decisions-2026-10-01.md)を参照。「未承認」「人間判断待ち」は本文作成当時の状態であり、現在の委任範囲の選定を停止させるものではない。全出現の実装完了・上流DS採用を意味しない。

作成日: 2026-10-01。**追加の調査資料のみ。mapping.md、baseline、未決85提案、製品コードの値・判定は変更していない。** A〜Fは[未決85提案](dads-mapping-review-proposal-2026-10-01.md)の判断群に対応する。親への方向性承認依頼は、この58行の承認や個別mapping確定とは扱わない。

## 根拠・対象・限界

実在するdigital-design-system commit `6051bceb67c60fb805b757c22bbd66f3318ea980`の[semantic.css](https://github.com/sera-inc/digital-design-system/blob/6051bceb67c60fb805b757c22bbd66f3318ea980/tokens/semantic.css)・Layer 1の参照先・inventory.mjsを照合。私有DS原本を転載せず、候補と数値の関係のみ記録した。文字サイズ換算はroot16px時。12px補助/labelはDS独自DEV-001。z階層もDS自身の自社定義で、DADS公式規定ではない。

対象は旧mappingのAI仮対応31と除外27、計58行。各行の安定キーはカテゴリ＋旧実装値、行番号は作成時の補助参照。表の証拠は宣言をregexで抽出し、代表箇所を最大2件示す。CSSの有効/無効・カスケード優先順位の網羅判定、目視承認、実行テストは本調査の範囲外。同じ値の全用途を一括承認する表ではない。既存baselineの回数を書き換えず、現状の追加出現とは区別した。

## 優先して訂正判断が必要な点

- **除外27のうち19行に、除外理由を否定する実宣言がある。** フォント9値（18/20/21/24/27/28/29/30/32px）、余白5値（1.5/27/36/45/50px）、角丸5値（0/1/2/3/11px）。未決85の集計に自動加算していない。人間が判定を訂正する際に再集計する。
- **8px余白→space-2は16pxへの倍増**。等値候補はspace-1。同値だから同用途とも限らず、負値やshorthandを保存する。
- **guardのz最大値→toast500は境界の誤認**。任意の第三者ページの重なりと競合するため、portalのグローバル階層へ機械統合しない。拡張ソースとportal配布コピーの両方に存在する。
- **白→surface、11px/9.5px→label、15pxは全てh3/h4という判断は文脈不一致**。暗色文字/合成、本文/補助/表、ブランド名を分ける。
- **角丸50%とfull、上角のみと単一radiusは非等価の場合がある**。Microsoft四色は実在するSVG描画色で、除外の適切な理由は第三者ブランド維持。

全58行を以下に列挙する。確認できたことと未承認の候補を分離し、誤除外を隠してPhase 1完了と主張しない。


## 色

| ID・元行キー | 旧判定・候補 | 実装証拠（代表） | 調査所見・人間判断候補 |
|---|---|---|---|
| R01 色 `#ffffff` / [元L54](mapping.md#L54) | AI仮対応 / `--app-surface` | [extension/demo/index.html:31](../extension/demo/index.html#L31)<br>[extension/demo/index.html:38](../extension/demo/index.html#L38) | 誤った用途推定。現在は暗色文字とhover合成のfallbackで、白い面の一括surface化は不可。text-inverse相当とhover-overlay相当を分離（C/F）。 |
| R02 色 `#10003` / [元L56](mapping.md#L56) | 除外 / `除外` | [portal/app/static/index.html:3893](../portal/app/static/index.html#L3893)<br>[portal/app/static/index.html:4907](../portal/app/static/index.html#L4907) | 除外根拠は妥当。HTML文字参照のチェック記号であり色宣言ではない。 |
| R03 色 `#00a4ef` / [元L60](mapping.md#L60) | 除外 / `除外` | [portal/app/static/index.html:1461](../portal/app/static/index.html#L1461) | MicrosoftロゴのSVG fillとして実在する描画色。「色でない誤検知」は不正確。第三者ブランド維持を理由とする除外候補。一般UIへ転用しない。 |
| R04 色 `#7fba00` / [元L63](mapping.md#L63) | 除外 / `除外` | [portal/app/static/index.html:1460](../portal/app/static/index.html#L1460) | MicrosoftロゴのSVG fillとして実在する描画色。「色でない誤検知」は不正確。第三者ブランド維持を理由とする除外候補。一般UIへ転用しない。 |
| R05 色 `#f25022` / [元L65](mapping.md#L65) | 除外 / `除外` | [portal/app/static/index.html:1459](../portal/app/static/index.html#L1459) | MicrosoftロゴのSVG fillとして実在する描画色。「色でない誤検知」は不正確。第三者ブランド維持を理由とする除外候補。一般UIへ転用しない。 |
| R06 色 `#ffb900` / [元L68](mapping.md#L68) | 除外 / `除外` | [portal/app/static/index.html:1462](../portal/app/static/index.html#L1462) | MicrosoftロゴのSVG fillとして実在する描画色。「色でない誤検知」は不正確。第三者ブランド維持を理由とする除外候補。一般UIへ転用しない。 |

## フォントサイズ

| ID・元行キー | 旧判定・候補 | 実装証拠（代表） | 調査所見・人間判断候補 |
|---|---|---|---|
| R07 フォントサイズ `11px` / [元L76](mapping.md#L76) | AI仮対応 / `--app-text-label-size` | [portal/app/static/enterprise.css:38](../portal/app/static/enterprise.css#L38)<br>[portal/app/static/enterprise.css:1310](../portal/app/static/enterprise.css#L1310) | 用途混在。表セル・入力・ボタン・補足・見出しがある。label12一括は不可。body/table14、補助12、heading別に分割し、幅/行高を再検証（A）。 |
| R08 フォントサイズ `9.5px` / [元L82](mapping.md#L82) | AI仮対応 / `--app-text-label-size` | [portal/app/static/enterprise.css:31](../portal/app/static/enterprise.css#L31)<br>[portal/app/static/enterprise.css:498](../portal/app/static/enterprise.css#L498) | labelだけではない。説明段落・脚注・入力にも存在。本文14/補助12/label12に用途別分割し、折返しと入力幅を検証（A）。 |
| R09 フォントサイズ `15px` / [元L88](mapping.md#L88) | AI仮対応 / `--app-text-heading-sm-size` | [portal/app/static/enterprise.css:998](../portal/app/static/enterprise.css#L998)<br>[portal/app/static/index.html:84](../portal/app/static/index.html#L84) | 「すべてh3/h4」は誤り。brand spanも含む。見出し18とブランド固有表現を分離（A）。 |
| R10 フォントサイズ `20px` / [元L92](mapping.md#L92) | 除外 / `除外` | [portal/app/static/enterprise.css:535](../portal/app/static/enterprise.css#L535)<br>[portal/app/static/enterprise.css:1043](../portal/app/static/enterprise.css#L1043) | 誤除外。font-size実宣言あり。heading20とKPI32を用途別候補として審査（A）。 |
| R11 フォントサイズ `18px` / [元L95](mapping.md#L95) | 除外 / `除外` | [portal/app/static/enterprise.css:1238](../portal/app/static/enterprise.css#L1238)<br>[portal/app/static/enterprise.css:1551](../portal/app/static/enterprise.css#L1551) | 誤除外。font-size実宣言あり。比率の単位とcompact数値を分け、用途別候補を審査（A）。 |
| R12 フォントサイズ `21px` / [元L96](mapping.md#L96) | 除外 / `除外` | [portal/app/static/enterprise.css:99](../portal/app/static/enterprise.css#L99)<br>[portal/app/static/enterprise.css:147](../portal/app/static/enterprise.css#L147) | 誤除外。font-size実宣言あり。見出し20/24とKPI32を用途別候補として審査（A）。 |
| R13 フォントサイズ `24px` / [元L97](mapping.md#L97) | 除外 / `除外` | [portal/app/static/enterprise.css:1019](../portal/app/static/enterprise.css#L1019)<br>[portal/app/static/enterprise.css:1134](../portal/app/static/enterprise.css#L1134) | 誤除外。font-size実宣言あり。KPI32（見出し役割なら24）を用途別候補として審査（A）。 |
| R14 フォントサイズ `28px` / [元L98](mapping.md#L98) | 除外 / `除外` | [portal/app/static/enterprise.css:1057](../portal/app/static/enterprise.css#L1057)<br>[portal/app/static/enterprise.css:1192](../portal/app/static/enterprise.css#L1192) | 誤除外。font-size実宣言あり。見出し24とKPI32を用途別候補として審査（A）。 |
| R15 フォントサイズ `30px` / [元L99](mapping.md#L99) | 除外 / `除外` | [portal/app/static/enterprise.css:259](../portal/app/static/enterprise.css#L259)<br>[portal/app/static/enterprise.css:955](../portal/app/static/enterprise.css#L955) | 誤除外。font-size実宣言あり。KPI32とCLI認証コードの専用可読性を用途別候補として審査（A）。 |
| R16 フォントサイズ `7.5px` / [元L100](mapping.md#L100) | AI仮対応 / `--app-text-label-size` | [portal/app/static/enterprise.css:860](../portal/app/static/enterprise.css#L860)<br>[portal/app/static/enterprise.css:872](../portal/app/static/enterprise.css#L872) | ラベル・表見出しの候補としてlabel12。ただし60%拡大となるため表幅・行高の確認が必須。12pxはDS独自DEV-001でDADS標準最小値ではない（A）。 |
| R17 フォントサイズ `27px` / [元L103](mapping.md#L103) | 除外 / `除外` | [portal/app/static/enterprise.css:225](../portal/app/static/enterprise.css#L225)<br>[portal/app/static/enterprise.css:1504](../portal/app/static/enterprise.css#L1504) | 誤除外。font-size実宣言あり。KPI32と姿勢表示見出しを用途別候補として審査（A）。 |
| R18 フォントサイズ `.9em` / [元L104](mapping.md#L104) | AI仮対応 / `--app-text-numeric-size` | [portal/app/static/index.html:60](../portal/app/static/index.html#L60) | codeとmonoの相対サイズ。numeric14は候補だが親サイズによって現在値が異なる。コードを数値専用用途と同一視せず、全親コンテキスト確認（A）。 |
| R19 フォントサイズ `1.05em` / [元L105](mapping.md#L105) | AI仮対応 / `--app-text-heading-sm-size` | [extension/demo/index.html:45](../extension/demo/index.html#L45) | デモh2→heading-sm18候補。相対emからremに変わるため親フォント拡大条件と行高もセットで確認（A/F）。 |
| R20 フォントサイズ `1.4em` / [元L106](mapping.md#L106) | AI仮対応 / `--app-text-heading-lg-size` | [extension/demo/index.html:45](../extension/demo/index.html#L45) | デモh1→heading-lg24候補。相対サイズの意味と読み上げ見出し階層を維持（A/F）。 |
| R21 フォントサイズ `15.5px` / [元L108](mapping.md#L108) | AI仮対応 / `--app-text-heading-sm-size` | [portal/app/static/index.html:194](../portal/app/static/index.html#L194) | 実在.card-name。heading-sm18は候補だがCSSクラスだけで見出しと確定しない。カード内のDOM役割・折返しを確認（A）。 |
| R22 フォントサイズ `29px` / [元L109](mapping.md#L109) | 除外 / `除外` | [portal/app/static/enterprise.css:1505](../portal/app/static/enterprise.css#L1505) | 誤除外。font-size実宣言あり。モバイルKPI32を用途別候補として審査（A）。 |
| R23 フォントサイズ `32px` / [元L110](mapping.md#L110) | 除外 / `除外` | [portal/app/static/enterprise.css:1016](../portal/app/static/enterprise.css#L1016) | 誤除外。font-size実宣言あり。display-sm32（等値）を用途別候補として審査（A）。 |

## 余白

| ID・元行キー | 旧判定・候補 | 実装証拠（代表） | 調査所見・人間判断候補 |
|---|---|---|---|
| R24 余白 `8px` / [元L117](mapping.md#L117) | AI仮対応 / `--app-space-2` | [extension/demo/index.html:55](../extension/demo/index.html#L55)<br>[extension/src/guard.js:318](../extension/src/guard.js#L318) | 数値不一致の誤対応。space-2は16pxなので2倍になる。等値候補はspace-1=8px。用途と負値符号を確認して人間が訂正（B）。 |
| R25 余白 `16px` / [元L121](mapping.md#L121) | AI仮対応 / `--app-space-2` | [portal/app/static/enterprise.css:172](../portal/app/static/enterprise.css#L172)<br>[portal/app/static/enterprise.css:203](../portal/app/static/enterprise.css#L203) | 既存候補は数値一致。余白宣言の各成分のみ置換する候補で、負号・0・複合値は保持。用途/レスポンシブ/固定要素の予約を確認（B）。 |
| R26 余白 `4px` / [元L122](mapping.md#L122) | AI仮対応 / `--app-space-05` | [extension/src/guard.js:307](../extension/src/guard.js#L307)<br>[portal/app/static/enterprise.css:59](../portal/app/static/enterprise.css#L59) | 既存候補は数値一致。余白宣言の各成分のみ置換する候補で、負号・0・複合値は保持。用途/レスポンシブ/固定要素の予約を確認（B）。 |
| R27 余白 `45px` / [元L139](mapping.md#L139) | 除外 / `除外` | [portal/app/static/enterprise.css:1145](../portal/app/static/enterprise.css#L1145)<br>[portal/app/static/enterprise.css:1211](../portal/app/static/enterprise.css#L1211) | 誤除外。padding/margin実宣言あり。drawer底部・編集toolbar予約・main底部が混在。予約高を保った構造改修と通常余白を分離（B）。 |
| R28 余白 `32px` / [元L142](mapping.md#L142) | AI仮対応 / `--app-space-4` | [extension/demo/index.html:43](../extension/demo/index.html#L43)<br>[portal/app/static/enterprise.css:952](../portal/app/static/enterprise.css#L952) | 既存候補は数値一致。余白宣言の各成分のみ置換する候補で、負号・0・複合値は保持。用途/レスポンシブ/固定要素の予約を確認（B）。 |
| R29 余白 `40px` / [元L149](mapping.md#L149) | AI仮対応 / `--app-space-5` | [portal/app/static/enterprise.css:182](../portal/app/static/enterprise.css#L182)<br>[portal/app/static/enterprise.css:1517](../portal/app/static/enterprise.css#L1517) | 既存候補は数値一致。余白宣言の各成分のみ置換する候補で、負号・0・複合値は保持。用途/レスポンシブ/固定要素の予約を確認（B）。 |
| R30 余白 `64px` / [元L151](mapping.md#L151) | AI仮対応 / `--app-space-8` | [portal/app/static/enterprise.css:421](../portal/app/static/enterprise.css#L421)<br>[portal/app/static/enterprise.css:426](../portal/app/static/enterprise.css#L426) | space-8=64pxで等値だがregister-editor/recordの左列揃え。両方同時維持し、通常余白と列オフセットを区別（B）。 |
| R31 余白 `1.5px` / [元L152](mapping.md#L152) | 除外 / `除外` | [portal/app/static/index.html:166](../portal/app/static/index.html#L166) | 誤除外。padding/margin実宣言あり。pillの上下padding。line-height/目標操作高を合わせて0/4等へ寄せるか構造例外を審査（B）。 |
| R32 余白 `27px` / [元L155](mapping.md#L155) | 除外 / `除外` | [portal/app/static/enterprise.css:251](../portal/app/static/enterprise.css#L251) | 誤除外。padding/margin実宣言あり。ssmain内padding。通常space-3=24/space-4=32への統合候補を面サイズで判断（B）。 |
| R33 余白 `36px` / [元L156](mapping.md#L156) | 除外 / `除外` | [portal/app/static/enterprise.css:1174](../portal/app/static/enterprise.css#L1174) | 誤除外。padding/margin実宣言あり。nav-childの右側操作予約。単純32化よりpin/展開ボタンの占有幅を確認（B）。 |
| R34 余白 `48px` / [元L158](mapping.md#L158) | AI仮対応 / `--app-space-6` | [portal/app/static/enterprise.css:1115](../portal/app/static/enterprise.css#L1115) | 既存候補は数値一致。余白宣言の各成分のみ置換する候補で、負号・0・複合値は保持。用途/レスポンシブ/固定要素の予約を確認（B）。 |
| R35 余白 `50px` / [元L159](mapping.md#L159) | 除外 / `除外` | [portal/app/static/enterprise.css:1190](../portal/app/static/enterprise.css#L1190) | 誤除外。padding/margin実宣言あり。main底padding。space-6=48候補だが固定footer/設定バーとの重なりを確認（B）。 |

## 角丸

| ID・元行キー | 旧判定・候補 | 実装証拠（代表） | 調査所見・人間判断候補 |
|---|---|---|---|
| R36 角丸 `8px` / [元L168](mapping.md#L168) | AI仮対応 / `--app-radius-md` | [extension/demo/index.html:62](../extension/demo/index.html#L62)<br>[portal/app/static/enterprise.css:70](../portal/app/static/enterprise.css#L70) | 既存候補は数値一致。単一角丸として候補を維持できるが、extension/デモではtoken可用性を別確認。注入先グローバルCSS依存を追加しない（D/F）。 |
| R37 角丸 `12px` / [元L169](mapping.md#L169) | AI仮対応 / `--app-radius-lg` | [portal/app/static/enterprise.css:111](../portal/app/static/enterprise.css#L111)<br>[portal/app/static/enterprise.css:203](../portal/app/static/enterprise.css#L203) | 既存候補は数値一致。単一角丸として候補を維持できるが、extension/デモではtoken可用性を別確認。注入先グローバルCSS依存を追加しない（D/F）。 |
| R38 角丸 `7px` / [元L170](mapping.md#L170) | AI仮対応 / `--app-radius-sm` | [portal/app/static/enterprise.css:20](../portal/app/static/enterprise.css#L20)<br>[portal/app/static/enterprise.css:27](../portal/app/static/enterprise.css#L27) | 数値統合であり等値ではない。7px→6pxの候補を部品の大小だけで確定せず、親子の接続・クリップ・メニューの角を確認（D）。 |
| R39 角丸 `10px` / [元L171](mapping.md#L171) | AI仮対応 / `--app-radius-lg` | [extension/demo/index.html:51](../extension/demo/index.html#L51)<br>[portal/app/static/enterprise.css:112](../portal/app/static/enterprise.css#L112) | 数値統合であり等値ではない。10px→12pxの候補を部品の大小だけで確定せず、親子の接続・クリップ・メニューの角を確認（D）。 |
| R40 角丸 `4px` / [元L172](mapping.md#L172) | AI仮対応 / `--app-radius-xs` | [extension/demo/index.html:56](../extension/demo/index.html#L56)<br>[extension/demo/index.html:59](../extension/demo/index.html#L59) | 既存候補は数値一致。単一角丸として候補を維持できるが、extension/デモではtoken可用性を別確認。注入先グローバルCSS依存を追加しない（D/F）。 |
| R41 角丸 `6px` / [元L173](mapping.md#L173) | AI仮対応 / `--app-radius-sm` | [extension/src/guard.js:287](../extension/src/guard.js#L287)<br>[portal/app/static/enterprise.css:55](../portal/app/static/enterprise.css#L55) | 既存候補は数値一致。単一角丸として候補を維持できるが、extension/デモではtoken可用性を別確認。注入先グローバルCSS依存を追加しない（D/F）。 |
| R42 角丸 `9px` / [元L174](mapping.md#L174) | AI仮対応 / `--app-radius-md` | [portal/app/static/enterprise.css:19](../portal/app/static/enterprise.css#L19)<br>[portal/app/static/enterprise.css:116](../portal/app/static/enterprise.css#L116) | 数値統合であり等値ではない。9px→8pxの候補を部品の大小だけで確定せず、親子の接続・クリップ・メニューの角を確認（D）。 |
| R43 角丸 `50%` / [元L175](mapping.md#L175) | AI仮対応 / `--app-radius-full` | [portal/app/static/enterprise.css:44](../portal/app/static/enterprise.css#L44)<br>[portal/app/static/enterprise.css:56](../portal/app/static/enterprise.css#L56) | fullは624.9375rem（root16で9999px）。正方形の円は同形でも非正方形は楕円からピルへ変わり得る。形状・縦横比を全箇所確認（D）。 |
| R44 角丸 `99px` / [元L176](mapping.md#L176) | AI仮対応 / `--app-radius-full` | [portal/app/static/enterprise.css:31](../portal/app/static/enterprise.css#L31)<br>[portal/app/static/enterprise.css:332](../portal/app/static/enterprise.css#L332) | pill用full候補。現在値より大きい624.9375remへ変わるため全対象の寸法と丸まりを確認。短辺が旧半径の2倍を超える要素では同形とは限らない（D）。 |
| R45 角丸 `0` / [元L177](mapping.md#L177) | 除外 / `除外` | [portal/app/static/enterprise.css:58](../portal/app/static/enterprise.css#L58)<br>[portal/app/static/enterprise.css:59](../portal/app/static/enterprise.css#L59) | 誤除外。border-radius実宣言あり。tabs、stats、note等の接続境界。0を構造例外とする候補（D）。 |
| R46 角丸 `3px` / [元L178](mapping.md#L178) | 除外 / `除外` | [portal/app/static/enterprise.css:115](../portal/app/static/enterprise.css#L115)<br>[portal/app/static/enterprise.css:798](../portal/app/static/enterprise.css#L798) | 誤除外。border-radius実宣言あり。dot/bar等の小形状。xs4は候補だが高さ2〜5pxに対する丸まり比率を検証（D）。 |
| R47 角丸 `5px` / [元L179](mapping.md#L179) | AI仮対応 / `--app-radius-xs` | [extension/demo/index.html:48](../extension/demo/index.html#L48)<br>[portal/app/static/enterprise.css:677](../portal/app/static/enterprise.css#L677) | 数値統合であり等値ではない。5px→4pxの候補を部品の大小だけで確定せず、親子の接続・クリップ・メニューの角を確認（D）。 |
| R48 角丸 `var(--app-radius-md)` / [元L180](mapping.md#L180) | 除外 / `除外` | [portal/app/static/dads-product.css:324](../portal/app/static/dads-product.css#L324)<br>[portal/app/static/dads-product.css:369](../portal/app/static/dads-product.css#L369) | token参照を生値として数えたため生値一覧からの除外候補は妥当。ただしトークン定義・読み込み順・fallback・computed style検証自体は省略しない。 |
| R49 角丸 `2px` / [元L181](mapping.md#L181) | 除外 / `除外` | [portal/app/static/enterprise.css:392](../portal/app/static/enterprise.css#L392)<br>[portal/app/static/enterprise.css:1721](../portal/app/static/enterprise.css#L1721) | 誤除外。border-radius実宣言あり。legend/graph/bar等の形状。装飾の意味・寸法比率を維持する例外も候補（D）。 |
| R50 角丸 `var(--radius-sm)` / [元L182](mapping.md#L182) | AI仮対応 / `--app-radius-sm` | [portal/app/static/enterprise.css:35](../portal/app/static/enterprise.css#L35)<br>[portal/app/static/enterprise.css:45](../portal/app/static/enterprise.css#L45) | 既存--radius-smはenterprise.css:9で7px。DS sm=6pxなので等値移行ではない。mobile-nav/back/export等の1px縮小を審査（D）。 |
| R51 角丸 `11px` / [元L183](mapping.md#L183) | 除外 / `除外` | [portal/app/static/enterprise.css:223](../portal/app/static/enterprise.css#L223)<br>[portal/app/static/enterprise.css:747](../portal/app/static/enterprise.css#L747) | 誤除外。border-radius実宣言あり。stats/health面。lg12候補として親子クリップ・影を確認（D）。 |
| R52 角丸 `var(--app-radius-sm)` / [元L184](mapping.md#L184) | 除外 / `除外` | [portal/app/static/dads-product.css:332](../portal/app/static/dads-product.css#L332)<br>[portal/app/static/dads-product.css:475](../portal/app/static/dads-product.css#L475) | token参照を生値として数えたため生値一覧からの除外候補は妥当。ただしトークン定義・読み込み順・fallback・computed style検証自体は省略しない。 |
| R53 角丸 `1px` / [元L189](mapping.md#L189) | 除外 / `除外` | [portal/app/static/enterprise.css:1289](../portal/app/static/enterprise.css#L1289) | 誤除外。border-radius実宣言あり。source dots。単純xs4では形が変わるため構造例外または図形再設計（D）。 |
| R54 角丸 `4px 4px 0 0` / [元L191](mapping.md#L191) | AI仮対応 / `--app-radius-xs` | [portal/app/static/enterprise.css:61](../portal/app/static/enterprise.css#L61) | 上角のみのtabs下線。宣言全体をradius-xs1個にすると下角も丸くなる。var(xs) var(xs) 0 0と成分単位に保持する候補（D）。 |
| R55 角丸 `999px` / [元L192](mapping.md#L192) | AI仮対応 / `--app-radius-full` | [portal/app/static/index.html:664](../portal/app/static/index.html#L664) | pill用full候補。現在値より大きい624.9375remへ変わるため全対象の寸法と丸まりを確認。短辺が旧半径の2倍を超える要素では同形とは限らない（D）。 |
| R56 角丸 `var(--app-radius-sm) var(--app-radius-sm` / [元L194](mapping.md#L194) | 除外 / `除外` | [portal/app/static/dads-product.css:364](../portal/app/static/dads-product.css#L364) | 40文字の抽出上限で切れたshorthand。実宣言を全文確認し、既存token参照として扱う候補。複数角の0を失わない。 |

## z-index

| ID・元行キー | 旧判定・候補 | 実装証拠（代表） | 調査所見・人間判断候補 |
|---|---|---|---|
| R57 z-index `60` / [元L202](mapping.md#L202) | AI仮対応 / `--app-z-popover` | [portal/app/static/index.html:109](../portal/app/static/index.html#L109)<br>[portal/app/static/index.html:349](../portal/app/static/index.html#L349) | tooltipだけでなくusermenu/setuppanel/動的popoverに存在。popover400候補は全体z順序・tour・drawerと連動しなければ覆い隠しが生じる（E）。 |
| R58 z-index `2147483647` / [元L204](mapping.md#L204) | AI仮対応 / `--app-z-toast` | [extension/src/guard.js:284](../extension/src/guard.js#L284)<br>[portal/extension-src/guard.js:284](../portal/extension-src/guard.js#L284) | 高リスク仮対応。第三者ページに注入するguardをportal toast500へ落とすと対象ページの要素に埋もれる。最大値保持を第一候補に外部境界として別審査。portal tokensの存在も保証されない（E/F）。 |

## 実装へ進む前の確認

1. 人間が誤除外の訂正、用途分割、候補採否・統合/構造例外を記録し、件数を再計算する。今回の資料は確定欄を代筆しない。
2. 宣言を変更する場合はカスケード・メディア条件を確認し、表/暗色/狭幅/拡張ガードを対象に変更箇所へ絞った回帰検証を追加する。
3. 現行31仮対応を承認済みとして85行だけ解消してもPhase 1完了とはならない。除外理由を含む全143キーのレビュー記録が必要。
