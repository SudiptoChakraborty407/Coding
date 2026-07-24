#include <stdio.h>
#include <string.h>
#define MAX 100

char stack1[MAX];
int top = -1;
void push(char ch);
char pop();

int main(){
    printf("Enter the String to be reversed: ");
    char str[100], nstr[100];
    scanf("%s", str);
    int n = strlen(str);
    for(int i=0;i<=n;i++){
        push(str[i]);
    }
    for(int i=0;i<=n;i++){
        nstr[i] = pop();
    }
    printf("The reversed string is %s", nstr);
}

char pop(){
    if (top>-1){
        top--;
        return stack1[top];
    }
    else {
        printf("Stack is empty \n");
        return '0';
    }
}

void push(char n){
    if (top<MAX-1){
        top++;
       stack1[top] = n;
    }
    else{
        printf("Stack Overflow \n");
    }
}