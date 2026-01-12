import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the generateOrderImageBlob function
old_func_pattern = r'function generateOrderImageBlob\(\) \{[\s\S]*?canvas\.toBlob\(blob => resolve\(blob\), \'image/png\'\);\s*\}\);\s*\}'

new_func = '''function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');

                // Compact portrait layout - mobile friendly
                const width = 1800;
                const margin = 80;
                const contentWidth = width - (margin * 2);
                const rowHeight = 90;
                const itemsHeight = currentOrderItems.length * rowHeight;
                const hasNotes = document.getElementById('orderNotes').value.trim();
                const hasSalesman = salesmanInfo.name || salesmanInfo.phone;

                // Calculate dynamic height
                const headerHeight = 420;
                const salesmanHeight = hasSalesman ? 100 : 0;
                const infoHeight = 140;
                const tableHeaderHeight = 70;
                const notesHeight = hasNotes ? 100 : 0;
                const totalHeight = 160;
                const footerHeight = 120;
                const height = headerHeight + salesmanHeight + infoHeight + tableHeaderHeight + itemsHeight + notesHeight + totalHeight + footerHeight;

                canvas.width = width;
                canvas.height = height;

                // White background
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);

                // Top accent bar - Forest green
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(0, 0, width, 14);

                let y = 60;

                // ===== HEADER =====
                // Light green header background
                ctx.fillStyle = '#f0fdf4';
                ctx.fillRect(0, 14, width, headerHeight - 14);

                // Company name - centered, forest green
                ctx.fillStyle = '#2d6a4f';
                ctx.font = 'bold 72px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('EVERFRESH PRODUCE', width / 2, y + 50);

                // GROUP text - spaced out
                ctx.font = '600 28px Arial, Helvetica, sans-serif';
                ctx.fillStyle = '#52b788';
                ctx.letterSpacing = '8px';
                ctx.fillText('G R O U P', width / 2, y + 90);

                y += 130;

                // Location line
                ctx.fillStyle = '#40916c';
                ctx.font = '32px Arial, Helvetica, sans-serif';
                ctx.fillText('Stand 275, Shed C  ·  Sydney Markets  ·  NSW', width / 2, y);

                y += 60;

                // ORDER SUMMARY badge
                ctx.fillStyle = '#2d6a4f';
                const badgeWidth = 460;
                const badgeHeight = 60;
                const badgeX = (width - badgeWidth) / 2;
                ctx.fillRect(badgeX, y, badgeWidth, badgeHeight);

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 32px Arial, Helvetica, sans-serif';
                ctx.fillText('ORDER SUMMARY', width / 2, y + 42);

                y += badgeHeight + 40;

                // ===== SALESMAN CONTACT BOX =====
                if (hasSalesman) {
                    ctx.fillStyle = '#d8f3dc';
                    ctx.fillRect(margin, y, contentWidth, 70);
                    ctx.strokeStyle = '#52b788';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(margin, y, contentWidth, 70);

                    ctx.fillStyle = '#1b4332';
                    ctx.font = 'bold 28px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';

                    let contactText = 'Sales: ';
                    if (salesmanInfo.name) contactText += salesmanInfo.name;
                    if (salesmanInfo.name && salesmanInfo.phone) contactText += '  ·  ';
                    if (salesmanInfo.phone) contactText += salesmanInfo.phone;

                    ctx.fillText(contactText, margin + 24, y + 46);

                    // Order number on right
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#40916c';
                    ctx.font = '26px Arial, Helvetica, sans-serif';
                    ctx.fillText('#' + Date.now().toString().slice(-6), width - margin - 24, y + 46);

                    y += 90;
                }

                // ===== BILL TO & DATE ROW =====
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(margin, y, contentWidth, infoHeight - 20);
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.strokeRect(margin, y, contentWidth, infoHeight - 20);

                // Left side - BILL TO
                ctx.textAlign = 'left';
                ctx.fillStyle = '#64748b';
                ctx.font = 'bold 22px Arial, Helvetica, sans-serif';
                ctx.fillText('BILL TO', margin + 24, y + 32);

                // Get business name - prioritize businessName from selected customer contact
                let billToName = 'Walk-in Customer';
                if (orderCustomerName && orderCustomerName !== 'Walk-in Customer') {
                    // Find the contact to get business name
                    const contact = customerContacts.find(c =>
                        c.name === orderCustomerName ||
                        c.businessName === orderCustomerName
                    );
                    if (contact && contact.businessName) {
                        billToName = contact.businessName;
                    } else if (contact) {
                        billToName = contact.businessName || contact.name;
                    } else {
                        // Check pricing tiers
                        const tier = customers.find(c => c.name === orderCustomerName);
                        if (tier && tier.linkedContactIndex !== undefined) {
                            const linkedContact = customerContacts[tier.linkedContactIndex];
                            if (linkedContact && linkedContact.businessName) {
                                billToName = linkedContact.businessName;
                            } else {
                                billToName = orderCustomerName;
                            }
                        } else {
                            billToName = orderCustomerName;
                        }
                    }
                }

                ctx.fillStyle = '#1b4332';
                ctx.font = 'bold 38px Arial, Helvetica, sans-serif';
                ctx.fillText(billToName, margin + 24, y + 80);

                // Right side - DATE
                ctx.textAlign = 'right';
                ctx.fillStyle = '#64748b';
                ctx.font = 'bold 22px Arial, Helvetica, sans-serif';
                ctx.fillText('DATE', width - margin - 24, y + 32);

                const dateStr = new Date().toLocaleDateString('en-AU', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric'
                });
                ctx.fillStyle = '#1b4332';
                ctx.font = 'bold 38px Arial, Helvetica, sans-serif';
                ctx.fillText(dateStr, width - margin - 24, y + 80);

                y += infoHeight;

                // ===== TABLE HEADER =====
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(margin, y, contentWidth, tableHeaderHeight);

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 26px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ITEM', margin + 24, y + 45);
                ctx.textAlign = 'center';
                ctx.fillText('QTY', width - margin - 380, y + 45);
                ctx.textAlign = 'right';
                ctx.fillText('RATE', width - margin - 180, y + 45);
                ctx.fillText('AMOUNT', width - margin - 24, y + 45);

                y += tableHeaderHeight;

                // ===== TABLE ROWS =====
                let grandTotal = 0;
                currentOrderItems.forEach((item, idx) => {
                    // Alternating row colors
                    ctx.fillStyle = idx % 2 === 0 ? '#ffffff' : '#f8fdf9';
                    ctx.fillRect(margin, y, contentWidth, rowHeight);

                    // Row bottom border
                    ctx.strokeStyle = '#e5e7eb';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(margin, y + rowHeight);
                    ctx.lineTo(width - margin, y + rowHeight);
                    ctx.stroke();

                    // Item name ONLY (no grade/size)
                    const displayName = item.product || item.name || 'Item';
                    ctx.fillStyle = '#1b4332';
                    ctx.font = '34px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText(displayName, margin + 24, y + 56);

                    // Quantity in circle
                    const qtyX = width - margin - 380;
                    ctx.fillStyle = '#d8f3dc';
                    ctx.beginPath();
                    ctx.arc(qtyX, y + 45, 28, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#1b4332';
                    ctx.font = 'bold 28px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(item.qty.toString(), qtyX, y + 55);

                    // Unit price
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#64748b';
                    ctx.font = '30px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.unitPrice.toFixed(item.unitPrice % 1 === 0 ? 0 : 2), width - margin - 180, y + 56);

                    // Line total
                    ctx.fillStyle = '#2d6a4f';
                    ctx.font = 'bold 34px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.lineTotal.toFixed(item.lineTotal % 1 === 0 ? 0 : 2), width - margin - 24, y + 56);

                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });

                // Table bottom border
                ctx.strokeStyle = '#2d6a4f';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                y += 20;

                // ===== NOTES (if any) =====
                const notes = document.getElementById('orderNotes').value.trim();
                if (notes) {
                    ctx.fillStyle = '#fefce8';
                    ctx.fillRect(margin, y, contentWidth * 0.6, 70);
                    ctx.strokeStyle = '#facc15';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(margin, y, contentWidth * 0.6, 70);

                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#854d0e';
                    ctx.font = 'bold 22px Arial, Helvetica, sans-serif';
                    ctx.fillText('NOTE', margin + 16, y + 28);
                    ctx.font = '26px Arial, Helvetica, sans-serif';
                    ctx.fillStyle = '#713f12';
                    // Truncate if too long
                    const maxLen = 45;
                    const noteText = notes.length > maxLen ? notes.substring(0, maxLen) + '...' : notes;
                    ctx.fillText(noteText, margin + 16, y + 54);

                    y += 90;
                } else {
                    y += 20;
                }

                // ===== GRAND TOTAL BOX =====
                const totalBoxWidth = 400;
                const totalBoxHeight = 80;
                const totalBoxX = width - margin - totalBoxWidth;

                // Green total box
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(totalBoxX, y, totalBoxWidth, totalBoxHeight);

                // Subtle top highlight
                ctx.fillStyle = '#40916c';
                ctx.fillRect(totalBoxX, y, totalBoxWidth, 4);

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 28px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('TOTAL', totalBoxX + 24, y + 52);

                ctx.textAlign = 'right';
                ctx.font = 'bold 44px Arial, Helvetica, sans-serif';
                ctx.fillText('$' + grandTotal.toFixed(grandTotal % 1 === 0 ? 0 : 2), totalBoxX + totalBoxWidth - 24, y + 56);

                y += totalBoxHeight + 30;

                // ===== FOOTER =====
                ctx.fillStyle = '#52b788';
                ctx.font = '28px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Thank you for your business!', width / 2, y);

                // Bottom accent bar
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(0, height - 14, width, 14);

                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

content = re.sub(old_func_pattern, new_func, content)
print("Replaced generateOrderImageBlob with compact professional design!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
