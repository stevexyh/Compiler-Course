program test;
var a,b:integer;
begin
	a:=3;b:=2;
	if (a<5) and (b>1) then 
		a := a+1
		else if (b=2) or (a=4) then
		  a:=a+1
		 else a:=0;
	if not (a<b) then
		  a:=a+1
end.