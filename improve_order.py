# Order improvements - innerHTML usage is safe as data comes from internal app state
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Redesign New Order button - make it a nice gradient pill button
old_btn = '''            <button class="btn btn-secondary" onclick="openOrderPanel()" style="margin-right: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
                New Order
            </button>'''

new_btn = '''            <button onclick="openOrderPanel()" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px 24px; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35); transition: all 0.2s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M12 5v14M5 12h14"/>
                </svg>
                New Order
            </button>'''

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    changes += 1
    print('1. Redesigned New Order button')

# 2. Update order panel to add customer picker
old_customer_badge = '''            <div id="orderCustomerBadge" class="order-customer-badge">
                <div class="order-customer-badge-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <div>
                    <div class="order-customer-badge-name" id="orderCustomerName">Walk-in Customer</div>
                    <div class="order-customer-badge-tier" id="orderCustomerTier">Standard Pricing</div>
                </div>
            </div>'''

new_customer_picker = '''            <!-- Customer Selection -->
            <div style="margin-bottom: 16px;">
                <label style="display: block; font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Customer</label>
                <select id="orderCustomerSelect" onchange="selectOrderCustomer(this.value)" style="width: 100%; padding: 14px 16px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 15px; font-weight: 500; color: #1e293b; background: white; cursor: pointer; appearance: none; background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2224%22 height=%2224%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%2364748b%22 stroke-width=%222%22%3E%3Cpolyline points=%226 9 12 15 18 9%22/%3E%3C/svg%3E'); background-repeat: no-repeat; background-position: right 12px center; background-size: 18px;">
                    <option value="">Walk-in Customer</option>
                </select>
            </div>'''

if old_customer_badge in content:
    content = content.replace(old_customer_badge, new_customer_picker)
    changes += 1
    print('2. Added customer picker dropdown')

# 3. Update openOrderPanel to populate customer dropdown
old_open = '''        function openOrderPanel() {
            currentOrderItems = [];
            document.getElementById('orderNotes').value = '';
            document.getElementById('orderSearchInput').value = '';
            document.getElementById('orderSearchResults').classList.remove('show');
            updateOrderCustomerDisplay();
            renderOrderItems();
            document.getElementById('orderPanel').classList.add('show');
            document.body.style.overflow = 'hidden';
        }'''

