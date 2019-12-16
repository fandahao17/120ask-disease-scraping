import os
import requests
from bs4 import BeautifulSoup

chars = 'abcdefg'
head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}
prefix = 'http://tag.120ask.com/jibing/'
pages = ['', 'gaishu/', 'bingyin/', 'zhengzhuang/', 'jiancha/',
        'jianbie/', 'bingfa/', 'yufang/', 'zhiliao/', 'yinshi/']


for index in chars:
    with open('{}.html'.format(index)) as file:
        print(index)
        try:
            os.mkdir(index)
        except:
            pass
        soup = BeautifulSoup(open('{}.html'.format(index)), 'html.parser')
        s = soup.find_all("div", "tag_li")
        tags = s[0].find_all("a")
        for tag in tags:
            name = tag.get("href").split('/')[-2]
            try:
                os.mkdir('{}/{}'.format(index, name))
            except Exception as e:
                print("{}".format(e))
                # continue
            name_prefix = prefix + name + '/'
            for page in pages:
                url = name_prefix + page
                print(url)
                try:
                    r = requests.get(url, headers=head)
                except Exception as e:
                    print('Failed to get {} because of {}'.format(url, e))
                else:
                    if page == '':
                        n = name
                    else:
                        n = page[:-1]
                    with open('{}/{}/{}.html'.format(index, name, n), 'w') as f:
                        try:
                            f.write(r.content.decode("UTF-8"))
                        except Exception as e:
                            print('Failed to write {} because of {}'.format(url, e))

