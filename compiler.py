from lexer import lex
from my_parser import Parser
import sys

# Função principal para gerar código Python a partir de uma AST
def generate_python(ast):
    code = []

    # Função recursiva que processa cada nó da AST
    def generate_node(node, indent="    "):
        if node[0] == 'prog':
            code.append("if __name__ == '__main__':")
            generate_node(('declara', node[1]), indent)
            generate_node(('bloco', node[2]), indent)
        elif node[0] == 'declara':
            for declaration in node[1]:
                var_type = declaration[0]
                for var in declaration[1]:
                    if var_type == 'inteiro':
                        code.append(f'{indent}{var} = 0')
                    elif var_type == 'decimal':
                        code.append(f'{indent}{var} = 0.0')
        elif node[0] == 'cmdLeitura':
            code.append(f'{indent}{node[1]} = float(input())')
        elif node[0] == 'cmdEscrita':
            if isinstance(node[1], str) and node[1].startswith('"'):
                code.append(f'{indent}print({node[1]})')
            else:
                code.append(f'{indent}print({node[1]})')
        elif node[0] == 'cmdExpr':
            code.append(f'{indent}{node[1]} = {generate_expr(node[2])}')
        elif node[0] == 'cmdSe':
            code.append(f'{indent}if {generate_expr(node[1])}:')
            generate_block(node[2], indent + "    ")
            if node[3]:
                code.append(f'{indent}else:')
                generate_block(node[3], indent + "    ")
        elif node[0] == 'cmdEnquanto':
            code.append(f'{indent}while {generate_expr(node[1])}:')
            generate_block(node[2], indent + "    ")
        elif node[0] == 'cmdPara':
            init = generate_node_inline(node[1])
            condition = generate_expr(node[2])
            update = generate_node_inline(node[3])
            code.append(f'{indent}{init}')
            code.append(f'{indent}while {condition}:')
            generate_block(node[4], indent + "    ")
            code.append(f'{indent}    {update}')
        elif node[0] == 'bloco':
            for command in node[1]:
                generate_node(command, indent)

    def generate_node_inline(node):
        if node[0] == 'cmdExpr':
            return f'{node[1]} = {generate_expr(node[2])}'
        return ""

    def generate_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            return expr[1]
        elif expr[0] == 'expr':
            return f'({generate_expr(expr[2])} {expr[1]} {generate_expr(expr[3])})'
        elif expr[0] == 'cmdExpr':
            return f'{expr[1]} = {generate_expr(expr[2])}'

    def generate_block(block, indent):
        for command in block:
            generate_node(command, indent)

    generate_node(ast)
    return '\n'.join(code)