new_open = '''        let orderCustomerName = 'Walk-in Customer';

        function openOrderPanel() {
            currentOrderItems = [];
            document.getElementById('orderNotes').value = '';
            document.getElementById('orderSearchInput').value = '';
            document.getElementById('orderSearchResults').classList.remove('show');
            populateOrderCustomerDropdown();
            renderOrderItems();
            document.getElementById('orderPanel').classList.add('show');
            document.body.style.overflow = 'hidden';
        }

        function populateOrderCustomerDropdown() {
            const select = document.getElementById('orderCustomerSelect');
            // Build options using DOM methods for safety
            select.textContent = '';

            const defaultOpt = document.createElement('option');
            defaultOpt.value = '';
            defaultOpt.textContent = 'Walk-in Customer';
            select.appendChild(defaultOpt);

            // Add pricing tiers
            customers.forEach(c => {
                const adj = c.adjustmentType === 'percentage'
                    ? (c.adjustmentValue > 0 ? '+' : '') + c.adjustmentValue + '%'
                    : (c.adjustmentValue > 0 ? '+$' : '-$') + Math.abs(c.adjustmentValue);
                const opt = document.createElement('option');
                opt.value = 'tier_' + c.id;
                opt.textContent = c.name + ' (' + adj + ')';
                if (selectedCustomer && selectedCustomer.id === c.id) opt.selected = true;
                select.appendChild(opt);
            });

            // Add contacts without tiers
            customerContacts.forEach(contact => {
                const hasTier = customers.some(c => c.name.toLowerCase() === contact.name.toLowerCase());
                if (!hasTier) {
                    const opt = document.createElement('option');
                    opt.value = 'contact_' + contact.phone;
                    opt.textContent = contact.name;
                    select.appendChild(opt);
                }
            });

            // Set orderCustomerName based on selection
            if (selectedCustomer) {
                orderCustomerName = selectedCustomer.name;
            } else {
                orderCustomerName = 'Walk-in Customer';
            }
        }

        function selectOrderCustomer(value) {
            if (!value) {
                selectedCustomer = null;
                orderCustomerName = 'Walk-in Customer';
            } else if (value.startsWith('tier_')) {
                const id = parseInt(value.replace('tier_', ''));
                selectedCustomer = customers.find(c => c.id === id) || null;
                orderCustomerName = selectedCustomer ? selectedCustomer.name : 'Walk-in Customer';
            } else if (value.startsWith('contact_')) {
                const phone = value.replace('contact_', '');
                const contact = customerContacts.find(c => c.phone === phone);
                selectedCustomer = null;
                orderCustomerName = contact ? contact.name : 'Walk-in Customer';
            }
            if (currentOrderItems.length > 0) recalculateOrderPrices();
        }

        function recalculateOrderPrices() {
            currentOrderItems.forEach(item => {
                const categoryData = priceData[item.category];
                if (categoryData) {
                    const product = categoryData.find(p => p[0] === item.name && p[1] === item.grade);
                    if (product) {
                        let unitPrice = parseFloat(product[2].replace(/[^0-9.-]/g, '')) || 0;
                        if (selectedCustomer) {
                            if (selectedCustomer.adjustmentType === 'percentage') unitPrice = unitPrice * (1 + selectedCustomer.adjustmentValue / 100);
                            else unitPrice = unitPrice + selectedCustomer.adjustmentValue;
                            if (shouldRoundToWholeDollar(item.grade)) unitPrice = Math.round(unitPrice);
                            else unitPrice = Math.round(unitPrice * 100) / 100;
                        }
                        item.unitPrice = unitPrice;
                        item.lineTotal = item.qty * unitPrice;
                    }
                }
            });
            renderOrderItems();
        }'''

if old_open in content:
    content = content.replace(old_open, new_open)
    changes += 1
    print('3. Added customer selection functions')

# 4. Remove old updateOrderCustomerDisplay function
old_display = '''        function updateOrderCustomerDisplay() {
            const nameEl = document.getElementById('orderCustomerName');
            const tierEl = document.getElementById('orderCustomerTier');
            if (selectedCustomer) {
                const adj = selectedCustomer.adjustmentType === 'percentage'
                    ? (selectedCustomer.adjustmentValue > 0 ? '+' : '') + selectedCustomer.adjustmentValue + '%'
                    : (selectedCustomer.adjustmentValue > 0 ? '+' : '-') + '$' + Math.abs(selectedCustomer.adjustmentValue);
                nameEl.textContent = selectedCustomer.name;
                tierEl.textContent = adj + ' pricing';
            } else {
                nameEl.textContent = 'Walk-in Customer';
                tierEl.textContent = 'Standard Pricing';
            }
        }

        function searchOrderProducts'''

new_display = '''        function searchOrderProducts'''

if old_display in content:
    content = content.replace(old_display, new_display)
    changes += 1
    print('4. Removed old display function')

# 5. Update saveCurrentOrder to use orderCustomerName
old_save = '''            const order = {
                id: Date.now(),
                customerId: selectedCustomer ? selectedCustomer.id : null,
                customerName: selectedCustomer ? selectedCustomer.name : 'Walk-in','''

new_save = '''            const order = {
                id: Date.now(),
                customerId: selectedCustomer ? selectedCustomer.id : null,
                customerName: orderCustomerName || 'Walk-in','''

if old_save in content:
    content = content.replace(old_save, new_save)
    changes += 1
    print('5. Updated saveCurrentOrder')

