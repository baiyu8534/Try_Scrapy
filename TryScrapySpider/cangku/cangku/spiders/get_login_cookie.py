from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
# import pyquery

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(options=chrome_options)

# driver.set_page_load_timeout(5)


driver.get("https://cangku.moe/auth/login")

driver.find_element_by_id("user_login").send_keys("657116885@qq.com")
driver.find_element_by_id("user_password").send_keys("657116885")

driver.find_element_by_xpath('//button[text()="登录"]').click()

cookies = driver.get_cookies()

cookie = {i["name"]: i["value"] for i in cookies}

# with open('cookies_file.json', 'a') as f:
#     json.dump(cookie, f)

with open('cookies_file.json', 'w') as f:
    json.dump(cookie, f)
# print(cookie)



driver.get("https://cangku.moe/category/7")


with open('html1.html', 'w', encoding='utf8') as f:
    f.write(driver.page_source)

# title_list = driver.find_elements_by_xpath('//a[@class="title"]/text()')
a_list = driver.find_elements_by_xpath('//a[@class="title"]')
for a in a_list:
    print("*"*10)
    print(a.text)
    print(a.get_attribute("href"))
    print("*"*10)


driver.close()
print("获取cookie成功")
