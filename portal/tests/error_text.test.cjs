// Run with: node --test portal/tests/error_text.test.cjs
//
// The portal's Japanese error messages, rendered by the browser's own
// functions. The receiver keeps its API details in English (its tests and
// logs read them that way) and the portal says the same thing in Japanese, so
// what matters here is which English sentences are recognised, that a Japanese
// tool or organisation name quoted inside an English sentence does not make
// the whole sentence look Japanese, and that a mail server's own words are
// kept as evidence rather than translated.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../app/static/index.html'), 'utf8');
// From the first helper of the block to the comment that follows uiRelayText.
const start = html.indexOf('const uiApiName = ');
const end = html.indexOf('// The refusal detail from a failed write');
assert.ok(start > 0 && end > start, 'the error-text block moved: update this slice');
const block = html.slice(start, end);
// The two tables uiErrorText reads before its own code runs.
// The two activation tables uiErrorText reads: one line each, defined side by side.
const lineAt = marker => { const i = html.indexOf(marker); return html.slice(i, html.indexOf('\n', i) + 1); };
const tables = lineAt('const JA_ACTIVATION_REFUSAL = ') + lineAt('const EN_ACTIVATION_REFUSAL_CODES = ');

function load() {
  const c = vm.createContext({});
  vm.runInContext(tables + block + '; this.uiErrorText = uiErrorText; this.uiRelayText = uiRelayText;', c);
  return c;
}
const { uiErrorText, uiRelayText } = load();

test('a known English sentence that quotes a Japanese name is still translated', () => {
  // The bug: any Japanese character made the whole string look Japanese, so
  // this reached the screen in English.
  assert.equal(uiErrorText('malformed tool id: 会議録ボット', 422),
               'ツール ID の形式が正しくありません: 会議録ボット');
  assert.equal(uiErrorText('not an email address: 山田太郎', 422),
               'メールアドレスの形式が正しくありません: 山田太郎');
  assert.match(uiErrorText('claude-code is already covered by the claude 世良チーム subscription - one licence, one subscription; fold them together instead', 422),
               /claude-code は、すでに claude の契約（世良チーム）の対象に含まれています/);
});

test('vendor refusals name the vendor and the reason', () => {
  assert.match(uiErrorText('the Anthropic API answered 401: the key is wrong, expired or revoked', 200),
               /^Anthropic API が 401 を返しました。キーが正しくないか/);
  assert.match(uiErrorText('the exchange-rate source answered 200, but not with JSON', 0),
               /^為替レートの取得元が 200 を返しましたが、JSON 形式ではありませんでした。$/);
  assert.match(uiErrorText('could not reach the Cursor API (ConnectTimeout)', 0),
               /^Cursor API に接続できませんでした（ConnectTimeout）。$/);
  assert.match(uiErrorText('the ECB publishes no reference rate for JPY', 0), /^欧州中央銀行（ECB）は JPY の参考レートを公表していません。$/);
});

test('a Japanese message passes through untouched, and an unknown English one does not', () => {
  assert.equal(uiErrorText('保存できませんでした: 入力内容を確認してください。', 422),
               '保存できませんでした: 入力内容を確認してください。');
  assert.equal(uiErrorText('something the portal has never heard of', 500),
               '処理できませんでした（HTTP 500）。');
  assert.equal(uiErrorText('', 0), '処理できませんでした。');
  assert.equal(uiErrorText(null, 404), '処理できませんでした（HTTP 404）。');
});

test('an English sentence with a Japanese organisation name is translated, and a Japanese one is not touched twice', () => {
  // The vendor refused, and the organisation happens to have a Japanese name:
  // the sentence is still English, so it must still be translated.
  assert.equal(uiErrorText('the Anthropic API answered 401: the key is wrong, expired or revoked', 401)
                 .startsWith('Anthropic API が 401 を返しました'), true);
  assert.match(uiErrorText('the Devin API answered 404: no organisation org-世良 - check the id on Settings > Service Users', 404),
               /^Devin API が 404 を返しました。組織 org-世良 が見つかりません。/);
  // A message that is already Japanese and matches no English pattern stays as it is.
  assert.equal(uiErrorText('世良チームの契約が見つかりません。', 404), '世良チームの契約が見つかりません。');
});

test('Devin refusals point at the vendor screen by its English labels, inside Japanese quotes', () => {
  // Devin's console is English-only, so an administrator has to look for the
  // labels exactly as Devin prints them. They are quoted as labels and
  // explained in Japanese instead of being left as a bare "A > B" path.
  const msgs = [
    uiErrorText('the Devin API answered 404: no organisation org-abc123 - check the id on Settings > Service Users', 404),
    uiErrorText('the Devin key needs the organisation id with it, as org-xxxx:cog_xxxx - both are on Settings > Service Users', 400),
    uiErrorText('cog_abcd is not a Devin organisation id: it should look like org-xxxx, from Settings > Service Users', 400),
  ];
  for (const m of msgs) {
    assert.match(m, /「Settings」>「Service Users」（サービスユーザーの管理ページ）/);
    assert.doesNotMatch(m, /[^「]Settings > Service Users/);
  }
  assert.match(msgs[0], /org-abc123 が見つかりません/);
});

test('activation refusals still map to their Japanese explanations', () => {
  assert.match(uiErrorText('no key was given', 400), /キーが入力されていません/);
});

test('the mail server\'s own words are kept as evidence, under a Japanese lead-in', () => {
  // SMTP replies are what an administrator searches for in the relay's
  // documentation, so the text and its code stay exactly as received.
  assert.equal(uiRelayText('535 5.7.8 Authentication credentials invalid'),
               'メールサーバーの応答: 535 5.7.8 Authentication credentials invalid');
  assert.equal(uiRelayText('ConnectionRefusedError'),
               'メールサーバーとの通信に失敗しました（ConnectionRefusedError）。');
  assert.equal(uiRelayText('no mail server is configured'), 'メールサーバーが設定されていません。');
  assert.equal(uiRelayText(''), 'メールサーバーから理由は示されませんでした。');
  assert.equal(uiRelayText('メールサーバーが応答しません'), 'メールサーバーが応答しません');
});

test('a relay reply that quotes a Japanese name is still labelled as the mail server\'s answer', () => {
  // The reply starts with the SMTP code, so it is the relay's own text even
  // though the address it refuses contains Japanese. It is kept verbatim.
  assert.equal(uiRelayText('550 5.1.1 <山田太郎@example.co.jp>: Recipient address rejected: User unknown'),
               'メールサーバーの応答: 550 5.1.1 <山田太郎@example.co.jp>: Recipient address rejected: User unknown');
  // A reply with no code that is entirely Japanese is passed through as it is.
  assert.equal(uiRelayText('宛先が拒否されました'), '宛先が拒否されました');
});
