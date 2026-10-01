# 承認済みA/B/D: portalの役割別文字・通常余白・角丸（2026-10-01）

ユーザーの「すすめてよい」により本文14px／補助12px／見出し18px／主要数値32px、通常余白4・8・16・24・32px（特殊配置保持）、カード12px／メニュー6pxの方向性が明示承認された。全85項目・配布方式・人間の画面レビューが完了したという意味ではない。

実参照: digital-design-system `6051bce` の `tokens/semantic.css`。原本の複製・変更はしていない。既存の `--app-text-body-size`(14)、`--app-text-body-sm-size`/label(12)、`--app-text-heading-sm-size`(18)、`--app-text-display-sm-size`(32)、`--app-space-05/1/2/3/4`(4/8/16/24/32)、`--app-radius-lg/sm`(12/6)を使用。root16px換算であり拡大可能なrem tokenを維持する。

## 変更と役割

- enterprise.cssの各文字selectorを用途別に分離。compact/mobileの小字化指定も同じ読みやすい階層へ。複合selectorで本文と補助が混在する規則は分割し、その他宣言を保持。
- index.htmlの実HTML/template内の補助span・small・label・説明・ID・タイムスタンプ41箇所を12pxの補助tokenへ。追加でinline見出し2件18px、設定強調2件14px、開閉操作summary/メール入力本文を14pxへ。JS動作・API・色・z値は触っていない。
- 後勝ちadapterでページ見出し18px、統計値32px、tableセル14px/header12px、ログイン等card12px、アカウント/設定/ナビmenu6pxを明示。
- 通常余白: card16px、SSO面24px、step8px、タブ間16px/下24px、tenant gap8px、KPI内16px、panel16px、source grid8×16px、code行8×16px、compact table8×16px。

## 特殊値を保持した範囲

- nav/tenant/accountのchevronとglyph、ゼロ文字によるアイコン化、avatar/ツールinitial寸法はテキスト階層と分離。図ノードの位置/幅/接続線/円形/ringの寸法は維持。
- overview gridの18px gapと半幅`calc(50% - 9px)`、compact10px gap/5px補正、editor toolbarの44px予約、drag/drop座標・高さ・固定offsetを保持。一般余白としての機械的丸めはしていない。
- circle/full pill、table継承/0、input/ボタン形状は「card12/menu6」へ一括置換していない。カード下端のstack stripだけ親cardと12pxで接続。
- Fの認証/配布、z操作、暗色配色はこの担当の変更外。

## 必要な実測（QA担当による統合後実行）

1440/390pxと明暗/compactで折返し・overflow・KPI桁数・table行高・SSO・設定・login・device一覧・budget・evidence・drawer・popover・overview編集/stack/dropを確認。特殊な図の小さなlabelは文字12px化後に線/箱と重ならないことを確認。既存全体回帰も統合後に行う。**本資料自体は検証成功報告ではない。**

## enterprise.cssの役割別対応selector（重複宣言は統合表示）

以下は実ソースの文字宣言一覧。後勝ちadapterに記載したtable/headerなどはより具体的な役割で上書きする。

