import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the generateOrderImageBlob function
old_func_pattern = r'function generateOrderImageBlob\(\) \{[\s\S]*?canvas\.toBlob\(blob => resolve\(blob\), \'image/png\'\);\s*\}\);\s*\}'

new_func = '''function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');

                // STRICT 9:16 aspect ratio
                const width = 1080;
                const height = 1920;
                canvas.width = width;
                canvas.height = height;

                // Price list color palette
                const colors = {
                    forestGreen: '#2d6a4f',    // Header, total box
                    freshGreen: '#52b788',      // Accents, subtitles
                    paleGreen: '#b7e4c7',       // Divider lines
                    lightGreen: '#d8f3dc',      // Note bg, dotted lines
                    barelyWhite: '#fafdf7',     // Table header bg
                    darkestGreen: '#1b4332',    // Main text
                    white: '#ffffff'
                };

                const margin = 60;
                const contentWidth = width - (margin * 2);

                // White background
                ctx.fillStyle = colors.white;
                ctx.fillRect(0, 0, width, height);

                let y = 0;

                // ===== HEADER =====
                const headerHeight = 220;
                ctx.fillStyle = colors.forestGreen;
                ctx.fillRect(0, 0, width, headerHeight);

                // Company name
                ctx.fillStyle = colors.white;
                ctx.font = 'bold 42px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('EVERFRESH PRODUCE GROUP', width / 2, 80);

                // Stand details
                ctx.fillStyle = colors.paleGreen;
                ctx.font = '28px Arial, Helvetica, sans-serif';
                ctx.fillText('Stand 275, Shed C', width / 2, 130);
                ctx.fillText('Sydney Markets', width / 2, 165);

                y = headerHeight + 40;

                // ===== CUSTOMER NAME =====
                ctx.fillStyle = colors.darkestGreen;
                ctx.font = 'bold 36px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';

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
                            billToName = linkedContact?.businessName || orderCustomerName;
                        } else {
                            billToName = orderCustomerName;
                        }
                    }
                }
                ctx.fillText(billToName, margin, y);

                y += 15;

                // Divider line
                ctx.strokeStyle = colors.paleGreen;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                y += 35;

                // Date, Order, Sales info
                ctx.font = '26px Arial, Helvetica, sans-serif';
                ctx.fillStyle = colors.darkestGreen;

                const dateStr = new Date().toLocaleDateString('en-AU', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric'
                });
                ctx.fillText('Date: ' + dateStr, margin, y);

                y += 35;

                // Order number
                ctx.fillStyle = colors.freshGreen;
                ctx.fillText('Order: #' + Date.now().toString().slice(-6), margin, y);

                y += 35;

                // Salesman info
                if (salesmanInfo.name || salesmanInfo.phone) {
                    ctx.fillStyle = colors.darkestGreen;
                    let salesText = 'Sales: ';
                    if (salesmanInfo.name) salesText += salesmanInfo.name;
                    if (salesmanInfo.name && salesmanInfo.phone) salesText += ' · ';
                    if (salesmanInfo.phone) salesText += salesmanInfo.phone;
                    ctx.fillText(salesText, margin, y);
                    y += 35;
                }

                y += 10;

                // Accent line
                ctx.strokeStyle = colors.freshGreen;
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                y += 30;

                // ===== TABLE HEADER =====
                ctx.fillStyle = colors.barelyWhite;
                ctx.fillRect(margin, y, contentWidth, 50);

                ctx.fillStyle = colors.forestGreen;
                ctx.font = 'bold 22px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ITEM', margin + 15, y + 33);
                ctx.textAlign = 'center';
                ctx.fillText('QTY', width - margin - 180, y + 33);
                ctx.textAlign = 'right';
                ctx.fillText('AMT', width - margin - 15, y + 33);

                y += 50;

                // ===== TABLE ROWS =====
                const rowHeight = 55;
                let grandTotal = 0;

                currentOrderItems.forEach((item, idx) => {
                    // Dotted divider between rows
                    if (idx > 0) {
                        ctx.strokeStyle = colors.lightGreen;
                        ctx.lineWidth = 2;
                        ctx.setLineDash([8, 8]);
                        ctx.beginPath();
                        ctx.moveTo(margin + 15, y);
                        ctx.lineTo(width - margin - 15, y);
                        ctx.stroke();
                        ctx.setLineDash([]);
                    }

                    y += 8;

                    // Item name
                    const displayName = item.product || item.name || 'Item';
                    ctx.fillStyle = colors.darkestGreen;
                    ctx.font = '28px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText(displayName, margin + 15, y + 32);

                    // Quantity
                    ctx.textAlign = 'center';
                    ctx.fillText(item.qty.toString(), width - margin - 180, y + 32);

                    // Amount
                    ctx.font = 'bold 28px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'right';
                    ctx.fillText('$' + item.lineTotal.toFixed(item.lineTotal % 1 === 0 ? 0 : 2), width - margin - 15, y + 32);

                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });

                y += 15;

                // Divider line
                ctx.strokeStyle = colors.paleGreen;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                y += 25;

                // ===== NOTES =====
                const notes = document.getElementById('orderNotes').value.trim();
                if (notes) {
                    ctx.fillStyle = colors.lightGreen;
                    ctx.fillRect(margin, y, contentWidth, 55);

                    ctx.fillStyle = colors.darkestGreen;
                    ctx.font = '24px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';
                    const maxLen = 40;
                    const noteText = notes.length > maxLen ? notes.substring(0, maxLen) + '...' : notes;
                    ctx.fillText('📝 ' + noteText, margin + 15, y + 36);

                    y += 75;
                }

                // Accent line
                ctx.strokeStyle = colors.freshGreen;
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                y += 35;

                // ===== TOTAL BOX =====
                const totalBoxHeight = 70;
                ctx.fillStyle = colors.forestGreen;
                ctx.fillRect(margin, y, contentWidth, totalBoxHeight);

                ctx.fillStyle = colors.white;
                ctx.font = 'bold 28px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('TOTAL', margin + 25, y + 45);

                ctx.font = 'bold 38px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'right';
                ctx.fillText('$' + grandTotal.toFixed(grandTotal % 1 === 0 ? 0 : 2), width - margin - 25, y + 48);

                y += totalBoxHeight + 40;

                // ===== FOOTER =====
                ctx.fillStyle = colors.freshGreen;
                ctx.font = '26px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Thank you for your', width / 2, y);
                ctx.fillText('business!', width / 2, y + 35);

                y += 60;

                // Footer accent line
                ctx.strokeStyle = colors.freshGreen;
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

content = re.sub(old_func_pattern, new_func, content)
print("Applied strict 9:16 invoice with price list colors!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
