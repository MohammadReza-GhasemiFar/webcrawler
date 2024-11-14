from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import os

# تنظیم WebDriver با استفاده از webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# اطلاعات مربوط به سایت‌ها (URL سایت‌ها)
site_info = {
    'digikala': {
        'url': 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/apple',
        'title_selector': "h3.ellipsis-2.text-body2-strong.text-neutral-700.styles_VerticalProductCard__productTitle__6zjjN",
        # تگ عنوان برای دیجی کالا
        'price_selector': "span[data-testid='price-final']",  # تگ قیمت برای دیجی کالا
    },
    'torob': {
        'url': 'https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop/b/14/apple-%D8%A7%D9%BE%D9%84/',
        'title_selector': "h2.desktopProductCard_product-name__qSDp9",  # تگ عنوان برای ترب
        'price_selector': "div.desktopProductCard_product-price-text__folP0",  # تگ قیمت برای ترب
    },
    # می‌توانید اطلاعات سایت‌های دیگر را به همین صورت اضافه کنید
}

# مسیر فایل Excel که داده‌ها در آن ذخیره می‌شود
file_path = "all_products_with_prices_auto_detected.xlsx"

# لیست برای ذخیره تمام محصولات جدید
all_products = []

# دیکشنری برای ذخیره تعداد محصولات برای هر سایت
site_product_counts = {}


# تابع برای اسکرول و استخراج داده‌ها از سایت
def extract_data_from_site(site_url, site_name, title_selector, price_selector):
    driver.get(site_url)
    sleep(5)  # صبر برای بارگذاری اولیه صفحه

    # تعداد دفعاتی که می‌خواهیم اسکرول کنیم (مثلاً 20 بار)
    scroll_count = 20
    site_count = 0  # شمارش تعداد محصولات پیدا شده در این سایت

    # اسکرول به پایین صفحه و استخراج اطلاعات
    for _ in range(scroll_count):
        # اسکرول به پایین صفحه
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # منتظر می‌مانیم تا صفحه بارگذاری شود
        sleep(3)

        # جستجوی تمام تگ‌ها برای پیدا کردن عنوان و قیمت
        try:
            # پیدا کردن عنوان محصول با استفاده از CSS Selector
            title_elements = driver.find_elements(By.CSS_SELECTOR, title_selector)
            # پیدا کردن قیمت محصول با استفاده از CSS Selector
            price_elements = driver.find_elements(By.CSS_SELECTOR, price_selector)

            titles = [element.text.strip() for element in title_elements if len(element.text.strip()) > 2]
            prices = [element.text.strip() for element in price_elements if len(element.text.strip()) > 2]

            # اضافه کردن به لیست و افزودن نام سایت و لینک صفحه
            for title, price in zip(titles, prices):
                all_products.append({'Product Name': title, 'Price': price, 'Site': site_name, 'Link': site_url})
                site_count += 1  # افزایش شمارش برای هر محصول

        except Exception as e:
            print(f"Error extracting data from {site_name}: {e}")

    # ذخیره تعداد محصولات پیدا شده در دیکشنری
    site_product_counts[site_name] = site_count


# اسکرپینگ از سایت‌ها
for site_name, site in site_info.items():
    print(f"Extracting data from {site_name}...")
    extract_data_from_site(site['url'], site_name, site['title_selector'], site['price_selector'])

# چک کردن اینکه آیا فایل قبلاً وجود دارد یا نه
if os.path.exists(file_path):
    # اگر فایل وجود دارد، داده‌های قبلی را می‌خوانیم
    existing_df = pd.read_excel(file_path, engine='openpyxl')
    # اضافه کردن داده‌های جدید به داده‌های قبلی
    new_df = pd.DataFrame(all_products)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    # اگر فایل وجود ندارد، فقط داده‌های جدید را می‌سازیم
    combined_df = pd.DataFrame(all_products)

# ذخیره داده‌ها به یک فایل Excel
combined_df.to_excel(file_path, index=False, engine='openpyxl')

# چاپ تعداد محصولات برای هر سایت
print("Products found for each site:")
for site_name, count in site_product_counts.items():
    print(f"{site_name}: {count} products")

# بستن WebDriver
driver.quit()
