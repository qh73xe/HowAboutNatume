# -*- coding: utf-8 -*
"""生成されたモデルから類義語を返します."""
from han.logger import getLogger
from typing import List

LOGGER = getLogger('ASK_MODULE')


def get_model(author: str):
    """モデルパスを返します."""
    from os import path
    from han.config import MODEL_DIR
    from gensim.models.word2vec import Word2Vec
    model_name = '.'.join([author, 'word2vec', 'model'])
    model_path = path.join(MODEL_DIR, model_name)
    return Word2Vec.load(model_path)


def ask(author: str, querys: List[str]) -> List:
    """Get 5 similar words for querys."""
    from han.tool.word2vec import get_noun
    model = get_model(author)
    try:
        results = model.most_similar(positive=querys, topn=10)
    except Exception as e:
        msg = "{author} can't answer. (hint: {hint})".format(
            author=author, hint=str(e)
        )
        LOGGER.error(msg)
    else:
        try:
            words = [
                {'word': get_noun(result[0])[0], 'similarity': result[1]}
                for result in results
                if len(result[0]) > 1
                if get_noun(result[0])
            ]
        except Exception as e:
            msg = ' '.join([
                "Querys have some problems",
                "(querys: {querys}, result: {result})".format(
                    querys=querys, result=results
                )
            ])

            LOGGER.error(msg)
        else:
            if len(words) > 3:
                return words[:3]
            else:
                return words


if __name__ == "__main__":
    import sys
    from han.tool.word2vec import separating_words
    querys = separating_words(sys.argv[1])
    print(ask('夏目漱石', querys))
