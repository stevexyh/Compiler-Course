program test;
var
s : integer;
n : integer;
begin
	s:=0;
	n:=6;
	if n >= 5 then
	begin
		while n >= 2 do
		begin
			s:=s+1;
			n:=n-1
		end
	end
	else s:=n
end.