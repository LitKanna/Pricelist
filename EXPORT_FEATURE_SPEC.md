# Everfresh Pricelist - Export Feature Specification

## Document Version
- Created: 2026-01-03
- Based on: In-depth technical interview and code analysis

---

## 1. Current State Analysis

### 1.1 Existing Export Functions
| Function | Location | Purpose |
|----------|----------|---------|
| `downloadImage()` | Line 4060 | Main export - generates PNG and downloads |
| `quickShareWhatsApp()` | Line 4350 | Web Share API with fallback |
| `sendToCustomer(index)` | Line 4480 | Send to specific customer |
| `generateImageBlob()` | Line 4550 | Helper for blob generation |
| `collectData()` | Line 3223 | Syncs DOM inputs to priceData |

### 1.2 Identified Issues

#### Critical
1. **Code Duplication**: `downloadImage()` and `generateImageBlob()` duplicate ~150 lines of canvas drawing code
2. **Text Overflow**: Long product names/grades overflow into adjacent columns
3. **Error UX**: Alert with 100+ empty prices becomes unreadable

#### Moderate
4. **Canvas Height Miscalculation**: Height pre-calculated before filtering NA items, causing whitespace
5. **Font Fallback**: Only specifies 'Arial' without fallback stack
6. **Timezone**: Uses local device time instead of Sydney business timezone

#### Minor
7. **Memory**: Blob URLs retained until next generation (acceptable)
8. **Loading indicator**: May not render before UI freeze on large lists

---

## 2. Sharing Architecture (NEW)

### 2.1 Share Options Hierarchy
```
[Share Button]
    ├── iMessage (iOS Shortcut - Auto Send)
    ├── WhatsApp (Clipboard + Direct Link)
    └── Download (Standard PNG Download)
```

### 2.2 iMessage Auto-Send Flow
```
User taps "Share to Customer" → Select iMessage
    ↓
Web app generates UHD image (3600px)
    ↓
Image copied to clipboard
    ↓
Trigger iOS Shortcut via URL: shortcuts://run-shortcut?name=Everfresh%20Pricelist&input=text&text=PHONE,MESSAGE
    ↓
Shortcut:
  1. Gets image from clipboard
  2. Sends to phone number via Messages app
  3. Silent send (Show When Run = OFF)
    ↓
Message delivered automatically
```

**Requirements:**
- User must install "Everfresh Pricelist" Shortcut once (iCloud link provided)
- Works on iOS 15+
- First run requires permission grant

### 2.3 WhatsApp Flow (Enhanced)
```
User taps "Share to Customer" → Select WhatsApp
    ↓
Web app generates UHD image (3600px)
    ↓
Image copied to clipboard via navigator.clipboard.write()
    ↓
If clipboard copy succeeds:
  → Open wa.me/PHONENUMBER?text=MESSAGE
  → Show toast: "Image copied! Paste in chat and send"
    ↓
If clipboard fails:
  → Show "Copy Image" button
  → On click: retry clipboard or download
```

### 2.4 Download Flow (Fallback)
```
User taps "Export"
    ↓
Validate all prices (non-empty)
    ↓
Generate UHD image (3600px)
    ↓
Download as everfresh-price-list-YYYY-MM-DD.png
```

---

## 3. Technical Specifications

### 3.1 Image Generation
| Property | Value |
|----------|-------|
| Width | 3600px (Ultra HD 3x) |
| Format | PNG |
| Quality | Maximum |
| Font | Arial, Helvetica, sans-serif (fallback stack) |

### 3.2 MMS Compression (Android Fallback)
When sending via iMessage to Android device (MMS):
- Detect if message fails or user reports issue
- Provide "Resend Compressed" option
- Target size: ≤800KB
- Method: Reduce canvas to 1600px width

### 3.3 Timezone Handling
- Use Sydney timezone (Australia/Sydney) for "Effective Date"
- Implementation: `toLocaleString('en-AU', { timeZone: 'Australia/Sydney' })`

