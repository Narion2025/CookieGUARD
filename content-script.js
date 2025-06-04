// Cookie Guardian Content Script
class CookieGuardianContent {
  constructor() {
    this.domain = window.location.hostname;
    this.bannerDetected = false;
    this.overlayShown = false;
    this.domainSetting = null;
    
    // German cookie banner patterns
    this.bannerSelectors = [
      // OneTrust
      '#onetrust-consent-sdk',
      '.onetrust-pc-dark-filter',
      '.ot-sdk-container',
      '#onetrust-banner-sdk',
      
      // Usercentrics
      '#usercentrics-cmp',
      '.uc-banner',
      '.usercentrics-dialog',
      
      // Cookiebot
      '#CybotCookiebotDialog',
      '#Cookiebot',
      '.cookiebot-banner',
      
      // SourcePoint
      '#sp-cc',
      '.sp-cc-banner',
      '.sp-message-container',
      
      // Generic patterns
      '[id*="cookie"]',
      '[class*="cookie"]',
      '[id*="consent"]', 
      '[class*="consent"]',
      '[aria-label*="cookie"]',
      '[aria-label*="Cookie"]',
      '.gdpr-banner',
      '.privacy-banner',
      '.cookie-notice',
      '.cookie-bar'
    ];

    // German button patterns
    this.buttonPatterns = {
      accept: [
        'alle akzeptieren',
        'cookies akzeptieren', 
        'einverstanden',
        'zustimmen',
        'accept all',
        'alle cookies',
        'geht klar',
        'akzeptieren'
      ],
      reject: [
        'alle ablehnen',
        'ablehnen',
        'nicht akzeptieren',
        'reject all',
        'deny',
        'nur erforderliche',
        'nur notwendige'
      ],
      settings: [
        'einstellungen',
        'auswahl bestätigen',
        'cookie-einstellungen',
        'datenschutz-einstellungen',
        'manage preferences',
        'weitere optionen'
      ]
    };

    this.init();
  }

  async init() {
    // Check for existing domain setting
    this.domainSetting = await this.getDomainSetting();
    
    if (this.domainSetting) {
      // Silent mode - apply saved setting
      this.applySilentMode();
    } else {
      // First visit - detect and show overlay
      this.detectBanners();
      this.observeForBanners();
    }

    // Update badge
    this.updateBadge();
  }

