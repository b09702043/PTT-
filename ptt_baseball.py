# 導入 模組(module) 
import requests 
import time

# 把 到 ptt 棒球版 網址存到URL 變數中
URL = "https://www.ptt.cc/bbs/Baseball/index.html"
# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}
# 發送get 請求 到 ptt 棒球版
response = requests.get(URL, headers = my_headers)

# 導入 BeautifulSoup 模組(module)：解析HTML 語法工具
import bs4
# 2-1 把網頁程式碼(HTML) 丟入 bs4模組分析
soup = bs4.BeautifulSoup(response.text,"html.parser")
# 找最新一頁的網址
cate_part = soup.find_all('div','btn-group btn-group-paging')
for tag in cate_part:
	cond = tag.find_all('a')
	for txt in cond:
		if "上頁" in txt.text:
			last_page_url = txt.get('href')
latest_page = int(last_page_url[last_page_url.find('index') + 5 : last_page_url.find('.html')]) + 1
latest_page_url = 'https://www.ptt.cc/' + last_page_url[:last_page_url.find('index') + 5] + str(latest_page) + '.html'
copy = latest_page

# 蒐集當天所有標題
while True:
	response2 = requests.get(latest_page_url, headers = my_headers)
	soup_page = bs4.BeautifulSoup(response2.text,"html.parser")

	# 2-2 查找所有html 元素 過濾出 標籤名稱為 'div' 同時class為 title 
	posts = soup_page.find_all('div','r-ent')
	today = time.strftime("%m/%d",time.localtime(time.time()))  # today = time.strftime("%Y-%m-%d",time.localtime(time.time()))

	first_date = ''
	i = 0
	#key = ["[分享] 今日", "[情報] 今日", "[閒聊] 今日"]
	for post in posts:
		filt = post.find('div', 'date').text.strip()  # 文章日期
		
		if filt.find('/') == 1:  # 調爬蟲網址日期格式
			filt = '0' + filt
		
		if i == 0 and filt == today:
			first_date = str(filt)
			print(post.find('div', 'title').text.strip() + '\n')
			
			if ("[分享] 今日") in post.find('div', 'title').text:
				# 查找所有html 元素 抓出內容
				web_get = post.find('a')
				web = 'https://www.ptt.cc/' + web_get.get('href')
		
				response_ohtani = requests.get(web)
				soup_ohtani = bs4.BeautifulSoup(response_ohtani.text,"html.parser")
				## 查找所有html 元素 抓出內容
				main_container = soup_ohtani.find(id='main-container')
				# 把所有文字都抓出來
				all_text = main_container.text
				# 把整個內容切割透過 "-- " 切割成2個陣列
				pre_text = all_text.split('--')[0]  # 切過字串後 list 的第一項 aka index = 0
    
				# 把每段文字 根據 '\n' 切開
				texts = pre_text.split('\n')
				# 如果你爬多篇你會發現 
				contents = texts[2:]
				# 內容
				content = '\n'.join(contents)
				print('\n' + content)
				
		elif filt == today: 
			print(post.find('div', 'title').text.strip() + '\n')
			
			if ("[分享] 今日") in post.find('div', 'title').text:
				# 查找所有html 元素 抓出內容
				web_get = post.find('a')
				web = 'https://www.ptt.cc/' + web_get.get('href')
		
				response_ohtani = requests.get(web)
				soup_ohtani = bs4.BeautifulSoup(response_ohtani.text,"html.parser")
				## 查找所有html 元素 抓出內容
				main_container = soup_ohtani.find(id='main-container')
				# 把所有文字都抓出來
				all_text = main_container.text
				# 把整個內容切割透過 "-- " 切割成2個陣列
				pre_text = all_text.split('--')[0]  # 切過字串後 list 的第一項 aka index = 0
    
				# 把每段文字 根據 '\n' 切開
				texts = pre_text.split('\n')
				# 如果你爬多篇你會發現 
				contents = texts[2:]
				# 內容
				content = '\n'.join(contents)
				print('\n' + content)
			
			
		elif filt != today and latest_page != copy:
			continue
		
		# print(i, filt, first_date)
		i += 1

	if first_date != today:
		break
	else:
		latest_page -= 1 
		latest_page_url = 'https://www.ptt.cc/' + last_page_url[:last_page_url.find('index') + 5] + str(latest_page) + '.html'
		print('=========================================================\n')