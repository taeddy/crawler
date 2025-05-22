from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tqdm
import pandas as pd
import os
url = 'https://n.news.naver.com/article/comment/081/0003543232'
keyword = '윤석열'

# URL 접속
driver = webdriver.Chrome()
driver.get(url)
time.sleep(1)
print('[ 접속 완료 ]')

# 댓글 캡쳐 폴더 생성
if not os.path.exists('comment_capture'):
    os.makedirs('comment_capture')

# 댓글 더보기
print('[ 댓글 더보기 ]')
attemp_count = 0
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, 'a.u_cbox_btn_more').click()
        attemp_count = 0
    except:
        attemp_count += 1
        if attemp_count > 5:
            break # 더보기 버튼이 없으면 종료

# 댓글 요소 찾기
comments = driver.find_elements(By.CSS_SELECTOR, 'li.u_cbox_comment')
print(f'[ {len(comments)}개의 댓글 ]')

# 댓글 내용 추출
## 댓글 작성자: span.u_cbox_nick
## 댓글 내용: span.u_cbox_contents
## 삭제된 댓글: span.u_cbox_comment_delete
result = []
keyword_result = []
for i, comment in enumerate(tqdm.tqdm(comments)):
    author = comment.find_element(By.CSS_SELECTOR, 'span.u_cbox_nick').text
    try:
        content = comment.find_element(By.CSS_SELECTOR, 'span.u_cbox_contents').text
        if keyword in content:
            keyword_result.append((i,author, content))
    except:
        content = '삭제된 댓글입니다.'
    result.append((author, content))

# 댓글 캡쳐
for idx, author, content in keyword_result:
    comments[idx].screenshot('comment_capture/capture{0:03d}.png'.format(idx))

df_comment = pd.DataFrame(result, columns=['작성자', '내용'])
df_comment.to_csv('news_comment.csv', index=False)

driver.quit()
