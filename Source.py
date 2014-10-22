#encoding=utf8
import re

# program = ["external_declaration", "program external_declaration", ]
# external_declaration = ["function_definition", "declaration", ]
# function_definition = ["type_specifier declarator compound_statement", ]
# type_specifier = ["VOID", "CHAR", "INT", "FLOAT", ]
# declarator = ["pointer direct_declarator", "direct_declarator", ]
# Pointer = ["'*'", "'*' pointer", ]
# direct_declarator = ["IDENTIFIER", "direct_declarator '[' ']'", "direct_declarator '[' constant_expression ']'",
#                      "IDENTIFIER '(' parameter_list ')'", "IDENTIFIER '(' ')'",
#                      "direct_declarator  ','  identifier_list", ]
# identifier_list = ["IDENTIFIER", "identifier_list ',' IDENTIFIER", ]
# constant_expression = ["conditional_expression", ]
# parameter_list = ["parameter_declaration", "parameter_list ',' parameter_declaration", ]
# parameter_declaration = ["declaration_specifiers  IDENTIFIER", ]
# compound_statement = ["'{' '}'", "'{' statement_list '}'", "'{' declaration_list statement_list '}'", ]
# declaration_list = ["declaration", "declaration_list declaration", ]
# Declaration = ["init_declarator", "init_declarator_list ',' init_declarator", ]
# init_declarator = ["declarator", "declarator '=' initializer", ]
# Initializer = ["assignment_expression", "'{' initializer_list '}'", "'{' initializer_list ',' '}'", ]
# initializer_list = ["initializer", "initializer_list ',' initializer", ]
# statement_list = ["statement", "statement_list statement", ]
# Statement = ["", "compound_statement", "expression_statement", "selection_statement", "iteration_statement",
#              "jump_statement", ]
# expression_statement = ["';'", "expression ';'", ]
# selection_statement = ["IF '(' expression ')' statement", "IF '(' expression ')' statement ELSE statement", ]
# iteration_statement = ["WHILE '(' expression ')' statement",
#                        "FOR '(' expression_statement expression_statement ')' statement",
#                        "FOR '(' expression_statement expression_statement expression ')' statement", ]
# jump_statement = [ "CONTINUE ';'", "BREAK ';'", "RETURN ';'", "RETURN expression ';'","", ]
# expression = ["assignment_expression", "expression ',' assignment_expression", ]
# assignment_expression = ["conditional_expression", "unary_expression assignment_operator assignment_expression", ]
# conditional_expression = ["logical_or_expression", "logical_or_expression '?' expression ':' conditional_expression", ]
# logical_or_expression = ["logical_and_expression", "logical_or_expression OR_OP logical_and_expression", ]
# logical_and_expression = ["inclusive_or_expression", "logical_and_expression AND_OP inclusive_or_expression", ]
# inclusive_or_expression = ["exclusive_or_expression", "inclusive_or_expression '", "' exclusive_or_expression", ]
# exclusive_or_expression = ["and_expression", "exclusive_or_expression '^' and_expression", ]
# and_expression = ["equality_expression", "and_expression '&' equality_expression", ]
# equality_expression = ["relational_expression", "equality_expression EQ_OP relational_expression",
#                        "equality_expression NE_OP relational_expression", ]
# relational_expression = ["shift_expression", "relational_expression '<' shift_expression",
#                          "relational_expression '>' shift_expression", "relational_expression LE_OP shift_expression",
#                          "relational_expression GE_OP shift_expression", ]
# shift_expression = ["additive_expression", "shift_expression LEFT_OP additive_expression",
#                     "shift_expression RIGHT_OP additive_expression", ]
# additive_expression = ["multiplicative_expression", "additive_expression '+' multiplicative_expression",
#                        "additive_expression '-' multiplicative_expression", ]
# multiplicative_expression = ["cast_expression", "multiplicative_expression '*' cast_expression",
#                              "multiplicative_expression '/' cast_expression",
#                              "multiplicative_expression '%' cast_expression", ]
# cast_expression = ["unary_expression", "'(' type_name ')' cast_expression", ]
# unary_expression = ["postfix_expression", "INC_OP unary_expression", "DEC_OP unary_expression",
#                     "unary_operator cast_expression", "SIZEOF unary_expression", "SIZEOF '(' type_name ')'", ]
# postfix_expression = ["primary_expression", "postfix_expression '[' expression ']'", "postfix_expression '(' ')'",
#                       "postfix_expression '(' argument_expression_list ')'", "postfix_expression '.' IDENTIFIER",
#                       "postfix_expression PTR_OP IDENTIFIER", "postfix_expression INC_OP",
#                       "postfix_expression DEC_OP", ]
# primary_expression = ["IDENTIFIER", "CONSTANT", "STRING_LITERAL", "'(' expression ')'", ]
# argument_expression_list = ["assignment_expression", "argument_expression_list ',' assignment_expression", ]
# unary_operator = ["'&'", "'*'", "'+'", "'-'", "'~'", "'!'", ]
# assignment_operator = ["'='", "MUL_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN", "LEFT_ASSIGN",
#                        "RIGHT_ASSIGN", "AND_ASSIGN", "XOR_ASSIGN", "OR_ASSIGN", ]
# storage_class_specifier = ["TYPEDEF", "EXTERN", "STATIC", "AUTO", "REGISTER", ]
# struct_or_union_specifier = ["struct_or_union IDENTIFIER '{' struct_declaration_list '}'",
#                              "struct_or_union '{' struct_declaration_list '}'", "struct_or_union IDENTIFIER", ]
# struct_or_union = ["STRUCT", "UNION", ]
# struct_declaration_list = ["struct_declaration", "struct_declaration_list struct_declaration", ]
# struct_declaration = ["specifier_qualifier_list struct_declarator_list ';'", ]
# specifier_qualifier_list = ["type_specifier specifier_qualifier_list", "type_specifier",
#                             "type_qualifier specifier_qualifier_list", "type_qualifier", ]
# struct_declarator_list = ["struct_declarator", "struct_declarator_list ',' struct_declarator", ]
# struct_declarator = ["declarator", "':' constant_expression", "declarator ':' constant_expression", ]
# enum_specifier = ["ENUM '{' enumerator_list '}'", "ENUM IDENTIFIER '{' enumerator_list '}'", "ENUM IDENTIFIER", ]
# enumerator_list = ["enumerator", "enumerator_list ',' enumerator", ]
# Enumerator = ["IDENTIFIER", "IDENTIFIER '=' constant_expression", ]
# type_qualifier = ["CONST", "VOLATILE", ]
# type_qualifier_list = ["type_qualifier", "type_qualifier_list type_qualifier", ]
# parameter_type_list = ["parameter_list", "parameter_list ',' ELLIPSIS", ]
# parameter_list = ["parameter_declaration", "parameter_list ',' parameter_declaration", ]
# type_name = ["specifier_qualifier_list", "specifier_qualifier_list abstract_declarator", ]
# abstract_declarator = ["pointer", "direct_abstract_declarator", "pointer direct_abstract_declarator", ]
# direct_abstract_declarator = ["'(' abstract_declarator ')'", "'[' ']'", "'[' constant_expression ']'",
#                               "direct_abstract_declarator '[' ']'",
#                               "direct_abstract_declarator '[' constant_expression ']'", "'(' ')'",
#                               "'(' parameter_type_list ')'", "direct_abstract_declarator '(' ')'",
#                               "direct_abstract_declarator '(' parameter_type_list ')'", ]
# labeled_statement = ["IDENTIFIER ':' statement", "CASE constant_expression ':' statement", "DEFAULT ':' statement", ]


