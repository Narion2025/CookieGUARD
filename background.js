// Cookie Guardian Background Service Worker
class CookieGuardianService {
  constructor() {
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.initializeStorage();
  }

  setupEventListeners() {
    // Extension installation
    chrome.runtime.onInstalled.addListener((details) => {
      this.handleInstall(details);
    });

    // Message handling
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      this.handleMessage(request, sender, sendResponse);
      return true; // Keep message channel open
    });

    // Update badge based on tab changes
    chrome.tabs.onActivated.addListener(async (activeInfo) => {
      await this.updateBadge(activeInfo.tabId);
    });

    chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && tab.url) {
        await this.updateBadge(tabId);
      }
    });
  }

  async handleInstall(details) {
    if (details.reason === 'install') {
      await chrome.storage.sync.set({
        cookieGuardianSettings: {
          silentMode: true,
          showNotifications: true,
          defaultAction: 'block'
        }
      });
    }
  }

  async handleMessage(request, sender, sendResponse) {
    try {
      switch (request.action) {
        case 'saveDomainSetting':
          await this.saveDomainSetting(request.domain, request.setting);
          sendResponse({ success: true });
          break;

        case 'getDomainSetting':
          const setting = await this.getDomainSetting(request.domain);
          sendResponse({ setting });
          break;

        case 'getStats':
          const stats = await this.getStats();
          sendResponse({ stats });
          break;

        case 'updateBadge':
          await this.updateBadge(sender.tab.id, request.status);
          sendResponse({ success: true });
          break;

        case 'clearDomainSetting':
          await this.clearDomainSetting(request.domain);
          sendResponse({ success: true });
          break;

        default:
          sendResponse({ error: 'Unknown action' });
      }
    } catch (error) {
      console.error('Background script error:', error);
      sendResponse({ error: error.message });
    }
  }

  async saveDomainSetting(domain, setting) {
    const data = await chrome.storage.local.get(['domainSettings']);
    const domainSettings = data.domainSettings || {};
    
    domainSettings[domain] = {
      action: setting,
      timestamp: Date.now()
    };
    
    await chrome.storage.local.set({ domainSettings });
    
    // Update stats
    await this.updateStats(setting);
  }

  async getDomainSetting(domain) {
    const data = await chrome.storage.local.get(['domainSettings']);
    const domainSettings = data.domainSettings || {};
    return domainSettings[domain] || null;
  }

  async clearDomainSetting(domain) {
    const data = await chrome.storage.local.get(['domainSettings']);
    const domainSettings = data.domainSettings || {};
    
    if (domainSettings[domain]) {
      delete domainSettings[domain];
      await chrome.storage.local.set({ domainSettings });
    }
  }

  async updateStats(action) {
    const data = await chrome.storage.local.get(['stats']);
    const stats = data.stats || {
      blocked: 0,
      essential: 0,
      accepted: 0,
      lastUpdated: Date.now()
    };

    switch (action) {
      case 'block':
        stats.blocked++;
        break;
      case 'essential':
        stats.essential++;
        break;
      case 'accept':
        stats.accepted++;
        break;
    }

    stats.lastUpdated = Date.now();
    await chrome.storage.local.set({ stats });
  }

  async getStats() {
    const data = await chrome.storage.local.get(['stats']);
    return data.stats || {
      blocked: 0,
      essential: 0,
      accepted: 0,
      lastUpdated: Date.now()
    };
  }

  async updateBadge(tabId, status = null) {
    try {
      const tab = await chrome.tabs.get(tabId);
      if (!tab.url || tab.url.startsWith('chrome://')) return;

      const domain = new URL(tab.url).hostname;
      const setting = await this.getDomainSetting(domain);

      let badgeText = '';
      let badgeColor = '#808080'; // Grau für unbekannt

      if (setting) {
        switch (setting.action) {
          case 'block':
            badgeText = '🛡️';
            badgeColor = '#d32f2f'; // Rot
            break;
          case 'essential':
            badgeText = '⚠️';
            badgeColor = '#f57c00'; // Orange
            break;
          case 'accept':
            badgeText = '✓';
            badgeColor = '#388e3c'; // Grün
            break;
        }
      }

      await chrome.action.setBadgeText({ text: badgeText, tabId });
      await chrome.action.setBadgeBackgroundColor({ color: badgeColor, tabId });
    } catch (error) {
      console.error('Badge update error:', error);
    }
  }

  async initializeStorage() {
    // Initialize default settings if not exist
    const settings = await chrome.storage.sync.get(['cookieGuardianSettings']);
    if (!settings.cookieGuardianSettings) {
      await chrome.storage.sync.set({
        cookieGuardianSettings: {
          silentMode: true,
          showNotifications: true,
          defaultAction: 'block'
        }
      });
    }
  }
}

// Initialize service worker
new CookieGuardianService();