import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace all order panel CSS with modern design
order_css_pattern = r'/\* ={40}\s+ORDER TAKING STYLES[\s\S]*?\.order-btn-share:hover \{[^}]+\}'

new_order_css = '''/* ========================================
       ORDER TAKING STYLES - MODERN
       ======================================== */

    /* Panel Header */
    .order-panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 24px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        margin: -24px -24px 24px -24px;
        border-radius: 20px 20px 0 0;
    }

    .order-panel-title {
        display: flex;
        align-items: center;
        gap: 12px;
        color: white;
    }

    .order-panel-title h2 {
        font-size: 20px;
        font-weight: 700;
        margin: 0;
        color: white;
    }

    .order-panel-icon {
        width: 40px;
        height: 40px;
        background: rgba(16, 185, 129, 0.2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .order-panel-icon svg {
        width: 22px;
        height: 22px;
        color: #10b981;
    }

    .order-close-btn {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .order-close-btn:hover {
        background: rgba(255,255,255,0.2);
        transform: rotate(90deg);
    }

    .order-close-btn svg {
        width: 18px;
        height: 18px;
        color: white;
    }

    /* Customer Selector */
    .order-customer-section {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 20px;
        border: 1px solid #bbf7d0;
    }

    .order-customer-label {
        font-size: 11px;
        font-weight: 700;
        color: #15803d;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .order-customer-select {
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #86efac;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        color: #166534;
        background: white;
        cursor: pointer;
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2315803d' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 12px center;
        background-size: 18px;
        transition: all 0.2s;
    }

    .order-customer-select:focus {
        outline: none;
        border-color: #22c55e;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
    }

    /* Search Box */
    .order-search-container {
        position: relative;
        margin-bottom: 20px;
    }

    .order-search-input {
        width: 100%;
        padding: 16px 20px 16px 52px;
        border: none;
        border-radius: 16px;
        font-size: 16px;
        font-weight: 500;
        background: #f1f5f9;
        box-sizing: border-box;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .order-search-input:focus {
        outline: none;
        background: white;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.08), 0 10px 40px rgba(0,0,0,0.08);
    }

    .order-search-input::placeholder {
        color: #94a3b8;
        font-weight: 400;
    }

    .order-search-icon {
        position: absolute;
        left: 18px;
        top: 50%;
        transform: translateY(-50%);
        color: #64748b;
        pointer-events: none;
    }

    .order-search-results {
        position: absolute;
        top: calc(100% + 8px);
        left: 0;
        right: 0;
        background: white;
        border-radius: 16px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        max-height: 280px;
        overflow-y: auto;
        z-index: 100;
        opacity: 0;
        transform: translateY(-10px) scale(0.98);
        pointer-events: none;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e2e8f0;
    }

    .order-search-results.show {
        opacity: 1;
        transform: translateY(0) scale(1);
        pointer-events: auto;
    }

    .search-result-item {
        padding: 14px 18px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.15s;
        border-bottom: 1px solid #f1f5f9;
    }

    .search-result-item:last-child {
        border-bottom: none;
    }

    .search-result-item:hover {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    }

    .search-result-item:active {
        transform: scale(0.99);
    }

    .search-result-info {
        flex: 1;
    }

    .search-result-name {
        font-weight: 600;
        color: #0f172a;
        font-size: 15px;
    }

    .search-result-detail {
        font-size: 13px;
        color: #64748b;
        margin-top: 2px;
    }

    .search-result-price {
        font-weight: 700;
        color: #10b981;
        font-size: 16px;
        background: #f0fdf4;
        padding: 6px 12px;
        border-radius: 20px;
    }

    /* Section Labels */
    .order-section-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .order-section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: #e2e8f0;
    }

    /* Items Container */
    .order-items-container {
        background: #f8fafc;
        border-radius: 16px;
        padding: 8px;
        margin-bottom: 20px;
        max-height: 260px;
        overflow-y: auto;
        border: 1px solid #e2e8f0;
    }

    .order-item-row {
        display: flex;
        align-items: center;
        background: white;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s;
    }

    .order-item-row:last-child {
        margin-bottom: 0;
    }

    .order-item-row:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .order-item-info {
        flex: 1;
        min-width: 0;
    }

    .order-item-name {
        font-weight: 600;
        color: #0f172a;
        font-size: 14px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .order-item-detail {
        font-size: 12px;
        color: #64748b;
    }

    .order-item-qty-controls {
        display: flex;
        align-items: center;
        gap: 4px;
        background: #f1f5f9;
        border-radius: 10px;
        padding: 4px;
        margin: 0 12px;
    }

    .order-qty-btn {
        width: 32px;
        height: 32px;
        border: none;
        border-radius: 8px;
        background: white;
        color: #0f172a;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.15s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    .order-qty-btn:hover {
        background: #0f172a;
        color: white;
    }

    .order-qty-btn:active {
        transform: scale(0.92);
    }

    .order-qty-value {
        min-width: 36px;
        text-align: center;
        font-weight: 700;
        font-size: 15px;
        color: #0f172a;
    }

    .order-item-total {
        font-weight: 700;
        color: #10b981;
        font-size: 15px;
        min-width: 70px;
        text-align: right;
    }

    .order-item-remove {
        width: 28px;
        height: 28px;
        border: none;
        border-radius: 8px;
        background: #fef2f2;
        color: #ef4444;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-left: 8px;
        transition: all 0.15s;
    }

    .order-item-remove:hover {
        background: #ef4444;
        color: white;
    }

    .order-empty {
        text-align: center;
        padding: 40px 20px;
        color: #94a3b8;
    }

    .order-empty-icon {
        font-size: 48px;
        margin-bottom: 12px;
        opacity: 0.5;
    }

    .order-empty-text {
        font-size: 14px;
    }

    /* Notes Input */
    .order-notes-input {
        width: 100%;
        padding: 14px 16px;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-size: 14px;
        resize: none;
        min-height: 70px;
        box-sizing: border-box;
        transition: all 0.2s;
        font-family: inherit;
    }

    .order-notes-input:focus {
        outline: none;
        border-color: #0f172a;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.08);
    }

    .order-notes-input::placeholder {
        color: #94a3b8;
    }

    /* Total Section */
    .order-total-section {
        background: #0f172a;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .order-total-label {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 500;
    }

    .order-total-amount {
        font-size: 32px;
        font-weight: 800;
        color: #10b981;
    }

    /* Action Buttons */
    .order-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 16px;
    }

    .order-btn {
        padding: 16px 20px;
        border: none;
        border-radius: 14px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .order-btn-save {
        background: #f1f5f9;
        color: #475569;
        border: 2px solid #e2e8f0;
    }

    .order-btn-save:hover {
        background: #e2e8f0;
        border-color: #cbd5e1;
    }

    .order-btn-share {
        background: #10b981;
        color: white;
    }

    .order-btn-share:hover {
        background: #059669;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35);
    }

    .order-btn:active {
        transform: scale(0.97);
    }

    /* History Button */
    .order-history-btn {
        width: 100%;
        padding: 14px;
        background: transparent;
        border: 2px dashed #e2e8f0;
        border-radius: 12px;
        color: #64748b;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.2s;
    }

    .order-history-btn:hover {
        border-color: #cbd5e1;
        background: #f8fafc;
        color: #475569;
    }'''