# c_dict={"program" : ["external_declaration","program external_declaration",],
# "external_declaration" : ["function_definition","declaration",],
# "function_definition" : ["type_specifier declarator compound_statement",],
# "type_specifier" : ["VOID","CHAR","INT","FLOAT",],
# "declarator" : ["pointer direct_declarator","direct_declarator",],
# "Pointer" : ["'*'","'*' pointer",],
# # "direct_declarator" : ["IDENTIFIER '(' parameter_list ')'","IDENTIFIER '(' ')'","IDENTIFIER",],
# "direct_declarator" : ["IDENTIFIER '(' ')' direct_declarator1","IDENTIFIER '(' parameter_list ')' direct_declarator1","IDENTIFIER direct_declarator1"],
# "direct_declarator1":["'[' ']' direct_declarator1","'[' constant_expression ']' direct_declarator1","','  identifier_list direct_declarator1",""],
# "identifier_list" : ["IDENTIFIER","identifier_list ',' IDENTIFIER",],
# "constant_expression" : ["conditional_expression",],
# "parameter_list" : ["parameter_declaration","parameter_list ',' parameter_declaration",],
# "parameter_declaration" : ["declaration_specifiers  IDENTIFIER",],
# "compound_statement" : ["'{' '}'","'{' statement_list '}'","'{' declaration_list statement_list '}'",],
# "declaration_list" : ["declaration","declaration_list declaration",],
# "declaration" : ["init_declarator","init_declarator_list ',' init_declarator",],
# "init_declarator" : ["declarator","declarator '=' initializer",],
# "initializer" : ["assignment_expression","'{' initializer_list '}'","'{' initializer_list ',' '}'",],
# "initializer_list" : ["initializer","initializer_list ',' initializer",],
# "statement_list" : ["statement","statement_list statement",],
# "statement" : ["expression_statement","selection_statement","iteration_statement","jump_statement","compound_statement",""],
# "expression_statement" : ["';'","expression ';'",],
# "selection_statement" : ["IF '(' expression ')' statement","IF '(' expression ')' statement ELSE statement",],
# "iteration_statement" : ["WHILE '(' expression ')' statement","FOR '(' expression_statement expression_statement ')' statement","FOR '(' expression_statement expression_statement expression ')' statement",],
# "jump_statement" : ["CONTINUE ';'","BREAK ';'","RETURN ';'","RETURN expression ';'","",],
# "expression" : ["assignment_expression","expression ',' assignment_expression",],
# "assignment_expression" : ["unary_expression assignment_operator assignment_expression","conditional_expression",],
# "conditional_expression" : ["logical_or_expression","logical_or_expression '?' expression ':' conditional_expression",],
# "logical_or_expression" : ["logical_and_expression","logical_or_expression OR_OP logical_and_expression",],
# "logical_and_expression" : ["inclusive_or_expression","logical_and_expression AND_OP inclusive_or_expression",],
# "inclusive_or_expression" : ["exclusive_or_expression","inclusive_or_expression '","' exclusive_or_expression",],
# "exclusive_or_expression" : ["and_expression","exclusive_or_expression '^' and_expression",],
# "and_expression" : ["equality_expression","and_expression '&' equality_expression",],
# "equality_expression" : ["relational_expression","equality_expression EQ_OP relational_expression","equality_expression NE_OP relational_expression",],
# "relational_expression" : ["shift_expression","relational_expression '<' shift_expression","relational_expression '>' shift_expression","relational_expression LE_OP shift_expression","relational_expression GE_OP shift_expression",],
# "shift_expression" : ["additive_expression","shift_expression LEFT_OP additive_expression","shift_expression RIGHT_OP additive_expression",],
# "additive_expression" : ["multiplicative_expression","additive_expression '+' multiplicative_expression","additive_expression '-' multiplicative_expression",],
# "multiplicative_expression" : ["cast_expression","multiplicative_expression '*' cast_expression","multiplicative_expression '/' cast_expression","multiplicative_expression '%' cast_expression",],
# "cast_expression" : ["unary_expression","'(' type_name ')' cast_expression",],
# "unary_expression" : ["postfix_expression","INC_OP unary_expression","DEC_OP unary_expression","unary_operator cast_expression","SIZEOF unary_expression","SIZEOF '(' type_name ')'",],
# "postfix_expression" : ["primary_expression","postfix_expression '[' expression ']'","postfix_expression '(' ')'","postfix_expression '(' argument_expression_list ')'","postfix_expression '.' IDENTIFIER","postfix_expression PTR_OP IDENTIFIER","postfix_expression INC_OP","postfix_expression DEC_OP",],
# "primary_expression" : ["IDENTIFIER","CONSTANT","STRING_LITERAL","'(' expression ')'",],
# "argument_expression_list" : ["assignment_expression","argument_expression_list ',' assignment_expression",],
# "unary_operator" : ["'&'","'*'","'+'","'-'","'~'","'!'",],
# "assignment_operator" : ["'='","MUL_ASSIGN","DIV_ASSIGN","MOD_ASSIGN","ADD_ASSIGN","SUB_ASSIGN","LEFT_ASSIGN","RIGHT_ASSIGN","AND_ASSIGN","XOR_ASSIGN","OR_ASSIGN",],
# "storage_class_specifier" : ["TYPEDEF","EXTERN","STATIC","AUTO","REGISTER",],
# "struct_or_union_specifier" : ["struct_or_union IDENTIFIER '{' struct_declaration_list '}'","struct_or_union '{' struct_declaration_list '}'","struct_or_union IDENTIFIER",],
# "struct_or_union" : ["STRUCT","UNION",],
# "struct_declaration_list" : ["struct_declaration","struct_declaration_list struct_declaration",],
# "struct_declaration" : ["specifier_qualifier_list struct_declarator_list ';'",],
# "specifier_qualifier_list" : ["type_specifier specifier_qualifier_list","type_specifier","type_qualifier specifier_qualifier_list","type_qualifier",],
# "struct_declarator_list" : ["struct_declarator","struct_declarator_list ',' struct_declarator",],
# "struct_declarator" : ["declarator","':' constant_expression","declarator ':' constant_expression",],
# "enum_specifier" : ["ENUM '{' enumerator_list '}'","ENUM IDENTIFIER '{' enumerator_list '}'","ENUM IDENTIFIER",],
# "enumerator_list" : ["enumerator","enumerator_list ',' enumerator",],
# "Enumerator" : ["IDENTIFIER","IDENTIFIER '=' constant_expression",],
# "type_qualifier" : ["CONST","VOLATILE",],
# "type_qualifier_list" : ["type_qualifier","type_qualifier_list type_qualifier",],
# "parameter_type_list" : ["parameter_list","parameter_list ',' ELLIPSIS",],
# "parameter_list" : ["parameter_declaration","parameter_list ',' parameter_declaration",],
# "type_name" : ["specifier_qualifier_list","specifier_qualifier_list abstract_declarator",],
# "abstract_declarator" : ["pointer","direct_abstract_declarator","pointer direct_abstract_declarator",],
# "direct_abstract_declarator" : ["'(' abstract_declarator ')'","'[' ']'","'[' constant_expression ']'","direct_abstract_declarator '[' ']'","direct_abstract_declarator '[' constant_expression ']'","'(' ')'","'(' parameter_type_list ')'","direct_abstract_declarator '(' ')'","direct_abstract_declarator '(' parameter_type_list ')'",],
# "labeled_statement" : ["IDENTIFIER ':' statement","CASE constant_expression ':' statement","DEFAULT ':' statement",]
#
# }
# c_dict={'Pointer': ["'*'", "'*' pointer"], 'shift_expression': ['additive_expression 1000'], 'function_definition': ['type_specifier declarator compound_statement'], '1001': ["'+' multiplicative_expression 1001", "'-' multiplicative_expression 1001"], 'type_qualifier': ['CONST', 'VOLATILE'], '1008': ["'[' ']' 1008", "'[' constant_expression ']' 1008", "'(' ')' 1008", "'(' parameter_type_list ')' 1008"], 'selection_statement': ["IF '(' expression ')' statement", "IF '(' expression ')' statement ELSE statement"], 'additive_expression': ['multiplicative_expression 1001'], 'relational_expression': ['additive_expression 1000'], '1009': ['statement 1009'], '1010': ["',' assignment_expression 1010"], 'compound_statement': ["'{' '}'", "'{' statement_list '}'", "'{' declaration_list statement_list '}'"], 'struct_declaration': ["specifier_qualifier_list struct_declarator_list ';'"], 'storage_class_specifier': ['TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER'], 'exclusive_or_expression': ['and_expression 1002'], 'type_name': ['specifier_qualifier_list', 'specifier_qualifier_list abstract_declarator'], '1006': ["',' IDENTIFIER 1006"], 'struct_or_union_specifier': ["struct_or_union IDENTIFIER '{' struct_declaration_list '}'", "struct_or_union '{' struct_declaration_list '}'", 'struct_or_union IDENTIFIER'], '1004': ["',' assignment_expression 1004"], 'expression_statement': ["';'", "expression ';'"], 'cast_expression': ['unary_expression', "'(' type_name ')' cast_expression"], 'declaration_list': ['declaration 1003'], 'external_declaration': ['type_specifier declarator compound_statement'], 'specifier_qualifier_list': ['CONST  specifier_qualifier_list', 'VOLATILE  specifier_qualifier_list'], 'multiplicative_expression': ['unary_expression', "'(' type_name ')' cast_expression"], 'argument_expression_list': ['assignment_expression 1004'], 'logical_or_expression': ['logical_and_expression 1005'], 'initializer': ['assignment_expression', "'{' initializer_list '}'", "'{' initializer_list ',' '}'"], '1011': ["',' enumerator 1011"], '1000': ['LEFT_OP additive_expression 1000', 'RIGHT_OP additive_expression 1000'], 'primary_expression': ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', "'(' expression ')'"], 'declarator': ['pointer direct_declarator', 'direct_declarator'], 'parameter_declaration': ['declaration_specifiers  IDENTIFIER'], 'struct_declaration_list': ["CONST  specifier_qualifier_list  struct_declarator_list ';'", "VOLATILE  specifier_qualifier_list  struct_declarator_list ';'"], 'postfix_expression': ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', "'(' expression ')'"], '1003': ['declaration 1003'], 'identifier_list': ['IDENTIFIER 1006'], 'type_qualifier_list': ['CONST', 'VOLATILE'], 'struct_declarator': ['pointer direct_declarator', 'direct_declarator'], 'program': ['type_specifier declarator compound_statement'], 'initializer_list': ['assignment_expression', "'{' initializer_list '}'", "'{' initializer_list ',' '}'"], 'logical_and_expression': ['inclusive_or_expression 1007'], 'direct_abstract_declarator': ["'(' abstract_declarator ')' 1008", "'[' ']' 1008", "'[' constant_expression ']' 1008", "'(' ')' 1008", "'(' parameter_type_list ')' 1008"], 'type_specifier': ['VOID', 'CHAR', 'INT', 'FLOAT'], 'Enumerator': ['IDENTIFIER', "IDENTIFIER '=' constant_expression"], 'statement_list': ['statement 1009'], 'equality_expression': ['additive_expression 1000'], 'conditional_expression': ['inclusive_or_expression 1007  1005'], 'struct_declarator_list': ['pointer direct_declarator', 'direct_declarator'], 'iteration_statement': ["WHILE '(' expression ')' statement", "FOR '(' expression_statement expression_statement ')' statement", "FOR '(' expression_statement expression_statement expression ')' statement"], 'expression': ['assignment_expression 1010'], 'init_declarator': ['pointer direct_declarator', 'direct_declarator'], '1002': ["'^' and_expression 1002"], 'jump_statement': ["CONTINUE ';'", "BREAK ';'", "RETURN ';'", "RETURN expression ';'", ''], 'and_expression': ['additive_expression 1000'], 'inclusive_or_expression': ['and_expression 1002'], 'struct_or_union': ['STRUCT', 'UNION'], 'enumerator_list': ['enumerator 1011'], 'parameter_type_list': ['parameter_list', "parameter_list ',' ELLIPSIS"], 'assignment_operator': ["'='", 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN'], 'abstract_declarator': ["'(' abstract_declarator ')' 1008", "'[' ']' 1008", "'[' constant_expression ']' 1008", "'(' ')' 1008", "'(' parameter_type_list ')' 1008"], '1005': ['OR_OP logical_and_expression 1005'], 'enum_specifier': ["ENUM '{' enumerator_list '}'", "ENUM IDENTIFIER '{' enumerator_list '}'", 'ENUM IDENTIFIER'], 'assignment_expression': ['and_expression 1002  1007  1005'], 'statement': ["IF '(' expression ')' statement", "IF '(' expression ')' statement ELSE statement"], 'direct_declarator': ["IDENTIFIER '(' parameter_list ')'", "IDENTIFIER '(' ')'", 'IDENTIFIER'], 'labeled_statement': ["IDENTIFIER ':' statement", "CASE constant_expression ':' statement", "DEFAULT ':' statement"], 'parameter_list': ['declaration_specifiers  IDENTIFIER'], 'unary_expression': ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', "'(' expression ')'"], 'declaration': ["IDENTIFIER '(' parameter_list ')'", "IDENTIFIER '(' ')'", 'IDENTIFIER'], '1007': ['AND_OP inclusive_or_expression 1007'], 'unary_operator': ["'&'", "'*'", "'+'", "'-'", "'~'", "'!'"], 'constant_expression': ['and_expression 1002  1007  1005']}
c_dict={"cast_expression":['unary_expression', "'(' type_name ')' cast_expression"],
"struct_declaration":["specifier_qualifier_list struct_declarator_list ';'"],
"struct_or_union_specifier":["struct_or_union IDENTIFIER '{' struct_declaration_list '}'", "struct_or_union '{' struct_declaration_list '}'", 'struct_or_union IDENTIFIER'],
"expression_statement":["';'", "expression ';'"],
"relational_expression":['shift_expression 1000'],
"labeled_statement":["IDENTIFIER '"],
"shift_expression":['additive_expression 1001'],
"multiplicative_expression":['unary_expression', "'(' type_name ')' cast_expression"],
"conditional_expression":['logical_or_expression', "logical_or_expression '?' expression '"],
"1010":['OR_OP logical_and_expression 1010'],
"argument_expression_list":['assignment_expression 1002'],
"specifier_qualifier_list":['type_specifier specifier_qualifier_list', 'type_specifier', 'type_qualifier specifier_qualifier_list', 'type_qualifier'],
"init_declarator_list":['init_declarator 1003'],
"assignment_expression":['logical_or_expression', "logical_or_expression '?' expression '"],
"function_definition":['declaration_specifiers declarator declaration_list compound_statement', 'declaration_specifiers declarator compound_statement', 'declarator declaration_list compound_statement', 'declarator compound_statement\t;'],
"struct_declaration_list":["type_specifier specifier_qualifier_list  struct_declarator_list ';'", "type_specifier  struct_declarator_list ';'", "type_qualifier specifier_qualifier_list  struct_declarator_list ';'", "type_qualifier  struct_declarator_list ';'"],
"1012":['AND_OP inclusive_or_expression 1012'],
"primary_expression":['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', "'(' expression ')'"],
"struct_or_union":['STRUCT', 'UNION'],
"pointer":["'*'", "'*' type_qualifier_list", "'*' pointer", "'*' type_qualifier_list pointer"],
"enumerator":['IDENTIFIER', "IDENTIFIER '=' constant_expression"],
"type_specifier":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'", "UNION  IDENTIFIER '{' struct_declaration_list '}'"],
"unary_operator":["'&'", "'*'", "'+'", "'-'", "'~'", "'!'"],
"exclusive_or_expression":['and_expression 1004'],
"iteration_statement":["WHILE '(' expression ')' statement", "DO statement WHILE '(' expression ')' ';'", "FOR '(' expression_statement expression_statement ')' statement", "FOR '(' expression_statement expression_statement expression ')' statement"],
"1004":["'^' and_expression 1004"],
"constant_expression":['logical_or_expression', "logical_or_expression '?' expression '"],
"1013":["'&' equality_expression 1013"],
"1015":["'[' ']' 1015", "'[' constant_expression ']' 1015", "'(' ')' 1015", "'(' parameter_type_list ')' 1015"],
"selection_statement":["IF '(' expression ')' statement", "IF '(' expression ')' statement ELSE statement", "SWITCH '(' expression ')' statement"],
"statement_list":['statement 1005'],
"1000":["'<' shift_expression 1000", "'>' shift_expression 1000", 'LE_OP shift_expression 1000', 'GE_OP shift_expression 1000'],
"1001":['LEFT_OP additive_expression 1001', 'RIGHT_OP additive_expression 1001'],
"1002":["',' assignment_expression 1002"],
"enumerator_list":['IDENTIFIER', "IDENTIFIER '=' constant_expression"],
"type_qualifier":['CONST', 'VOLATILE'],
"storage_class_specifier":['TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER'],
"1006":["',' struct_declarator 1006"],
"1007":["',' IDENTIFIER 1007"],
"1008":["',' initializer 1008"],
"compound_statement":["'{' '}'", "'{' statement_list '}'", "'{' declaration_list '}'", "'{' declaration_list statement_list '}'"],
"struct_declarator_list":['struct_declarator 1006'],
"type_qualifier_list":['CONST', 'VOLATILE'],
"identifier_list":['IDENTIFIER 1007'],
"1005":['statement 1005'],
"initializer_list":['initializer 1008'],
"parameter_type_list":['parameter_list', "parameter_list ',' ELLIPSIS"],
"initializer":['logical_or_expression', "logical_or_expression '?' expression '"],
"jump_statement":["GOTO IDENTIFIER ';'", "CONTINUE ';'", "BREAK ';'", "RETURN ';'", "RETURN expression ';'"],
"declaration_list":['declaration 1009'],
"declaration_specifiers":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'", "UNION  IDENTIFIER '{' struct_declaration_list '}'"],
"postfix_expression":['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', "'(' expression ')'"],
"logical_or_expression":['logical_and_expression 1010'],
"statement":["';'", "expression ';'"],
"type_name":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'  specifier_qualifier_list", "UNION  IDENTIFIER '{' struct_declaration_list '}'  specifier_qualifier_list"],
"init_declarator":['declarator', "declarator '=' initializer"],
"1009":['declaration 1009'],
"external_declaration":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'  declarator declaration_list compound_statement", "UNION  IDENTIFIER '{' struct_declaration_list '}'  declarator declaration_list compound_statement"],
"unary_expression":["'&'  cast_expression", "'*'  cast_expression", "'+'  cast_expression", "'-'  cast_expression", "'~'  cast_expression", "'!'  cast_expression"],
"additive_expression":['unary_expression', "'(' type_name ')' cast_expression"],
"direct_declarator":['IDENTIFIER 1011', "'(' declarator ')' 1011"],
"declarator":["'*'  direct_declarator", "'*' type_qualifier_list  direct_declarator", "'*' pointer  direct_declarator", "'*' type_qualifier_list pointer  direct_declarator"],
"logical_and_expression":['inclusive_or_expression 1012'],
"declaration":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'  ';'", "UNION  IDENTIFIER '{' struct_declaration_list '}'  ';'"],
"and_expression":['equality_expression 1013'],
"enum_specifier":["ENUM '{' enumerator_list '}'", "ENUM IDENTIFIER '{' enumerator_list '}'", 'ENUM IDENTIFIER'],
"parameter_list":['parameter_declaration 1014'],
"direct_abstract_declarator":["'(' abstract_declarator ')' 1015", "'[' ']' 1015", "'[' constant_expression ']' 1015", "'(' ')' 1015", "'(' parameter_type_list ')' 1015"],
"1003":["',' init_declarator 1003"],
"abstract_declarator":["'*'", "'*' type_qualifier_list", "'*' pointer", "'*' type_qualifier_list pointer"],
"1014":["',' parameter_declaration 1014"],
"assignment_operator":["'='", 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN'],
"inclusive_or_expression":['equality_expression 1013  1004'],
"1011":["'[' constant_expression ']' 1011", "'[' ']' 1011", "'(' parameter_type_list ')' 1011", "'(' identifier_list ')' 1011", "'(' ')' 1011"],
"equality_expression":['unary_expression  1001  1000', "'(' type_name ')' cast_expression  1001  1000"],
"translation_unit":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'  declarator declaration_list compound_statement", "UNION  IDENTIFIER '{' struct_declaration_list '}'  declarator declaration_list compound_statement"],
"struct_declarator":["'*'  direct_declarator", "'*' type_qualifier_list  direct_declarator", "'*' pointer  direct_declarator", "'*' type_qualifier_list pointer  direct_declarator"],
"parameter_declaration":["STRUCT  IDENTIFIER '{' struct_declaration_list '}'  declarator", "UNION  IDENTIFIER '{' struct_declaration_list '}'  declarator"],
"expression":['unary_expression  1001  1000  1013  1004  1012  1010', "'(' type_name ')' cast_expression  1001  1000  1013  1004  1012  1010"],
}
CONTROLLER=8080
terminals={"IDENTIFIER","CONSTANT","STRING_LITERAL","SIZEOF","PTR_OP","INC_OP","DEC_OP","LEFT_OP","RIGHT_OP","LE_OP","GE_OP","EQ_OP","NE_OP","AND_OP","OR_OP","MUL_ASSIGN","DIV_ASSIGN","MOD_ASSIGN","ADD_ASSIGN","SUB_ASSIGN","LEFT_ASSIGN","RIGHT_ASSIGN","AND_ASSIGN","XOR_ASSIGN","OR_ASSIGN","TYPE_NAME","TYPEDEF","EXTERN","STATIC","AUTO","REGISTER","CHAR","SHORT","INT","LONG","SIGNED","UNSIGNED","FLOAT","DOUBLE","CONST","VOLATILE","VOID","STRUCT","UNION","ENUM","ELLIPSIS","CASE","DEFAULT","IF","ELSE","SWITCH","WHILE","DO","FOR","GOTO","CONTINUE","BREAK","RETURN"}




def get_terminals():
    global terminals
    if len(terminals)!=0:
        return terminals
    terminals={"IDENTIFIER","CONSTANT","STRING_LITERAL","SIZEOF","PTR_OP","INC_OP","DEC_OP","LEFT_OP","RIGHT_OP","LE_OP","GE_OP","EQ_OP","NE_OP","AND_OP","OR_OP","MUL_ASSIGN","DIV_ASSIGN","MOD_ASSIGN","ADD_ASSIGN","SUB_ASSIGN","LEFT_ASSIGN","RIGHT_ASSIGN","AND_ASSIGN","XOR_ASSIGN","OR_ASSIGN","TYPE_NAME","TYPEDEF","EXTERN","STATIC","AUTO","REGISTER","CHAR","SHORT","INT","LONG","SIGNED","UNSIGNED","FLOAT","DOUBLE","CONST","VOLATILE","VOID","STRUCT","UNION","ENUM","ELLIPSIS","CASE","DEFAULT","IF","ELSE","SWITCH","WHILE","DO","FOR","GOTO","CONTINUE","BREAK","RETURN"}
    for item_key in c_dict.keys():
        for items in c_dict[item_key]:
            for item in re.split(r'\s+',items):
                if (item.lower() in [c_upper.lower() for c_upper in c_dict.keys()])or (item.isspace() or item.upper() in c_dict.keys()):
                    continue
                terminals.add(item)

    terminals.add("")
    return terminals

def main():
    for item in get_terminals():
        print(item)
if __name__=="__main__":
    main()
