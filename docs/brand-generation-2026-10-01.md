# AIミハル 独自マーク生成記録（2026-10-01）

## 承認と生成手段

親から伝達されたユーザー承認「現在使える画像生成機能で作成してよい」に基づき、Codex の `image_gen.imagegen` を1回実行した。`transparent_background: true`。このツールにはモデル選択・モデル識別フィールドがないため、**モデル名は未指定・未確認であり、Image2.5で作ったとは主張しない**。外部写真や他社ロゴは入力していない。

## 成果物

- 新規候補：`assets/brand/ai-miharu-symbol-generated-20261001.png`
- 生成原本：`/workspace/generated_images/exec-a729470f-660e-4bfe-9023-f2de076ed185.png`（原本を残してコピー）
- PNG / RGBA / 1254 × 1254px。アルファ値0〜255、完全透明ピクセル1,129,780を確認。
- 生成時は別候補として保存。その後rootが確認し、ポータルのサイドバー・サインイン・PNG iconへ採用。`portal/app/static/ai-miharu-symbol.png`、互換`logo.png`、apple-touch PNGへ原本をコピーした。古いSVGルートは互換用に保持し、原本画像の手描き加工・モデル名の偽装はしていない。

## 意図と実際の見え方

AI利用の見守りを、中央の点と、それを囲む開いた二つの青い曲線で表す。目・盾・錠前・チェックマークの直接的な組合せを避け、視認・受容・安全な流れを抽象化した。名称は「AIミハル」を維持し、画像内に文字は入れていない。官章・公的機関の印章・政府の公式サービスを示す要素は指示にも画像にも含めない。

生成結果を実際に表示して、青い点と二本の曲線、透明な余白、文字や紋章がないことを確認した。指定は単色だったが、実際のラスター画像には近似した青色と微小な色差・半透明画素があるため、完全な単色SVGとは扱わない。小さいサイズでは曲線の細い末端が弱くなる可能性があり、採用時には16/24/32/48px、明暗両背景で確認する。現時点ではそれらの実表示確認を完了したとは主張しない。

## 再現用プロンプト要旨

> Create ONE original polished vector-style brand symbol for AIミハル, a Japanese B2B product helping organizations see AI usage and support safe AI use. SYMBOL ONLY; no text, letters, numbers, mockups, border, canvas background or watermark. Transparent RGBA. Two broad gently rounded blue ribbon strokes form a welcoming open circular perimeter around a single clear blue dot offset slightly toward the upper right. Restrained asymmetric abstract shape; no eye, shield, checkmark, padlock, generic sparkle, government seal or insignia. Saturated medium blue around #0875DC, no gradients, textures, shadows, or thin lines. Generous transparent margin; readable on white and near-black. Do not imitate an existing logo.

商標・既存意匠との網羅的類似調査は今回の生成確認に含めていない。既存READMEの過去モデル記録は、この新規画像の生成証明として扱わない。

旧SVG由来の互換route/ICOは保持するが、現行画面とPNG faviconは新マークを参照。旧`tools/brand-render.cjs`の実行で新PNGを意図せず上書きしないよう、旧書出しには`--legacy-brand`明示を要求する。
