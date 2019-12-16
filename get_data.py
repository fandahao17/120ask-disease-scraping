from bs4 import BeautifulSoup
import json

url_prefix = "http://tag.120ask.com/jibing/"

def get_data(chinese_name, name, first_chat):
    dis_dict = {"类型": "疾病"}
    dis_dict['网址'] = url_prefix + name
    dis_dict['名称'] = chinese_name

    with open('{}/{}/gaishu.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        gaishu = soup.find_all("div", "art_cont")
        if gaishu:
            overview = gaishu[0].text
            dis_dict['简介'] = overview
        else:
            print("WARNING: Can't find gaishu in {}".format(file))

    attr, xgzz, tjyp = {}, [], []
    with open('{0}/{1}/{1}.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        bikan = soup.find_all("div", "disease-list-left")
        if bikan:
            for li in bikan[0].find_all("li"):
                key, value = li.span.text, li.var.text
                attr[key[:-1]] = value
                # print(key, value)
        else:
            print("WARNING: Can't find bikan in {}".format(file))

        tieshi = soup.find_all("div", "disease-list-center")
        if tieshi:
            for li in tieshi[0].find_all("li"):
                key, value = li.span.text, li.var.text
                attr[key[:-1]] = value
                # print(key, value)
        else:
            print("WARNING: Can't find tieshi in {}".format(file))

        related = soup.find_all("div", "disease-Related-List clear")
        if related:
            for a in related[0].find_all("a"):
                link, dis_name = a['href'], a.text
                xgzz.append({"名称": dis_name, "网址": link})
                # print(link, dis_name)
        else:
            print("WARNING: Can't find related in {}".format(file))

        tuijian = soup.find_all("div", "clear img-list")
        if tuijian:
            for a in tuijian[0].find_all("a"):
                link, med_name = "https:" + a['href'], a.text
                tjyp.append({"名称": med_name, "网址": link})
                # print(link, med_name)
        else:
            print("WARNING: Can't find tuijian in {}".format(file))

    with open('{}/{}/shilia.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        food = soup.find_all("span", "sp")
        if food:
            yi = food[0].var.text
            ji = food[1].var.text
            attr['饮食宜'] = yi
            attr['饮食忌'] = ji
            # print(yi)
            # print(ji)
        else:
            print("WARNING: Can't find food in {}".format(file))

    with open('{}/{}/bingyin.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        bingyin = soup.find_all("div", "art_cont")
        if bingyin:
            cause = bingyin[0].text
            attr['病因'] = cause
            # print(cause)
        else:
            print("WARNING: Can't find cause in {}".format(file))

    with open('{}/{}/zhengzhuang.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        symp = soup.find_all("div", "art_cont")
        if symp:
            symp = symp[0].text
            attr['症状'] = symp
            # print(symp)
        else:
            print("WARNING: Can't find symp in {}".format(file))

    with open('{}/{}/jiancha.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        check = soup.find_all("div", "art_cont")
        if check:
            check = check[0].text
            attr['检查'] = check
            # print(check)
        else:
            print("WARNING: Can't find check in {}".format(file))

    with open('{}/{}/jianbie.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        ensure = soup.find_all("div", "art_cont")
        if ensure:
            ensure = ensure[0].text
            attr['鉴别'] = ensure
            # print(ensure)
        else:
            print("WARNING: Can't find ensure in {}".format(file))

    with open('{}/{}/bingfa.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        side = soup.find_all("div", "art_cont")
        if side:
            side = side[0].text
            attr['并发症'] = side
            # print(side)
        else:
            print("WARNING: Can't find side in {}".format(file))

    with open('{}/{}/yufang.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        avoid = soup.find_all("div", "art_cont")
        if avoid:
            avoid = avoid[0].text
            attr['预防'] = avoid
            # print(avoid)
        else:
            print("WARNING: Can't find avoid in {}".format(file))

    with open('{}/{}/zhiliao.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        cure = soup.find_all("div", "art_cont")
        if cure:
            cure = cure[0].text
            attr['治疗'] = cure
            # print(food)
        else:
            print("WARNING: Can't find food in {}".format(file))

    with open('{}/{}/yinshi.html'.format(first_chat, name)) as file:
        soup = BeautifulSoup(file, 'html.parser')
        food = soup.find_all("div", "art_cont")
        if food:
            food = food[0].text
            attr['饮食'] = food
            # print(food)
        else:
            print("WARNING: Can't find food in {}".format(file))

    dis_dict['属性'] = attr
    dis_dict['相关症状'] = xgzz
    dis_dict['推荐药品'] = tjyp

    # js = json.dumps(dis_dict, ensure_ascii=False, indent=4)
    with open('{}/{}.json'.format(first_chat, name), 'w') as outfile:
        json.dump(dis_dict, outfile, ensure_ascii=False, indent=4)
    # return js

for ch in 'g':
    soup = BeautifulSoup(open('{}.html'.format(ch)), 'html.parser')
    s = soup.find_all("div", "tag_li")
    tags = s[0].find_all("a")
    for tag in tags:
        name = tag.get("href").split('/')[-2]
        chinese_name = tag.get("title")
        try:
            get_data(chinese_name, name, ch)
        except Exception as e:
            # raise(e)
            print('ERROR: Failed to dump {} because {}'.format(name, e))
        else:
            print('{} success!'.format(name))
