import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the ugly blue button with modern design
old_button = '''            <button onclick="openOrderPanel()" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px 24px; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35); transition: all 0.2s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M12 5v14M5 12h14"/>
                </svg>
                New Order
            </button>'''

new_button = '''            <button onclick="openOrderPanel()" class="new-order-btn">
                <span class="order-icon-wrap">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="3"/>
                        <line x1="8" y1="10" x2="16" y2="10"/>
                        <line x1="8" y1="14" x2="13" y2="14"/>
                        <circle cx="16.5" cy="17.5" r="4.5" fill="#10b981" stroke="#10b981"/>
                        <path d="M15 17.5l1 1 2-2" stroke="white" stroke-width="1.5"/>
                    </svg>
                </span>
                <span>Order</span>
            </button>'''

content = content.replace(old_button, new_button)
print("1. Replaced button HTML")

# 2. Add CSS for the new button - find place after btn-primary:hover
css_insert_point = ".btn-primary:hover {\n        background: #1e293b;\n    }"

new_css = '''.btn-primary:hover {
        background: #1e293b;
    }

    .new-order-btn {
        position: relative;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        background: #0f172a;
        color: #f8fafc;
        border: none;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.02em;
        cursor: pointer;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .new-order-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.1);
        background: #1e293b;
    }

    .new-order-btn:active {
        transform: translateY(0) scale(0.98);
    }

    .order-icon-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
    }

    .order-icon-wrap svg {
        width: 22px;
        height: 22px;
    }'''

content = content.replace(css_insert_point, new_css)
print("2. Added modern button CSS")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone - Modern unique button applied!")
