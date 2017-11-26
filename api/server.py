# -*- coding: utf-8 -*
"""トルネードを使用した ask.api を作成します."""
from json import dumps

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.web import Application, RequestHandler

from tornado.options import define, options
from tokenizer import get_entity

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
        self.write(
            dumps(
                answers,
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
