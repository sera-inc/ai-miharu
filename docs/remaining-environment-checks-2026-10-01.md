# 継続調査: build・計測保護・画像モデル・操作プレビュー

2026-10-01、親からの継続指示に基づく再確認。コードの回帰テスト全体は再実行せず、今回新たに確認すべき境界だけを調査した。main公開はしていない。

## 公開サイトの通常build

通常buildには `scripts/resources/verify-catalog-release.mjs` の必須gateがある。ViteのbuildStartでも同じ照合を行う。DB側snapshotのschemaVersion/version/key/totalがフロントと一致することが条件で、ローカルfixtureで代替すると通常build成功の証明にならない。

Node v24.19.0で次を再実行した。

```sh
NODE_USE_ENV_PROXY=1 node scripts/resources/verify-catalog-release.mjs
```

結果: exit 1、`fetch failed` の原因は `Proxy response (403) !== 200 when HTTP Tunneling` / `UND_ERR_ABORTED`。対象は設定済みSupabase `resource-catalog` Edge Function。プロキシ設定の値や資格情報は資料に含めていない。

設定担当者への最小許可依頼: 宛先host `jmtkgixrvzqagzqsqrrr.supabase.co` のTCP443へのHTTPS CONNECT。HTTP単位で制限できる場合は `GET /functions/v1/resource-catalog`、クエリ `operation=asset&key=all%2Fsummary&version=1cec0452da4cc176`。現在の固定snapshotの読取り照合だけで、Supabase全体のwildcard、DBポート、管理API、書込み権限は不要。API認証失敗ではなくトンネル確立前の拒否として切り分けた。

前回の `npm run build` のprerender `dist/index.html` 不在は、先行するgate失敗の後に出る二次エラー。必須gateを単独実行し、接続拒否を切り分けた。外部gate無効化時のコンパイル・4,213ルート生成・静的検証成功を通常build成功へ読み替えない。gateを変更せず、接続許可されたビルド環境で通常buildを実行することが残件。拒否された経路を別プロキシで迂回していない。

## 10/1 SEO変更・観察ロックの保護

`git fetch origin main` 後のmainは `af27978d59957a3bbe17fbe08bb93257bb03f159`。SEO修正PR #73のmerge `7e08660d` と実装 `aae985a8` は、このLPブランチの分岐前に既に含まれる。

- 実装commitが変更した6ファイル（measure-products、product-paths、analyticsCatalog、siteAnalytics、対応する2テスト）は最新mainとbyte一致。親の「8ファイル」の記録を6ファイルに読み替えず、追加で `data/seo/` 全体と共有SumaiLandingの差分が空であることも確認した。ハッシュは [証拠JSON](evidence/2026-10-01/seo-preservation.json)。
- 対象の既存テスト21件成功。AIミハルcanonicalの末尾slash、product context、CTA、同意・社内除外を含む。顧客イベントは送信していない。
- 7件のobserving実験（重要事項OCR、AIコンサルティング、sumai-mente/desk/sketch/madori/search）は維持。履歴・固定baseline・観察期間は変更していない。
- `routeSeo.ts` の変更はAIミハルの参考料金1行だけ。llms2ファイルはその生成物。公開統合時は最新mainで再生成し、endpoint担当の変更を含める。

## Image2.5の指定可否

利用可能ツールのメタデータを確認した。ネイティブ `image_gen__imagegen` が受け付けるのは `prompt`、`num_last_images_to_include`、`referenced_image_paths`、`transparent_background`。`model`引数・モデル一覧・選択されたモデルを確認する専用機能は提示されていない。従って「Image2.5を指定して実行した」とは証明できない。これはそのモデル自体が存在しないという判断ではない。

関連skill `creative-production:produce` も調査した。同skillはbuilt-in Codex ImageGenへのルーティングを指定するが、Image2.5を指定・保証する方法は記載しない。また要求される `creative_production_board` は現在のcallable toolsにない。Canvaの画像生成も利用可能だが、指定モデルの保証はなく代替実行していない。ローカル `/workspace/.agents/skills` は存在せず、ワークスペース内のSKILL.md検索にも追加の画像生成経路はなかった。

必要なのは、Image2.5の実行を保証するモデル選択/識別を備えたCodexツール、または現在のネイティブツールが指定モデルであることを確認できる環境情報。未確認のまま生成して指定モデルを使ったと表示しない。今回は新規生成・有料API契約・クレジット購入なし。

## 人が操作できるプレビュー

現状は未達。画像の共有は操作確認の代わりにならない。

| 経路 | 確認結果 | 必要なもの |
|---|---|---|
| クラウド内localhost | 前回8091等で実製品と合成データの操作検証成功。外部からのアクセスURLではない | 現環境のポート公開・転送機能 |
| Cloudflare Quick Tunnel | 前回のトンネル作成はDNS connection refused。その後のプロキシ経由確認も403。今回同じ拒否経路を繰り返し迂回しない | 許可されたトンネル接続環境 |
| ネイティブツール | 利用可能ツールに任意ローカルportの転送/tunnel機能が見つからない | プラットフォーム側のpreview機能 |
| Sites | hosting skillを実際に確認。サーバー成果物はCloudflare Workers互換が必要。Python FastAPI・SQLite・Lokiの既存Composeをそのままホストする機能ではない。Sites URLはproduction deployment扱い | 実製品backendを動かせる別環境。偽API/静的再現を実サービス確認としない |
| Lovable | callable toolsのpreviewはLovable projectの成果物用。ローカルComposeの転送ではない | backend hostingとproject接続。追加生成/新規購入はしていない |

既存製品を安全に共有する最小の必要条件は、合成データ専用のクラウド環境へ認証付きHTTPSで到達できる、許可されたポート転送または既存VM。公開時はreceiver等の内部ポートを露出させず、portalの通常認証と合成データを確認し、親へURLを渡して操作の機会を確保する。

利用可能な外部経路を確認できていないため、今回は稼働したまま放置せず停止状態を維持。通信制約が解消した時点で同じ保存済み環境を再起動する。Macは使用しない。
