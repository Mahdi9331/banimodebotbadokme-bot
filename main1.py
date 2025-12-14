import time
import requests
import os
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ---------------------------------------------------------
# 👇 تنظیمات شما 👇
TELEGRAM_TOKEN = "7762314384:AAFhTNTOOq8KzvqNGqFJ1plxu2IGvbfaygg"
CHAT_ID = "243519314"

# 👇 لیست لینک‌ها 👇
DEFAULT_TARGETS = [
    {"name": "کت تک مردانه", "url": "https://www.banimode.com/1319/%DA%A9%D8%AA-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "پیراهن مردانه (همه)", "url": "https://www.banimode.com/11/%D9%BE%DB%8C%D8%B1%D8%A7%D9%87%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "پیراهن مردانه (برندها)", "url": "https://www.banimode.com/11/%D9%BE%DB%8C%D8%B1%D8%A7%D9%87%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?brand=694%2C2113%2C3274%2C522%2C4%2C469%2C1552%2C479%2C1414%2C3328%2C631%2C1238%2C1293%2C1018%2C1256%2C2455%2C693%2C665%2C2038%2C360%2C1%2C2%2C683%2C614%2C415%2C1040%2C849%2C1276%2C3427%2C1335%2C377%2C2080%2C3151%2C445%2C965%2C801%2C82%2C2524%2C1072%2C2713%2C905%2C748%2C488%2C921%2C823%2C733%2C848%2C1148%2C3730&sort%7Cprice=asc"},
    {"name": "ژاکت و پلیور", "url": "https://www.banimode.com/9/%DA%98%D8%A7%DA%A9%D8%AA-%D9%88-%D9%BE%D9%84%DB%8C%D9%88%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوار کتان", "url": "https://www.banimode.com/371/%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%DA%A9%D8%AA%D8%A7%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوار مردانه", "url": "https://www.banimode.com/8/%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوارک مردانه", "url": "https://www.banimode.com/12/%D8%B4%D9%84%D9%88%D8%A7%D8%B1%DA%A9-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کت چرم", "url": "https://www.banimode.com/1780/%DA%A9%D8%AA-%DA%86%D8%B1%D9%85-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "لباس راحتی", "url": "https://www.banimode.com/871/%D9%84%D8%A8%D8%A7%D8%B3-%D8%B1%D8%A7%D8%AD%D8%AA%DB%8C-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کفش ورزشی", "url": "https://www.banimode.com/529/category-men-sport-shoes?sort%7Cprice=asc"},
    {"name": "کفش رسمی", "url": "https://www.banimode.com/817/%DA%A9%D9%81%D8%B4-%D8%B1%D8%B3%D9%85%DB%8C-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کت و شلوار", "url": "https://www.banimode.com/1105/%DA%A9%D8%AA-%D9%88-%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "لباس ورزشی", "url": "https://www.banimode.com/932/category-men-sportswear?sort%7Cprice=asc"},
    {"name": "پالتو مردانه", "url": "https://www.banimode.com/886/%D9%BE%D8%A7%D9%84%D8%AA%D9%88-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "مایو شنا", "url": "https://www.banimode.com/4651/%D9%85%D8%A7%DB%8C%D9%88-%D8%B4%D9%86%D8%A7-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "برند هالیدی", "url": "https://www.banimode.com/Brand/693/%D9%87%D8%A7%D9%84%DB%8C%D8%AF%DB%8C?category=832%2C871%2C1338%2C11%2C1630%2C8%2C703%2C3205%2C1545%2C1544%2C3&sort%7Cprice=asc"},
    {"name": "کاپشن مردانه", "url": "https://www.banimode.com/883/%DA%A9%D8%A7%D9%BE%D8%B4%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کفش روزمره", "url": "https://www.banimode.com/815/%DA%A9%D9%81%D8%B4-%D8%B1%D9%88%D8%B2%D9%85%D8%B1%D9%87-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"}
]
# ---------------------------------------------------------

def show_menu(text):
    """نمایش دکمه‌های شیشه‌ای"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    keyboard = {
        "keyboard": [[{"text": "📜 دریافت لیست کامل (تضمینی)"}]],
        "resize_keyboard": True
    }
    requests.post(url, data={"chat_id": CHAT_ID, "text": text, "reply_markup": json.dumps(keyboard)})

def get_last_command():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if not data.get('result'): return None
        
        last_msg = data['result'][-1]['message']
        if str(last_msg['chat']['id']) != CHAT_ID: return None
        if int(time.time()) - last_msg['date'] > 1500: return None
        return last_msg.get('text', '')
    except:
        return None

def take_half_screenshot(target_url):
    print(f"📸 عکس گرفتن از: {target_url[:20]}...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(90)
        driver.get(target_url)
        time.sleep(4)
        
        total = driver.execute_script("return document.body.scrollHeight")
        half = max(3500, int(total/2))
        half = min(half, total)
        
        for i in range(0, half, 800):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.3)
            
        driver.set_window_size(1920, half+50)
        driver.execute_script("window.scrollTo(0,0)")
        time.sleep(1.5)
        driver.save_screenshot("screenshot.png")
        return "screenshot.png"
    except:
        return None
    finally:
        if driver: driver.quit()

def send_photo_strict(image_path, caption):
    """این تابع تا زمانی که عکس ارسال نشود، ول کن نیست!"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    # 🔴 حلقه تلاش (Retry) تا ۵ بار
    # اگر بیشتر از ۵ بار شد، یعنی مشکل جدی است و باید رد کنیم تا سرور هنگ نکند
    for attempt in range(1, 6):
        try:
            with open(image_path, "rb") as f:
                res = requests.post(url, files={"photo": f}, data={"chat_id": CHAT_ID, "caption": caption}, timeout=120)
                
            if res.status_code == 200:
                print("✅ ارسال موفق.")
                return True # موفقیت، خروج از حلقه
            else:
                print(f"⚠️ ارور تلگرام ({attempt}/5): {res.text}")
                
        except Exception as e:
            print(f"⚠️ ارور شبکه ({attempt}/5): {e}")
            
        time.sleep(5) # ۵ ثانیه صبر قبل از تلاش بعدی
        
    return False # شکست بعد از ۵ بار تلاش

def main():
    print("--- شروع ---")
    command = get_last_command()
    
    if not command:
        print("💤 دستوری نیست.")
        return

    if "لیست" in command or command.lower() in ['all', 'list']:
        show_menu("🔄 شروع ارسال لیست (حالت تضمینی). لطفاً صبر کنید...")
        
        for index, item in enumerate(DEFAULT_TARGETS):
            print(f"\n--- آیتم {index+1} از {len(DEFAULT_TARGETS)}: {item['name']} ---")
            
            # 1. عکس گرفتن
            img = take_half_screenshot(item['url'])
            
            if img:
                # 2. ارسال (با شرط اینکه حتماً ارسال شود)
                sent = send_photo_strict(img, f"🛍 {item['name']}\n🔗 {item['url']}")
                
                try: os.remove(img)
                except: pass
                
                if not sent:
                    print("❌❌ ارسال ناموفق بود. توقف اضطراری!")
                    # اینجا تصمیم با شماست:
                    # break # اگر می‌خواهید کل لیست متوقف شود این را فعال کنید
                    pass # فعلاً می‌گوییم ادامه بده به بعدی (چون شاید فقط همین لینک خراب است)
            else:
                print("❌ عکس گرفته نشد.")

            time.sleep(2) # استراحت کوتاه
            
        show_menu("✅ تمام لیست ارسال شد.")

    elif command == "/start":
        show_menu("👋 ربات آماده است. دکمه را بزنید.")

    elif command.startswith("http"):
        img = take_half_screenshot(command)
        if img:
            send_photo_strict(img, f"🔗 {command}")
            try: os.remove(img)
            except: pass

if __name__ == "__main__":
    main()
