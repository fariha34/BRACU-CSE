%{

#include"symbol_info.h"
#define YYSTYPE symbol_info*
int yyparse(void);
int yylex(void);
extern FILE *yyin;
int line_num;
void yyerror(char *s);
ofstream outlog;

// declare any other variables or functions needed here

%}

%token IF ELSE FOR WHILE DO BREAK VOID SWITCH DEFAULT INT CHAR GOTO FLOAT DOUBLE RETURN CONTINUE CASE PRINTLN
%token ID CONST_INT CONST_FLOAT
%token ADDOP MULOP INCOP DECOP RELOP ASSIGNOP LOGICOP NOT LPAREN RPAREN LCURL RCURL LTHIRD RTHIRD COMMA COLON SEMICOLON


/* resolves the dangling-else ambiguity: bind ELSE to the nearest unmatched IF */
%nonassoc IFX
%nonassoc ELSE

%%

start : program
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" start : program "<<endl<<endl;
		outlog<<endl;
	}
	;

program : program unit
	{
		$$ = new symbol_info($1->getnameofsymbol()+"\n"+$2->getnameofsymbol(),"program");
		outlog<<"At line no: "<<line_num<<" program : program unit "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| unit
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" program : unit "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

unit : variable_decl
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" unit : variable_decl "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| func_definition
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" unit : func_definition "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

func_definition : type_specifier ID LPAREN param_list RPAREN compound_statement
	{
		outlog<<"At line no: "<<line_num<<" func_definition : type_specifier ID LPAREN param_list RPAREN compound_statement "<<endl<<endl;
		outlog<<$1->getnameofsymbol()<<" "<<$2->getnameofsymbol()<<"("<<$4->getnameofsymbol()<<")\n"<<$6->getnameofsymbol()<<endl<<endl;

		$$ = new symbol_info($1->getnameofsymbol()+" "+$2->getnameofsymbol()+"("+$4->getnameofsymbol()+")\n"+$6->getnameofsymbol(),"func_def");
	}
	| type_specifier ID LPAREN RPAREN compound_statement
	{

		outlog<<"At line no: "<<line_num<<" func_definition : type_specifier ID LPAREN RPAREN compound_statement "<<endl<<endl;
		outlog<<$1->getnameofsymbol()<<" "<<$2->getnameofsymbol()<<"()\n"<<$5->getnameofsymbol()<<endl<<endl;

		$$ = new symbol_info($1->getnameofsymbol()+" "+$2->getnameofsymbol()+"()\n"+$5->getnameofsymbol(),"func_def");
	}
 	;

param_list : param_list COMMA type_specifier ID
	{
		$$ = new symbol_info($1->getnameofsymbol()+","+$3->getnameofsymbol()+" "+$4->getnameofsymbol(),"param_list");
		outlog<<"At line no: "<<line_num<<" param_list : param_list COMMA type_specifier ID "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| param_list COMMA type_specifier
	{
		$$ = new symbol_info($1->getnameofsymbol()+","+$3->getnameofsymbol(),"param_list");
		outlog<<"At line no: "<<line_num<<" param_list : param_list COMMA type_specifier "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| type_specifier ID
	{
		$$ = new symbol_info($1->getnameofsymbol()+" "+$2->getnameofsymbol(),"param_list");
		outlog<<"At line no: "<<line_num<<" param_list : type_specifier ID "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| type_specifier
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" param_list : type_specifier "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

compound_statement : LCURL statements RCURL
	{
		$$ = new symbol_info("{\n"+$2->getnameofsymbol()+"\n}","compound");
		outlog<<"At line no: "<<line_num<<" compound_statement : LCURL statements RCURL "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| LCURL RCURL
	{
		$$ = new symbol_info("{\n}","compound");
		outlog<<"At line no: "<<line_num<<" compound_statement : LCURL RCURL "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

variable_decl : type_specifier declaration_list SEMICOLON
	{
		$$ = new symbol_info($1->getnameofsymbol()+" "+$2->getnameofsymbol()+";","var_decl");
		outlog<<"At line no: "<<line_num<<" variable_decl : type_specifier declaration_list SEMICOLON "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

type_specifier : INT
	{
		$$ = new symbol_info("int","type");
		outlog<<"At line no: "<<line_num<<" type_specifier : INT "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| FLOAT
	{
		$$ = new symbol_info("float","type");
		outlog<<"At line no: "<<line_num<<" type_specifier : FLOAT "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| VOID
	{
		$$ = new symbol_info("void","type");
		outlog<<"At line no: "<<line_num<<" type_specifier : VOID "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| CHAR
	{
		$$ = new symbol_info("char","type");
		outlog<<"At line no: "<<line_num<<" type_specifier : CHAR "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

declaration_list : declaration_list COMMA ID
	{
		$$ = new symbol_info($1->getnameofsymbol()+","+$3->getnameofsymbol(),"decl_list");
		outlog<<"At line no: "<<line_num<<" declaration_list : declaration_list COMMA ID "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| declaration_list COMMA ID LTHIRD CONST_INT RTHIRD
	{
		$$ = new symbol_info($1->getnameofsymbol()+","+$3->getnameofsymbol()+"["+$5->getnameofsymbol()+"]","decl_list");
		outlog<<"At line no: "<<line_num<<" declaration_list : declaration_list COMMA ID LTHIRD CONST_INT RTHIRD "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| ID
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" declaration_list : ID "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| ID LTHIRD CONST_INT RTHIRD
	{
		$$ = new symbol_info($1->getnameofsymbol()+"["+$3->getnameofsymbol()+"]","decl_list");
		outlog<<"At line no: "<<line_num<<" declaration_list : ID LTHIRD CONST_INT RTHIRD "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

statements : statement
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" statements : statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| statements statement
	{
		$$ = new symbol_info($1->getnameofsymbol()+"\n"+$2->getnameofsymbol(),"statements");
		outlog<<"At line no: "<<line_num<<" statements : statements statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

statement : variable_decl
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" statement : variable_decl "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| expression_statement
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" statement : expression_statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| compound_statement
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" statement : compound_statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| FOR LPAREN expression_statement expression_statement expression RPAREN statement
	{
		outlog<<"At line no: "<<line_num<<" statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement "<<endl<<endl;
		outlog<<"for("<<$3->getnameofsymbol()<<$4->getnameofsymbol()<<$5->getnameofsymbol()<<")\n"<<$7->getnameofsymbol()<<endl<<endl;

		$$ = new symbol_info("for("+$3->getnameofsymbol()+$4->getnameofsymbol()+$5->getnameofsymbol()+")\n"+$7->getnameofsymbol(),"stmnt");
	}
	| IF LPAREN expression RPAREN statement %prec IFX
	{
		$$ = new symbol_info("if("+$3->getnameofsymbol()+")\n"+$5->getnameofsymbol(),"stmnt");
		outlog<<"At line no: "<<line_num<<" statement : IF LPAREN expression RPAREN statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| IF LPAREN expression RPAREN statement ELSE statement
	{
		$$ = new symbol_info("if("+$3->getnameofsymbol()+")\n"+$5->getnameofsymbol()+"\nelse\n"+$7->getnameofsymbol(),"stmnt");
		outlog<<"At line no: "<<line_num<<" statement : IF LPAREN expression RPAREN statement ELSE statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| WHILE LPAREN expression RPAREN statement
	{
		$$ = new symbol_info("while("+$3->getnameofsymbol()+")\n"+$5->getnameofsymbol(),"stmnt");
		outlog<<"At line no: "<<line_num<<" statement : WHILE LPAREN expression RPAREN statement "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| PRINTLN LPAREN ID RPAREN SEMICOLON
	{
		$$ = new symbol_info("printf("+$3->getnameofsymbol()+");","stmnt");
		outlog<<"At line no: "<<line_num<<" statement : PRINTLN LPAREN ID RPAREN SEMICOLON "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| RETURN expression SEMICOLON
	{
		$$ = new symbol_info("return "+$2->getnameofsymbol()+";","stmnt");
		outlog<<"At line no: "<<line_num<<" statement : RETURN expression SEMICOLON "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

expression_statement : SEMICOLON
	{
		$$ = new symbol_info(";","expr_stmt");
		outlog<<"At line no: "<<line_num<<" expression_statement : SEMICOLON "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| expression SEMICOLON
	{
		$$ = new symbol_info($1->getnameofsymbol()+";","expr_stmt");
		outlog<<"At line no: "<<line_num<<" expression_statement : expression SEMICOLON "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

variable : ID
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" variable : ID "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| ID LTHIRD expression RTHIRD
	{
		$$ = new symbol_info($1->getnameofsymbol()+"["+$3->getnameofsymbol()+"]","variable");
		outlog<<"At line no: "<<line_num<<" variable : ID LTHIRD expression RTHIRD "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

expression : logic_expression
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" expression : logic_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| variable ASSIGNOP logic_expression
	{
		$$ = new symbol_info($1->getnameofsymbol()+"="+$3->getnameofsymbol(),"expression");
		outlog<<"At line no: "<<line_num<<" expression : variable ASSIGNOP logic_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

logic_expression : rel_expression
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" logic_expression : rel_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| rel_expression LOGICOP rel_expression
	{
		$$ = new symbol_info($1->getnameofsymbol()+$2->getnameofsymbol()+$3->getnameofsymbol(),"logic_expr");
		outlog<<"At line no: "<<line_num<<" logic_expression : rel_expression LOGICOP rel_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

rel_expression : simple_expression
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" rel_expression : simple_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| simple_expression RELOP simple_expression
	{
		$$ = new symbol_info($1->getnameofsymbol()+$2->getnameofsymbol()+$3->getnameofsymbol(),"rel_expr");
		outlog<<"At line no: "<<line_num<<" rel_expression : simple_expression RELOP simple_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

simple_expression : term
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" simple_expression : term "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| simple_expression ADDOP term
	{
		$$ = new symbol_info($1->getnameofsymbol()+$2->getnameofsymbol()+$3->getnameofsymbol(),"simple_expr");
		outlog<<"At line no: "<<line_num<<" simple_expression : simple_expression ADDOP term "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

term : unary_expression
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" term : unary_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| term MULOP unary_expression
	{
		$$ = new symbol_info($1->getnameofsymbol()+$2->getnameofsymbol()+$3->getnameofsymbol(),"term");
		outlog<<"At line no: "<<line_num<<" term : term MULOP unary_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

unary_expression : ADDOP unary_expression
	{
		$$ = new symbol_info($1->getnameofsymbol()+$2->getnameofsymbol(),"unary_expr");
		outlog<<"At line no: "<<line_num<<" unary_expression : ADDOP unary_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| NOT unary_expression
	{
		$$ = new symbol_info("!"+$2->getnameofsymbol(),"unary_expr");
		outlog<<"At line no: "<<line_num<<" unary_expression : NOT unary_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| factor_info
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" unary_expression : factor_info "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

factor_info : factor
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" factor_info : factor "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

factor : variable
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" factor : variable "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| ID LPAREN argument_list RPAREN
	{
		$$ = new symbol_info($1->getnameofsymbol()+"("+$3->getnameofsymbol()+")","factor");
		outlog<<"At line no: "<<line_num<<" factor : ID LPAREN argument_list RPAREN "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| LPAREN expression RPAREN
	{
		$$ = new symbol_info("("+$2->getnameofsymbol()+")","factor");
		outlog<<"At line no: "<<line_num<<" factor : LPAREN expression RPAREN "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| CONST_INT
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" factor : CONST_INT "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| CONST_FLOAT
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" factor : CONST_FLOAT "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| variable INCOP
	{
		$$ = new symbol_info($1->getnameofsymbol()+"++","factor");
		outlog<<"At line no: "<<line_num<<" factor : variable INCOP "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| variable DECOP
	{
		$$ = new symbol_info($1->getnameofsymbol()+"--","factor");
		outlog<<"At line no: "<<line_num<<" factor : variable DECOP "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

argument_list : arguments
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" argument_list : arguments "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	|
	{
		$$ = new symbol_info("","arg_list");
		outlog<<"At line no: "<<line_num<<" argument_list : "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

arguments : arguments COMMA logic_expression
	{
		$$ = new symbol_info($1->getnameofsymbol()+","+$3->getnameofsymbol(),"arguments");
		outlog<<"At line no: "<<line_num<<" arguments : arguments COMMA logic_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	| logic_expression
	{
		$$ = $1;
		outlog<<"At line no: "<<line_num<<" arguments : logic_expression "<<endl<<endl;
		outlog<<$$->getnameofsymbol()<<endl<<endl;
	}
	;

%%

int main(int c, char *v[])
{
	if(c != 2)
	{
		cout<<"Usage: "<<v[0]<<" <input_file>"<<endl;
		return 0;
	}

	yyin = fopen(v[1], "r");

	outlog.open("22299434_23101451_log.txt", ios::trunc);
    
	if(yyin == NULL)
	{
		cout<<"Couldn't open file"<<endl;
		return 0;
	}

	line_num = 1;

	yyparse();

	
    int total_lines = line_num;
    if(fseek(yyin, -1, SEEK_END) == 0 && fgetc(yyin) == '\n')
	   total_lines--;
    outlog<<"Total lines: "<<total_lines<<endl;
	outlog.close();

	fclose(yyin);

	return 0;
}

void yyerror(char *s)
{
	cout<<"At line no "<<line_num<<": syntax error: "<<s<<endl;
}
