# DADS トークンの暫定ランタイム参照

**状態**: Phase 1 の準備。Ollama Cloud `deepseek-v4.1-flash:cloud` の配布経路案に基づく。DADS 設計書 U-03 の正式なパッケージ配布方式は未決、ダークトークンのドラフト PR #2 は未承認。製品 UI はまだ DADS を参照しない。

## 狙い

公開元ソースと Docker image に private な `digital-design-system` のファイルや認証情報を含めず、管理者の試験環境だけで DADS の CSS を読み込めるように準備する。CSS を直接コピーしたり `--app-*` / `--dads-*` を製品側で上書きしない。

## 管理者試験

1. 権限のあるアカウントで `sera-inc/digital-design-system` を別途 clone し、採用する Git commit/tag を固定する。Layer 1 の `tokens/dads.css` を手編集しない。
2. `DADS_TOKENS_DIR` にその clone の `tokens/` の**絶対パス**を指定する。
3. `docker compose -f demo/docker-compose.yml -f demo/docker-compose.dads.yml config --quiet` でマウント設定を検証する。起動時にも両方の `-f` を指定する。通常の `docker compose -f demo/docker-compose.yml up` は private repo 無しで起動する。
4. 認証済みの Portal から `/digital-design-system/tokens/index.css` と相対 `dads.css`、`brand.css`、`semantic.css` を取得できる。各 URL は固定ルートで `require_auth` を通す。認証済みでも未設定/ファイル不在なら 404。未認証なら先に 401。

管理モードでは `require_page_auth` がログイン前ページを公開するため、DADS 固定ルートには使わない。未ログインの CSS 取得は 401 とし、ログイン画面は既存の CSS だけで表示する。

この段階では `index.html` や `enterprise.css` に import を追加していない。ドラフト PR #2 の承認、正式な配布方式、対応表の保留値解消を経てから CSS 参照とコンポーネント移行を行う。

## 検証

- 4 固定ルートの認証依存、FileResponse、`Cache-Control: private, no-store`、未設定 404、未知の動的 CSS ルート無しを unit test で確認。
- `PYTHONPATH=portal PORTAL_AUTH=none ../.venv/bin/pytest portal/ -q` を実行。`PORTAL_AUTH=none` はテスト設定であり、デプロイの無認証化を意味しない。
- Compose overlay は読み取り専用 bind mount。`docker compose config` と実行環境内の CSS 応答を別に確認する。

正式配布へ切り替える際は、この暫定マウントの撤去、DADS バージョン固定、認証・キャッシュ境界、ブラウザ表示・機能テストを一つの変更としてレビューする。
