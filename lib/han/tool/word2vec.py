# -*- coding: utf-8 -*
"""Mongo DB の結果から word2dec のモデルを作成します."""
from han.config import AUTHORS
from han.logger import getLogger

LOGGER = getLogger('WORD2VEC_FACTORY')


def load_document(author):
    """Mongo DB からデータを習得します."""
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
        documents = [
            document.get('contents').split('。')
            for document in list(collection.find({'author': author}))
            if document.get('contents')
        ]
    else:
        LOGGER.error('Certification failed for MongoDB.')
        documents = None
    return documents


def separating_words(document):
    """日本語の分かち書きを行います."""
    import MeCab
    mecab = MeCab.Tagger("-Ochasen")
    ret = mecab.parse(document)
    words = [
        words.split('\t')
        for words in ret.split('\n')
        if '\t' in words
    ]
    words = [
        w[2] for w in words
        if w[3].split('-')[0] in ['名詞', '動詞', '形容詞', '副詞']
    ]
    return words


def get_noun(document):
    """Document のうち名詞のみを返します."""
    import MeCab
    mecab = MeCab.Tagger("-Ochasen")
    ret = mecab.parse(document)
    words = [
        words.split('\t')
        for words in ret.split('\n')
        if '\t' in words
    ]
    words = [
        w[2] for w in words
        if w[3].split('-')[0] in ['名詞']
    ]
    return words


def create_model(sentences):
    """word2vec のモデルを作成します."""
    from gensim.models.word2vec import Word2Vec
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    return model


if __name__ == "__main__":
    from han.config import MODEL_DIR
    from os import path
    LOGGER.info(
        'Start to create model.'
    )
    for author_info in AUTHORS:
        author = author_info.get('name')
        LOGGER.info(
            'Load documents by {author}.'.format(
                author=author
            )
        )
        documents = [
            separating_words(text)
            for documents in load_document(author)
            for text in documents
        ]
        LOGGER.info(
            'creating model for {author}...'.format(
                author=author
            )
        )
        model = create_model(documents)
        LOGGER.info(
            'Saving model ...'
        )
        model.save(
            path.join(MODEL_DIR, '.'.join([author, 'word2vec', 'model']))
        )
