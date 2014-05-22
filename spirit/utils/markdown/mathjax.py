#-*- coding: utf-8 -*-
# adapted from https://github.com/mayoff/python-markdown-mathjax

import re

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern


class MathjaxPattern(Pattern):

    def __init__(self):
        super(MathjaxPattern, self).__init__(self, r'(?<!\\)(\$\$?)(.+?)\2')

    def handleMatch(self, m):
        node = markdown.util.etree.Element('mathjax')
        node.text = markdown.util.AtomicString(m.group(2) + m.group(3) + m.group(2))
        return node


class MathjaxExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('mathjax', MathjaxPattern(), '<escape')


def makeExtension(configs=None):
    return MathjaxExtension(configs=configs)