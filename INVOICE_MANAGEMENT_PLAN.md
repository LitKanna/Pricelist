# Invoice Management System - Implementation Plan

## Overview
A comprehensive invoice management system that allows customer lookup, persistent invoice tracking, and multiple share/print options.

---

## 1. Enhanced Order/Invoice Data Structure

### Current Structure:
```javascript
{
  id: Date.now(),           // timestamp
  customerId: number|null,
  customerName: string,
  items: array,
  notes: string,
  grandTotal: number,
  createdAt: ISO string,
  status: 'saved'
}
```

### New Structure:
```javascript
{
  id: Date.now(),                    // internal ID (timestamp)
  invoiceNumber: 'INV-20260112-0001', // persistent, human-readable
  customerId: number|null,
  customerName: string,
  businessName: string|null,         // NEW: store business name
  items: array,
  notes: string,
  grandTotal: number,
  createdAt: ISO string,
  status: 'active' | 'cancelled',    // CHANGED: soft delete support
  cancelledAt: ISO string|null       // NEW: when cancelled
}
```

### Invoice Number Format:
- Pattern: `INV-YYYYMMDD-XXXX`
- Example: `INV-20260112-0001`
- Sequential counter per day, stored in localStorage: `everfresh_invoice_counter_YYYYMMDD`
- Generated ONCE when order is created, never changes

---

## 2. New UI Components

### A. Invoice Management Panel (`#invoiceManagementPanel`)
Full-screen panel (same pattern as `orderHistoryPanel`)

**Layout:**
```
┌─────────────────────────────────────────┐
│  ← Invoice Management              [X]  │
├─────────────────────────────────────────┤
│  🔍 [Search customer name/business...] │
├─────────────────────────────────────────┤
│  Filter: [All ▼] [Date Range ▼]        │
├─────────────────────────────────────────┤
│  CUSTOMER: Tony's Restaurant            │
│  ┌─────────────────────────────────────┐│
│  │ INV-20260112-0001    $245    [>]   ││
│  │ 12 Jan 2026 • 8 items              ││
│  └─────────────────────────────────────┘│
│  ┌─────────────────────────────────────┐│
│  │ INV-20260110-0003    $180    [>]   ││
│  │ 10 Jan 2026 • 5 items  CANCELLED   ││
│  └─────────────────────────────────────┘│
│                                         │
│  CUSTOMER: Walk-in                      │
│  ┌─────────────────────────────────────┐│
│  │ INV-20260111-0002    $50     [>]   ││
│  │ 11 Jan 2026 • 2 items              ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

### B. Invoice Detail Modal (`#invoiceDetailModal`)
Overlay modal showing single invoice details

**Layout:**
```
┌─────────────────────────────────────────┐
│           INV-20260112-0001        [X]  │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │                                     ││
│  │     [Invoice Preview Image]        ││
│  │     (tap to expand fullscreen)     ││
│  │                                     ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  Customer: Tony's Restaurant            │
│  Date: 12 Jan 2026 at 10:30 AM         │
│  Items: 8 items                         │
│  Total: $245                            │
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌───────────┐ │
│  │ 🖨 Print │ │ 📤 Share│ │ 🗑 Cancel │ │
│  └─────────┘ └─────────┘ └───────────┘ │
└─────────────────────────────────────────┘
```

### C. Share Options Submenu
When "Share" is tapped, show options:
```
┌─────────────────────────────────────────┐
│  Share Invoice                          │
├─────────────────────────────────────────┤
│  💬 iMessage          Auto-send via iOS │
│  📱 WhatsApp          Open in WhatsApp  │
│  ✉️  Email             Attach to email   │
│  💾 Download          Save as PNG       │
└─────────────────────────────────────────┘
```

---

## 3. New JavaScript Functions

