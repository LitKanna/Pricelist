import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the generateOrderImageBlob function
old_func_pattern = r'function generateOrderImageBlob\(\) \{[\s\S]*?canvas\.toBlob\(blob => resolve\(blob\), \'image/png\'\);\s*\}\);\s*\}'

new_func = '''function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');

                // Compact portrait layout
                const width = 1800;
                const margin = 100;
                const contentWidth = width - (margin * 2);
                const rowHeight = 100;
                const itemsHeight = currentOrderItems.length * rowHeight;
                const hasNotes = document.getElementById('orderNotes').value.trim();
                const hasSalesman = salesmanInfo.name || salesmanInfo.phone;

                // Calculate dynamic height with better spacing
                const headerHeight = 480;
                const salesmanHeight = hasSalesman ? 120 : 0;
                const infoHeight = 180;
                const tableHeaderHeight = 80;
                const notesHeight = hasNotes ? 120 : 0;
                const totalHeight = 200;
                const footerHeight = 140;
                const height = headerHeight + salesmanHeight + infoHeight + tableHeaderHeight + itemsHeight + notesHeight + totalHeight + footerHeight;

                canvas.width = width;
                canvas.height = height;

                // ===== BACKGROUND =====
                // Soft warm white background
                ctx.fillStyle = '#fefefe';
                ctx.fillRect(0, 0, width, height);

                // Decorative top section with gradient effect
                const gradient = ctx.createLinearGradient(0, 0, width, 0);
                gradient.addColorStop(0, '#1b4332');
                gradient.addColorStop(0.5, '#2d6a4f');
                gradient.addColorStop(1, '#1b4332');
                ctx.fillStyle = gradient;
                ctx.fillRect(0, 0, width, 200);

                // Curved bottom for header
                ctx.fillStyle = '#2d6a4f';
                ctx.beginPath();
                ctx.moveTo(0, 180);
                ctx.quadraticCurveTo(width / 2, 240, width, 180);
                ctx.lineTo(width, 200);
                ctx.lineTo(0, 200);
                ctx.fill();

                let y = 50;

                // ===== HEADER =====
                // Company name - white on dark green, bold
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 82px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('EVERFRESH PRODUCE', width / 2, y + 60);

                // Decorative line under company name
                ctx.strokeStyle = '#52b788';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(width / 2 - 300, y + 90);
                ctx.lineTo(width / 2 + 300, y + 90);
                ctx.stroke();

                // Small decorative dots
                ctx.fillStyle = '#52b788';
                ctx.beginPath();
                ctx.arc(width / 2 - 320, y + 90, 6, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(width / 2 + 320, y + 90, 6, 0, Math.PI * 2);
                ctx.fill();

                y += 140;

                // Location - on dark background
                ctx.fillStyle = '#95d5b2';
                ctx.font = '600 28px Arial, Helvetica, sans-serif';
                ctx.fillText('Stand 275, Shed C  ·  Sydney Markets  ·  NSW', width / 2, y);

                y = 260;

                // ORDER SUMMARY pill badge
                const pillWidth = 380;
                const pillHeight = 56;
                const pillX = (width - pillWidth) / 2;
                const pillY = y;

                // Pill shadow
                ctx.fillStyle = 'rgba(45, 106, 79, 0.2)';
                ctx.beginPath();
                ctx.roundRect(pillX + 4, pillY + 4, pillWidth, pillHeight, 28);
                ctx.fill();

                // Pill background
                ctx.fillStyle = '#40916c';
                ctx.beginPath();
                ctx.roundRect(pillX, pillY, pillWidth, pillHeight, 28);
                ctx.fill();

                // Pill text
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 26px Arial, Helvetica, sans-serif';
                ctx.fillText('ORDER SUMMARY', width / 2, pillY + 38);

                y += 100;

                // ===== SALESMAN CONTACT =====
                if (hasSalesman) {
                    // Subtle card style
                    ctx.fillStyle = '#f0fdf4';
                    ctx.beginPath();
                    ctx.roundRect(margin, y, contentWidth, 80, 12);
                    ctx.fill();

                    // Left accent bar
                    ctx.fillStyle = '#52b788';
                    ctx.beginPath();
                    ctx.roundRect(margin, y, 6, 80, [12, 0, 0, 12]);
                    ctx.fill();

                    ctx.fillStyle = '#1b4332';
                    ctx.font = '600 30px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';

                    let contactText = '';
                    if (salesmanInfo.name) contactText += salesmanInfo.name;
                    if (salesmanInfo.name && salesmanInfo.phone) contactText += '   ·   ';
                    if (salesmanInfo.phone) contactText += salesmanInfo.phone;

                    ctx.fillText(contactText, margin + 30, y + 50);

                    // Order number badge on right
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#2d6a4f';
                    ctx.font = 'bold 24px Arial, Helvetica, sans-serif';
                    const orderNum = '#' + Date.now().toString().slice(-6);

                    // Order number pill
                    const numWidth = ctx.measureText(orderNum).width + 30;
                    ctx.fillStyle = '#d8f3dc';
                    ctx.beginPath();
                    ctx.roundRect(width - margin - numWidth - 15, y + 22, numWidth + 20, 36, 18);
                    ctx.fill();

                    ctx.fillStyle = '#1b4332';
                    ctx.fillText(orderNum, width - margin - 20, y + 50);

                    y += 110;
                }

                // ===== BILL TO & DATE =====
                // Two cards side by side
                const cardWidth = (contentWidth - 30) / 2;
                const cardHeight = 120;

                // Bill To card
                ctx.fillStyle = '#ffffff';
                ctx.shadowColor = 'rgba(0, 0, 0, 0.06)';
                ctx.shadowBlur = 20;
                ctx.shadowOffsetY = 4;
                ctx.beginPath();
                ctx.roundRect(margin, y, cardWidth, cardHeight, 16);
                ctx.fill();
                ctx.shadowColor = 'transparent';

                // Border
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.textAlign = 'left';
                ctx.fillStyle = '#64748b';
                ctx.font = '600 20px Arial, Helvetica, sans-serif';
                ctx.fillText('BILL TO', margin + 24, y + 35);

                // Get business name
                let billToName = 'Walk-in Customer';
                if (orderCustomerName && orderCustomerName !== 'Walk-in Customer') {
                    const contact = customerContacts.find(c =>
                        c.name === orderCustomerName ||
                        c.businessName === orderCustomerName
                    );
                    if (contact && contact.businessName) {
                        billToName = contact.businessName;
                    } else if (contact) {
                        billToName = contact.businessName || contact.name;
                    } else {
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
                ctx.font = 'bold 36px Arial, Helvetica, sans-serif';
                ctx.fillText(billToName, margin + 24, y + 82);

                // Date card
                const dateCardX = margin + cardWidth + 30;
                ctx.fillStyle = '#ffffff';
                ctx.shadowColor = 'rgba(0, 0, 0, 0.06)';
                ctx.shadowBlur = 20;
                ctx.shadowOffsetY = 4;
                ctx.beginPath();
                ctx.roundRect(dateCardX, y, cardWidth, cardHeight, 16);
                ctx.fill();
                ctx.shadowColor = 'transparent';
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.textAlign = 'right';
                ctx.fillStyle = '#64748b';
                ctx.font = '600 20px Arial, Helvetica, sans-serif';
                ctx.fillText('DATE', dateCardX + cardWidth - 24, y + 35);

                const dateStr = new Date().toLocaleDateString('en-AU', {
                    weekday: 'short',
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric'
                });
                ctx.fillStyle = '#1b4332';
                ctx.font = 'bold 34px Arial, Helvetica, sans-serif';
                ctx.fillText(dateStr, dateCardX + cardWidth - 24, y + 82);

                y += cardHeight + 30;

                // ===== TABLE =====
                // Table container with rounded corners
                const tableHeight = tableHeaderHeight + itemsHeight + 10;

                // Table shadow
                ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
                ctx.beginPath();
                ctx.roundRect(margin + 4, y + 4, contentWidth, tableHeight, 16);
                ctx.fill();

                // Table background
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.roundRect(margin, y, contentWidth, tableHeight, 16);
                ctx.fill();

                // Table border
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Table header
                ctx.save();
                ctx.beginPath();
                ctx.roundRect(margin, y, contentWidth, tableHeaderHeight, [16, 16, 0, 0]);
                ctx.clip();
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(margin, y, contentWidth, tableHeaderHeight);
                ctx.restore();

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 24px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ITEM', margin + 30, y + 50);
                ctx.textAlign = 'center';
                ctx.fillText('QTY', width - margin - 420, y + 50);
                ctx.textAlign = 'right';
                ctx.fillText('RATE', width - margin - 220, y + 50);
                ctx.fillText('AMOUNT', width - margin - 30, y + 50);

                y += tableHeaderHeight;

                // Table rows
                let grandTotal = 0;
                currentOrderItems.forEach((item, idx) => {
                    // Alternating subtle backgrounds
                    if (idx % 2 === 1) {
                        ctx.fillStyle = '#f8fdf9';
                        ctx.fillRect(margin + 2, y, contentWidth - 4, rowHeight);
                    }

                    // Subtle row divider
                    if (idx < currentOrderItems.length - 1) {
                        ctx.strokeStyle = '#f0f0f0';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(margin + 30, y + rowHeight);
                        ctx.lineTo(width - margin - 30, y + rowHeight);
                        ctx.stroke();
                    }

                    // Item name
                    const displayName = item.product || item.name || 'Item';
                    ctx.fillStyle = '#1b4332';
                    ctx.font = '600 32px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText(displayName, margin + 30, y + 60);

                    // Quantity badge
                    const qtyX = width - margin - 420;
                    ctx.fillStyle = '#d8f3dc';
                    ctx.beginPath();
                    ctx.roundRect(qtyX - 28, y + 30, 56, 42, 21);
                    ctx.fill();
                    ctx.fillStyle = '#1b4332';
                    ctx.font = 'bold 26px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(item.qty.toString(), qtyX, y + 60);

                    // Unit price
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#64748b';
                    ctx.font = '28px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.unitPrice.toFixed(item.unitPrice % 1 === 0 ? 0 : 2), width - margin - 220, y + 60);

                    // Line total
                    ctx.fillStyle = '#2d6a4f';
                    ctx.font = 'bold 32px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.lineTotal.toFixed(item.lineTotal % 1 === 0 ? 0 : 2), width - margin - 30, y + 60);

                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });

                y += 30;

                // ===== NOTES =====
                const notes = document.getElementById('orderNotes').value.trim();
                if (notes) {
                    ctx.fillStyle = '#fefce8';
                    ctx.beginPath();
                    ctx.roundRect(margin, y, contentWidth * 0.55, 80, 12);
                    ctx.fill();
                    ctx.strokeStyle = '#fbbf24';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // Note icon circle
                    ctx.fillStyle = '#fbbf24';
                    ctx.beginPath();
                    ctx.arc(margin + 35, y + 40, 18, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 20px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('!', margin + 35, y + 48);

                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#92400e';
                    ctx.font = '600 26px Arial, Helvetica, sans-serif';
                    const maxLen = 40;
                    const noteText = notes.length > maxLen ? notes.substring(0, maxLen) + '...' : notes;
                    ctx.fillText(noteText, margin + 70, y + 50);

                    y += 110;
                } else {
                    y += 20;
                }

                // ===== GRAND TOTAL =====
                const totalBoxWidth = 450;
                const totalBoxHeight = 100;
                const totalBoxX = width - margin - totalBoxWidth;

                // Shadow
                ctx.fillStyle = 'rgba(27, 67, 50, 0.25)';
                ctx.beginPath();
                ctx.roundRect(totalBoxX + 6, y + 6, totalBoxWidth, totalBoxHeight, 20);
                ctx.fill();

                // Gradient background
                const totalGradient = ctx.createLinearGradient(totalBoxX, y, totalBoxX + totalBoxWidth, y);
                totalGradient.addColorStop(0, '#1b4332');
                totalGradient.addColorStop(1, '#2d6a4f');
                ctx.fillStyle = totalGradient;
                ctx.beginPath();
                ctx.roundRect(totalBoxX, y, totalBoxWidth, totalBoxHeight, 20);
                ctx.fill();

                ctx.fillStyle = '#95d5b2';
                ctx.font = '600 26px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('GRAND TOTAL', totalBoxX + 30, y + 62);

                ctx.fillStyle = '#ffffff';
                ctx.textAlign = 'right';
                ctx.font = 'bold 48px Arial, Helvetica, sans-serif';
                ctx.fillText('$' + grandTotal.toFixed(grandTotal % 1 === 0 ? 0 : 2), totalBoxX + totalBoxWidth - 30, y + 68);

                y += totalBoxHeight + 40;

                // ===== FOOTER =====
                // Decorative line
                ctx.strokeStyle = '#d8f3dc';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin + 200, y);
                ctx.lineTo(width - margin - 200, y);
                ctx.stroke();

                // Dots
                ctx.fillStyle = '#52b788';
                ctx.beginPath();
                ctx.arc(margin + 185, y, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(width - margin - 185, y, 5, 0, Math.PI * 2);
                ctx.fill();

                y += 40;

                ctx.fillStyle = '#2d6a4f';
                ctx.font = '600 30px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Thank you for your business!', width / 2, y);

                // Bottom accent bar
                const bottomGradient = ctx.createLinearGradient(0, height - 20, width, height - 20);
                bottomGradient.addColorStop(0, '#1b4332');
                bottomGradient.addColorStop(0.5, '#2d6a4f');
                bottomGradient.addColorStop(1, '#1b4332');
                ctx.fillStyle = bottomGradient;
                ctx.fillRect(0, height - 18, width, 18);

                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

content = re.sub(old_func_pattern, new_func, content)
print("Applied modern vibrant invoice design!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
