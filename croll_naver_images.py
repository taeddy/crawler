from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
import tqdm
import os
import time


keyword = input("검색어를 입력해주세요: ")
url = "https://search.naver.com/search.naver?where=image&query={}".format(keyword)


driver = webdriver.Chrome()
# driver.maximize_window()
driver.get(url)
driver.implicitly_wait(3)


body = driver.find_element(By.CSS_SELECTOR, "body")
for i in range(3):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

imgs = driver.find_elements(By.CSS_SELECTOR, "img._fe_image_tab_content_thumbnail_image")
# print(len(imgs))
links = []
for img in imgs:
    link = img.get_attribute("src")
    if 'http' in link:
        links.append(link)
# print(links)
# print(len(links))

if not os.path.exists('./{}'.format(keyword)):
    os.makedirs('./{}'.format(keyword))
already_downloaded_images_count = len(os.listdir('./{}/'.format(keyword)))
downloaded_images_count = 0

# 이미지 확장자 확인 후 다운로드
image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
# for idx, link in tqdm.tqdm(enumerate(links)):
for idx, link in enumerate(tqdm.tqdm(links)):
    start, end = link.rfind('.'), link.rfind('&')
    filetype = link[start:end]
    if '%' in filetype:
        filetype = filetype[:filetype.rfind('%')]
    if filetype not in image_ext:
        continue
    filename = "{0}{1:03d}{2}".format(keyword, already_downloaded_images_count+idx, filetype)
    # print(filename)
    urlretrieve(link, './{}/'.format(keyword) + filename)
    downloaded_images_count += 1
print("[ 다운로드 이미지 수: {}개 ]".format(downloaded_images_count))

time.sleep(3)
driver.quit()

import zipfile
zf = zipfile.ZipFile('./{}.zip'.format(keyword), 'w')
for file in os.listdir('./{}'.format(keyword)):
    zf.write('./{}/'.format(keyword) + file)
zf.close()
print("[ 압축 완료 ]")