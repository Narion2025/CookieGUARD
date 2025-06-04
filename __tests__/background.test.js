const { TextEncoder, TextDecoder } = require('util');

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

// mock chrome APIs needed for initialization
global.chrome = {
  runtime: {
    onInstalled: { addListener: jest.fn() },
    onMessage: { addListener: jest.fn() },
  },
  tabs: {
    onActivated: { addListener: jest.fn() },
    onUpdated: { addListener: jest.fn() },
    get: jest.fn(() => Promise.resolve({ url: 'https://example.com' })),
  },
  action: {
    setBadgeText: jest.fn(() => Promise.resolve()),
    setBadgeBackgroundColor: jest.fn(() => Promise.resolve()),
  },
  storage: {
    sync: {
      get: jest.fn(() => Promise.resolve({})),
      set: jest.fn(() => Promise.resolve()),
    },
    local: {
      _data: {},
      get: jest.fn(function (keys) {
        const data = global.chrome.storage.local._data;
        if (Array.isArray(keys) && keys.includes('stats')) {
          return Promise.resolve({ stats: data.stats });
        }
        return Promise.resolve({ domainSettings: data.domainSettings });
      }),
      set: jest.fn(function (obj) {
        global.chrome.storage.local._data = {
          ...global.chrome.storage.local._data,
          ...obj,
        };
        return Promise.resolve();
      }),
    },
  },
};

// load background.js code and evaluate in JSDOM
const dom = new JSDOM('', { url: 'https://example.com' });
const rawScript = fs.readFileSync(
  path.join(__dirname, '..', 'background.js'),
  'utf8'
);
const wrapped = `((global)=>{ ${rawScript}; global.CookieGuardianService = CookieGuardianService; })(global);`;
const runInContext = new dom.window.Function('global', wrapped);
runInContext(global);

const ServiceClass = global.CookieGuardianService;
const service = new ServiceClass();

describe('updateStats', () => {
  test('increments stats correctly', async () => {
    await service.updateStats('block');
    const stats = await service.getStats();
    expect(stats.blocked).toBe(1);
  });
});
