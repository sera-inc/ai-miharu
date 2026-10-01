# DSの依存・配布経路の確認

2026-10-01。A〜Eの対応判断は承認待ち。確定mapping、トークン値、配布方式の変更はしていない。新しい永続認証・CI secret・有料契約は作成していない。

## 現在使える経路

| 経路 | 実装と認証 | 状態 |
|---|---|---|
| 標準起動 | `portal/app/static/dads/` の生成済みLayer 1と製品adapterを読む。private DSへのアクセス不要 | 既存の起動経路を維持 |
| Layer 1再生成 | `tools/dads/package-lock.json` が公開npm `@digital-go-jp/tailwind-theme-plugin` 1.0.1とintegrityを固定。`npm ci` / `npm run check` | private registry token不要。製品独自Layer 2の承認を意味しない |
| 任意の組織DSマウント | 既取得の固定commit `6051bce` のtokensディレクトリをread-only mount。4ファイル揃わなければ同梱へfallback | 既存の許可されたローカル検証経路。clone権限と他者への再配布判断は別 |
| build時private取得案 | 上流U-03はprivate npm / GitHub Packages / monorepoが未決。package.jsonはprivate:true、独自部分の包括licenseを今回確認できない | 新しい永続credentialの発行・保存はしていない。第一候補の提案のみで、採用済みではない |

`private:true` はnpm公開の抑止設定であり、著作権ライセンスでも公開禁止の包括的判断でもない。同様に、cloneできたことは原本・独自Layer 2を公開repoや一般配布イメージに入れる承認ではない。MITの公開依存、組織独自コード、ドキュメント、Figma、アイコンは資産ごとに区別する。

## 一次資料で確認した条件

- 公開依存1.0.1の[公式MIT全文](https://github.com/digital-go-jp/tailwind-theme-plugin/blob/v1.0.1/LICENSE)は、複製・配布等を認め、copyrightとpermission noticeの保持を求める。製品rootの `licenses/dads-tailwind-theme-plugin-MIT.txt` と `NOTICE` は維持する。
- [デジタル庁の利用上の注意事項](https://design.digital.go.jp/dads/introduction/notices/)は、文書本体、Figma、コード、第三者素材を区別する。加工物を同庁が作成したように見せない。UI上の出典表示要否と、配布物内のライセンス保持を同じ問題として扱わない。
- 共通DSのREADMEが明示するMIT対象はvendorと `@digital-go-jp/*`。この記載を独自 `tokens/semantic.css` や自社コンポーネントの包括的な公開許諾へ拡張しない。独自部分の公開・生成物再配布条件は管理者の方針決定が必要。

## 配布物の独立修正

portalのDocker build contextは `portal/` のため、rootにあるLICENSE/NOTICEとDADSライセンス全文は従来のDockerfileではイメージへ入っていなかった。既存ファイルのbyte-identicalなコピーを `portal/` 内へ置き、Dockerfileで `/srv/LICENSE`、`/srv/NOTICE`、`/srv/licenses/` へ同梱するよう修正した。ライセンス本文・表示用CSS・DS値は変更しない。

`test_portal_image_license_copies_match_the_source_notices` が4ファイルの原本一致を検査する。対象CSS/配布境界の17テスト成功。イメージの実buildは今回branchのCIで別途確認し、ソース検査だけを配布後検証と扱わない。

Layer 1は既存lockを使う `npm ci --ignore-scripts` 後、`npm run check` が成功（plugin v1.0.1、215 variables、55 text styles）。生成物の変更はなし。公開registryの依存取得にprivate認証を追加していない。
