import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the generateOrderImageBlob function
old_func_pattern = r'function generateOrderImageBlob\(\) \{[\s\S]*?canvas\.toBlob\(blob => resolve\(blob\), \'image/png\'\);\s*\}\);\s*\}'

new_func = '''function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');

                const width = 1800;
                const margin = 100;
                const contentWidth = width - (margin * 2);
                const rowHeight = 105;
                const itemsHeight = currentOrderItems.length * rowHeight;
                const hasNotes = document.getElementById('orderNotes').value.trim();
                const hasSalesman = salesmanInfo.name || salesmanInfo.phone;

                const headerHeight = 380;
                const waveHeight = 80;
                const salesmanHeight = hasSalesman ? 100 : 0;
                const infoHeight = 160;
                const tableHeaderHeight = 75;
                const notesHeight = hasNotes ? 110 : 0;
                const totalHeight = 180;
                const footerHeight = 160;
                const height = headerHeight + waveHeight + salesmanHeight + infoHeight + tableHeaderHeight + itemsHeight + notesHeight + totalHeight + footerHeight;

                canvas.width = width;
                canvas.height = height;

                // ===== BACKGROUND =====
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);

                // ===== HEADER WITH LAYERED GRADIENT =====
                // Base dark layer
                const headerGrad = ctx.createLinearGradient(0, 0, 0, headerHeight);
                headerGrad.addColorStop(0, '#0d3320');
                headerGrad.addColorStop(0.5, '#1b4332');
                headerGrad.addColorStop(1, '#2d6a4f');
                ctx.fillStyle = headerGrad;
                ctx.fillRect(0, 0, width, headerHeight);

                // Subtle radial glow in center
                const glowGrad = ctx.createRadialGradient(width/2, 150, 0, width/2, 150, 500);
                glowGrad.addColorStop(0, 'rgba(82, 183, 136, 0.15)');
                glowGrad.addColorStop(1, 'rgba(82, 183, 136, 0)');
                ctx.fillStyle = glowGrad;
                ctx.fillRect(0, 0, width, headerHeight);

                // ===== ELEGANT WAVE TRANSITION =====
                // Multiple layered waves for depth
                const waveStart = headerHeight - 20;

                // Back wave (darker, subtle)
                ctx.fillStyle = '#1b4332';
                ctx.beginPath();
                ctx.moveTo(0, waveStart + 30);
                ctx.bezierCurveTo(width * 0.25, waveStart - 10, width * 0.75, waveStart + 70, width, waveStart + 20);
                ctx.lineTo(width, waveStart + 80);
                ctx.lineTo(0, waveStart + 80);
                ctx.closePath();
                ctx.fill();

                // Front wave (main color)
                ctx.fillStyle = '#2d6a4f';
                ctx.beginPath();
                ctx.moveTo(0, waveStart + 50);
                ctx.bezierCurveTo(width * 0.3, waveStart + 10, width * 0.7, waveStart + 90, width, waveStart + 40);
                ctx.lineTo(width, waveStart + 100);
                ctx.lineTo(0, waveStart + 100);
                ctx.closePath();
                ctx.fill();

                // Accent wave (lightest, thin)
                ctx.strokeStyle = '#52b788';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(0, waveStart + 60);
                ctx.bezierCurveTo(width * 0.35, waveStart + 25, width * 0.65, waveStart + 95, width, waveStart + 55);
                ctx.stroke();

                // White transition
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.moveTo(0, waveStart + 70);
                ctx.bezierCurveTo(width * 0.4, waveStart + 40, width * 0.6, waveStart + 100, width, waveStart + 60);
                ctx.lineTo(width, height);
                ctx.lineTo(0, height);
                ctx.closePath();
                ctx.fill();

                // ===== HEADER CONTENT =====
                let y = 80;

                // Company name with subtle text shadow
                ctx.fillStyle = 'rgba(0,0,0,0.2)';
                ctx.font = 'bold 78px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('EVERFRESH PRODUCE', width / 2 + 3, y + 63);

                ctx.fillStyle = '#ffffff';
                ctx.fillText('EVERFRESH PRODUCE', width / 2, y + 60);

                y += 100;

                // Elegant divider with fade effect
                const divGrad = ctx.createLinearGradient(width/2 - 250, 0, width/2 + 250, 0);
                divGrad.addColorStop(0, 'rgba(149, 213, 178, 0)');
                divGrad.addColorStop(0.2, 'rgba(149, 213, 178, 0.8)');
                divGrad.addColorStop(0.5, 'rgba(149, 213, 178, 1)');
                divGrad.addColorStop(0.8, 'rgba(149, 213, 178, 0.8)');
                divGrad.addColorStop(1, 'rgba(149, 213, 178, 0)');
                ctx.strokeStyle = divGrad;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(width/2 - 250, y);
                ctx.lineTo(width/2 + 250, y);
                ctx.stroke();

                // Center diamond
                ctx.fillStyle = '#95d5b2';
                ctx.save();
                ctx.translate(width/2, y);
                ctx.rotate(Math.PI / 4);
                ctx.fillRect(-6, -6, 12, 12);
                ctx.restore();

                y += 40;

                // Location text
                ctx.fillStyle = '#b7e4c7';
                ctx.font = '500 28px Arial, Helvetica, sans-serif';
                ctx.fillText('Stand 275, Shed C  ·  Sydney Markets  ·  NSW', width / 2, y);

                y = headerHeight + waveHeight + 20;

                // ===== SALESMAN SECTION - MODERN CARD =====
                if (hasSalesman) {
                    // Glassmorphism-inspired card
                    ctx.fillStyle = 'rgba(240, 253, 244, 0.9)';
                    ctx.beginPath();
                    ctx.roundRect(margin, y, contentWidth, 75, 16);
                    ctx.fill();

                    // Gradient left border
                    const borderGrad = ctx.createLinearGradient(margin, y, margin, y + 75);
                    borderGrad.addColorStop(0, '#40916c');
                    borderGrad.addColorStop(1, '#2d6a4f');
                    ctx.fillStyle = borderGrad;
                    ctx.beginPath();
                    ctx.roundRect(margin, y, 5, 75, [16, 0, 0, 16]);
                    ctx.fill();

                    // Contact icon circle
                    ctx.fillStyle = '#2d6a4f';
                    ctx.beginPath();
                    ctx.arc(margin + 45, y + 37, 18, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 18px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText('✆', margin + 45, y + 44);

                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#1b4332';
                    ctx.font = '600 28px Arial, Helvetica, sans-serif';

                    let contactText = '';
                    if (salesmanInfo.name) contactText += salesmanInfo.name;
                    if (salesmanInfo.name && salesmanInfo.phone) contactText += '   ·   ';
                    if (salesmanInfo.phone) contactText += salesmanInfo.phone;

                    ctx.fillText(contactText, margin + 80, y + 47);

                    // Order number - elegant pill
                    const orderNum = '#' + Date.now().toString().slice(-6);
                    ctx.font = 'bold 22px Arial';
                    const numWidth = ctx.measureText(orderNum).width;

                    // Pill with gradient
                    const pillGrad = ctx.createLinearGradient(width - margin - numWidth - 50, y + 20, width - margin - 10, y + 20);
                    pillGrad.addColorStop(0, '#2d6a4f');
                    pillGrad.addColorStop(1, '#40916c');
                    ctx.fillStyle = pillGrad;
                    ctx.beginPath();
                    ctx.roundRect(width - margin - numWidth - 45, y + 22, numWidth + 40, 32, 16);
                    ctx.fill();

                    ctx.fillStyle = '#ffffff';
                    ctx.textAlign = 'right';
                    ctx.fillText(orderNum, width - margin - 25, y + 47);

                    y += 100;
                }

                // ===== BILL TO & DATE CARDS =====
                const cardWidth = (contentWidth - 40) / 2;
                const cardHeight = 110;

                // Bill To card with refined shadow
                ctx.shadowColor = 'rgba(45, 106, 79, 0.12)';
                ctx.shadowBlur = 30;
                ctx.shadowOffsetY = 8;
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.roundRect(margin, y, cardWidth, cardHeight, 20);
                ctx.fill();
                ctx.shadowColor = 'transparent';

                // Top accent line
                const accentGrad = ctx.createLinearGradient(margin + 20, 0, margin + 120, 0);
                accentGrad.addColorStop(0, '#52b788');
                accentGrad.addColorStop(1, 'rgba(82, 183, 136, 0)');
                ctx.strokeStyle = accentGrad;
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(margin + 20, y + 1);
                ctx.lineTo(margin + 120, y + 1);
                ctx.stroke();

                ctx.textAlign = 'left';
                ctx.fillStyle = '#64748b';
                ctx.font = '600 18px Arial, Helvetica, sans-serif';
                ctx.fillText('BILL TO', margin + 28, y + 38);

                // Business name
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
                            billToName = linkedContact?.businessName || orderCustomerName;
                        } else {
                            billToName = orderCustomerName;
                        }
                    }
                }

                ctx.fillStyle = '#1b4332';
                ctx.font = 'bold 34px Arial, Helvetica, sans-serif';
                ctx.fillText(billToName, margin + 28, y + 80);

                // Date card
                const dateCardX = margin + cardWidth + 40;
                ctx.shadowColor = 'rgba(45, 106, 79, 0.12)';
                ctx.shadowBlur = 30;
                ctx.shadowOffsetY = 8;
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.roundRect(dateCardX, y, cardWidth, cardHeight, 20);
                ctx.fill();
                ctx.shadowColor = 'transparent';

                // Top accent
                const accentGrad2 = ctx.createLinearGradient(dateCardX + cardWidth - 120, 0, dateCardX + cardWidth - 20, 0);
                accentGrad2.addColorStop(0, 'rgba(82, 183, 136, 0)');
                accentGrad2.addColorStop(1, '#52b788');
                ctx.strokeStyle = accentGrad2;
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(dateCardX + cardWidth - 120, y + 1);
                ctx.lineTo(dateCardX + cardWidth - 20, y + 1);
                ctx.stroke();

                ctx.textAlign = 'right';
                ctx.fillStyle = '#64748b';
                ctx.font = '600 18px Arial, Helvetica, sans-serif';
                ctx.fillText('DATE', dateCardX + cardWidth - 28, y + 38);

                const dateStr = new Date().toLocaleDateString('en-AU', {
                    weekday: 'short',
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric'
                });
                ctx.fillStyle = '#1b4332';
                ctx.font = 'bold 32px Arial, Helvetica, sans-serif';
                ctx.fillText(dateStr, dateCardX + cardWidth - 28, y + 80);

                y += cardHeight + 35;

                // ===== TABLE =====
                const tableHeight = tableHeaderHeight + itemsHeight;

                // Table shadow
                ctx.shadowColor = 'rgba(0, 0, 0, 0.08)';
                ctx.shadowBlur = 25;
                ctx.shadowOffsetY = 5;
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.roundRect(margin, y, contentWidth, tableHeight, 20);
                ctx.fill();
                ctx.shadowColor = 'transparent';

                // Table header with gradient
                ctx.save();
                ctx.beginPath();
                ctx.roundRect(margin, y, contentWidth, tableHeaderHeight, [20, 20, 0, 0]);
                ctx.clip();
                const tableHeadGrad = ctx.createLinearGradient(margin, y, margin + contentWidth, y);
                tableHeadGrad.addColorStop(0, '#1b4332');
                tableHeadGrad.addColorStop(0.5, '#2d6a4f');
                tableHeadGrad.addColorStop(1, '#1b4332');
                ctx.fillStyle = tableHeadGrad;
                ctx.fillRect(margin, y, contentWidth, tableHeaderHeight);
                ctx.restore();

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 22px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ITEM', margin + 35, y + 48);
                ctx.textAlign = 'center';
                ctx.fillText('QTY', width - margin - 400, y + 48);
                ctx.textAlign = 'right';
                ctx.fillText('RATE', width - margin - 200, y + 48);
                ctx.fillText('AMOUNT', width - margin - 35, y + 48);

                y += tableHeaderHeight;

                // Table rows
                let grandTotal = 0;
                currentOrderItems.forEach((item, idx) => {
                    if (idx % 2 === 1) {
                        ctx.fillStyle = '#f8fdfb';
                        ctx.fillRect(margin + 2, y, contentWidth - 4, rowHeight);
                    }

                    // Gradient divider line
                    if (idx < currentOrderItems.length - 1) {
                        const rowDivGrad = ctx.createLinearGradient(margin + 35, 0, width - margin - 35, 0);
                        rowDivGrad.addColorStop(0, 'rgba(216, 243, 220, 0)');
                        rowDivGrad.addColorStop(0.1, 'rgba(216, 243, 220, 0.8)');
                        rowDivGrad.addColorStop(0.9, 'rgba(216, 243, 220, 0.8)');
                        rowDivGrad.addColorStop(1, 'rgba(216, 243, 220, 0)');
                        ctx.strokeStyle = rowDivGrad;
                        ctx.lineWidth = 2;
                        ctx.beginPath();
                        ctx.moveTo(margin + 35, y + rowHeight);
                        ctx.lineTo(width - margin - 35, y + rowHeight);
                        ctx.stroke();
                    }

                    // Item name
                    const displayName = item.product || item.name || 'Item';
                    ctx.fillStyle = '#1b4332';
                    ctx.font = '600 30px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText(displayName, margin + 35, y + 62);

                    // Quantity badge with gradient
                    const qtyX = width - margin - 400;
                    const qtyGrad = ctx.createLinearGradient(qtyX - 26, y + 35, qtyX + 26, y + 35);
                    qtyGrad.addColorStop(0, '#d8f3dc');
                    qtyGrad.addColorStop(1, '#b7e4c7');
                    ctx.fillStyle = qtyGrad;
                    ctx.beginPath();
                    ctx.roundRect(qtyX - 26, y + 35, 52, 38, 19);
                    ctx.fill();
                    ctx.fillStyle = '#1b4332';
                    ctx.font = 'bold 24px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(item.qty.toString(), qtyX, y + 62);

                    // Rate
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#64748b';
                    ctx.font = '26px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.unitPrice.toFixed(item.unitPrice % 1 === 0 ? 0 : 2), width - margin - 200, y + 62);

                    // Amount
                    ctx.fillStyle = '#2d6a4f';
                    ctx.font = 'bold 30px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.lineTotal.toFixed(item.lineTotal % 1 === 0 ? 0 : 2), width - margin - 35, y + 62);

                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });

                y += 30;

                // ===== NOTES =====
                const notes = document.getElementById('orderNotes').value.trim();
                if (notes) {
                    ctx.fillStyle = '#fefce8';
                    ctx.beginPath();
                    ctx.roundRect(margin, y, contentWidth * 0.5, 75, 16);
                    ctx.fill();
                    ctx.strokeStyle = '#fcd34d';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.fillStyle = '#f59e0b';
                    ctx.beginPath();
                    ctx.arc(margin + 38, y + 38, 16, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 18px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText('✎', margin + 38, y + 44);

                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#92400e';
                    ctx.font = '500 24px Arial, Helvetica, sans-serif';
                    const maxLen = 35;
                    const noteText = notes.length > maxLen ? notes.substring(0, maxLen) + '...' : notes;
                    ctx.fillText(noteText, margin + 68, y + 46);

                    y += 100;
                } else {
                    y += 15;
                }

                // ===== GRAND TOTAL =====
                const totalBoxWidth = 420;
                const totalBoxHeight = 90;
                const totalBoxX = width - margin - totalBoxWidth;

                // Multi-layer shadow for depth
                ctx.shadowColor = 'rgba(27, 67, 50, 0.3)';
                ctx.shadowBlur = 30;
                ctx.shadowOffsetY = 10;

                // Gradient background
                const totalGrad = ctx.createLinearGradient(totalBoxX, y, totalBoxX + totalBoxWidth, y + totalBoxHeight);
                totalGrad.addColorStop(0, '#1b4332');
                totalGrad.addColorStop(0.5, '#2d6a4f');
                totalGrad.addColorStop(1, '#1b4332');
                ctx.fillStyle = totalGrad;
                ctx.beginPath();
                ctx.roundRect(totalBoxX, y, totalBoxWidth, totalBoxHeight, 22);
                ctx.fill();
                ctx.shadowColor = 'transparent';

                // Inner glow line
                ctx.strokeStyle = 'rgba(149, 213, 178, 0.3)';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(totalBoxX + 4, y + 4, totalBoxWidth - 8, totalBoxHeight - 8, 18);
                ctx.stroke();

                ctx.fillStyle = '#95d5b2';
                ctx.font = '500 22px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('GRAND TOTAL', totalBoxX + 28, y + 55);

                ctx.fillStyle = '#ffffff';
                ctx.textAlign = 'right';
                ctx.font = 'bold 44px Arial, Helvetica, sans-serif';
                ctx.fillText('$' + grandTotal.toFixed(grandTotal % 1 === 0 ? 0 : 2), totalBoxX + totalBoxWidth - 28, y + 60);

                y += totalBoxHeight + 40;

                // ===== ELEGANT FOOTER =====
                // Gradient fade line
                const footerLineGrad = ctx.createLinearGradient(margin + 150, 0, width - margin - 150, 0);
                footerLineGrad.addColorStop(0, 'rgba(82, 183, 136, 0)');
                footerLineGrad.addColorStop(0.3, 'rgba(82, 183, 136, 0.6)');
                footerLineGrad.addColorStop(0.5, 'rgba(82, 183, 136, 1)');
                footerLineGrad.addColorStop(0.7, 'rgba(82, 183, 136, 0.6)');
                footerLineGrad.addColorStop(1, 'rgba(82, 183, 136, 0)');
                ctx.strokeStyle = footerLineGrad;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin + 150, y);
                ctx.lineTo(width - margin - 150, y);
                ctx.stroke();

                // Center leaf/diamond ornament
                ctx.fillStyle = '#52b788';
                ctx.beginPath();
                ctx.moveTo(width/2, y - 8);
                ctx.lineTo(width/2 + 10, y);
                ctx.lineTo(width/2, y + 8);
                ctx.lineTo(width/2 - 10, y);
                ctx.closePath();
                ctx.fill();

                y += 45;

                // Thank you with gradient text effect
                ctx.fillStyle = '#2d6a4f';
                ctx.font = '600 28px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Thank you for your business!', width / 2, y);

                y += 35;

                // Subtle tagline
                ctx.fillStyle = '#94a3b8';
                ctx.font = '400 20px Arial, Helvetica, sans-serif';
                ctx.fillText('Fresh produce, delivered with care', width / 2, y);

                // Bottom wave accent
                ctx.fillStyle = '#2d6a4f';
                ctx.beginPath();
                ctx.moveTo(0, height - 25);
                ctx.bezierCurveTo(width * 0.3, height - 35, width * 0.7, height - 15, width, height - 25);
                ctx.lineTo(width, height);
                ctx.lineTo(0, height);
                ctx.closePath();
                ctx.fill();

                // Accent line on wave
                ctx.strokeStyle = '#52b788';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, height - 22);
                ctx.bezierCurveTo(width * 0.3, height - 32, width * 0.7, height - 12, width, height - 22);
                ctx.stroke();

                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

content = re.sub(old_func_pattern, new_func, content)
print("Applied designer-level invoice!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
