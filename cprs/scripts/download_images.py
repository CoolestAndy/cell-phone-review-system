import csv
import json
import requests
from lxml import etree
from multiprocessing.pool import Pool


def get_phone_image(keyword: str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    try:
        content = requests.get(f'https://www.amazon.com/s?k={keyword}&ref=nb_sb_noss', headers=headers)
        tree = etree.HTML(content.text)
        links = tree.cssselect('a[class="a-link-normal a-text-normal"]')
        href = links[0].attrib['href']

        content = requests.get('https://www.amazon.com' + href, headers=headers)
        tree = etree.HTML(content.text)
        images = tree.cssselect('img[id="landingImage"]')
        image = images[0].attrib['src']
        print(f'Succeeded to get phone image of {keyword}')
        return image
    except Exception as e:
        print(f'Failed to get phone image of {keyword}')
        print(e)
        return ""


def run():
    urls = set()
    with open('phone_user_review_file.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            urls.add(row[0].split('/')[2])

    urls = list(urls)
    pool = Pool(10)
    images = pool.map(get_phone_image, urls)

    cache = {}
    for i, url in enumerate(urls):
        cache[url] = images[i]

    with open('phone_images.json', 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)
