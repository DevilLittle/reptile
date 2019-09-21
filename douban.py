import requests
import re
from openpyxl import Workbook
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# fake_useragent使用
ua = UserAgent()

wb = Workbook()
filename = 'Top250.xlsx'
sheet = wb.active
sheet.title = 'Top250'


def download_page(url):
    headers = {
        'User-Agent': ua.random,
        'Referer': 'https: // movie.douban.com / top250',
        'Sec - Fetch - Mode': 'no - cors'
    }
    r = requests.get(url, headers)
    return r.content


def get_contents(html):
    # 一次爬250条太多了，被豆瓣反爬后soul获取失败
    soul = BeautifulSoup(html, 'html.parser')

    try:
        ol = soul.find('ol', class_='grid_view')
    except Exception as e:
        print('解析页面异常:', e)
    ol_list = ol.find_all('li')
    index = []  # 排名
    name = []  # 名字
    score = []  # 评分
    director = []  # 导演
    info_list = []  # 短评
    for i in ol_list:
        detail = i.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).get_text()
        movie_index = i.find('div', attrs={'class': 'pic'}).find('em').get_text()
        level_score = i.find('span', attrs={'class': 'rating_num'}).get_text()

        director_info = i.find('div', attrs={'class': 'bd'}).find('p').get_text()
        s = '*\/:?"<>|'  # 这9个字符在Windows系统下是不可以出现在文件名中的
        str1 = '\巴拉<1"!11【】>1*hgn/p:?|'  # 样例

        director_list = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', director_info, re.S)  # 只要字符串中的中文，字母，数字
        director_list = "".join(director_list)
        info = i.find('span', attrs={'class': 'inq'})  # 短评
        if info:
            info_list.append(info.get_text())
        else:
            info_list.append('无')
        index.append(movie_index)
        name.append(movie_name)
        score.append(level_score)
        director.append(director_list)

    return index, name, score, director, info_list


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
    movie_index = []  # 排名
    name = []  # 电影名
    score = []  # 评分
    director = []  # 导演
    info_list = []  # 短评

    index = 1
    for i in range(0, 11):
        print('开始下载第{}次'.format(index))
        url = 'https://movie.douban.com/top250?start={}'.format(i * 25)
        html = download_page(url)
        print('下载第{}次完成'.format(index))

        _index, _name, _score, _director, _info_list = get_contents(html)
        movie_index = movie_index + _index
        name = name + _name
        score = score + _score
        director = director + _director
        info_list = info_list + _info_list

        index = index + 1

    table_col = list(zip(movie_index, name, score, director, info_list))
    # print(table_col)
    # print(len(table_col))
    title = ['排名', '电影名', '分数', '导演', '短评']
    write_sheet(title, table_col)


if __name__ == '__main__':
    main()
