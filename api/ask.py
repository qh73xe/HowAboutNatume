# -*- coding: utf-8 -*
"""生成されたモデルから類義語を返します."""
from typing import List

from tokenizer import get_noun, get_adjective
from logger import getLogger


LOGGER = getLogger('ASK_MODULE')


def get_model(author: str):
    """モデルパスを返します."""
    from os import path
    from config import MODEL_DIR
    from gensim.models.word2vec import Word2Vec
    model_name = '.'.join([author, 'word2vec', 'model'])
    model_path = path.join(MODEL_DIR, model_name)
    return Word2Vec.load(model_path)


def ask(author: str, querys: List[str]) -> List:
    """Get 5 similar words for querys."""
    model = get_model(author)
    try:
        results = model.most_similar(positive=querys, topn=150)
    except Exception as e:
        msg = "{author} can't answer. (hint: {hint})".format(
            author=author, hint=str(e)
        )
        LOGGER.error(msg)
    else:
        noun = []
        adjective = []

        try:
            for result in results:
                word = result[0]
                noun.extend(get_noun(word))
                adjective.extend(get_adjective(word))
        except Exception as e:
            msg = ' '.join([
                "Querys have some problems",
                "(querys: {querys}, result: {result})".format(
                    querys=querys, result=results
                )
            ])
            LOGGER.error(msg)
        else:
            return {
                'nouns': noun[:3],
                'adjective': adjective[:1]
            }


if __name__ == "__main__":
    import sys
    from tokenizer import get_entity
    querys = get_entity(sys.argv[1])
    print('querys: {}'.format(querys))
    print(ask('夏目漱石', querys))
