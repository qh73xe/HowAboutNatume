# -*- coding: utf-8 -*
"""青空文庫から夏目漱石の文章を取得するスクリプト群.

基本的にはバッチ処理でデータを取得し学習をすればよいと考える.
"""
from han.config import AUTHORS
from han.logger import getLogger

LOGGER = getLogger('DOCUMENT_FACTORY')


def load_html(url: str):
    """URL を get メゾットで読み込みます."""
    import requests
    from bs4 import BeautifulSoup
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def get_books(author_url: str):
    """登録済み作品の URL 一覧を取得."""
    from urllib.parse import urljoin
    domain = 'http://www.aozora.gr.jp/index_pages/'
    author_url = urljoin(domain, author_url)
    try:
        author_soup = load_html(author_url)
        card_urls = [
            urljoin(author_url, li.a.get('href'))
            for li in author_soup.find_all('li')
            if li.a
        ]
        links = []
        for url in card_urls:
            card_soup = load_html(url)
            table = card_soup.find('table', class_='download')
            for a in table.find_all('a'):
                if '.html' in a.get('href'):
                    links.append(
                        urljoin(url, a.get('href'))
                    )
        return links
    except Exception as e:
        LOGGER.error(e.msg)


def clean_document(soup):
    """ドキュメントの内容をクリーニングする."""
    for rp in soup.find_all('rp'):
        rp.decompose()
    for rt in soup.find_all('rt'):
        rt.decompose()
    docment = soup.text
    return ''.join([t.strip() for t in docment.strip().split('\n')])


def get_documents(url):
    """URL 先の文章内容を取得."""
    docment = load_html(url)
    content = {
        'title': str(docment.find(class_='title').text),
        'author': str(docment.find(class_='author').text),
        'contents': clean_document(docment.find(class_='main_text'))
    }
    return content


def addMongo(docment):
    """文章内容を Mongo DB に保存します."""
    from pymongo import MongoClient
    from han.config import MONGOSETTING
    host = MONGOSETTING.get('host')
    port = MONGOSETTING.get('port')
    db = MONGOSETTING.get('db')
    user = MONGOSETTING.get('user')
    pwd = MONGOSETTING.get('pwd')
    client = MongoClient(host, port)
    if client[db].authenticate(user, pwd):
        collection = client[db]['documents']
        post_id = collection.insert_one(docment).inserted_id
    else:
        post_id = None
        LOGGER.error('Certification failed for MongoDB.')
    return post_id


if __name__ == "__main__":
    from progressbar import ProgressBar
    LOGGER.info('Start to get documents.')

    for auth in AUTHORS:
        url = auth.get('url', None)
        authorname = auth.get('name', None)
        if url:
            LOGGER.info('load documents by {name}.'.format(name=authorname))
            book_urls = get_books(url)
            p = ProgressBar(len(book_urls))
            for book_url in book_urls:
                try:
                    document = get_documents(book_url)
                except Exception as e:
                    msg = ' '.join([
                        'Failed to get document.',
                        '[url: {url}] (hint: {hint})'.format(
                            url=book_url, hint=str(e)
                        )
                    ])
                    LOGGER.error(msg)
                else:
                    try:
                        post_id = addMongo(document)
                    except Exception as e:
                        msg = ' '.join([
                            'Failed to save document.',
                            '[document: {document}] (hint: {hint})'.format(
                                document=document, hint=str(e)
                            )
                        ])
                        LOGGER.error(msg)
                    else:
                        if post_id:
                            msg = 'Insert {title} ({author}) as {post_id}'.format(
                                title=document.get('title'),
                                author=document.get('author'),
                                post_id=post_id
                            )
                            LOGGER.info(msg)
                        else:
                            break
