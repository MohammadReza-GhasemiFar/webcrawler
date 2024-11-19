import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from googlesearch import search
from webdriver_manager.chrome import ChromeDriverManager

# گرفتن ورودی از کاربر
query = input("کلمه مورد نظر خود را وارد کنید: ")

# ایجاد فایل اکسل جدید
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Results"
ws.append(["Title", "Price", "Link"])  # اضافه کردن هدرها

# پیکربندی و راه‌اندازی مرورگر با Selenium
options = Options()
options.headless = True  # به منظور اجرای مرورگر بدون نمایش UI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# جستجو در گوگل
search_results = search(query, num_results=10)  # تعداد نتایج را می‌توان تغییر داد


# تابعی برای استخراج عنوان و قیمت از صفحات وب با استفاده از Selenium
def extract_product_info(url):
    try:
        driver.get(url)
        time.sleep(2)  # منتظر می‌مانیم تا صفحه به طور کامل بارگذاری شود

        # استخراج عنوان صفحه
        title = driver.title

        # تلاش برای استخراج قیمت (باید این بخش را بر اساس ساختار سایت تغییر دهید)
        price = None
        try:
            # مثال: جستجو برای پیدا کردن قیمت با یک CSS Selector
            price_element = driver.find_element(By.CSS_SELECTOR, '.price')  # به عنوان مثال کلاس 'price'
            if price_element:
                price = price_element.text.strip()
        except:
            price = "Price not found"

        return title, price
    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        return None, None


# پردازش نتایج جستجو
for url in search_results:
    title, price = extract_product_info(url)
    if title and price:
        ws.append([title, price, url])  # ذخیره کردن داده‌ها در فایل اکسل

# ذخیره کردن فایل اکسل
wb.save("products_info.xlsx")
print("اطلاعات در فایل products_info.xlsx ذخیره شد.")

# بستن مرورگر
driver.quit()