  async getDomainSetting() {
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'getDomainSetting',
        domain: this.domain
      });
      return response.setting;
    } catch (error) {
      console.error('Error getting domain setting:', error);
      return null;
    }
  }

  async saveDomainSetting(setting) {
    try {
      await chrome.runtime.sendMessage({
        action: 'saveDomainSetting',
        domain: this.domain,
        setting: setting
      });
    } catch (error) {
      console.error('Error saving domain setting:', error);
    }
  }

  detectBanners() {
    for (const selector of this.bannerSelectors) {
      const banner = document.querySelector(selector);
      if (banner && this.isVisible(banner)) {
        this.handleBannerDetected(banner);
        break;
      }
    }
  }

  observeForBanners() {
    const observer = new MutationObserver((mutations) => {
      if (this.bannerDetected) return;

      mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
          mutation.addedNodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
              this.checkNodeForBanner(node);
            }
          });
        }
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    // Stop observing after 10 seconds
    setTimeout(() => observer.disconnect(), 10000);
  }

  checkNodeForBanner(element) {
    for (const selector of this.bannerSelectors) {
      if (element.matches && element.matches(selector)) {
        if (this.isVisible(element)) {
          this.handleBannerDetected(element);
          return;
        }
      }
      
      const banner = element.querySelector(selector);
      if (banner && this.isVisible(banner)) {
        this.handleBannerDetected(banner);
        return;
      }
    }
  }

  isVisible(element) {
    const rect = element.getBoundingClientRect();
    const style = window.getComputedStyle(element);
    
    return rect.width > 0 && 
           rect.height > 0 && 
           style.display !== 'none' && 
           style.visibility !== 'hidden' &&
           style.opacity !== '0';
  }

  handleBannerDetected(banner) {
    if (this.bannerDetected) return;
    
    this.bannerDetected = true;
    this.currentBanner = banner;
    
    const riskLevel = this.assessRiskLevel(banner);
    this.showGuardianOverlay(banner, riskLevel);
    
    console.log('Cookie Guardian: Banner detected', {
      domain: this.domain,
      risk: riskLevel,
      banner: banner
    });
  }

  assessRiskLevel(banner) {
    // Risk assessment based on banner content and domain
    let riskScore = 0;
    const bannerText = banner.textContent.toLowerCase();
    
    // High-risk indicators
    if (bannerText.includes('marketing') || 
        bannerText.includes('werbung') ||
        bannerText.includes('personalisierung') ||
        bannerText.includes('targeting') ||
        bannerText.includes('werbepartner') ||
        bannerText.includes('drittanbieter')) {
      riskScore += 3;
    }
    
    // Medium-risk indicators  
    if (bannerText.includes('analyse') ||
        bannerText.includes('statistik') ||
        bannerText.includes('performance') ||
        bannerText.includes('tracking')) {
      riskScore += 2;
    }
    
    // Check for third-party domains mentioned
    const commonTrackers = ['google', 'facebook', 'amazon', 'microsoft'];
    commonTrackers.forEach(tracker => {
      if (bannerText.includes(tracker)) riskScore += 1;
    });
    
    // Domain-based risk (commercial vs non-commercial)
    if (this.domain.includes('.com') || 
        this.domain.includes('shop') ||
        this.domain.includes('store')) {
      riskScore += 1;
    }
    
    // Return traffic light color
    if (riskScore >= 4) return 'red';
    if (riskScore >= 2) return 'yellow';
    return 'green';
  }

  showGuardianOverlay(banner, riskLevel) {
    if (this.overlayShown) return;
    this.overlayShown = true;

    const overlay = this.createOverlay(riskLevel);
    document.body.appendChild(overlay);
    
    // Position overlay over banner
    this.positionOverlay(overlay, banner);
    
    // Add event listeners
    this.setupOverlayListeners(overlay);
    
    // Auto-hide after 15 seconds if no interaction
    setTimeout(() => {
      if (overlay.parentNode) {
        this.hideOverlay(overlay);
        this.applySilentMode('block'); // Default to block
      }
    }, 15000);
  }

  createOverlay(riskLevel) {
    const overlay = document.createElement('div');
    overlay.className = 'cookie-guardian-overlay';
    overlay.innerHTML = `
      <div class="guardian-popup">
        <div class="guardian-header">
          <div class="guardian-logo">🛡️ Cookie Guardian</div>
          <div class="guardian-risk ${riskLevel}">
            <span class="risk-indicator ${riskLevel}"></span>
            ${this.getRiskText(riskLevel)}
          </div>
        </div>
        
        <div class="guardian-content">
          <h3>Cookie-Banner erkannt auf ${this.domain}</h3>
          <p class="risk-explanation">${this.getRiskExplanation(riskLevel)}</p>
          
          <div class="guardian-actions">
            <button class="guardian-btn block" data-action="block">
              🔴 Dauerhaft blockieren
              <small>Alle nicht-essentiellen Cookies ablehnen</small>
            </button>
            
            <button class="guardian-btn essential" data-action="essential">
              🟡 Nur notwendige Cookies
              <small>Funktionale Cookies erlauben</small>
            </button>
            
            <button class="guardian-btn accept" data-action="accept">
              🟢 Alle akzeptieren
              <small>Vollständige Zustimmung erteilen</small>
            </button>
          </div>
          
          <div class="guardian-footer">
            <small>Diese Einstellung wird für ${this.domain} gespeichert</small>
          </div>
        </div>
      </div>
    `;
    
    return overlay;
  }

  getRiskText(level) {
    switch (level) {
      case 'red': return 'Hohes Datenschutz-Risiko';
      case 'yellow': return 'Mittleres Datenschutz-Risiko';
      case 'green': return 'Geringes Datenschutz-Risiko';
      default: return 'Unbekanntes Risiko';
    }
  }

  getRiskExplanation(level) {
    switch (level) {
      case 'red': 
        return 'Diese Website verwendet wahrscheinlich Marketing-Cookies und Tracking-Technologien für Werbezwecke.';
      case 'yellow':
        return 'Diese Website nutzt möglicherweise Analyse-Cookies zur Verbesserung der Nutzererfahrung.';
      case 'green':
        return 'Diese Website scheint hauptsächlich funktionale Cookies zu verwenden.';
      default:
        return 'Cookie-Verwendung konnte nicht eindeutig bewertet werden.';
    }
  }

  positionOverlay(overlay, banner) {
    const bannerRect = banner.getBoundingClientRect();
    const overlayElement = overlay.querySelector('.guardian-popup');
    
    // Position overlay above or below banner based on available space
    if (bannerRect.top > window.innerHeight / 2) {
      // Position above banner
      overlayElement.style.top = Math.max(10, bannerRect.top - 350) + 'px';
    } else {
      // Position below banner
      overlayElement.style.top = Math.min(bannerRect.bottom + 10, window.innerHeight - 350) + 'px';
    }
    
    // Center horizontally
    overlayElement.style.left = '50%';
    overlayElement.style.transform = 'translateX(-50%)';
  }

  setupOverlayListeners(overlay) {
    const buttons = overlay.querySelectorAll('.guardian-btn');
    
    buttons.forEach(button => {
      button.addEventListener('click', async (e) => {
        const action = e.currentTarget.dataset.action;
        await this.handleUserChoice(action);
        this.hideOverlay(overlay);
      });
    });

    // Close on click outside
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        this.hideOverlay(overlay);
        this.applySilentMode('block'); // Default to block
      }
    });
  }

  async handleUserChoice(action) {
    // Save user preference
    await this.saveDomainSetting(action);
    
    // Apply the choice to current banner
    this.applyBannerAction(action);
    
    // Update badge
    this.updateBadge(action);
    
    console.log('Cookie Guardian: User choice applied', {
      domain: this.domain,
      action: action
    });
  }

  applyBannerAction(action) {
    if (!this.currentBanner) return;

    switch (action) {
      case 'block':
        this.clickBannerButton('reject');
        break;
      case 'essential':
        this.clickBannerButton('settings') || this.clickBannerButton('reject');
        break;
      case 'accept':
        this.clickBannerButton('accept');
        break;
    }

    // Hide banner after short delay
    setTimeout(() => {
      if (this.currentBanner) {
        this.currentBanner.style.display = 'none';
      }
    }, 1000);
  }

  clickBannerButton(buttonType) {
    const patterns = this.buttonPatterns[buttonType];
    
    for (const pattern of patterns) {
      // Try direct button text matching
      const buttons = this.currentBanner.querySelectorAll('button, a, [role="button"]');
      
      for (const button of buttons) {
        const text = button.textContent.toLowerCase().trim();
        if (text.includes(pattern)) {
          this.simulateHumanClick(button);
          return true;
        }
      }
      
      // Try attribute matching
      const attrButton = this.currentBanner.querySelector(
        `[data-testid*="${pattern}"], [class*="${pattern}"], [id*="${pattern}"]`
      );
      
      if (attrButton) {
        this.simulateHumanClick(attrButton);
        return true;
      }
    }
    
    return false;
  }

  simulateHumanClick(element) {
    // Add small random delay to appear more human-like
    setTimeout(() => {
      if (element && typeof element.click === 'function') {
        element.click();
      }
    }, Math.random() * 100 + 50);
  }

  applySilentMode(defaultAction = null) {
    if (this.domainSetting || defaultAction) {
      const action = this.domainSetting ? this.domainSetting.action : defaultAction;
      
      // Wait a bit for banner to appear
      setTimeout(() => {
        this.detectBanners();
        if (this.currentBanner) {
          this.applyBannerAction(action);
        }
      }, 1000);
      
      console.log('Cookie Guardian: Silent mode applied', {
        domain: this.domain,
        action: action
      });
    }
  }

  hideOverlay(overlay) {
    if (overlay && overlay.parentNode) {
      overlay.remove();
    }
    this.overlayShown = false;
  }

  updateBadge(status = null) {
    chrome.runtime.sendMessage({
      action: 'updateBadge',
      status: status || (this.domainSetting ? this.domainSetting.action : null)
    }).catch(console.error);
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new CookieGuardianContent());
} else {
  new CookieGuardianContent();
}