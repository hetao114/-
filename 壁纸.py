import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool

def get_page(offset):
    data={
        'query': 'nasa',
        'xp': 'search - cervantes - v1:experiment',
        'per_page': '20',
        'page':offset
    }
    url='https://unsplash.com/napi/search/photos?'+urlencode(data)

    response=requests.get(url)


    try:
        if response.status_code ==200:
            return response.json()   #字典

    except requests.ConnectionError:
        print("请求索引页失败")
        return None
def get_image(json):
    if json.get("results"):
        data = json.get("results")


        for item in data:
            title=item.get('id')
            link=item.get('links')
            yield {
                'image': link.get('download'),

                'title': title
            }  # 返回一个字典


def save_image(item):#item为传入的的字典
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):#	路径存在则返回True,路径损坏返回False
        os.makedirs(img_path)#创建imgpath文件夹 递归文件夹创建函数
    try:
        image=item.get('image')

        resp = requests.get(image)#请求item中的image链接
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % item)



def main(offset):
    json=get_page(offset)

    for item in get_image(json):
        print(item)
        save_image(item)

GROUP_START = 0
GROUP_END = 2

if __name__ == '__main__':
    pool = Pool()
    groups = ([x*1 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()