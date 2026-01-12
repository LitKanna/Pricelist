import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the searchOrderProducts function to filter N/A and add manual option
old_search = '''        function searchOrderProducts(query) {
            const resultsEl = document.getElementById('orderSearchResults');
            if (!query || query.length < 2) { resultsEl.classList.remove('show'); return; }
            const results = [];
            const lowerQuery = query.toLowerCase();
            for (const category in priceData) {
                priceData[category].forEach((item, idx) => {
                    const name = item[0] || '';
                    const grade = item[1] || '';
                    const price = item[2] || '';
                    if (name.toLowerCase().includes(lowerQuery) || grade.toLowerCase().includes(lowerQuery) || category.toLowerCase().includes(lowerQuery)) {
                        let displayPrice = price;
                        if (selectedCustomer && price) {
                            const numPrice = parseFloat(price.replace(/[^0-9.-]/g, ''));
                            if (!isNaN(numPrice)) {
                                let adjusted = numPrice;
                                if (selectedCustomer.adjustmentType === 'percentage') adjusted = numPrice * (1 + selectedCustomer.adjustmentValue / 100);
                                else adjusted = numPrice + selectedCustomer.adjustmentValue;
                                if (shouldRoundToWholeDollar(grade)) adjusted = Math.round(adjusted);
                                else adjusted = Math.round(adjusted * 100) / 100;
                                displayPrice = '$' + adjusted.toFixed(adjusted % 1 === 0 ? 0 : 2);
                            }
                        }
                        results.push({ category, index: idx, name, grade, price: displayPrice });
                    }
                });
            }
            if (results.length === 0) {
                resultsEl.textContent = '';
                const div = document.createElement('div');
                div.style.cssText = 'padding: 16px; text-align: center; color: #94a3b8;';
                div.textContent = 'No products found';
                resultsEl.appendChild(div);
            } else {
                resultsEl.textContent = '';
                results.slice(0, 10).forEach(r => {
                    const div = document.createElement('div');
                    div.className = 'search-result-item';
                    div.onclick = () => addProductToOrder(r.category, r.index);
                    const priceSpan = document.createElement('span');
                    priceSpan.className = 'search-result-price';
                    priceSpan.textContent = r.price;
                    const nameDiv = document.createElement('div');
                    nameDiv.className = 'search-result-name';
                    nameDiv.textContent = r.name;
                    const detailsDiv = document.createElement('div');
                    detailsDiv.className = 'search-result-details';
                    detailsDiv.textContent = r.grade + ' - ' + r.category;
                    div.appendChild(priceSpan);
                    div.appendChild(nameDiv);
                    div.appendChild(detailsDiv);'''

new_search = '''        function isProductAvailable(price) {
            if (!price || price === '') return false;
            const cleaned = price.toString().replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
            return cleaned !== 'na' && cleaned !== 'notavailable';
        }

        function searchOrderProducts(query) {
            const resultsEl = document.getElementById('orderSearchResults');
            if (!query || query.length < 2) { resultsEl.classList.remove('show'); return; }
            const results = [];
            const lowerQuery = query.toLowerCase();
            for (const category in priceData) {
                priceData[category].forEach((item, idx) => {
                    const name = item[0] || '';
                    const grade = item[1] || '';
                    const price = item[2] || '';
                    // Skip unavailable products
                    if (!isProductAvailable(price)) return;
                    if (name.toLowerCase().includes(lowerQuery) || grade.toLowerCase().includes(lowerQuery) || category.toLowerCase().includes(lowerQuery)) {
                        let displayPrice = price;
                        if (selectedCustomer && price) {
                            const numPrice = parseFloat(price.replace(/[^0-9.-]/g, ''));
                            if (!isNaN(numPrice)) {
                                let adjusted = numPrice;
                                if (selectedCustomer.adjustmentType === 'percentage') adjusted = numPrice * (1 + selectedCustomer.adjustmentValue / 100);
                                else adjusted = numPrice + selectedCustomer.adjustmentValue;
                                if (shouldRoundToWholeDollar(grade)) adjusted = Math.round(adjusted);
                                else adjusted = Math.round(adjusted * 100) / 100;
                                displayPrice = '$' + adjusted.toFixed(adjusted % 1 === 0 ? 0 : 2);
                            }
                        }
                        results.push({ category, index: idx, name, grade, price: displayPrice });
                    }
                });
            }
            resultsEl.textContent = '';

            // Show matching products
            if (results.length > 0) {
                results.slice(0, 8).forEach(r => {
                    const div = document.createElement('div');
                    div.className = 'search-result-item';
                    div.onclick = () => addProductToOrder(r.category, r.index);
                    const priceSpan = document.createElement('span');
                    priceSpan.className = 'search-result-price';
                    priceSpan.textContent = r.price;
                    const nameDiv = document.createElement('div');
                    nameDiv.className = 'search-result-name';
                    nameDiv.textContent = r.name;
                    const detailsDiv = document.createElement('div');
                    detailsDiv.className = 'search-result-details';
                    detailsDiv.textContent = r.grade + ' - ' + r.category;
                    div.appendChild(priceSpan);
                    div.appendChild(nameDiv);
                    div.appendChild(detailsDiv);'''

