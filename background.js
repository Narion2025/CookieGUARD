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

/**
 * Lädt und integriert neue Crawler-Daten in die Site-Database
 */
async function integrateCrawlerData() {
  try {
    console.log('🔄 Integriere neue Crawler-Daten...');
    
    // Lade aktuelle Site-Database
    const result = await chrome.storage.local.get(['siteDatabase', 'crawlerData']);
    let siteDatabase = result.siteDatabase || { version: "1.0.0", sites: {} };
    const crawlerData = result.crawlerData || {};
    
    let updatedCount = 0;
    let newSitesCount = 0;
    
    // Integriere Crawler-Daten
    for (const [domain, data] of Object.entries(crawlerData)) {
      const cleanDomain = domain.replace('www.', '');
      const isNewSite = !siteDatabase.sites[cleanDomain];
      
      if (isNewSite) newSitesCount++;
      else updatedCount++;
      
      // Berechne Rating basierend auf Cookies und Compliance
      const rating = calculateSiteRating(data);
      
      // Erstelle/Update Site-Eintrag
      siteDatabase.sites[cleanDomain] = {
        rating: rating,
        cookieCount: getTotalCookieCount(data.cookies),
        hasBanner: hasCookieBanner(data.banner),
        stats: {
          tracking: data.cookies.marketing?.length || 0,
          analytics: data.cookies.analytics?.length || 0,
          essential: data.cookies.essential?.length || 0,
          functional: data.cookies.functional?.length || 0
        },
        banner: data.banner.selectors.container.length > 0 ? {
          buttons: getTotalButtonCount(data.banner),
          hasAccept: data.banner.selectors.accept.length > 0,
          hasReject: data.banner.selectors.reject.length > 0,
          hasSettings: data.banner.selectors.settings.length > 0,
          selectors: data.banner.selectors,
          automation: data.automation
        } : null,
        compliance: data.compliance,
        lastUpdated: data.timestamp
      };
    }
    
    // Update Metadaten
    siteDatabase.version = "1.1.0";
    siteDatabase.generatedAt = new Date().toISOString();
    siteDatabase.totalSites = Object.keys(siteDatabase.sites).length;
    siteDatabase.lastCrawlerUpdate = new Date().toISOString();
    
    // Speichere aktualisierte Database
    await chrome.storage.local.set({ siteDatabase });
    
    console.log(`✅ Crawler-Daten integriert: ${newSitesCount} neue Seiten, ${updatedCount} aktualisiert`);
    
    // Benachrichtige alle Tabs über das Update
    const tabs = await chrome.tabs.query({});
    tabs.forEach(tab => {
      if (tab.url && !tab.url.startsWith('chrome://')) {
        chrome.tabs.sendMessage(tab.id, {
          type: 'DATABASE_UPDATED',
          newSites: newSitesCount,
          updatedSites: updatedCount
        }).catch(() => {}); // Ignoriere Fehler für Tabs ohne Content-Script
      }
    });
    
  } catch (error) {
    console.error('❌ Fehler beim Integrieren der Crawler-Daten:', error);
  }
}

/**
 * Berechnet das Rating einer Seite basierend auf Cookies und Compliance
 */
function calculateSiteRating(data) {
  const cookies = data.cookies;
  const compliance = data.compliance;
  
  // Zähle problematische Cookies
  const trackingCookies = cookies.marketing?.length || 0;
  const analyticsCookies = cookies.analytics?.length || 0;
  const totalProblematic = trackingCookies + analyticsCookies;
  
  // Zähle Compliance-Verstöße
  const gdprViolations = compliance.gdpr?.violations?.length || 0;
  const eprivacyViolations = compliance.eprivacy?.violations?.length || 0;
  const ttdsgViolations = compliance.ttdsg?.violations?.length || 0;
  const totalViolations = gdprViolations + eprivacyViolations + ttdsgViolations;
  
  // Rating-Logik (angepasst an realistische Werte)
  if (totalProblematic === 0 && totalViolations <= 8) {
    return 'green';
  } else if (totalProblematic <= 2 && totalViolations <= 12) {
    return 'yellow';
  } else {
    return 'red';
  }
}

