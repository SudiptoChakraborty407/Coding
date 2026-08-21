#include <stdio.h>
#include <string.h>
#define MAX 100

char stack1[MAX];
int top = -1;

int main(){
    push (10);
    push (20);
    push (30);
    push (40);
    push (50);
    display();
    
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

void display(){
    if(top==-1){
        printf("Stack is empty \n");
    }
    else{
        printf("The elements of the stack are: \n");
        for(int i=0;i<=top;i++){
            printf("%d ", stack1[i]);
        }
        printf("\n");
    }
}