content = re.sub(order_css_pattern, new_order_css, content)
print("1. Replaced order panel CSS")

# 2. Replace the order panel HTML
old_panel_html = '''        <!-- Order Taking Panel -->
        <div class="settings-panel" id="orderPanel">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
                <h2 style="font-size: 22px; font-weight: 700; color: #0f172a; margin: 0;">New Order</h2>
                <button onclick="closeOrderPanel()" style="background: none; border: none; padding: 8px; cursor: pointer; color: #64748b;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            </div>
            <!-- Customer Selection -->
            <div style="margin-bottom: 16px;">
                <label style="display: block; font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Customer</label>
                <select id="orderCustomerSelect" onchange="selectOrderCustomer(this.value)" style="width: 100%; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 15px; background: white; cursor: pointer;">
                    <option value="">Walk-in Customer</option>
                </select>
            </div>
            <div class="order-search-container">
                <svg class="order-search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input type="text" id="orderSearchInput" class="order-search-input" placeholder="Search products..." oninput="searchOrderProducts(this.value)" onfocus="showSearchResults()">
                <div id="orderSearchResults" class="order-search-results"></div>
            </div>
            <div style="font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Order Items</div>
            <div id="orderItemsContainer" class="order-items-container">
                <div class="order-empty" id="orderEmpty"><div class="order-empty-icon">📦</div><div>Search and add products above</div></div>
            </div>
            <div style="font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Notes</div>
            <textarea id="orderNotes" class="order-notes-input" placeholder="Delivery instructions, special requests..."></textarea>
            <div class="order-total-section">
                <div class="order-total-label">Grand Total</div>
                <div class="order-total-amount" id="orderGrandTotal">$0</div>
            </div>
            <div class="order-actions">
                <button class="order-btn order-btn-save" onclick="saveCurrentOrder()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                    Save Order
                </button>
                <button class="order-btn order-btn-share" onclick="shareCurrentOrder()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                    Share Order
                </button>
            </div>
            <button onclick="openOrderHistory()" style="width: 100%; margin-top: 16px; padding: 12px; background: none; border: 1px solid #e2e8f0; border-radius: 10px; color: #64748b; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                View Order History
            </button>
        </div>'''

