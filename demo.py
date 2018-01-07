import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    #pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?<img alt="(.*?)".*?src="(.*?)">.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<p class="score">.*?integer">(.*?)</i>.*?fraction">(\d)</i>.*?</dd>', re.S)
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?title="(.*?)".*?<img.*?<img.*?src="(.*?)".*?>.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">(.*?)</i>.*?<i class="fraction">(\d)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    #print items
    for item in items:
        yield{
            'index': item[0],
            'title': item[1],
            'image': item[2],
            'actor': item[3],
            'time': item[4],
            'score': item[5]+item[6]
        }
        '''
        print '\n'
        for i in item:
            print i
        '''
def  write_to_file(content):
    with open('result.txt', 'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        #print('writing'+item+'\n\n')
        write_to_file(item)
        #for i in item:
            #print i,':',item[i].strip()


if __name__ == '__main__':
    #for i in range(10):
    #    main(i*10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
