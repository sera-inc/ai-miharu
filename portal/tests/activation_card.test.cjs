// Run with: node --test portal/tests/activation_card.test.cjs
//
// The activation card, rendered by the browser's own function against the
// shapes the receiver actually answers with. Same harness as the overview
// renderers, for the same reason: this card makes claims about what a
// deployment is entitled to, and the wrong claim is worse than a broken
// layout. What is checked here is mostly what it must NOT say - never that
// a deployment is on the open edition when the read failed, and never the
// key itself.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../app/static/index.html'), 'utf8');
const card = html.slice(html.indexOf('let ACT = null, ACTMSG = null;'),
                        html.indexOf('function diagnosticsCards() {'));
const uiErrorText = html.slice(html.indexOf('function uiErrorText('),
                               html.indexOf('// The refusal detail from a failed write'));
const escape = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function render(act, {role = 'owner', msg = null} = {}) {
  const c = vm.createContext({
    AUTH: {role},
    DIAG: {deployment: {namespace: 'ai-guard'}},
    location: {origin: 'https://ai-guard-portal.example.com'},
    esc: escape,
    uiCommand: cmd => `<div class="ui-cmd"><code>${escape(cmd)}</code></div>`,
  });
  vm.runInContext(card + uiErrorText + '; ACT = this.act; ACTMSG = this.msg; this.out = activationCard();',
                  Object.assign(c, {act, msg}));
  return c.out;
}

const ACTIVE = {state: 'active', id: 'NYX-0001', org: 'Acme Group Ltd',
  plan: 'enterprise', devices: 2500, issued: '2026-01-01',
  expires: '2027-06-30', days_left: 300, registry: 'registry.example.com',
  fingerprint: '58aa-0b39-7247'};

test('with no key, the card says open edition and claims nothing else', () => {
  const out = render({state: 'none'});
  assert.match(out, /オープン版/);
  assert.match(out, /オープンエディション/);
  assert.match(out, /Apache 2\.0/);
  assert.match(out, /オフライン、外部リクエストなし/);
  assert.doesNotMatch(out, /有効化済み/);
});

test('a failed read is not "no subscription"', () => {
  // The bug this exists to stop: answering the question from a read that
  // never happened, and telling a paying customer they have no licence.
  const out = render({state: 'unknown'});
  assert.match(out, /未取得/);
  assert.match(out, /有効・無効のどちらとも表示していません/);
  assert.doesNotMatch(out, /オープンエディション/);
  assert.doesNotMatch(out, /アクティベーション キーを貼り付け/);
});

test('an activated deployment shows what it bought, and never the key', () => {
  const out = render(ACTIVE);
  assert.match(out, /Acme Group Ltd/);
  assert.match(out, /エンタープライズ/);
  assert.match(out, /最大 2500 デバイス/);
  assert.match(out, /2027-06-30/);
  assert.match(out, /300 日後/);
  assert.match(out, /58aa-0b39-7247/);
  assert.doesNotMatch(out, /nyxl_/);
});

test('moving to Nyxus is one command against this portal, with the key from the shell', () => {
  const out = render(ACTIVE);
  assert.match(out, /このデプロイを Nyxus に移行する/);
  assert.match(out, /aiguardctl upgrade --edition nyxus --portal https:\/\/ai-guard-portal\.example\.com --nyxus-version &lt;version&gt; --dry-run/);
  assert.match(out, /export NYXUS_KEY=/);
  // Not the old steps: a second release on new storage, and a key on a command line.
  assert.doesNotMatch(out, /helm upgrade --install nyxus/);
  assert.doesNotMatch(out, /--docker-password/);
  assert.doesNotMatch(out, /nyxl_/);
});

test('a key that names no registry gets the same command, because the command reads the registry', () => {
  const out = render(Object.assign({}, ACTIVE, {registry: ''}));
  assert.match(out, /aiguardctl upgrade --edition nyxus/);
  assert.doesNotMatch(out, /&lt;registry&gt;/);
});

test('a subscription close to its end says so before it ends', () => {
  const soon = render(Object.assign({}, ACTIVE, {days_left: 20}));
  assert.match(soon, /health-note warning/);
  assert.match(soon, /2027-06-30 に期限切れになります/);
  // And says plainly that nothing stops working, because nothing does.
  assert.match(soon, /当日に動作が停止することはありません/);
  assert.doesNotMatch(render(ACTIVE), /health-note warning/);
});

test('an expired key is shown as genuine and lapsed, not as a forgery', () => {
  const out = render(Object.assign({}, ACTIVE,
    {state: 'expired', expires: '2026-02-01', days_left: -29}));
  assert.match(out, /期限切れ/);
  assert.match(out, /29 日前/);
  assert.match(out, /Acme Group Ltd/);
  assert.match(out, /デプロイはそのまま継続します/);
  // The move needs an active key, so it is named rather than offered.
  assert.match(out, /このデプロイを Nyxus に移行するには有効なキーが必要です/);
  assert.doesNotMatch(out, /aiguardctl upgrade --edition nyxus/);
});

test('a key this release cannot verify says to upgrade before suspecting it', () => {
  const out = render({state: 'invalid', fingerprint: 'aaaa-bbbb-cccc',
                      code: 'not_ours',
                      reason: 'this key was not issued for this software'});
  assert.match(out, /このリリースでは確認できません/);
  assert.match(out, /このキーはこのソフトウェア向けに発行されていない/);
  assert.doesNotMatch(out, /this key was not issued/);
  assert.match(out, /まずアップグレードし/);
  assert.match(out, /aaaa-bbbb-cccc/);
  assert.match(out, /削除する/);
});

test('only an owner is offered the field', () => {
  for (const role of ['admin', 'viewer']) {
    const out = render({state: 'none'}, {role});
    assert.doesNotMatch(out, /data-act="act-save"/);
    assert.match(out, /契約の有効化はオーナーが行います/);
  }
  assert.match(render({state: 'none'}, {role: 'owner'}), /data-act="act-save"/);
});

test('an activated owner can replace or remove, and a viewer sees the facts', () => {
  const owner = render(ACTIVE);
  assert.match(owner, /このキーを置き換えるには、更新されたキーを貼り付けてください/);
  assert.match(owner, /data-act="act-clear"/);
  const viewer = render(ACTIVE, {role: 'viewer'});
  assert.match(viewer, /Acme Group Ltd/);
  assert.doesNotMatch(viewer, /data-act="act-/);
});

test('a refusal is shown as one, and escaped', () => {
  const out = render({state: 'none'},
                     {msg: {ok: false, text: 'このキーは <damaged> です'}});
  assert.match(out, /health-note danger/);
  assert.match(out, /このキーは &lt;damaged&gt; です/);
});

test('an unknown English backend message is replaced by the Japanese fallback', () => {
  const out = render({state: 'none'},
                     {msg: {ok: false, text: 'Unknown backend error'}});
  assert.match(out, /health-note danger/);
  assert.doesNotMatch(out, /Unknown backend error/);
});

test('an organisation name is escaped rather than rendered', () => {
  const out = render(Object.assign({}, ACTIVE, {org: '<img src=x onerror=1>'}));
  assert.match(out, /&lt;img src=x/);
  assert.doesNotMatch(out, /<img src=x/);
});