new_panel_html = '''        <!-- Order Taking Panel -->
        <div class="settings-panel" id="orderPanel">
            <div class="order-panel-header">
                <div class="order-panel-title">
                    <div class="order-panel-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                            <line x1="16" y1="13" x2="8" y2="13"/>
                            <line x1="16" y1="17" x2="8" y2="17"/>
                        </svg>
                    </div>
                    <h2>New Order</h2>
                </div>
                <button class="order-close-btn" onclick="closeOrderPanel()">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            </div>

            <div class="order-customer-section">
                <div class="order-customer-label">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    Customer
                </div>
                <select id="orderCustomerSelect" class="order-customer-select" onchange="selectOrderCustomer(this.value)">
                    <option value="">Walk-in Customer</option>
                </select>
            </div>

            <div class="order-search-container">
                <svg class="order-search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input type="text" id="orderSearchInput" class="order-search-input" placeholder="Search products..." oninput="searchOrderProducts(this.value)" onfocus="showSearchResults()">
                <div id="orderSearchResults" class="order-search-results"></div>
            </div>

            <div class="order-section-label">Order Items</div>
            <div id="orderItemsContainer" class="order-items-container">
                <div class="order-empty" id="orderEmpty">
                    <div class="order-empty-icon">📋</div>
                    <div class="order-empty-text">Search and add products above</div>
                </div>
            </div>

            <div class="order-section-label">Notes (Optional)</div>
            <textarea id="orderNotes" class="order-notes-input" placeholder="Delivery instructions, special requests..."></textarea>

            <div class="order-total-section">
                <div class="order-total-label">Grand Total</div>
                <div class="order-total-amount" id="orderGrandTotal">$0</div>
            </div>

            <div class="order-actions">
                <button class="order-btn order-btn-save" onclick="saveCurrentOrder()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                    Save
                </button>
                <button class="order-btn order-btn-share" onclick="shareCurrentOrder()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
                    Share
                </button>
            </div>

            <button class="order-history-btn" onclick="openOrderHistory()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                View Order History
            </button>
        </div>'''

content = content.replace(old_panel_html, new_panel_html)
print("2. Replaced order panel HTML")

# 3. Update the renderOrderItems JS to use new empty text class
old_empty = "empty.innerHTML = '<div class=\"order-empty-icon\">📦</div><div>Search and add products above</div>';"
new_empty = "empty.innerHTML = '<div class=\"order-empty-icon\">📋</div><div class=\"order-empty-text\">Search and add products above</div>';"
content = content.replace(old_empty, new_empty)
print("3. Updated empty state JS")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone - Modern order panel applied!")
