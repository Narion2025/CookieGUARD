# Test Report

| Browser | Cookie Method | What didn't work | How to reproduce | How to fix |
|---------|---------------|------------------|-----------------|------------|
| jsdom (Node 20) | "essential" option in popup | Text in popup displayed "essentiielle" (typo) | Build extension and open popup, choose a domain with saved setting, observe message under yellow status | Correct typo in `popup.js` to read "Nur essentielle Cookies" |

All automated Jest tests passed after adding a basic test environment.

