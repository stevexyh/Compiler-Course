%%
[\t]+
is   | 
am   |
are  |
was  |
were {printf("%s: is a verb\n",yytext);}
[a-zA-Z]+ {printf("%s: is not a verb\n",yytext);}
[0-9]+ {printf("%s: is a number\n",yytext);}
.|\n
%%

int main(){
	yylex();
}