| selector | 適用token |
|---|---|
| `nav button` | `--app-text-body-size` |
| `nav .count` | `--app-text-body-sm-size` |
| `.top-context b` | `--app-text-body-size` |
| `.top-context span` | `--app-text-body-sm-size` |
| `.search-key` | `--app-text-body-sm-size` |
| `.live-state` | `--app-text-body-sm-size` |
| `.topbar #who` | `--app-text-body-sm-size` |
| `.meta-chip` | `--app-text-body-sm-size` |
| `table` | `--app-text-body-size` |
| `.card h3` | `--app-text-heading-sm-size` |
| `.card-meta` | `--app-text-body-sm-size` |
| `h2` | `--app-text-heading-sm-size` |
| `.lede` | `--app-text-body-size` |
| `.src-note` | `--app-text-body-sm-size` |
| `.note` | `--app-text-body-sm-size` |
| `.view-head h2` | `--app-text-heading-sm-size` |
| `.trust-state` | `--app-text-body-sm-size` |
| `.tabs button` | `--app-text-body-sm-size` |
| `.posture-copy span` | `--app-text-body-sm-size` |
| `.posture-copy strong` | `--app-text-heading-sm-size` |
| `.posture-copy p` | `--app-text-body-sm-size` |
| `.posture-fact b` | `--app-text-display-sm-size` |
| `.posture-fact span` | `--app-text-body-sm-size` |
| `.gcard>.stats dt` | `--app-text-display-sm-size` |
| `.gcard>.stats dd` | `--app-text-body-sm-size` |
| `.card-name` | `--app-text-heading-sm-size` |
| `.card-section` | `--app-text-body-sm-size` |
| `.card-kv` | `--app-text-body-size` |
| `.card-kv dt` | `--app-text-body-sm-size` |
| `.drawer h2` | `--app-text-heading-sm-size` |
| `.ag-verdict` | `--app-text-display-sm-size` |
| `.ag-node b` | `--app-text-body-sm-size` |
| `.ag-node i` | `--app-text-body-sm-size` |
| `#usermenu .umhead span` | `--app-text-body-sm-size` |
| `#setupbell .bcount` | `--app-text-body-sm-size` |
| `.register-toolbar>div span` | `--app-text-body-sm-size` |
| `.register-legend` | `--app-text-body-sm-size` |
| `.reg-export` | `--app-text-body-size` |
| `.register-cell small` | `--app-text-body-sm-size` |
| `.register-cell .gov-sub` | `--app-text-body-sm-size` |
| `.register-cell .pill` | `--app-text-body-sm-size` |
| `.register-risk-value` | `--app-text-numeric-size` |
| `.decision-widget-head p` | `--app-text-body-sm-size` |
| `.decision-widget-head>.count` | `--app-text-body-sm-size` |
| `.decision-section-head strong` | `--app-text-body-sm-size` |
| `.decision-section-head>div>span` | `--app-text-body-sm-size` |
| `.decision-section-head>.count` | `--app-text-body-sm-size` |
| `.candidate-identity>strong` | `--app-text-body-size` |
| `.candidate-identity>p` | `--app-text-body-sm-size` |
| `.candidate-suggestion` | `--app-text-body-sm-size` |
| `.candidate-scope b` | `--app-text-body-size` |
| `.candidate-scope span` | `--app-text-body-sm-size` |
| `.candidate-linker select.mfield` | `--app-text-body-sm-size` |
| `.undecided-list>a>strong` | `--app-text-body-size` |
| `.undecided-list time` | `--app-text-body-sm-size` |
| `.decision-footer` | `--app-text-body-sm-size` |
| `.trend-heading h3` | `--app-text-heading-sm-size` |
| `.trend-heading p` | `--app-text-body-sm-size` |
| `.exposure-chart>.clegend` | `--app-text-body-sm-size` |
| `.exposure-trend-card .tdays` | `--app-text-body-sm-size` |
| `.executive-posture>strong` | `--app-text-heading-sm-size` |
| `.widget-picker-head strong` | `--app-text-heading-sm-size` |
| `.widget-picker-head>div>span,.widget-picker-foot>div>span` | `--app-text-body-sm-size` |
| `.widget-enabled-count` | `--app-text-body-sm-size` |
| `.widget-choice-title` | `--app-text-body-sm-size` |
| `.widget-choice-desc` | `--app-text-body-sm-size` |
| `.widget-choice-meta` | `--app-text-body-sm-size` |
| `.widget-picker-foot strong` | `--app-text-body-sm-size` |
| `.evidence-summary-lead>span` | `--app-text-body-sm-size` |
| `.evidence-summary-lead>p` | `--app-text-body-sm-size` |
| `.evidence-summary dd` | `--app-text-body-sm-size` |
| `.evidence-summary dd small` | `--app-text-body-sm-size` |
| `.evidence-panel-head h3` | `--app-text-heading-sm-size` |
| `.evidence-panel-head p` | `--app-text-body-sm-size` |
| `.evidence-panel-head>span` | `--app-text-body-sm-size` |
| `.evidence-columns` | `--app-text-body-sm-size` |
| `.evidence-theme>span` | `--app-text-body-sm-size` |
| `.evidence-theme strong` | `--app-text-body-size` |
| `.evidence-statement` | `--app-text-body-size` |
| `.evidence-source a` | `--app-text-body-size` |
| `.evidence-source>span` | `--app-text-body-sm-size` |
| `.evidence-review-copy>span` | `--app-text-body-sm-size` |
| `.evidence-review-copy h3` | `--app-text-heading-sm-size` |
| `.evidence-review-copy p` | `--app-text-body-sm-size` |
| `.evidence-review-items>a` | `--app-text-body-size` |
| `.evidence-review-items>p` | `--app-text-body-sm-size` |
| `.evidence-footnote` | `--app-text-body-sm-size` |
| `.evidence-footnote strong` | `--app-text-body-sm-size` |
| `.view-meta .meta-chip` | `--app-text-body-sm-size` |
| `.view-meta button.mini` | `--app-text-body-size` |
| `.meta-export` | `--app-text-body-sm-size` |
| `.nav-pinned>span` | `--app-text-body-sm-size` |
| `#navflyout .navfly-title` | `--app-text-body-sm-size` |
| `.budget-wizard .kv .bw-tool-picker` | `--app-text-body-sm-size` |
| `.budget-wizard .kv .bw-provider-picker` | `--app-text-body-sm-size` |
| `.budget-wizard .tiers thead th` | `--app-text-body-sm-size` |
| `.health-summary-copy>span,.health-card-head>div>span,.health-deployment>div>span,.health-activity .health-card-head>div>span` | `--app-text-body-sm-size` |
| `.health-summary-copy>strong` | `--app-text-heading-sm-size` |
| `.health-summary-copy>p` | `--app-text-body-sm-size` |
| `.health-summary dt` | `--app-text-display-sm-size` |
| `.health-summary dd` | `--app-text-body-sm-size` |
| `.health-intro` | `--app-text-body-sm-size` |
| `.health-card-head h3` | `--app-text-heading-sm-size` |
| `.health-card-head>span:last-child:not(.pill)` | `--app-text-body-sm-size` |
| `.health-facts dt` | `--app-text-body-sm-size` |
| `.health-facts dd` | `--app-text-body-size` |
| `.health-note` | `--app-text-body-sm-size` |
| `.health-deployment h3` | `--app-text-heading-sm-size` |
| `.health-deployment p` | `--app-text-body-sm-size` |
| `.health-deployment dt` | `--app-text-body-sm-size` |
| `.health-deployment dd` | `--app-text-body-size` |
| `.window-pick` | `--app-text-body-sm-size` |
| `.window-pick select` | `--app-text-body-size` |
| `.qr-head` | `--app-text-body-sm-size` |
| `.qr-item` | `--app-text-body-size` |
| `.qr-kind` | `--app-text-body-sm-size` |
| `.qr-none` | `--app-text-body-size` |
| `.print-head` | `--app-text-body-sm-size` |
| `.budget-eyebrow,.budget-section-head>div>span` | `--app-text-body-sm-size` |
| `.budget-card-copy` | `--app-text-body-sm-size` |
| `.budget-renewal` | `--app-text-body-sm-size` |
| `.budget-disclosure` | `--app-text-body-sm-size` |
| `.budget-disclosure b` | `--app-text-body-sm-size` |
| `.budget-card-body>.note` | `--app-text-body-sm-size` |
| `.budget-kpis em` | `--app-text-body-sm-size` |
| `.budget-kpis small` | `--app-text-body-sm-size` |
| `.budget-section-head h4` | `--app-text-heading-sm-size` |
| `.budget-section-head>span` | `--app-text-body-sm-size` |
| `.budget-tier-table th` | `--app-text-body-sm-size` |
| `.budget-tier-table td` | `--app-text-body-size` |
| `.budget-data-note` | `--app-text-body-sm-size` |
| `.budget-details summary` | `--app-text-body-size` |
| `.budget-details>ul` | `--app-text-body-size` |
| `.budget-details>table th` | `--app-text-body-sm-size` |
| `.budget-details>table td` | `--app-text-body-size` |
| `.budget-add-member>span` | `--app-text-body-sm-size` |
| `.budget-add-member .mfield` | `--app-text-body-size` |
| `.window-field select` | `--app-text-body-size` |
| `.act-entry .mfield` | `--app-text-body-size` |
| `.upgrade-run-head` | `--app-text-body-size` |
| `.upgrade-run-head>span` | `--app-text-body-sm-size` |
| `.upgrade-steps li` | `--app-text-body-size` |
| `.upgrade-steps li>span:last-child:not(.pill)` | `--app-text-body-sm-size` |
| `.cli-grant-user-code` | `--app-text-display-sm-size` |
| `nav button.nav-child` | `--app-text-body-sm-size` |
| `.topbar #refresh` | `--app-text-body-sm-size` |
| `.account-copy span,#freshness` | `--app-text-body-sm-size` |
| `.view-head .lede,.lede` | `--app-text-body-size` |
| `button.mini,.btn,.back,.reg-export` | `--app-text-body-size` |
| `.src-note,.note,.card-meta,.card-section,.row-key,.muted-value` | `--app-text-body-sm-size` |
| `.device-inventory td strong` | `--app-text-body-size` |
| `.wcard .bars` | `--app-text-body-sm-size` |
| `.wcard .covrow` | `--app-text-body-sm-size` |
| `.wcard table td` | `--app-text-body-size` |
| `.exposure-trend-card .trend-heading h3` | `--app-text-heading-sm-size` |
| `.trend-heading p,.exposure-chart>.clegend,.exposure-trend-card .tdays` | `--app-text-body-sm-size` |
| `.decision-widget h3` | `--app-text-heading-sm-size` |
| `.decision-widget-head p,.decision-section-head>div>span,.candidate-identity>p, .candidate-suggestion,.decision-footer,.undecided-list time` | `--app-text-body-sm-size` |
| `.register-score-head span` | `--app-text-body-sm-size` |
| `.register-score-head strong` | `--app-text-display-sm-size` |
| `.register-score p` | `--app-text-body-sm-size` |
| `.register-metrics dt` | `--app-text-display-sm-size` |
| `.register-metrics dd` | `--app-text-body-sm-size` |
| `.register-toolbar strong` | `--app-text-heading-sm-size` |
| `.register-toolbar>div span,.register-legend` | `--app-text-body-sm-size` |
| `.register-identity>strong` | `--app-text-body-size` |
| `.register-identity>span` | `--app-text-body-sm-size` |
| `.register-cell>span:first-child` | `--app-text-body-sm-size` |
| `.register-cell>b` | `--app-text-body-size` |
| `.register-cell small,.register-cell .gov-sub,.register-cell .pill` | `--app-text-body-sm-size` |
| `.register-secondary` | `--app-text-body-sm-size` |
| `.register-secondary>span>b` | `--app-text-body-sm-size` |
| `.register-editor>div:first-child>strong` | `--app-text-heading-sm-size` |
| `.register-editor>div:first-child>span` | `--app-text-body-sm-size` |
| `.register-record>.exc` | `--app-text-body-size` |
| `.budget-card-title` | `--app-text-heading-sm-size` |
| `.budget-eyebrow,.budget-section-head>div>span,.budget-kpis em, .budget-add-member>span` | `--app-text-body-sm-size` |
| `.budget-kpis strong` | `--app-text-display-sm-size` |
| `.budget-tier-table th,.budget-details>table th` | `--app-text-body-sm-size` |
| `.budget-tier-table td,.budget-details>table td,.budget-add-member .mfield` | `--app-text-body-size` |
| `.evidence-summary-lead>span,.evidence-summary dd,.evidence-columns, .evidence-review-copy>span,.health-deployment dt` | `--app-text-body-sm-size` |
| `.evidence-summary-lead>strong` | `--app-text-heading-sm-size` |
| `.evidence-summary dt` | `--app-text-display-sm-size` |
| `.evidence-actions .mini` | `--app-text-body-sm-size` |
| `.ssstep .t` | `--app-text-body-size` |
| `.ssstep .val,.ssstep .pend,.ssstep .need` | `--app-text-body-sm-size` |
| `.ssmain h4` | `--app-text-heading-sm-size` |
| `.drawer .lede` | `--app-text-body-size` |
| `.search input` | `--app-text-body-size` |
| `.view-head .lede` | `--app-text-body-size` |
| `body` | `--app-text-body-size` |
| `.tenant-copy b` | `--app-text-body-size` |
| `.tenant-copy span` | `--app-text-body-sm-size` |
| `.nav-area-trigger` | `--app-text-body-size` |
| `.nav-child` | `--app-text-body-size` |
| `.nav-section-label` | `--app-text-body-sm-size` |
| `.foot` | `--app-text-body-sm-size` |
| `.topbar .back` | `--app-text-body-size` |
| `.account-copy b` | `--app-text-body-size` |
| `.account-copy span` | `--app-text-body-sm-size` |
| `.view-kicker` | `--app-text-body-sm-size` |
| `.view-meta .mini,.meta-chip` | `--app-text-body-sm-size` |
| `.wcard h3` | `--app-text-heading-sm-size` |
| `.wform button` | `--app-text-body-size` |
| `button.mini,.btn,.back` | `--app-text-body-size` |
| `input,select,.mfield` | `--app-text-body-size` |
| `th` | `--app-text-body-sm-size` |
| `td` | `--app-text-body-size` |
| `.ui-eyebrow` | `--app-text-body-sm-size` |
| `.ui-estate-line` | `--app-text-body-sm-size` |
| `.ui-estate-line>span:first-child` | `--app-text-body-sm-size` |
| `.executive-posture>span` | `--app-text-body-sm-size` |
| `.executive-posture>p` | `--app-text-body-sm-size` |
| `.executive-actions button.mini` | `--app-text-body-size` |
| `.ui-posture-note` | `--app-text-body-sm-size` |
| `.executive-metrics dd` | `--app-text-body-sm-size` |
| `.executive-metrics dt` | `--app-text-display-sm-size` |
| `.executive-metrics small` | `--app-text-body-sm-size` |
| `.ui-percent` | `--app-text-body-sm-size` |
| `.ui-denominator` | `--app-text-body-sm-size` |
| `.executive-metrics .trend` | `--app-text-body-sm-size` |
| `.ui-panel-head h3` | `--app-text-heading-sm-size` |
| `.ui-panel-head p` | `--app-text-body-sm-size` |
| `.ui-action-copy strong` | `--app-text-body-size` |
| `.ui-action-copy>span` | `--app-text-body-sm-size` |
| `.ui-action-copy small` | `--app-text-body-sm-size` |
| `.ui-badge` | `--app-text-body-sm-size` |
| `.ui-queue-details>summary` | `--app-text-body-sm-size` |
| `.ui-empty` | `--app-text-body-size` |
| `.ui-ring strong` | `--app-text-display-sm-size` |
| `.ui-ring strong span` | `--app-text-body-sm-size` |
| `.ui-ring-caption` | `--app-text-body-sm-size` |
| `.ui-coverage-legend p` | `--app-text-body-sm-size` |
| `.ui-coverage-legend small` | `--app-text-body-sm-size` |
| `.ui-source-heading h4` | `--app-text-heading-sm-size` |
| `.ui-source-heading>span:not(.wform)` | `--app-text-body-sm-size` |
| `.ui-source-grid .covrow,.ui-source-grid .meterrow` | `--app-text-body-sm-size` |
| `.ui-source-grid .covrow>span:first-child,.ui-source-grid .meterrow>span:first-child` | `--app-text-body-sm-size` |
| `.ui-source-grid .covrow>b,.ui-source-grid .meterrow>b` | `--app-text-body-sm-size` |
| `.ui-panel-footer` | `--app-text-body-sm-size` |
| `.ui-panel-footer .mini` | `--app-text-body-size` |
| `.ui-coverage-note` | `--app-text-body-sm-size` |
| `.ui-coverage-note p` | `--app-text-body-sm-size` |
| `.ui-tools-card h3>.count` | `--app-text-body-sm-size` |
| `.ui-tool-filters button` | `--app-text-body-size` |
| `.wcard .ui-inventory th` | `--app-text-body-sm-size` |
| `.wcard .ui-inventory td` | `--app-text-body-size` |
| `.ui-tool-button strong` | `--app-text-body-size` |
| `.ui-tool-button small` | `--app-text-body-sm-size` |
| `.ui-surface` | `--app-text-body-sm-size` |
| `.ui-muted` | `--app-text-body-sm-size` |
| `.ui-table-note` | `--app-text-body-sm-size` |
| `.wcard .stats dt` | `--app-text-display-sm-size` |
| `.wcard .stats dd` | `--app-text-body-sm-size` |
| `.wcard h3 .count` | `--app-text-body-sm-size` |
| `.ui-activity-count` | `--app-text-body-size` |
| `.budget-lines td` | `--app-text-body-size` |
| `.wcard .lede` | `--app-text-body-size` |
| `.wcard>table td` | `--app-text-body-size` |
| `.tcard th` | `--app-text-body-sm-size` |
| `.tcard td` | `--app-text-body-size` |
| `.tcard td strong` | `--app-text-body-size` |
| `.tcard>p.lede` | `--app-text-body-sm-size` |
| `.ui-row-actions .mini` | `--app-text-body-size` |
| `.ui-row-actions .mfield` | `--app-text-body-size` |
| `.ui-tool-chip` | `--app-text-body-sm-size` |
| `.ui-id` | `--app-text-body-sm-size` |
| `.muted-value` | `--app-text-body-sm-size` |
| `.row-key` | `--app-text-body-sm-size` |
| `.pill` | `--app-text-body-sm-size` |
| `#app>.stats dt` | `--app-text-display-sm-size` |
| `#app>.stats dd` | `--app-text-body-sm-size` |
| `.inventory-summary span` | `--app-text-body-sm-size` |
| `.inventory-summary b` | `--app-text-display-sm-size` |
| `.ui-widget-lede` | `--app-text-body-sm-size` |
| `.ui-tiles dt` | `--app-text-display-sm-size` |
| `.ui-tiles>div:first-child dt` | `--app-text-display-sm-size` |
| `.ui-tiles dd` | `--app-text-body-sm-size` |
| `.ui-widget-table td strong` | `--app-text-body-size` |
| `.ui-widget-table td small` | `--app-text-body-sm-size` |
| `.ui-silent-table td:last-child` | `--app-text-body-sm-size` |
| `.ui-notes li` | `--app-text-body-size` |
| `.ui-tool-main strong` | `--app-text-body-size` |
| `.ui-tool-main small` | `--app-text-body-sm-size` |
| `.ui-tool-nums b` | `--app-text-body-size` |
| `.ui-tool-nums i` | `--app-text-body-sm-size` |
| `.ui-compact` | `--app-text-body-size` |
| `.ui-compact .view-head h2` | `--app-text-heading-sm-size` |
| `.ui-compact .view-head .lede` | `--app-text-body-size` |
| `.ui-compact .view-meta .mini,.ui-compact .meta-chip` | `--app-text-body-sm-size` |
| `.ui-compact .executive-posture>strong` | `--app-text-heading-sm-size` |
| `.ui-compact .executive-posture>p` | `--app-text-body-sm-size` |
| `.ui-compact .executive-actions button.mini` | `--app-text-body-size` |
| `.ui-compact .executive-metrics dt` | `--app-text-display-sm-size` |
| `.ui-compact .executive-metrics dd` | `--app-text-body-sm-size` |
| `.ui-compact .wcard .ui-inventory td` | `--app-text-body-size` |
| `.ui-compact .ui-tool-initial` | `--app-text-body-sm-size` |
| `.ui-compact .ui-tool-button strong` | `--app-text-body-size` |
| `.ui-compact .tcard td` | `--app-text-body-size` |
| `.ui-compact .inventory-summary b` | `--app-text-display-sm-size` |
| `.ui-compact #app>.stats dt` | `--app-text-display-sm-size` |
| `.ui-compact .ui-tiles dt` | `--app-text-display-sm-size` |
| `.ui-compact .ui-ring strong` | `--app-text-display-sm-size` |
| `.ui-panel-footer .ui-more` | `--app-text-body-sm-size` |
| `.ui-steps>p` | `--app-text-body-size` |
| `.ui-steplist>li` | `--app-text-body-size` |
| `.ui-steplist>li::before` | `--app-text-body-sm-size` |
| `.ui-steplist code,.ui-steps code` | `--app-text-body-sm-size` |
| `.ui-cmd>code` | `--app-text-body-size` |
| `.ui-cmd>.ui-copy` | `--app-text-body-size` |
| `.dragging .editing .gcard>.ov-stack-zone,.dragging .gcard>.ov-stack-zone` | `--app-text-body-sm-size` |
| `.ov-placeholder b` | `--app-text-body-size` |
| `.ov-placeholder span` | `--app-text-body-sm-size` |
| `.ov-placeholder small` | `--app-text-body-sm-size` |
| `.ov-tray-label` | `--app-text-body-sm-size` |
| `.ov-chip b` | `--app-text-body-size` |
| `.ov-chip button` | `--app-text-body-size` |
| `.ov-drop-end` | `--app-text-body-size` |
| `.ov-drop-end.empty` | `--app-text-body-sm-size` |
| `.ui-silent-table td:last-child em` | `--app-text-body-sm-size` |
| `.ui-compact .device-inventory td strong` | `--app-text-body-size` |
| `.executive-metrics dd.ui-metric-note` | `--app-text-body-sm-size` |
| `.ui-compact .executive-metrics dd.ui-metric-note` | `--app-text-body-sm-size` |
