// Cookie Guardian Popup
class CookieGuardianPopup {
  constructor() {
    this.currentTab = null;
    this.currentDomain = null;
    this.domainSetting = null;
    this.init();
  }

  async init() {
    await this.getCurrentTab();
    this.setupEventListeners();
    await this.loadDomainStatus();
    await this.loadStats();
  }

  async getCurrentTab() {
    try {
      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true,
      });
      this.currentTab = tab;

      if (tab.url && !tab.url.startsWith('chrome://')) {
        this.currentDomain = new URL(tab.url).hostname;
        document.getElementById('currentDomain').textContent =
          this.currentDomain;
      } else {
        document.getElementById('currentDomain').textContent = 'Chrome-Seite';
        this.disableActions();
      }
    } catch (error) {
      console.error('Error getting current tab:', error);
      document.getElementById('currentDomain').textContent = 'Fehler';
      this.disableActions();
    }
  }

  setupEventListeners() {
    // Quick action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach((button) => {
      button.addEventListener('click', (e) => {
        const action = e.target.dataset.action;
        this.setDomainAction(action);
      });
    });

    // Clear domain setting
    document.getElementById('clearDomainBtn').addEventListener('click', () => {
      this.clearDomainSetting();
    });

    // Settings
    document.getElementById('settingsBtn').addEventListener('click', () => {
      chrome.runtime.openOptionsPage();
    });
  }

  async loadDomainStatus() {
    if (!this.currentDomain) return;

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'getDomainSetting',
        domain: this.currentDomain,
      });

      this.domainSetting = response.setting;
      this.updateStatusDisplay();
    } catch (error) {
      console.error('Error loading domain status:', error);
    }
  }

  updateStatusDisplay() {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const actionButtons = document.querySelectorAll('.action-btn');

    // Reset button states
    actionButtons.forEach((btn) => btn.classList.remove('active'));

    let riskLevel = 'yellow';
    if (this.domainSetting) {
      const action = this.domainSetting.action;
      const timestamp = new Date(
        this.domainSetting.timestamp
      ).toLocaleDateString('de-DE');

      switch (action) {
        case 'block':
          statusIndicator.className = 'status-indicator red';
          statusText.textContent = `Cookies werden blockiert (seit ${timestamp})`;
          document
            .querySelector('[data-action="block"]')
            .classList.add('active');
          riskLevel = 'red';
          break;
        case 'essential':
          statusIndicator.className = 'status-indicator yellow';
          statusText.textContent = `Nur essentielle Cookies (seit ${timestamp})`;
          document
            .querySelector('[data-action="essential"]')
            .classList.add('active');
          riskLevel = 'yellow';
          break;
        case 'accept':
          statusIndicator.className = 'status-indicator green';
          statusText.textContent = `Alle Cookies akzeptiert (seit ${timestamp})`;
          document
            .querySelector('[data-action="accept"]')
            .classList.add('active');
          riskLevel = 'green';
          break;
      }
    } else {
      statusIndicator.className = 'status-indicator gray';
      statusText.textContent = 'Keine Einstellung für diese Domain';
      riskLevel = 'yellow';
    }
    this.setTrafficLight(riskLevel);
  }

  setTrafficLight(riskLevel) {
    const trafficLightImg = document.getElementById('traffic-light-img');
    if (!trafficLightImg) return;

    let imagePath;
    switch (riskLevel) {
      case 'green':
        imagePath = 'icons/ampel-gruen.png';
        break;
      case 'yellow':
        imagePath = 'icons/ampel-gelb.png';
        break;
      case 'red':
        imagePath = 'icons/ampel-rot.png';
        break;
      default:
        imagePath = 'icons/ampel-gelb.png';
    }

    trafficLightImg.src = imagePath;
  }

  async setDomainAction(action) {
    if (!this.currentDomain) return;

    try {
      await chrome.runtime.sendMessage({
        action: 'saveDomainSetting',
        domain: this.currentDomain,
        setting: action,
      });

      // Update local state
      this.domainSetting = {
        action: action,
        timestamp: Date.now(),
      };

      this.updateStatusDisplay();
      await this.loadStats();

      // Reload the current tab to apply new setting
      chrome.tabs.reload(this.currentTab.id);

      // Show success feedback
      this.showFeedback('Einstellung gespeichert!');
    } catch (error) {
      console.error('Error setting domain action:', error);
      this.showFeedback('Fehler beim Speichern', 'error');
    }
  }

  async clearDomainSetting() {
    if (!this.currentDomain || !this.domainSetting) return;

    try {
      await chrome.runtime.sendMessage({
        action: 'clearDomainSetting',
        domain: this.currentDomain,
      });

      this.domainSetting = null;
      this.updateStatusDisplay();
      this.showFeedback('Einstellung gelöscht!');

      // Reload the current tab
      chrome.tabs.reload(this.currentTab.id);
    } catch (error) {
      console.error('Error clearing domain setting:', error);
      this.showFeedback('Fehler beim Löschen', 'error');
    }
  }

  async loadStats() {
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'getStats',
      });

      const stats = response.stats;
      document.getElementById('blockedCount').textContent = stats.blocked || 0;
      document.getElementById('essentialCount').textContent =
        stats.essential || 0;
      document.getElementById('acceptedCount').textContent =
        stats.accepted || 0;
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  }

  disableActions() {
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach((button) => {
      button.disabled = true;
      button.style.opacity = '0.5';
    });

    document.getElementById('clearDomainBtn').disabled = true;
    document.getElementById('clearDomainBtn').style.opacity = '0.5';
  }

  showFeedback(message, type = 'success') {
    // Simple feedback mechanism
    const existingFeedback = document.querySelector('.feedback');
    if (existingFeedback) {
      existingFeedback.remove();
    }

    const feedback = document.createElement('div');
    feedback.className = `feedback ${type}`;
    feedback.textContent = message;
    feedback.style.cssText = `
      position: fixed;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      background: ${type === 'error' ? '#f44336' : '#4caf50'};
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      font-size: 12px;
      z-index: 1000;
    `;

    document.body.appendChild(feedback);

    setTimeout(() => {
      if (feedback.parentNode) {
        feedback.remove();
      }
    }, 2000);
  }

  /**
   * Lädt Crawler-Daten und integriert sie in die Database
   */
  async loadCrawlerData() {
    try {
      // Lade die Crawler-Daten aus der JSON-Datei
      const response = await fetch('dokumente/GitHub/backend/crawler/data/crawl-results.json');
      if (!response.ok) {
        throw new Error('Crawler-Daten konnten nicht geladen werden');
      }
      
      const crawlerData = await response.json();
      
      // Sende Daten an Background-Script zur Integration
      const result = await chrome.runtime.sendMessage({
        type: 'LOAD_CRAWLER_FILE',
        fileContent: JSON.stringify(crawlerData)
      });
      
      if (result.success) {
        console.log('✅ Crawler-Daten erfolgreich geladen und integriert');
        this.showNotification('Crawler-Daten erfolgreich aktualisiert!', 'success');
        
        // Aktualisiere das Popup
        await this.loadCurrentTab();
      } else {
        throw new Error(result.error || 'Unbekannter Fehler');
      }
      
    } catch (error) {
      console.error('❌ Fehler beim Laden der Crawler-Daten:', error);
      this.showNotification('Fehler beim Laden der Crawler-Daten: ' + error.message, 'error');
    }
  }

  /**
   * Zeigt eine Benachrichtigung im Popup
   */
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
      position: fixed;
      top: 10px;
      left: 10px;
      right: 10px;
      padding: 10px;
      border-radius: 4px;
      color: white;
      font-size: 12px;
      z-index: 1000;
      background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 3000);
  }

  /**
   * Integriert bereits geladene Crawler-Daten
   */
  async integrateCrawlerData() {
    try {
      const result = await chrome.runtime.sendMessage({
        type: 'INTEGRATE_CRAWLER_DATA'
      });
      
      if (result.success) {
        console.log('✅ Crawler-Daten erfolgreich integriert');
        this.showNotification('Crawler-Daten erfolgreich integriert!', 'success');
        
        // Aktualisiere das Popup
        await this.loadCurrentTab();
      } else {
        throw new Error(result.error || 'Unbekannter Fehler');
      }
      
    } catch (error) {
      console.error('❌ Fehler beim Integrieren der Crawler-Daten:', error);
      this.showNotification('Fehler beim Integrieren: ' + error.message, 'error');
    }
  }
}

// Initialize popup when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new CookieGuardianPopup();
});