# Função principal para gerar código C++ a partir de uma AST
def generate_cpp(ast):
    code = ["#include <iostream>", "using namespace std;", "int main() {"]
    indent = "    "

    def generate_node(node, indent):
        if node[0] == 'prog':
            generate_node(('declara', node[1]), indent)
            generate_node(('bloco', node[2]), indent)
            code.append("    return 0;")
            code.append("}")
        elif node[0] == 'declara':
            for declaration in node[1]:
                var_type = "int" if declaration[0] == 'inteiro' else "double"
                vars = ', '.join(declaration[1])
                code.append(f'{indent}{var_type} {vars};')
        elif node[0] == 'cmdLeitura':
            code.append(f'{indent}cin >> {node[1]};')
        elif node[0] == 'cmdEscrita':
            code.append(f'{indent}cout << {node[1]} << endl;')
        elif node[0] == 'cmdExpr':
            code.append(f'{indent}{node[1]} = {generate_expr(node[2])};')
        elif node[0] == 'cmdSe':
            code.append(f'{indent}if ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
            if node[3]:
                code.append(f'{indent}else {{')
                generate_block(node[3], indent + "    ")
                code.append(f'{indent}}}')
        elif node[0] == 'cmdEnquanto':
            code.append(f'{indent}while ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'cmdPara':
            init = generate_expr(node[1])
            condition = generate_expr(node[2])
            update = generate_expr(node[3])
            code.append(f'{indent}for ({init}; {condition}; {update}) {{')
            generate_block(node[4], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'bloco':
            for command in node[1]:
                generate_node(command, indent)

    def generate_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            return expr[1]
        elif expr[0] == 'expr':
            return f'({generate_expr(expr[2])} {expr[1]} {generate_expr(expr[3])})'

    def generate_block(block, indent):
        for command in block:
            generate_node(command, indent)

    generate_node(ast, indent)
    return '\n'.join(code)

# Função principal para gerar código C a partir de uma AST
def generate_c(ast):
    code = ["#include <stdio.h>", "int main() {"]
    indent = "    "
    variables = {}

    def generate_node(node, indent):
        if node[0] == 'prog':
            generate_node(('declara', node[1]), indent)
            generate_node(('bloco', node[2]), indent)
            code.append("    return 0;")
            code.append("}")
        elif node[0] == 'declara':
            for declaration in node[1]:
                var_type = "int" if declaration[0] == 'inteiro' else "double"
                for var in declaration[1]:
                    variables[var] = var_type
                vars = ', '.join(declaration[1])
                code.append(f'{indent}{var_type} {vars};')
        elif node[0] == 'cmdLeitura':
            var_type = variables.get(node[1], 'int')
            format_specifier = "%d" if var_type == "int" else "%lf"
            code.append(f'{indent}scanf("{format_specifier}", &{node[1]});')
        elif node[0] == 'cmdEscrita':
            var_type = variables.get(node[1], 'int')
            format_specifier = "%d" if var_type == "int" else "%lf"
            if isinstance(node[1], str) and node[1].startswith('"'):
                code.append(f'{indent}printf({node[1]});')
            else:
                code.append(f'{indent}printf("{format_specifier}\\n", {node[1]});')
        elif node[0] == 'cmdExpr':
            code.append(f'{indent}{node[1]} = {generate_expr(node[2])};')
        elif node[0] == 'cmdSe':
            code.append(f'{indent}if ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
            if node[3]:
                code.append(f'{indent}else {{')
                generate_block(node[3], indent + "    ")
                code.append(f'{indent}}}')
        elif node[0] == 'cmdEnquanto':
            code.append(f'{indent}while ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'cmdPara':
            init = generate_expr(node[1])
            condition = generate_expr(node[2])
            update = generate_expr(node[3])
            code.append(f'{indent}for ({init}; {condition}; {update}) {{')
            generate_block(node[4], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'bloco':
            for command in node[1]:
                generate_node(command, indent)

    def generate_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            return expr[1]
        elif expr[0] == 'expr':
            return f'({generate_expr(expr[2])} {expr[1]} {generate_expr(expr[3])})'

    def generate_block(block, indent):
        for command in block:
            generate_node(command, indent)

    generate_node(ast, indent)
    return '\n'.join(code)


# Função principal para orquestrar o processo de compilação
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {'python', 'cpp', 'c'}:
        print("Usage: compiler.py [python|cpp|c]")
        return

    target_language = sys.argv[1]
    output_file = 'output.' + {'python': 'py', 'cpp': 'cpp', 'c': 'c'}[target_language]

    print("Reading input file...")
    with open('input.txt', 'r') as f:
        code = f.read()
    
    print("Performing lexical analysis...")
    tokens = list(lex(code))
    print("Tokens:", tokens)
    
    print("Performing syntax analysis...")
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
    
    if target_language == 'python':
        print("Generating Python code...")
        output_code = generate_python(ast)
    elif target_language == 'cpp':
        print("Generating C++ code...")
        output_code = generate_cpp(ast)
    elif target_language == 'c':
        print("Generating C code...")
        output_code = generate_c(ast)
    
    print("Generated code:")
    print(output_code)
    
    print(f"Writing output to {output_file}...")
    with open(output_file, 'w') as f:
        f.write(output_code)
    print("Compilation complete.")

if __name__ == '__main__':
    main()
from lexer import lex
from my_parser import Parser
import sys

def generate_python(ast):
    code = []

    def generate_node(node, indent="    "):
        if node[0] == 'prog':
            code.append("if __name__ == '__main__':")
            generate_node(('declara', node[1]), indent)
            generate_node(('bloco', node[2]), indent)
        elif node[0] == 'declara':
            for declaration in node[1]:
                var_type = declaration[0]
                for var in declaration[1]:
                    if var_type == 'inteiro':
                        code.append(f'{indent}{var} = 0')
                    elif var_type == 'decimal':
                        code.append(f'{indent}{var} = 0.0')
        elif node[0] == 'cmdLeitura':
            code.append(f'{indent}{node[1]} = float(input())')
        elif node[0] == 'cmdEscrita':
            if isinstance(node[1], str) and node[1].startswith('"'):
                code.append(f'{indent}print({node[1]})')
            else:
                code.append(f'{indent}print({node[1]})')
        elif node[0] == 'cmdExpr':
            code.append(f'{indent}{node[1]} = {generate_expr(node[2])}')
        elif node[0] == 'cmdSe':
            code.append(f'{indent}if {generate_expr(node[1])}:')
            generate_block(node[2], indent + "    ")
            if node[3]:
                code.append(f'{indent}else:')
                generate_block(node[3], indent + "    ")
        elif node[0] == 'cmdEnquanto':
            code.append(f'{indent}while {generate_expr(node[1])}:')
            generate_block(node[2], indent + "    ")
        elif node[0] == 'cmdPara':
            init = generate_node_inline(node[1])
            condition = generate_expr(node[2])
            update = generate_node_inline(node[3])
            code.append(f'{indent}{init}')
            code.append(f'{indent}while {condition}:')
            generate_block(node[4], indent + "    ")
            code.append(f'{indent}    {update}')
        elif node[0] == 'bloco':
            for command in node[1]:
                generate_node(command, indent)

    def generate_node_inline(node):
        if node[0] == 'cmdExpr':
            return f'{node[1]} = {generate_expr(node[2])}'
        return ""

    def generate_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            return expr[1]
        elif expr[0] == 'expr':
            return f'({generate_expr(expr[2])} {expr[1]} {generate_expr(expr[3])})'
        elif expr[0] == 'cmdExpr':
            return f'{expr[1]} = {generate_expr(expr[2])}'

    def generate_block(block, indent):
        for command in block:
            generate_node(command, indent)

    generate_node(ast)
    return '\n'.join(code)

def generate_cpp(ast):
    code = ["#include <iostream>", "using namespace std;", "int main() {"]
    indent = "    "

    def generate_node(node, indent):
        if node[0] == 'prog':
            generate_node(('declara', node[1]), indent)
            generate_node(('bloco', node[2]), indent)
            code.append("    return 0;")
            code.append("}")
        elif node[0] == 'declara':
            for declaration in node[1]:
                var_type = "int" if declaration[0] == 'inteiro' else "double"
                vars = ', '.join(declaration[1])
                code.append(f'{indent}{var_type} {vars};')
        elif node[0] == 'cmdLeitura':
            code.append(f'{indent}cin >> {node[1]};')
        elif node[0] == 'cmdEscrita':
            code.append(f'{indent}cout << {node[1]} << endl;')
        elif node[0] == 'cmdExpr':
            code.append(f'{indent}{node[1]} = {generate_expr(node[2])};')
        elif node[0] == 'cmdSe':
            code.append(f'{indent}if ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
            if node[3]:
                code.append(f'{indent}else {{')
                generate_block(node[3], indent + "    ")
                code.append(f'{indent}}}')
        elif node[0] == 'cmdEnquanto':
            code.append(f'{indent}while ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'cmdPara':
            init = generate_expr(node[1])
            condition = generate_expr(node[2])
            update = generate_expr(node[3])
            code.append(f'{indent}for ({init}; {condition}; {update}) {{')
            generate_block(node[4], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'bloco':
            for command in node[1]:
                generate_node(command, indent)

    def generate_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            return expr[1]
        elif expr[0] == 'expr':
            return f'({generate_expr(expr[2])} {expr[1]} {generate_expr(expr[3])})'

    def generate_block(block, indent):
        for command in block:
            generate_node(command, indent)

    generate_node(ast, indent)
    return '\n'.join(code)

def generate_c(ast):
    code = ["#include <stdio.h>", "int main() {"]
    indent = "    "
    variables = {}

    def generate_node(node, indent):
        if node[0] == 'prog':
            generate_node(('declara', node[1]), indent)
            generate_node(('bloco', node[2]), indent)
            code.append("    return 0;")
            code.append("}")
        elif node[0] == 'declara':
            for declaration in node[1]:
                var_type = "int" if declaration[0] == 'inteiro' else "double"
                for var in declaration[1]:
                    variables[var] = var_type
                vars = ', '.join(declaration[1])
                code.append(f'{indent}{var_type} {vars};')
        elif node[0] == 'cmdLeitura':
            var_type = variables.get(node[1], 'int')
            format_specifier = "%d" if var_type == "int" else "%lf"
            code.append(f'{indent}scanf("{format_specifier}", &{node[1]});')
        elif node[0] == 'cmdEscrita':
            var_type = variables.get(node[1], 'int')
            format_specifier = "%d" if var_type == "int" else "%lf"
            if isinstance(node[1], str) and node[1].startswith('"'):
                code.append(f'{indent}printf({node[1]});')
            else:
                code.append(f'{indent}printf("{format_specifier}\\n", {node[1]});')
        elif node[0] == 'cmdExpr':
            code.append(f'{indent}{node[1]} = {generate_expr(node[2])};')
        elif node[0] == 'cmdSe':
            code.append(f'{indent}if ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
            if node[3]:
                code.append(f'{indent}else {{')
                generate_block(node[3], indent + "    ")
                code.append(f'{indent}}}')
        elif node[0] == 'cmdEnquanto':
            code.append(f'{indent}while ({generate_expr(node[1])}) {{')
            generate_block(node[2], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'cmdPara':
            init = generate_expr(node[1])
            condition = generate_expr(node[2])
            update = generate_expr(node[3])
            code.append(f'{indent}for ({init}; {condition}; {update}) {{')
            generate_block(node[4], indent + "    ")
            code.append(f'{indent}}}')
        elif node[0] == 'bloco':
            for command in node[1]:
                generate_node(command, indent)

    def generate_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            return expr[1]
        elif expr[0] == 'expr':
            return f'({generate_expr(expr[2])} {expr[1]} {generate_expr(expr[3])})'

    def generate_block(block, indent):
        for command in block:
            generate_node(command, indent)

    generate_node(ast, indent)
    return '\n'.join(code)

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {'python', 'cpp', 'c'}:
        print("Usage: compiler.py [python|cpp|c]")
        return

    target_language = sys.argv[1]
    output_file = 'output.' + {'python': 'py', 'cpp': 'cpp', 'c': 'c'}[target_language]

    print("Reading input file...")
    with open('input.txt', 'r') as f:
        code = f.read()
    
    print("Performing lexical analysis...")
    tokens = list(lex(code))
    print("Tokens:", tokens)
    
    print("Performing syntax analysis...")
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
    
    if target_language == 'python':
        print("Generating Python code...")
        output_code = generate_python(ast)
    elif target_language == 'cpp':
        print("Generating C++ code...")
        output_code = generate_cpp(ast)
    elif target_language == 'c':
        print("Generating C code...")
        output_code = generate_c(ast)
    
    print("Generated code:")
    print(output_code)
    
    print(f"Writing output to {output_file}...")
    with open(output_file, 'w') as f:
        f.write(output_code)
    print("Compilation complete.")

if __name__ == '__main__':
    main()
