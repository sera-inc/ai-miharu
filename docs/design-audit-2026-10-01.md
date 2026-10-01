# AIミハル デザイン移行監査（2026-10-01）

調査担当: Codex。ソース読取による監査。製品CSSの編集・ブラウザ実測・承認判定は本監査では実施していない。

## 固定した証拠

- 製品: `sera-inc/ai-miharu` commit `a33af4487d6ab3bd4ab80c21a37ce13a1b0e3e06`。
- 指定された実デザインシステム: `sera-inc/digital-design-system` commit `6051bceb67c60fb805b757c22bbd66f3318ea980`。`/workspace/digital-design-system` の実ファイルを参照した。
- 読了: 両repoの `CLAUDE.md`、DSの `README.md`、`docs/01_SaaS向けデザインシステム拡張_設計書.md` §6–9、`docs/02_digital-design-system_運用方針設計書.md`、`docs/03_移行手順チェックリスト.md`、`tokens/semantic.css`、製品の `docs/mapping.md`、`docs/deviations.md`、`DADS-VERSION`、製品CSS。
- `/workspace/AGENTS.md`、両repoルートの `AGENTS.md` はない。vendor配下のAGENTSはそのvendor編集時に適用される。本作業はvendorを編集しない。

ユーザーの今回の依頼はCodexで全面改善する実装権限を与えている。過去のDeepSeek管理者試験例外が今回も承認済みである、あるいは標準手順の人間レビューに合格した、と読み替えない。実装を進めることと、DS標準移行の完了を宣言することを区別する。

## 現状と差分

| 項目 | 指定DSの規則・実値 | 製品の現状 / 証拠 |
|---|---|---|
| 段階 | §6、チェックリスト: 一括変換禁止、Phase 1→5 | `CLAUDE.md` と `mapping.md` はPhase 1未完了 |
| 対応表 | レビュー承認・未解決0 | 2026-09-30の14ファイル、143種/2,180出現。仮対応31、保留65、除外36、未判定11。値単位の旧判定を引き継ぎ、現行文脈で再判定していない |
| レイヤー | Layer 1変更禁止、Layer 3は `--app-*` のみ | `dads-product.css` はローカルLayer 2案。既存の色参照がその案に移っただけで正式semantic採用ではない |
| 境界 | `--app-border` = solid-gray-420（白背景3:1を意図） | `--app-sg-border-subtle` = solid-gray-200。これを入力境界に使えば公式の境界仕様を満たすとは言えない |
| 本文 | `--app-text` = solid-gray-800 | `--app-sg-text-primary` = solid-gray-900 |
| リンク | `--app-text-link` = blue-1000、下線必須 | `--app-sg-text-link` = blue-700。使用文脈ごとの下線確認も必要 |
| ホバー面 | `--app-surface-hover` = solid-gray-50 | `--app-sg-surface-hover` = solid-gray-100 |
| 文字 | 本文/表Dense14、見出し18/20/24、補助12 | `enterprise.css` に8–13.5px等が多数。例27行ナビ12.5px、39行補助9px、85行表12px、91行見出し13px |
| フォーカス | `:focus-visible` と共有リング、除去禁止 | `enterprise.css:106,794,930,1648` にoutline:0（1648は!important）、`index.html:121` にoutline:none。後勝ちの上書きも存在するため実際の可視性は計算スタイルで判定する |
| ターゲット | DS `CLAUDE.md`: 44px相当 | `enterprise.css:27` ナビ37px、`:110` 閉じる32px。実ヒット領域をブラウザで測る必要 |
| ダーク | 上流U-04は未決 | DEV-001の製品適応。既存機能として維持し、ライトと別にコントラスト検証 |
| 配布 | DS READMEは `tokens/index.css`、運用方針§0.1は必ず共通repo経由 | 製品は公開パッケージ生成Layer 1と代替Layer 2。DEV-005/006に逸脱あり。U-03は未決でありこれを正式配布決定と扱わない |
| a11y証拠 | axe、キーボード、支援技術、UIチェックリスト | DEV-007は過去20画面×2テーマaxe違反0と記載。今回の変更後証拠でも支援技術の合格でもない |

`index.html:973,975` はenterprise→dads-product順で読み込む。上書きCSSがあるため、基底CSSの文字列検出だけで最終表示を断定しない。例 `.barrow` と `.qr-item` のフォーカス除去は `dads-product.css:438` に後続修正がある。