### 3.4 Text Overflow Handling
```javascript
// Truncate with ellipsis if text exceeds column width
function drawTextTruncated(ctx, text, x, y, maxWidth) {
    let displayText = text;
    while (ctx.measureText(displayText).width > maxWidth && displayText.length > 0) {
        displayText = displayText.slice(0, -1);
    }
    if (displayText !== text) {
        displayText = displayText.slice(0, -3) + '...';
    }
    ctx.fillText(displayText, x, y);
}
```

### 3.5 Empty Price Validation (Smart Notification)
```javascript
// If > 5 empty prices, show summary instead of full list
if (emptyPriceProducts.length > 5) {
    alert(`Cannot export: ${emptyPriceProducts.length} products have empty prices.\n\n` +
          `First 5:\n- ${emptyPriceProducts.slice(0, 5).join('\n- ')}\n\n` +
          `...and ${emptyPriceProducts.length - 5} more.\n\n` +
          `Please fill all prices or mark as "NA".`);
} else {
    // Show full list for ≤5 items
}
```

---

## 4. iOS Shortcut Specification

### 4.1 Shortcut Name
**"Everfresh Pricelist"**

### 4.2 Shortcut Actions
```
1. Receive [Text] input from Share Sheet
2. Split Text by ","
   → Item 1 = Phone Number
   → Item 2 = Message Text
3. Get Clipboard (Image)
4. Send Message
   - Recipients: [Phone Number from step 2]
   - Body: [Message Text from step 2]
   - Attachments: [Clipboard Image from step 3]
   - Show When Run: OFF
```

### 4.3 Distribution
- Host on iCloud: `https://www.icloud.com/shortcuts/[SHORTCUT_ID]`
- Add "Setup iMessage" button in Settings with link
- First-time setup instructions shown in app

### 4.4 URL Scheme Format
```
shortcuts://run-shortcut?name=Everfresh%20Pricelist&input=text&text=PHONE,MESSAGE

Example:
shortcuts://run-shortcut?name=Everfresh%20Pricelist&input=text&text=+61412345678,Hi%20John!%20Here%20are%20today's%20prices.
```

---

## 5. UI Changes

### 5.1 Button Layout Change
**Before:**
```
[Export Button]  [WhatsApp Dropdown]
```

**After:**
```
[Share Button] → Opens submenu:
    ├── [iMessage] - Auto-send via iOS Shortcut
    ├── [WhatsApp] - Clipboard + direct link
    ├── [Download] - Standard PNG export
    └── [Quick Share] - General share sheet
```

### 5.2 Customer Share Menu Enhancement
Add method selection when sharing to specific customer:
```
Customer: John Smith (+61412345678)
[Send via iMessage]  [Send via WhatsApp]
```

### 5.3 Settings Addition
Add in Settings panel:
```
--- iMessage Setup ---
[Install Shortcut] → Opens iCloud link
Status: ✓ Ready / ⚠ Not installed

--- Share Preferences ---
Default method: [iMessage ▼] / WhatsApp / Ask each time
```

---

## 6. Code Refactoring Plan

### 6.1 Eliminate Duplication
Extract shared canvas drawing logic:
```javascript
function drawPriceListCanvas(canvas, priceData, salesmanInfo, options = {}) {
    // All canvas drawing code here
    // Used by both downloadImage() and generateImageBlob()
}
```

### 6.2 New Functions to Add
```javascript
// Clipboard image copy
async function copyImageToClipboard(blob) { ... }

// iMessage via Shortcut
function sendViaIMessage(phone, message) { ... }

// WhatsApp with clipboard
async function sendViaWhatsApp(phone, message, blob) { ... }

// Smart error display
function showValidationErrors(errors) { ... }

// Text truncation helper
function measureAndTruncate(ctx, text, maxWidth) { ... }

// Sydney timezone date
function getSydneyDate() { ... }
```

---

## 7. Data Flow

