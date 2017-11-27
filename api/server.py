# -*- coding: utf-8 -*
"""トルネードを使用した ask.api を作成します."""
from json import dumps

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.web import Application, RequestHandler

from tornado.options import define, options
from tokenizer import get_entity

from logger import getLogger

LOGGER = getLogger('API_MODULE')
define("port", default=8000, help="run on the given port", type=int)


class AskHandler(RequestHandler):
    """question に get された文章と親密度の高い語を返します."""

    def get(self):
        """Question に答えます."""
        from ask import ask
        author = self.get_argument('author')
        question = self.get_argument('question')
        answers = {
            'answers': ask(author, get_entity(question))
        }
        self.finish(
            dumps(
                answers,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
                separators=(',', ': ')
            )
        )

    def post(self):
        """Action on google の web フック用レスポンス"""
        from ask import ask
        import json
        data = json.loads(self.request.body)
        LOGGER.info('input: {data}'.format(data=data))

        author = data.get('author', '夏目漱石')
        question = data.get('question')
        answers = ask(author, get_entity(question))

        if answers:
            adjective = answers.get('adjective', None)
            nouns = answers.get('nouns')

            if adjective:
                speech = '。'.join([
                    'それは {adjective} 質問ですね'.format(adjective=adjective[0]),
                    'きっと, {0} や {1} あるいは {2} のことです'.format(*nouns)
                ])
            else:
                speech = 'それはきっと, {0} や {1} あるいは {2} のことです'.format(*nouns)
        else:
            speech = '。'.join([
                '{q} についてですか'.format(q=question),
                '難しいことを聞きますね',
                '私にはわからないです'
            ])

        displayText = speech
        respose = {
            'speech': speech,
            'displayText': displayText,
            'data': answers,
            'contextOut': [answers],
            'source': 'how-about-natume'
        }
        self.finish(
            dumps(
                respose,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
                separators=(',', ': ')
            )
        )



if __name__ == "__main__":
    parse_command_line()
    app = Application(handlers=[(r"/", AskHandler)])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.instance().start()
