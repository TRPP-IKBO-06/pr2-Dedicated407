from collections import namedtuple
import json
from pathlib import Path
from sly import Lexer, Parser

"""
directives ::= directive directives | empty
directive ::= simple_directive | block_directive
names ::= name names | empty
simple_directive ::= name names ";"
block_directive ::= name names "{" directives "}"
"""

Directive = namedtuple("Directive", "type args ctx")

class ConfLexer(Lexer):
    tokens = { BEGIN, END, NAME, SEMICOL, STRING }
    BEGIN = r'{'
    END = r'}'
    ignore = r' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'
    NAME = r'[^ \t\#{};\']+'
    SEMICOL = r';'
    STRING = r"'.*'"


class ConfParser(Parser):
    tokens = ConfLexer.tokens

    @_('directive directives')
    def directives(self, p):
        return [p.directive] + p.directives

    @_('empty')
    def directives(self, p):
        return []

    @_('simple_directive', 'block_directive')
    def directive(self, p):
        return p[0]

    @_('name names SEMICOL')
    def simple_directive(self, p):
        return dict(type="simple", args=[p.name] + p.names, ctx=[])

    @_('name names BEGIN directives END')
    def block_directive(self, p):
        return dict(type="block", args=[p.name] + p.names, ctx=p.directives)

    @_('name names')
    def names(self, p):
        return [p.name] + p.names

    @_('empty')
    def names(self, p):
        return []

    @_('NAME')
    def name(self, p):
        return p[0]

    @_('STRING')
    def name(self, p):
        return p[0][1:-1]

    @_('')
    def empty(self, p):
        pass


def main():
    text = Path("nginx.conf").read_text()
    lexer = ConfLexer()
    parser = ConfParser()
    data = parser.parse(lexer.tokenize(text))
    Path("confResult.json").write_text(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