### 7.1 Export Data Source
| Function | Data Source | Notes |
|----------|-------------|-------|
| downloadImage() | priceData | Base prices only |
| generateImageBlob() | selectedCustomer ? getAdjustedPriceData() : priceData | Respects customer tier |

**Decision**: Keep current behavior (export always uses base prices)

### 7.2 Customer Data Structure (Enhanced)
```javascript
customerContacts = [
    {
        name: "John Smith",
        phone: "+61412345678",
        preferredMethod: "imessage" // NEW: imessage | whatsapp | ask
    }
]
```

---

## 8. Error Handling

### 8.1 Clipboard API Fallback
```javascript
async function copyImageToClipboard(blob) {
    try {
        await navigator.clipboard.write([
            new ClipboardItem({ 'image/png': blob })
        ]);
        return { success: true };
    } catch (error) {
        return { success: false, error: error.message };
    }
}
```

### 8.2 Shortcut Not Installed Detection
- After triggering URL, set a flag
- If user returns within 2 seconds, shortcut likely not installed
- Show "Install Shortcut" prompt

### 8.3 Canvas Size Limits
- Maximum canvas size varies by device (~16k-32k pixels)
- For 50+ categories, height may exceed limits
- Add validation: if estimated height > 16000px, show warning

---

## 9. Testing Checklist

### 9.1 Export Tests
- [ ] Export with all prices filled
- [ ] Export with NA prices (should be filtered)
- [ ] Export with empty prices (should show error)
- [ ] Export with long product names (truncation)
- [ ] Export with 50+ products (performance)
- [ ] Export with customer tier active (should use base prices)

### 9.2 iMessage Tests
- [ ] Shortcut installation via iCloud link
- [ ] First-time permission grant
- [ ] Send to iPhone contact (iMessage)
- [ ] Send to Android contact (MMS)
- [ ] Image quality verification

### 9.3 WhatsApp Tests
- [ ] Clipboard copy success → opens WhatsApp
- [ ] Clipboard copy failure → shows copy button
- [ ] Direct link opens correct contact
- [ ] Paste and send workflow

### 9.4 Cross-Platform Tests
- [ ] iOS Safari
- [ ] iOS Chrome
- [ ] Android Chrome
- [ ] Desktop Chrome (download only)

---

## 10. Implementation Priority

### Phase 1: Bug Fixes (Critical)
1. Text overflow handling
2. Smart error messages
3. Font fallback stack
4. Sydney timezone

### Phase 2: Code Quality
5. Extract shared canvas drawing function
6. Add proper error handling for all paths

### Phase 3: Enhanced Sharing
7. Single Share button with submenu
8. WhatsApp clipboard flow
9. Explicit copy button fallback

### Phase 4: iMessage Integration
10. Create iOS Shortcut
11. Add Shortcut trigger from web
12. Settings panel for Shortcut setup
13. Preferred method per customer

---

## 11. Configuration Constants
```javascript
const EXPORT_CONFIG = {
    canvasWidth: 3600,
    mmsMaxSize: 800000, // 800KB for MMS
    shortcutName: 'Everfresh Pricelist',
    timezone: 'Australia/Sydney',
    maxErrorsToShow: 5,
    fonts: {
        primary: 'Arial, Helvetica, sans-serif',
        sizes: {
            companyName: 168,
            title: 144,
            categoryHeader: 102,
            columnHeader: 78,
            productText: 72,
            price: 78,
            notes: 60
        }
    }
};
```

---

## Appendix A: Decisions Made During Interview

| Topic | Decision | Rationale |
|-------|----------|-----------|
| Resolution | Keep 3600px UHD | User preference |
| Customer tier export | Use base prices | Current behavior acceptable |
| Category order | Use modern JS order | ES6+ guarantees insertion order |
| Notes section | Keep hardcoded | Standard branding |
| Address | Keep hardcoded | Single location business |
| Phone format | Display as entered | User preference |
| Shortcut storage | Web app is source of truth | Single source management |
| OS detection | Try iMessage, manual fallback | Simplest approach |
| Error cleanup | Current try-catch sufficient | User assessment |