/**
 * Berechnet die Gesamtanzahl der Cookies
 */
function getTotalCookieCount(cookies) {
  return (cookies.essential?.length || 0) +
         (cookies.functional?.length || 0) +
         (cookies.analytics?.length || 0) +
         (cookies.marketing?.length || 0);
}

/**
 * Prüft, ob die Seite ein Cookie-Banner hat
 */
function hasCookieBanner(banner) {
  return banner.selectors.container.length > 0 ||
         banner.selectors.accept.length > 0 ||
         banner.selectors.reject.length > 0 ||
         banner.selectors.settings.length > 0;
}

/**
 * Berechnet die Gesamtanzahl der Banner-Buttons
 */
function getTotalButtonCount(banner) {
  return banner.selectors.accept.length +
         banner.selectors.reject.length +
         banner.selectors.settings.length +
         banner.selectors.close.length;
}

/**
 * Lädt Crawler-Daten aus einer JSON-Datei
 */
async function loadCrawlerDataFromFile(fileContent) {
  try {
    const crawlerData = JSON.parse(fileContent);
    await chrome.storage.local.set({ crawlerData });
    console.log('✅ Crawler-Daten aus Datei geladen');
    
    // Integriere die Daten sofort
    await integrateCrawlerData();
    
  } catch (error) {
    console.error('❌ Fehler beim Laden der Crawler-Daten:', error);
  }
}

// Event-Listener für Crawler-Daten-Integration
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'INTEGRATE_CRAWLER_DATA') {
    integrateCrawlerData().then(() => {
      sendResponse({ success: true });
    }).catch(error => {
      sendResponse({ success: false, error: error.message });
    });
    return true; // Async response
  }
  
  if (message.type === 'LOAD_CRAWLER_FILE') {
    loadCrawlerDataFromFile(message.fileContent).then(() => {
      sendResponse({ success: true });
    }).catch(error => {
      sendResponse({ success: false, error: error.message });
    });
    return true; // Async response
  }

  if (message.type === 'UPDATE_BADGE') {
    updateBadgeForTab(sender.tab.id, message.rating, message.cookieCount);
    sendResponse({ success: true });
  }
});

/**
 * Aktualisiert das Badge für einen Tab basierend auf dem Site-Rating
 */
function updateBadgeForTab(tabId, rating, cookieCount) {
  try {
    // Setze Badge-Farbe basierend auf Rating
    let badgeColor;
    let badgeText = cookieCount > 0 ? cookieCount.toString() : '';
    
    switch (rating) {
      case 'green':
        badgeColor = '#4CAF50'; // Grün
        break;
      case 'yellow':
        badgeColor = '#FF9800'; // Orange/Gelb
        break;
      case 'red':
        badgeColor = '#F44336'; // Rot
        break;
      default:
        badgeColor = '#9E9E9E'; // Grau
    }
    
    // Setze Badge-Text (Cookie-Anzahl)
    chrome.action.setBadgeText({
      text: badgeText,
      tabId: tabId
    });
    
    // Setze Badge-Farbe
    chrome.action.setBadgeBackgroundColor({
      color: badgeColor,
      tabId: tabId
    });
    
    console.log(`🎯 Badge updated for tab ${tabId}: ${rating} (${cookieCount} cookies)`);
    
  } catch (error) {
    console.error('❌ Fehler beim Aktualisieren des Badges:', error);
  }
}

// Automatische Integration beim Start (falls Crawler-Daten vorhanden)
chrome.runtime.onStartup.addListener(async () => {
  const result = await chrome.storage.local.get('crawlerData');
  if (result.crawlerData && Object.keys(result.crawlerData).length > 0) {
    console.log('🔄 Automatische Integration der Crawler-Daten beim Start...');
    await integrateCrawlerData();
  }
});

// Initialize service worker
new CookieGuardianService();