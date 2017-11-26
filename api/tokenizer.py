# -*- coding: utf-8 -*
"""日本語形態素解析を行います.

How About Natume の API は google platform での運用を前提に考えているので，
Python のみで形態素解析が行える janome を利用します.
"""
from janome.tokenizer import Tokenizer
from typing import List

TOKENIZER = Tokenizer()


def get_noun(text: str) -> List:
    """文章中の名詞のみを返します."""
    return [
        t.base_form for t in TOKENIZER.tokenize(text)
        if t.part_of_speech.split(',')[0] == '名詞'
    ]


def get_adjective(text: str) -> List:
    """文章中の形容詞のみを返します."""
    return [
        t.base_form for t in TOKENIZER.tokenize(text)
        if t.part_of_speech.split(',')[0] == '形容詞'
    ]


def get_entity(text: str) -> List:
    """文章中の名詞, 動詞, 形容詞のみを返します."""
    return [
        t.base_form for t in TOKENIZER.tokenize(text)
        if t.part_of_speech.split(',')[0] in ['名詞', '動詞', '形容詞']
    ]
