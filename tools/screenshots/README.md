# 画面と動画の撮影ツール

README とランディングページ（株式会社世良のサイト）に載せる、ポータルの実画面と貼り付けガードの動作を、**起動中のデモ**から撮影する開発用ツールです。
製品のイメージには含まれません。実運用の環境には向けないでください（サインインして全画面を開きます）。

## 使い方

```bash
# 1. 撮影前に、デモを作り直す（期間やコンパクト表示の選択はアカウントごとに保存されるため）
cd demo && docker compose down -v && docker compose up -d --build && cd ..

# 2. 撮影ツールの準備（初回のみ）
cd tools/screenshots && npm ci
export CHROMIUM_PATH=/path/to/chromium   # 省略すると Playwright が取得したものを使う: npx playwright-core install chromium

# 3. 撮影
npm run portal -- --out ./out              # 20 画面（PNG と WebP、1440×900・倍率 1.5）
npm run paste-guard -- --out ./out         # 貼り付けガードの動画（WebM）と警告・ブロックの静止画
```

- サインインは、デモの公開の値（`admin` / `admin-demo-portal`）が既定です。`PORTAL_URL`、`PORTAL_USER`、`PORTAL_PASSWORD`、`GUARD_DEMO_URL` で変更できます。
- 画面は日本語のフォントに依存します（Noto Sans CJK JP など）。フォントの違いで、文字の幅が少し変わります。
- 出力を、LP（サイトの `public/images/ai-governance/screens/`、`public/videos/ai-governance/`）と README（`assets/screenshots/`）にコピーします。手順の詳細はサイト側の `docs/sera-ai-governance-lp.md` にあります。

## 撮影したものについて

- データはすべて、デモの架空のサンプルです。撮影の前に、デモの状態が想定どおりか（未解決の個人アカウント 4 件、AI 台帳の判断記録 4/8 など）を目で確認してください。
- 設定の他のタブ（URL・識別子・メールアドレスを含む）と、登録トークンの全文は、撮影の対象にしていません。
- 貼り付けガードの録画は、拡張機能の実際の `guard.js` を変更せずに動かします。テスト用の文字列は架空、または公式資料の値です。
