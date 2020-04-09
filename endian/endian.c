#include<stdio.h>

int main()

{

    short int x;

    char x0,x1;
    

    x=0x1122;

    x0=((char *)&x)[0];  //低地址单元

    x1=((char *)&x)[1];  //高地址单元
    

    printf("x0=0x%x,x1=0x%x",x0,x1);// 若x0=0x11,则是大端; 若x0=0x22,则是小端......

    return 0;
}
