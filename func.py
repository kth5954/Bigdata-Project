import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
from math import *

# url 호출 및 html 긁어오기
def parser(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# 리스트에서 가장 긴 값을 return
def max_len_finder(list):
    max_len = len(list[0])
    for i in range(1, len(list)):
        if len(list[i]) > max_len:
            max_len = len(list[i])
    return max_len

# 상이한 수의 배우 및 감독이 포함된 영화들에 대한 데이터프레임 생성
def dataFrameMaker(list, role):
    column = []
    max_len = int(max_len_finder(list))
    for i in range(max_len):
        column.append(role + "%d" % (i+1))
    return pd.DataFrame(list, columns=column)

# 영화 제목으로 감독, 배우 목록 가져오기
def crawl_names(movies):
    baseUrl = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
    big_list = []
    directors = []
    main_actors = []
    for i in range(len(movies)):
        movies[i] = movies[i].strip()
        plusUrl = "영화" + movies[i] + "출연진"
        url = baseUrl + urllib.parse.quote_plus(plusUrl)
        soup = parser(url)
        if soup.find(class_="title_box") is None:
            plusUrl = movies[i] + "출연진"
            url = baseUrl + urllib.parse.quote_plus(plusUrl)
            soup = parser(url)
        director = soup.select('div ul li:nth-child(1) > div > ul div.title_box strong span')
        main_actor = soup.select('div ul li:nth-child(2) > div > ul div.title_box strong span')
        directors.append([i.text for i in director])
        main_actors.append([i.text for i in main_actor])
        print(i, end=" ")
        if i % 20 == 0:
            print(" ")
    big_list.append(directors)
    big_list.append(main_actors)
    directors = pd.DataFrame(directors)
    directors.columns = ['director%d' % (i+1) for i in range(len(directors.columns))]
    main_actors = pd.DataFrame(main_actors)
    main_actors.columns = ['actor%d' % (i+1) for i in range(len(main_actors.columns))]
    df = pd.concat([directors, main_actors], axis=1)
    return df


def directors_df_maker(fileName):
    file = pd.read_csv(fileName)
    a = list(file["name"])
    directors = []
    crawl_names(a, directors)
    directors = pd.DataFrame(directors, columns=["directors"])
    directors.to_csv("asset/new/directors/directors_%s.csv" % fileName[14:16])


def add_actor_and_director(fileName):
    year = fileName[12:14]
    file = pd.read_csv(fileName)
    a = list(file["name"])
    directors = []
    actors = []
    crawl_names(a, directors, actors)
    directors = dataFrameMaker(directors, "director")
    actors = dataFrameMaker(actors, "actor")
    s = file.join(directors, how='left')
    s = s.join(actors, how='left')
    new_file_name = "asset/new/mov_" + year + ".csv"
    s.to_csv(new_file_name)

def csv_maker():
    for i in range(7):
        filename = "asset/movie_1" + str(i + 3) +".csv"
        add_actor_and_director(filename)

# 배우, 감독 필모그래피 가져오기
def crawl_filmo(names):
    baseUrl = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
    big_list = []
    for i in range(len(names)):
        print(i, end=" ")
        # 검색
        plusUrl = "영화" + names[i] + " 필모그래피"
        url = baseUrl + urllib.parse.quote_plus(plusUrl)
        soup = parser(url)
        filmo_list = []
        filmo_num = soup.find(class_='this_text_number')
        badge_title = soup.find(class_='badge_title')
        if filmo_num is None:
            filmo_list.append("None")
        else:
            filmo_list.append(int(filmo_num.text))
        if badge_title is None:
            filmo_list.append("None")
        elif "천만관객" in badge_title.text:
            filmo_list.append("천만관객")
        else:
            filmo_list.append("??")
        plusUrl = names[i] + "프로필"
        url = baseUrl + urllib.parse.quote_plus(plusUrl)
        soup = parser(url)
        num_of_awards = len(soup.find_all(class_='text', attrs='ul > li > span'))
        if num_of_awards is None:
            filmo_list.append("None")
            continue
        filmo_list.append(num_of_awards)
        big_list.append(filmo_list)
        if i % 20 == 0:
            print(" ")
    return big_list


# 영화제목으로 등급 가져오기
def crawl_grade(movies):
    big_list = []
    baseUrl = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
    for i in range(len(movies)):
        plusUrl = "영화" + movies[i] + "정보"
        url = baseUrl + urllib.parse.quote_plus(plusUrl)
        soup = parser(url)
        print(i, end=" ")
        grade = soup.select_one("div.cm_content_area._cm_content_area_info div div.detail_info dl div:nth-child(2) dd")
        if grade is None:
            big_list.append(None)
            continue
        big_list.append(grade)
        if i % 20 == 0:
            print(" ")
    return big_list

def rating_and_audience(names, job):
    a_avg_list = []
    r_avg_list = []
    cnt = 1
    for name in names:
        print(cnt, name, end=" ")
        baseUrl = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
        plusUrl = name + "필모그래피"
        url = baseUrl + urllib.parse.quote_plus(plusUrl)
        soup = parser(url)

        if soup.find(id="mflick") is None or job not in soup.find(class_="sub_title first_elss"):
            plusUrl = job + name + "필모그래피"
            url = baseUrl + urllib.parse.quote_plus(plusUrl)
            soup = parser(url)

        card_items = soup.find_all(class_="card_item")
        rating_list = []
        r_sum = 0
        aud_num_list = []
        a_sum = 0
        for item in card_items:
            item = (item.get_text()).split(" ")
            for i in range(len(item)):
                if item[i] == '평점':
                    rating_list.append(item[i+1])
                if item[i] == '관객':
                    aud_num_list.append(item[i+1])
        for rating in rating_list:
            r_sum += float(rating)

        for aud_num in aud_num_list:
            if '만' in aud_num:
                a_sum += float(aud_num.replace('만', ""))*10000
            elif ',' in aud_num:
                a_sum += int(aud_num.replace(",", ""))
            else:
                a_sum += float(aud_num)

        try:
            r_avg_list.append(r_sum / len(rating_list))
        except ZeroDivisionError:
            r_avg_list.append("NULL")

        try:
            a_avg_list.append(a_sum / len(aud_num_list))
        except ZeroDivisionError:
            a_avg_list.append("NULL")

        cnt += 1
        if cnt % 10 == 0:
            print("|")

    res = [r_avg_list, a_avg_list]
    res_df_t = pd.DataFrame(res).transpose()
    ret = pd.concat([pd.DataFrame(names), res_df_t], axis=1)
    ret.columns = ['name', 'r_avg', 'a_avg']
    if "감독" in job:
        ret.to_csv("asset/new/director_rna1.csv")
    else:
        ret.to_csv("asset/new/actor_rna1.csv")
    return ret

def name_dropper(job, df):
    i = 1
    while True:
        try:
            df = df.drop(["%s%d" % (job, i)], axis=1)
            i += 1
        except KeyError:
            break
    return df

def merge_avg_value(mov_df, job_df, version):
    r_big = []
    a_big = []
    job_list = list(job_df['name'])
    for idx in range(len(mov_df['name'])):
        print(idx, end=" ")
        r_avg_list = []
        a_avg_list = []
        row = list(mov_df.loc[idx])
        for item in row:
            for t in range(len(job_list)):
                if item == job_list[t]:
                    item = job_df['r_avg'][t]
                    r_avg_list.append(item)
                    item = job_df['a_avg'][t]
                    a_avg_list.append(item)
        r_big.append(r_avg_list)
        a_big.append(a_avg_list)
        if idx % 20 == 19:
            print("|")

    new_r = []
    new_a = []
    r_avg = []
    a_avg = []

    for a in a_big:
        a = [x for x in a if isnan(x) == False]
        new_a.append(a)
    for r in r_big:
        r = [x for x in r if isnan(x) == False]
        new_r.append(r)

    for a in new_a:
        try:
            a_avg.append(sum(a)/len(a))
        except ZeroDivisionError:
            a_avg.append(0)

    for r in new_r:
        try:
            r_avg.append(sum(r)/len(r))
        except ZeroDivisionError:
            r_avg.append(0)

    k = pd.concat([mov_df['name'], pd.Series(a_avg), pd.Series(r_avg)],
              ignore_index=True, axis=1)
    k.columns = ['name', '%s_a_avg' % version, '%s_r_avg' % version]
    k.to_csv("asset/new/mov_avg_%s.csv" % version)


