import requests
from openpyxl import Workbook
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

wb = Workbook()
filename = 'Top250.xlsx'
sheet = wb.active
sheet.title = 'Top250'

def download_page(url):
    headers = {
        'User-Agent': str(UserAgent().random),
        'Referer': 'https: // movie.douban.com / top250',
        'Sec - Fetch - Mode': 'no - cors'
    }
    r = requests.get(url, headers)
    return r.content


def get_contents(html):
    # 一次爬250条太多了，被豆瓣反爬后soul获取失败
    soul = BeautifulSoup(html, 'html.parser')
    ol = soul.find('ol', class_='grid_view')
    ol_list = ol.find_all('li')
    name = []  # 名字
    score = []  # 评分
    for i in ol_list:
        detail = i.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).get_text()
        level_score = i.find('span', attrs={'class': 'rating_num'}).get_text()
        name.append(movie_name)
        score.append(level_score)

    return name, score


def write_sheet(table_head, table_col):
    idx = 1
    for i in range(len(table_head)):
        sheet[chr(ord('A') + i) + str(idx)] = table_head[i]

    # write data
    for i in range(len(table_col)):
        idx += 1
        for j in range(len(table_col[i])):
            sheet[chr(ord('A') + j) + str(idx)] = str(table_col[i][j])

    wb.save(filename)


def main():
    url = 'https://movie.douban.com/top250'
    # time.sleep(random.random() * 3)

    name = []
    score = []

    index = 1
    while url:
        print('开始下载第{}次'.format(index))
        # for i in range(1, 11):
        # time.sleep(random.random() * 3)
        # time.sleep(1)
        html = download_page(url)
        print('下载第{}次完成'.format(index))
        _name, _score = get_contents(html)
        name = name + _name
        score = score + _score
        index = index+1
    table_col = list(zip(name, score))
    print(table_col)
    print(len(table_col))
    title = ['电影名', '分数']
    write_sheet(title, table_col)


if __name__ == '__main__':
    main()
