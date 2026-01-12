import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire generateOrderImageBlob function
old_func = '''        function generateOrderImageBlob() {
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

new_func = '''        function generateOrderImageBlob() {
            return new Promise((resolve) => {
                const canvas = document.getElementById('downloadCanvas');
                const ctx = canvas.getContext('2d');

                // Match price list quality - 3600px width
                const width = 3600;
                const margin = 180;
                const contentWidth = width - (margin * 2);
                const rowHeight = 120;
                const itemsHeight = currentOrderItems.length * rowHeight;
                const headerHeight = 600;
                const tableHeaderHeight = 100;
                const notesHeight = document.getElementById('orderNotes').value ? 180 : 0;
                const footerHeight = 400;
                const height = headerHeight + tableHeaderHeight + itemsHeight + notesHeight + footerHeight;

                canvas.width = width;
                canvas.height = height;

                // White background
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);

                // Green header background - same as price list
                ctx.fillStyle = '#fafdf7';
                ctx.fillRect(0, 0, width, headerHeight);

                // Top accent bar
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(0, 0, width, 18);

                let y = 120;

                // Company name - Forest green (matching price list)
                ctx.fillStyle = '#2d6a4f';
                ctx.font = 'bold 144px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('EVERFRESH PRODUCE', width / 2, y + 100);
                y += 180;

                // ORDER SUMMARY title - Fresh green
                ctx.fillStyle = '#52b788';
                ctx.font = 'bold 96px Arial, Helvetica, sans-serif';
                ctx.fillText('ORDER SUMMARY', width / 2, y + 80);
                y += 140;

                // Customer and Date row with green background
                const infoBoxY = y;
                ctx.fillStyle = '#d8f3dc';
                ctx.fillRect(margin, infoBoxY, contentWidth, 140);
                ctx.strokeStyle = '#52b788';
                ctx.lineWidth = 4;
                ctx.strokeRect(margin, infoBoxY, contentWidth, 140);

                // Customer name - left
                ctx.textAlign = 'left';
                ctx.fillStyle = '#1b4332';
                ctx.font = 'bold 54px Arial, Helvetica, sans-serif';
                ctx.fillText(orderCustomerName || 'Walk-in Customer', margin + 40, infoBoxY + 88);

                // Date - right
                ctx.textAlign = 'right';
                const dateStr = new Date().toLocaleDateString('en-AU', {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                });
                ctx.fillStyle = '#2d6a4f';
                ctx.font = '48px Arial, Helvetica, sans-serif';
                ctx.fillText(dateStr, width - margin - 40, infoBoxY + 88);

                y = infoBoxY + 180;

                // Table header - Green background
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(margin, y, contentWidth, tableHeaderHeight);

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 42px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ITEM', margin + 50, y + 65);
                ctx.fillText('QTY', margin + 1800, y + 65);
                ctx.textAlign = 'right';
                ctx.fillText('PRICE', margin + 2400, y + 65);
                ctx.fillText('TOTAL', width - margin - 50, y + 65);

                y += tableHeaderHeight;

                // Table rows
                let grandTotal = 0;
                currentOrderItems.forEach((item, idx) => {
                    // Alternating row colors - light green tint
                    ctx.fillStyle = idx % 2 === 0 ? '#ffffff' : '#f0fdf4';
                    ctx.fillRect(margin, y, contentWidth, rowHeight);

                    // Row border
                    ctx.strokeStyle = '#d1fae5';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(margin, y + rowHeight);
                    ctx.lineTo(width - margin, y + rowHeight);
                    ctx.stroke();

                    // Item name
                    ctx.fillStyle = '#1b4332';
                    ctx.font = 'bold 48px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'left';
                    const displayName = item.product || item.name || 'Item';
                    ctx.fillText(displayName, margin + 50, y + 55);

                    // Grade/description below name
                    if (item.grade && item.grade !== '-' && item.grade !== 'Custom Item') {
                        ctx.fillStyle = '#64748b';
                        ctx.font = '36px Arial, Helvetica, sans-serif';
                        ctx.fillText(item.grade, margin + 50, y + 95);
                    }

                    // Quantity - with circle background
                    ctx.fillStyle = '#d8f3dc';
                    ctx.beginPath();
                    ctx.arc(margin + 1850, y + 60, 45, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#1b4332';
                    ctx.font = 'bold 48px Arial, Helvetica, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(item.qty.toString(), margin + 1850, y + 75);

                    // Unit price
                    ctx.textAlign = 'right';
                    ctx.fillStyle = '#64748b';
                    ctx.font = '44px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.unitPrice.toFixed(item.unitPrice % 1 === 0 ? 0 : 2), margin + 2400, y + 70);

                    // Line total
                    ctx.fillStyle = '#2d6a4f';
                    ctx.font = 'bold 52px Arial, Helvetica, sans-serif';
                    ctx.fillText('$' + item.lineTotal.toFixed(item.lineTotal % 1 === 0 ? 0 : 2), width - margin - 50, y + 70);

                    grandTotal += item.lineTotal;
                    y += rowHeight;
                });

                // Bottom border of table
                ctx.strokeStyle = '#2d6a4f';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(margin, y);
                ctx.lineTo(width - margin, y);
                ctx.stroke();

                y += 50;

                // Notes section if present
                const notes = document.getElementById('orderNotes').value;
                if (notes) {
                    ctx.fillStyle = '#fef3c7';
                    ctx.fillRect(margin, y, contentWidth, 120);
                    ctx.strokeStyle = '#fbbf24';
                    ctx.lineWidth = 3;
                    ctx.strokeRect(margin, y, contentWidth, 120);

                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#92400e';
                    ctx.font = 'bold 36px Arial, Helvetica, sans-serif';
                    ctx.fillText('NOTE:', margin + 30, y + 50);
                    ctx.font = '40px Arial, Helvetica, sans-serif';
                    ctx.fillStyle = '#78350f';
                    ctx.fillText(notes, margin + 180, y + 50);
                    y += 150;
                }

                y += 30;

                // Grand total box - Large and prominent
                const totalBoxWidth = 800;
                const totalBoxHeight = 140;
                const totalBoxX = width - margin - totalBoxWidth;

                // Green gradient-like effect (solid for canvas)
                ctx.fillStyle = '#2d6a4f';
                ctx.fillRect(totalBoxX, y, totalBoxWidth, totalBoxHeight);

                // Inner highlight
                ctx.fillStyle = '#40916c';
                ctx.fillRect(totalBoxX + 4, y + 4, totalBoxWidth - 8, 8);

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 48px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('GRAND TOTAL', totalBoxX + 50, y + 90);

                ctx.textAlign = 'right';
                ctx.font = 'bold 72px Arial, Helvetica, sans-serif';
                ctx.fillText('$' + grandTotal.toFixed(grandTotal % 1 === 0 ? 0 : 2), totalBoxX + totalBoxWidth - 50, y + 98);

                y += totalBoxHeight + 60;

                // Footer
                ctx.fillStyle = '#94a3b8';
                ctx.font = '36px Arial, Helvetica, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Thank you for your business!', width / 2, y);

                y += 50;
                ctx.fillStyle = '#cbd5e1';
                ctx.font = '30px Arial, Helvetica, sans-serif';
                ctx.fillText('Stand 275, Shed C, Sydney Markets', width / 2, y);

                canvas.toBlob(blob => resolve(blob), 'image/png');
            });
        }'''

content = content.replace(old_func, new_func)
print("Replaced generateOrderImageBlob with beautiful design matching price list!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
