import re

# Definição de padrões de tokens
token_specs = [
    ('NUM',   r'\d+(\.\d*)?'),   # Números inteiros ou decimais
    ('ID',    r'[a-zA-Z_]\w*'),  # Identificadores
    ('OP',    r'[+\-*/%]'),      # Operadores aritméticos
    ('REL',   r'[<>!=]=|[<>]'),  # Operadores relacionais
    ('ASSIGN',r'='),             # Operador de atribuição
    ('LPAREN',r'\('),            # Parênteses esquerdo
    ('RPAREN',r'\)'),            # Parênteses direito
    ('LBRACE',r'\{'),            # Chave esquerda
    ('RBRACE',r'\}'),            # Chave direita
    ('COMMA', r','),             # Vírgula
    ('SEMI',  r';'),             # Ponto e vírgula
    ('STRING',r'"[^"]*"'),       # Strings
    ('SKIP',  r'[ \t]+'),        # Espaços em branco e tabs
    ('NEWLINE', r'\n'),          # Nova linha
    ('MISMATCH', r'.'),          # Qualquer outro caractere
]

# Palavras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'fimprog': 'FIMPROG',
    'inteiro': 'INTEIRO',
    'decimal': 'DECIMAL',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'se': 'SE',
    'senao': 'SENAO',
    'enquanto': 'ENQUANTO',
    'para': 'PARA',
}

# Compilação dos padrões em expressões regulares
token_re = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
get_token = re.compile(token_re).match

def lex(code):
    line_num = 1
    line_start = 0
    pos = 0
    mo = get_token(code)
    while mo is not None:
        typ = mo.lastgroup
        if typ == 'NEWLINE':
            line_start = pos
            line_num += 1
        elif typ != 'SKIP':
            val = mo.group(typ)
            if typ == 'ID' and val in reserved:
                typ = reserved[val]
            yield (typ, val, line_num, mo.start() - line_start)
        pos = mo.end()
        mo = get_token(code, pos)
    if pos != len(code):
        raise RuntimeError(f'Unexpected character {code[pos]} at line {line_num}')
