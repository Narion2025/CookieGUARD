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
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      this.currentTab = tab;
      
      if (tab.url && !tab.url.startsWith('chrome://')) {
        this.currentDomain = new URL(tab.url).hostname;
        document.getElementById('currentDomain').textContent = this.currentDomain;
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
    actionButtons.forEach(button => {
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
        domain: this.currentDomain
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
    actionButtons.forEach(btn => btn.classList.remove('active'));

    if (this.domainSetting) {
      const action = this.domainSetting.action;
      const timestamp = new Date(this.domainSetting.timestamp).toLocaleDateString('de-DE');

      switch (action) {
        case 'block':
          statusIndicator.className = 'status-indicator red';
          statusText.textContent = `Cookies werden blockiert (seit ${timestamp})`;
          document.querySelector('[data-action="block"]').classList.add('active');
          break;
        case 'essential':
          statusIndicator.className = 'status-indicator yellow';
          statusText.textContent = `Nur essentiielle Cookies (seit ${timestamp})`;
          document.querySelector('[data-action="essential"]').classList.add('active');
          break;
        case 'accept':
          statusIndicator.className = 'status-indicator green';
          statusText.textContent = `Alle Cookies akzeptiert (seit ${timestamp})`;
          document.querySelector('[data-action="accept"]').classList.add('active');
          break;
      }
    } else {
      statusIndicator.className = 'status-indicator gray';
      statusText.textContent = 'Keine Einstellung für diese Domain';
    }
  }

  async setDomainAction(action) {
    if (!this.currentDomain) return;

    try {
      await chrome.runtime.sendMessage({
        action: 'saveDomainSetting',
        domain: this.currentDomain,
        setting: action
      });

      // Update local state
      this.domainSetting = {
        action: action,
        timestamp: Date.now()
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
        domain: this.currentDomain
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
        action: 'getStats'
      });

      const stats = response.stats;
      document.getElementById('blockedCount').textContent = stats.blocked || 0;
      document.getElementById('essentialCount').textContent = stats.essential || 0;
      document.getElementById('acceptedCount').textContent = stats.accepted || 0;

    } catch (error) {
      console.error('Error loading stats:', error);
    }
  }

  disableActions() {
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
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
}

// Initialize popup when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new CookieGuardianPopup();
});