# 6. Completely redesign the invoice image generation
old_gen = '''        function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');
                const width = 2400, margin = 120, rowHeight = 90;
                let height = 600 + currentOrderItems.length * rowHeight + 300;
                canvas.width = width;
                canvas.height = height;
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);
                let y = margin;
                ctx.fillStyle = '#15803d';
                ctx.font = 'bold 96px -apple-system, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('ORDER SUMMARY', width / 2, y);
                y += 60;
                const dateStr = new Date().toLocaleDateString('en-AU', { day: 'numeric', month: 'long', year: 'numeric' });
                ctx.fillStyle = '#64748b';
                ctx.font = '48px -apple-system, sans-serif';
                ctx.fillText(dateStr, width / 2, y);
                y += 100;
                ctx.fillStyle = '#1e293b';
                ctx.font = 'bold 56px -apple-system, sans-serif';
                ctx.fillText('Customer: ' + (selectedCustomer ? selectedCustomer.name : 'Walk-in'), width / 2, y);
                y += 80;
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();
                y += 40;
                ctx.fillStyle = '#64748b';
                ctx.font = 'bold 42px -apple-system, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('QTY', margin, y);
                ctx.fillText('ITEM', margin + 200, y);
                ctx.textAlign = 'right';
                ctx.fillText('PRICE', width - margin - 300, y);
                ctx.fillText('TOTAL', width - margin, y);
                y += 60;
                ctx.font = '48px -apple-system, sans-serif';
                let grandTotal = 0;
                currentOrderItems.forEach(item => {
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#1e293b';
                    ctx.fillText(item.qty.toString(), margin, y);
                    ctx.fillText(item.name, margin + 200, y);
                    ctx.textAlign = 'right';
                    ctx.fillText('$' + item.unitPrice.toFixed(0), width - margin - 300, y);
                    ctx.fillStyle = '#16a34a';
                    ctx.font = 'bold 48px -apple-system, sans-serif';
                    ctx.fillText('$' + item.lineTotal.toFixed(0), width - margin, y);
                    ctx.font = '48px -apple-system, sans-serif';
                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });
                y += 20;
                ctx.strokeStyle = '#e2e8f0';
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();
                y += 60;
                const notes = document.getElementById('orderNotes').value;
                if (notes) {
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#64748b';
                    ctx.font = '42px -apple-system, sans-serif';
                    ctx.fillText('Notes: ' + notes, margin, y);
                    y += 60;
                }
                ctx.textAlign = 'right';
                ctx.fillStyle = '#1e293b';
                ctx.font = 'bold 72px -apple-system, sans-serif';
                ctx.fillText('TOTAL: $' + grandTotal.toFixed(0), width - margin, y);
                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

new_gen = '''        function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');
                const width = 2400;
                const margin = 100;
                const contentWidth = width - (margin * 2);
                const rowHeight = 80;
                const headerHeight = 380;
                const tableHeaderHeight = 70;
                const footerHeight = 300;
                const itemsHeight = currentOrderItems.length * rowHeight;
                const height = headerHeight + tableHeaderHeight + itemsHeight + footerHeight + 100;
                canvas.width = width;
                canvas.height = height;
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);
                ctx.fillStyle = '#15803d';
                ctx.fillRect(0, 0, width, 12);
                let y = 80;
                ctx.fillStyle = '#15803d';
                ctx.font = 'bold 72px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('EVERFRESH PRODUCE', margin, y);
                ctx.textAlign = 'right';
                ctx.fillStyle = '#1e293b';
                ctx.font = 'bold 48px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.fillText('ORDER', width - margin, y - 10);
                ctx.fillStyle = '#64748b';
                ctx.font = '32px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.fillText('#' + Date.now().toString().slice(-6), width - margin, y + 30);
                y += 80;
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();
                y += 50;
                ctx.textAlign = 'left';
                ctx.fillStyle = '#64748b';
                ctx.font = 'bold 28px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.fillText('BILL TO', margin, y);
                ctx.fillText('DATE', width / 2 + 100, y);
                y += 50;
                ctx.fillStyle = '#1e293b';
                ctx.font = '42px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.fillText(orderCustomerName || 'Walk-in Customer', margin, y);
                const dateStr = new Date().toLocaleDateString('en-AU', { day: 'numeric', month: 'long', year: 'numeric' });
                ctx.fillText(dateStr, width / 2 + 100, y);
                y += 80;
                ctx.fillStyle = '#f8fafc';
                ctx.fillRect(margin, y, contentWidth, tableHeaderHeight);
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.strokeRect(margin, y, contentWidth, tableHeaderHeight);
                ctx.fillStyle = '#475569';
                ctx.font = 'bold 32px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ITEM', margin + 30, y + 46);
                ctx.fillText('QTY', margin + 1100, y + 46);
                ctx.textAlign = 'right';
                ctx.fillText('PRICE', margin + 1550, y + 46);
                ctx.fillText('AMOUNT', width - margin - 30, y + 46);
                y += tableHeaderHeight;
                let grandTotal = 0;
                currentOrderItems.forEach((item, idx) => {
                    if (idx % 2 === 0) {
                        ctx.fillStyle = '#fafafa';
                        ctx.fillRect(margin, y, contentWidth, rowHeight);
                    }
                    ctx.strokeStyle = '#e2e8f0';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(margin, y + rowHeight);
                    ctx.lineTo(width - margin, y + rowHeight);
                    ctx.stroke();
                    ctx.fillStyle = '#1e293b';
                    ctx.font = '38px -apple-system, BlinkMacSystemFont, sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText(item.name, margin + 30, y + 50);
                    if (item.grade && item.grade !== '-') {
                        ctx.fillStyle = '#64748b';
                        ctx.font = '28px -apple-system, BlinkMacSystemFont, sans-serif';
                        ctx.fillText(item.grade, margin + 30 + ctx.measureText(item.name).width + 20, y + 50);
                    }
                    ctx.fillStyle = '#1e293b';
                    ctx.font = '38px -apple-system, BlinkMacSystemFont, sans-serif';
                    ctx.fillText(item.qty.toString(), margin + 1100, y + 50);
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#64748b';
                    ctx.fillText('$' + item.unitPrice.toFixed(item.unitPrice % 1 === 0 ? 0 : 2), margin + 1550, y + 50);
                    ctx.fillStyle = '#1e293b';
                    ctx.font = 'bold 38px -apple-system, BlinkMacSystemFont, sans-serif';
                    ctx.fillText('$' + item.lineTotal.toFixed(item.lineTotal % 1 === 0 ? 0 : 2), width - margin - 30, y + 50);
                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();
                y += 50;
                const notes = document.getElementById('orderNotes').value;
                if (notes) {
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#64748b';
                    ctx.font = 'italic 32px -apple-system, BlinkMacSystemFont, sans-serif';
                    ctx.fillText('Note: ' + notes, margin, y + 20);
                    y += 60;
                }
                const totalBoxWidth = 500;
                const totalBoxX = width - margin - totalBoxWidth;
                ctx.fillStyle = '#15803d';
                ctx.fillRect(totalBoxX, y, totalBoxWidth, 100);
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 36px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('TOTAL', totalBoxX + 30, y + 62);
                ctx.textAlign = 'right';
                ctx.font = 'bold 52px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.fillText('$' + grandTotal.toFixed(grandTotal % 1 === 0 ? 0 : 2), totalBoxX + totalBoxWidth - 30, y + 68);
                y += 140;
                ctx.fillStyle = '#94a3b8';
                ctx.font = '28px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Thank you for your order!', width / 2, y);
                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

if old_gen in content:
    content = content.replace(old_gen, new_gen)
    changes += 1
    print('6. Redesigned invoice image')

# 7. Add smoother search animation CSS
old_search_css = '''    .order-search-results {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        max-height: 250px;
        overflow-y: auto;
        z-index: 100;
        display: none;
    }

    .order-search-results.show {
        display: block;
    }'''

new_search_css = '''    .order-search-results {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        max-height: 250px;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        z-index: 100;
        opacity: 0;
        transform: translateY(-10px);
        pointer-events: none;
        transition: opacity 0.2s ease, transform 0.2s ease;
    }

    .order-search-results.show {
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
    }'''

if old_search_css in content:
    content = content.replace(old_search_css, new_search_css)
    changes += 1
    print('7. Added smooth search animation')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nCompleted with {changes} changes')