### Invoice Number Generation
```javascript
function generateInvoiceNumber() {
  const today = new Date().toISOString().slice(0,10).replace(/-/g, '');
  const counterKey = `everfresh_invoice_counter_${today}`;
  let counter = parseInt(localStorage.getItem(counterKey) || '0') + 1;
  localStorage.setItem(counterKey, counter.toString());
  return `INV-${today}-${counter.toString().padStart(4, '0')}`;
}
```

### Customer Search & Filter
```javascript
function searchInvoices(query) {
  // Search by customerName, businessName, or invoiceNumber
  // Return filtered and grouped by customer
}

function getInvoicesByCustomer(customerId) {
  // Return all invoices for a customer, sorted by date desc
}
```

### Invoice Actions
```javascript
function openInvoiceDetail(orderId) {
  // Show invoice detail modal with preview
}

function printInvoice(orderId) {
  // Generate invoice image and trigger print
}

function shareInvoice(orderId, method) {
  // method: 'imessage' | 'whatsapp' | 'email' | 'download'
}

function cancelInvoice(orderId) {
  // Soft delete: set status='cancelled', cancelledAt=now
  // Show confirmation dialog first
}
```

### Updated Save Order
```javascript
function saveCurrentOrder() {
  // Generate persistent invoice number
  // Include businessName from customer
  // Set status='active'
}
```

---

## 4. CSS Additions

### Invoice Management Panel Styles
- Reuse `.settings-panel` pattern
- Search input styling
- Filter dropdown styling
- Customer group headers
- Invoice list items with status indicators

### Invoice Detail Modal Styles
- Centered overlay modal
- Preview thumbnail with expand capability
- Action buttons row
- Cancelled status styling (red tint, strikethrough)

### Share Submenu Styles
- Reuse existing `.share-option` pattern from share menu

---

## 5. Implementation Steps

### Step 1: Data Migration
- Update `saveCurrentOrder()` to generate invoice numbers
- Add migration for existing orders (assign retroactive invoice numbers)
- Update `saveOrdersToLocal()` and `loadOrdersFromLocal()`

### Step 2: Invoice Management Panel HTML
- Add new panel HTML after `orderHistoryPanel`
- Include search input, filters, invoice list container

### Step 3: Invoice Management Panel CSS
- Add styles for new components
- Cancelled invoice styling

### Step 4: Invoice Detail Modal HTML/CSS
- Add modal HTML
- Preview container
- Action buttons

### Step 5: JavaScript Functions
- `generateInvoiceNumber()`
- `openInvoiceManagement()`
- `searchInvoices(query)`
- `renderInvoiceList(filteredOrders)`
- `openInvoiceDetail(orderId)`
- `generateInvoicePreview(orderId)` - returns blob
- `printInvoice(orderId)`
- `shareInvoice(orderId, method)`
- `cancelInvoice(orderId)`

### Step 6: Integration
- Add "Invoices" button to main UI
- Connect search input to filter
- Wire up all action buttons
- Test all share methods

### Step 7: Data Persistence
- Ensure cloud sync includes new fields
- Migration for existing cloud data

---

## 6. Entry Point

Add button in main UI header area:
```html
<button onclick="openInvoiceManagement()" class="btn btn-secondary">
  📋 Invoices
</button>
```

Or replace/enhance "View Order History" button.

---

## 7. Cancelled Invoice Behavior

- Shows in list with "CANCELLED" badge (red)
- Invoice number displayed with strikethrough
- Can still view details and preview
- Cannot share or print (buttons disabled)
- Shows cancellation date
- Confirmation required before cancelling

---

## Summary of Changes

| File | Changes |
|------|---------|
| index.html (CSS) | ~80 lines new styles |
| index.html (HTML) | ~120 lines new panels/modals |
| index.html (JS) | ~250 lines new functions |
| **Total** | ~450 lines |

This creates a professional invoice management system with:
- Customer lookup by name/business
- Persistent invoice numbers
- Date-wise organization
- Preview, Print, Share (iMessage/WhatsApp/Email)
- Soft delete with audit trail
