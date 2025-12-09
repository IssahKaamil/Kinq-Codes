#include<iostream>
using namespace std;
int main(){
    char oper;
    float num1, num2;
   cout<<"Enter the first number and enter:"<<endl;
   cin>>num1;
   cout<<"Enter an operator (+,-,*,/):";
   cin>>oper;
  cout<<"Enter te second number"<<endl;
  cin>>num2;
  switch(oper){
    case '+':
    cout<<num1<<"+"<<num2<<"="<<num1+num2;
    break;
    case '-':
    cout<<num1<<"-"<<num2<<"="<<num1-num2;
    break;
    case '*';
    cout<<num1<<"*"<<num2<<"="<<num1*num2;
    break;
    case '/';
    cout<<num1<<"/"<<num2<<"="<<num1/num2;
    break;
    default:
    //operator does not match any case constant (+,-,*,/);
    cout<<"Error! the operator is not correct";
    break;
 return 0;
}