## 対応表の誤判定（優先是正）

保留76種だけを解消しても対応表は正しくならない。少なくとも次のz-indexは、表では「宣言がなく誤検出」と除外しているが、実際の宣言が存在する。

| 値 | 実在する宣言の例（基準commit） |
|---|---|
| 1 | `enterprise.css:206,208,212,397,1589`、姿勢表示・テーブル見出し等 |
| 2 | `enterprise.css:674` `.nav-pin`、`index.html:827,842` |
| 3 | `index.html:806` |
| 4 | `enterprise.css:1623` ダッシュボード編集ドロップ領域 |
| 5 | `index.html:118` stickyヘッダー |
| 20 | `index.html:396` drawer |
| 40 | `index.html:267` `.setbar` |
| 70 | `enterprise.css:802` `#qresults` |
| 90 | `enterprise.css:123` モバイルaside |

さらに75は表の推測（setupbell）ではなく `enterprise.css:679` の `#navflyout` で確認できる。19は `index.html:394` のoverlayである。拡張機能の2147483647は他サイト上に表示するガード通知なので、ポータルのtoast用z-indexへ機械置換すると機能が変わり得る。

公式inventoryスクリプトのz-index抽出は `(?:z-index|zIndex)\s*:\s*['"]?(-?\d+)` に限定される。著作権年やURLの数字を理由に除外した旧説明は、抽出実装とも矛盾する。CSS解析結果とソース行を併記して再レビューする。

## 安全に全面移行する最小段階

1. **基準固定**: 作業branch、合成データ、全ナビ画面、ライト/ダーク、390/768/900/1440pxを撮影。API/JS回帰結果と取得commitを保存する。ロールバック用に従来テーマをGitに保持。
2. **文脈別mapping**: 公式inventoryの再実行に加え、各実宣言のselector/property/value/sourceを記録。誤除外を訂正。本文・補助・アイコンの同じpx値は別の用途として判定し、統合した箇所には「※統合」を記載。Codex提案であることと標準レビュー状態を明記する。
3. **配布経路を明示**: 既存mount経路で実DSのtokensを使った検証環境を先に構成し、参照commitと使用ファイルを記録。公開成果物にprivate原本を暗黙同梱しない。標準起動に必要な正式配布方法U-03は別の決定記録にする。
4. **Phase 2**: 承認済み項目から既存CSS変数の参照先を変更する。DOM ID、イベント、API契約は保つ。上流のsurface/border/text/primaryの役割へ合わせる。未解決値を近い数値という理由だけで置換しない。主要画面全ての機能・視覚差分を確認。
5. **Phase 3**: Button→Input→Select→Checkbox/Radio→Textareaの順。正規手順は1 PR=1コンポーネント。同時置換の一括PRを標準準拠と記載しない。既存HTMLを残す場合はDEV-002の方針を再評価し、DADS HTML実装の該当仕様と挙動を照合する。
6. **Phase 4**: AppShell→DataGrid→Toast/EmptyState/Skeleton→個別画面。情報密度を落とす際も、既存のソート・フィルタ・保存・エクスポート・モーダル・キーボード・ダッシュボード編集機能を残す。独自チャート/ダーク/900px drawerは逸脱の根拠と検証を更新する。
7. **Phase 5**: 全画面/全テーマaxe、キーボード主要フロー、フォーカス・44px実測、200%ズーム、狭幅、強制色/reduced-motion。支援技術は利用できる環境で実施し、LinuxのみでNVDA/VoiceOver未実行なら未実行と書く。UIチェックリストを埋め、DADS-VERSIONと完了状態を証拠に合わせる。

## 完了チェック

- [x] 指定された実DS原本と現行コードを照合
- [x] 旧対応表の誤判定と共有semanticとの差を特定
- [ ] 新mappingの文脈別再検証・未解決解消
- [ ] 配布経路の決定と標準起動での同一性検証
- [ ] 全コンポーネント・全主要画面の段階移行
- [ ] 変更後の全機能回帰・視覚比較・アクセシビリティ証拠
- [ ] DS標準手順が要求するレビュー記録（今回の実装権限をレビュー合格と同一視しない）

この文書は移行の準備と問題点を記録したもので、全面移行完了の証明ではない。
