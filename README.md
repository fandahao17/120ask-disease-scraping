# 120ask-disease-scraping

我选择的开放作业题目是[快速问医生-疾病](https://git.bdaa.pro/yxonic/data-specification/wikis/快速问医生%20疾病)。

## 爬取网页

我的做法是，先按拼音a-z爬取所有疾病的[列表](http://tag.120ask.com/jibing/pinyin/a.html)，再根据该列表依次爬取我们需要的网页。在本实验中，我们需要爬取的网页有：概述、病因、症状、检查、鉴别、并发、预防、治疗、饮食、食疗。爬取的代码见[get_all_docs.py](./get_all_docs.py)。

我是在阿里云学生机上爬取的，因为它的网速更快，而且可以保证长时间在线。因为需要爬取的网页数很多（大概有十几万个），所以我开启了四个进程同时爬取。事实上，因为爬取的任务是完全I/O-bound的， 所以完全可以开更多个进程并行爬取。

爬取到网页后，我用`BeautifulSoup`库抓取了html文件中对应的域。然后又将不同首字母的疾病信息合并在了一起，见[get_data.py](./get_data.py)和[merge_json.py](./merge_json.py)。

## 绕开反爬虫机制

快速问医生是有反爬虫机制的，如果直接用Python的request库访问的话就会返回403。所以，需要在HTTP请求头部中加入伪装的User-Agent信息：

```python
head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}

r = requests.get(url, headers=head)
```

这样就可以正常爬取了。