content = content.replace(old_search, new_search)
print("1. Updated search to filter N/A products")

# 2. Find and update the end of search results to add manual option
old_search_end = '''                    resultsEl.appendChild(div);
                });
            }
            resultsEl.classList.add('show');
        }'''

new_search_end = '''                    resultsEl.appendChild(div);
                });
            }

            // Always show "Add custom item" option at the bottom
            const manualDiv = document.createElement('div');
            manualDiv.className = 'search-result-manual';
            manualDiv.onclick = () => openManualProductModal(query);
            const iconSpan = document.createElement('span');
            iconSpan.className = 'manual-add-icon';
            iconSpan.textContent = '+';
            const textSpan = document.createElement('span');
            textSpan.textContent = 'Add "';
            const strongEl = document.createElement('strong');
            strongEl.textContent = query;
            textSpan.appendChild(strongEl);
            textSpan.appendChild(document.createTextNode('" manually'));
            manualDiv.appendChild(iconSpan);
            manualDiv.appendChild(textSpan);
            resultsEl.appendChild(manualDiv);

            resultsEl.classList.add('show');
        }

        function openManualProductModal(prefillName) {
            const modal = document.createElement('div');
            modal.className = 'share-menu-overlay';
            modal.id = 'manualProductModal';

            const menuDiv = document.createElement('div');
            menuDiv.className = 'share-menu';
            menuDiv.style.maxWidth = '360px';

            // Header
            const header = document.createElement('div');
            header.className = 'share-menu-header';
            const h3 = document.createElement('h3');
            h3.textContent = 'Add Custom Item';
            const closeBtn = document.createElement('button');
            closeBtn.className = 'share-menu-close';
            closeBtn.onclick = closeManualProductModal;
            closeBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
            header.appendChild(h3);
            header.appendChild(closeBtn);

            // Body
            const body = document.createElement('div');
            body.className = 'share-menu-body';

            // Name field
            const nameGroup = document.createElement('div');
            nameGroup.style.marginBottom = '16px';
            const nameLabel = document.createElement('label');
            nameLabel.style.cssText = 'display: block; font-size: 12px; font-weight: 600; color: #64748b; margin-bottom: 6px;';
            nameLabel.textContent = 'Product Name';
            const nameInput = document.createElement('input');
            nameInput.type = 'text';
            nameInput.id = 'manualProductName';
            nameInput.value = prefillName || '';
            nameInput.style.cssText = 'width: 100%; padding: 12px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 15px; box-sizing: border-box;';
            nameInput.placeholder = 'e.g. Special Order Item';
            nameGroup.appendChild(nameLabel);
            nameGroup.appendChild(nameInput);

            // Desc field
            const descGroup = document.createElement('div');
            descGroup.style.marginBottom = '16px';
            const descLabel = document.createElement('label');
            descLabel.style.cssText = 'display: block; font-size: 12px; font-weight: 600; color: #64748b; margin-bottom: 6px;';
            descLabel.textContent = 'Description (optional)';
            const descInput = document.createElement('input');
            descInput.type = 'text';
            descInput.id = 'manualProductDesc';
            descInput.style.cssText = 'width: 100%; padding: 12px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 15px; box-sizing: border-box;';
            descInput.placeholder = 'e.g. 10kg box';
            descGroup.appendChild(descLabel);
            descGroup.appendChild(descInput);

            // Price field
            const priceGroup = document.createElement('div');
            priceGroup.style.marginBottom = '20px';
            const priceLabel = document.createElement('label');
            priceLabel.style.cssText = 'display: block; font-size: 12px; font-weight: 600; color: #64748b; margin-bottom: 6px;';
            priceLabel.textContent = 'Price ($)';
            const priceInput = document.createElement('input');
            priceInput.type = 'number';
            priceInput.id = 'manualProductPrice';
            priceInput.style.cssText = 'width: 100%; padding: 12px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 15px; box-sizing: border-box;';
            priceInput.placeholder = '0.00';
            priceInput.step = '0.01';
            priceInput.min = '0';
            priceGroup.appendChild(priceLabel);
            priceGroup.appendChild(priceInput);

            // Add button
            const addBtn = document.createElement('button');
            addBtn.onclick = addManualProduct;
            addBtn.style.cssText = 'width: 100%; padding: 14px; background: #10b981; color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer;';
            addBtn.textContent = 'Add to Order';

            body.appendChild(nameGroup);
            body.appendChild(descGroup);
            body.appendChild(priceGroup);
            body.appendChild(addBtn);

            menuDiv.appendChild(header);
            menuDiv.appendChild(body);
            modal.appendChild(menuDiv);
            document.body.appendChild(modal);
            document.body.classList.add('modal-open');
            nameInput.focus();
        }

        function closeManualProductModal() {
            const modal = document.getElementById('manualProductModal');
            if (modal) modal.remove();
            document.body.classList.remove('modal-open');
        }

        function addManualProduct() {
            const name = document.getElementById('manualProductName').value.trim();
            const desc = document.getElementById('manualProductDesc').value.trim();
            const price = parseFloat(document.getElementById('manualProductPrice').value) || 0;

            if (!name) {
                alert('Please enter a product name');
                return;
            }
            if (price <= 0) {
                alert('Please enter a valid price');
                return;
            }

            currentOrderItems.push({
                category: 'CUSTOM',
                product: name,
                grade: desc || 'Custom Item',
                qty: 1,
                unitPrice: price,
                lineTotal: price,
                isManual: true
            });

            renderOrderItems();
            closeManualProductModal();
            document.getElementById('orderSearchInput').value = '';
            document.getElementById('orderSearchResults').classList.remove('show');
        }'''

content = content.replace(old_search_end, new_search_end)
print("2. Added manual product input option")

# 3. Add CSS for the manual add option
css_insert = '''.order-history-btn:hover {
        border-color: #cbd5e1;
        background: #f8fafc;
        color: #475569;
    }'''

css_with_manual = '''.order-history-btn:hover {
        border-color: #cbd5e1;
        background: #f8fafc;
        color: #475569;
    }

    .search-result-manual {
        padding: 14px 18px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 12px;
        background: #f8fafc;
        border-top: 2px dashed #e2e8f0;
        color: #64748b;
        font-size: 14px;
        transition: all 0.15s;
    }

    .search-result-manual:hover {
        background: #f1f5f9;
        color: #0f172a;
    }

    .manual-add-icon {
        width: 28px;
        height: 28px;
        background: #10b981;
        color: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 600;
    }

    .search-result-manual strong {
        color: #0f172a;
    }'''

content = content.replace(css_insert, css_with_manual)
print("3. Added CSS for manual add option")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone - Search now filters N/A products and has manual add option!")
