import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Inicializa a lista de tokens.
        self.pos = 0  # Inicializa a posição atual no token.

    def parse(self):
        return self.prog()  # Inicia a análise sintática a partir do programa principal.

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1  # Se o token atual corresponde ao tipo esperado, avança a posição e retorna True.
            return True
        return False  # Se não, retorna False.

    def prog(self):
        if self.match('PROGRAMA'):
            declarations = self.declara()  # Analisa as declarações.
            commands = self.bloco()  # Analisa o bloco de comandos.
            if self.match('FIMPROG'):
                return ('prog', declarations, commands)  # Retorna a árvore sintática do programa.
        self.error()  # Se não encontrar os tokens esperados, gera um erro.

    def declara(self):
        declarations = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ['INTEIRO', 'DECIMAL']:
            var_type = self.tipo()  # Analisa o tipo da variável.
            ids = self.ids()  # Analisa os identificadores das variáveis.
            declarations.append((var_type, ids))  # Adiciona a declaração à lista.
            if not self.match('SEMI'):
                self.error()  # Se não encontrar um ponto e vírgula, gera um erro.
        return declarations  # Retorna a lista de declarações.

    def tipo(self):
        if self.match('INTEIRO'):
            return 'inteiro'  # Retorna o tipo 'inteiro'.
        elif self.match('DECIMAL'):
            return 'decimal'  # Retorna o tipo 'decimal'.
        self.error()  # Se não encontrar um tipo válido, gera um erro.

    def ids(self):
        ids = []
        if self.match('ID'):
            ids.append(self.tokens[self.pos - 1][1])  # Adiciona o identificador à lista.
            while self.match('COMMA'):
                if self.match('ID'):
                    ids.append(self.tokens[self.pos - 1][1])  # Adiciona o próximo identificador à lista.
                else:
                    self.error()  # Se não encontrar um identificador após uma vírgula, gera um erro.
        return ids  # Retorna a lista de identificadores.

    def bloco(self):
        commands = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ['INTEIRO', 'DECIMAL', 'LEIA', 'ESCREVA', 'ID', 'SE', 'ENQUANTO', 'PARA']:
            if self.tokens[self.pos][0] in ['INTEIRO', 'DECIMAL']:
                declarations = self.declara()  # Analisa declarações dentro do bloco.
                commands.extend(declarations)  # Adiciona as declarações aos comandos.
            else:
                command = self.cmd()  # Analisa comandos.
                commands.append(command)  # Adiciona o comando à lista.
        return commands  # Retorna a lista de comandos.

    def cmd(self):
        if self.match('LEIA'):
            if self.match('LPAREN'):
                if self.match('ID'):
                    var = self.tokens[self.pos - 1][1]
                    if self.match('RPAREN'):
                        if self.match('SEMI'):
                            return ('cmdLeitura', var)  # Retorna o comando de leitura.
        elif self.match('ESCREVA'):
            if self.match('LPAREN'):
                if self.match('STRING'):
                    text = self.tokens[self.pos - 1][1]
                    if self.match('RPAREN'):
                        if self.match('SEMI'):
                            return ('cmdEscrita', text)  # Retorna o comando de escrita com string.
                elif self.match('ID'):
                    var = self.tokens[self.pos - 1][1]
                    if self.match('RPAREN'):
                        if self.match('SEMI'):
                            return ('cmdEscrita', var)  # Retorna o comando de escrita com variável.
        elif self.match('ID'):
            var = self.tokens[self.pos - 1][1]
            if self.match('ASSIGN'):
                expr = self.expr()
                if self.match('SEMI'):
                    return ('cmdExpr', var, expr)  # Retorna o comando de atribuição.
        elif self.match('SE'):
            return self.cmdSe()  # Analisa e retorna o comando 'SE'.
        elif self.match('ENQUANTO'):
            return self.cmdEnquanto()  # Analisa e retorna o comando 'ENQUANTO'.
        elif self.match('PARA'):
            return self.cmdPara()  # Analisa e retorna o comando 'PARA'.
        self.error()  # Se não encontrar nenhum comando válido, gera um erro.

    def cmdSe(self):
        if self.match('LPAREN'):
            condition = self.expr()
            if self.match('RPAREN'):
                if self.match('LBRACE'):
                    true_block = self.bloco()
                    if self.match('RBRACE'):
                        false_block = []
                        if self.match('SENAO'):
                            if self.match('LBRACE'):
                                false_block = self.bloco()
                                if not self.match('RBRACE'):
                                    self.error()
                        return ('cmdSe', condition, true_block, false_block)  # Retorna o comando 'SE' com blocos verdadeiro e falso.
        self.error()  # Se não encontrar a estrutura esperada, gera um erro.

    def cmdEnquanto(self):
        if self.match('LPAREN'):
            condition = self.expr()
            if self.match('RPAREN'):
                if self.match('LBRACE'):
                    block = self.bloco()
                    if self.match('RBRACE'):
                        return ('cmdEnquanto', condition, block)  # Retorna o comando 'ENQUANTO' com a condição e o bloco.
        self.error()  # Se não encontrar a estrutura esperada, gera um erro.

    def cmdPara(self):
        if self.match('LPAREN'):
            init = self.cmdExpr()
            if self.match('SEMI'):
                condition = self.expr()
                if self.match('SEMI'):
                    update = self.cmdExpr()
                    if self.match('RPAREN'):
                        if self.match('LBRACE'):
                            block = self.bloco()
                            if self.match('RBRACE'):
                                return ('cmdPara', init, condition, update, block)  # Retorna o comando 'PARA' com inicialização, condição, atualização e bloco.
        self.error()  # Se não encontrar a estrutura esperada, gera um erro.

    def expr(self):
        left = self.termo()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ['OP', 'REL']:
            op = self.tokens[self.pos][1]
            self.pos += 1
            right = self.termo()
            left = ('expr', op, left, right)  # Retorna a expressão com operador e operandos.
        return left  # Retorna o termo se não houver operadores adicionais.

    def termo(self):
        if self.match('NUM'):
            return ('num', self.tokens[self.pos - 1][1])  # Retorna um número.
        elif self.match('ID'):
            return ('id', self.tokens[self.pos - 1][1])  # Retorna um identificador.
        elif self.match('LPAREN'):
            expr = self.expr()
            if self.match('RPAREN'):
                return expr  # Retorna a expressão entre parênteses.
        self.error()  # Se não encontrar um termo válido, gera um erro.

    def cmdExpr(self):
        if self.match('ID'):
            var = self.tokens[self.pos - 1][1]
            if self.match('ASSIGN'):
                expr = self.expr()
                return ('cmdExpr', var, expr)  # Retorna o comando de expressão com variável e expressão.
        self.error()  # Se não encontrar a estrutura esperada, gera um erro.

    def op_rel(self):
        if self.match('REL'):
            return self.tokens[self.pos - 1][1]  # Retorna o operador relacional.
        self.error()  # Se não encontrar um operador relacional, gera um erro.

    def error(self):
        if self.pos < len(self.tokens):
            sys.stderr.write(f'Syntax error at token {self.tokens[self.pos]}\n')  # Exibe mensagem de erro indicando o token onde ocorreu o erro.
        else:
            sys.stderr.write('Unexpected end of input\n')  # Exibe mensagem de erro indicando fim inesperado da entrada.
        sys.exit(1)  # Encerra o programa com código de erro.
