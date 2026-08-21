#include <stdio.h>
#define MAX 5
int stack1[MAX], top = -1;

int main(){
    printf ("Press \n 0 -> terminate \n 1 to push \n 2 to pop \n 3 to peek \n 4 to display\n");
    int n=-1;
    while (n!=0){
        scanf("%d", &n);
        switch (n){
            case 0:
                break;
            case 1:
                push();
                break;
            case 2:
                pop();
                break;
            case 3:
                peek();
                break;
            case 4:
                display();
                break;
            default:
                printf("Input incorrect");
                break;
        }
    }
}

void pop(){
    if (top>-1){
        printf("The element removed was %d \n", stack1[top]);
        top--;
    }
    else {
        printf("Stack is empty \n");
    }
}

void push(){
    if (top<MAX-1){
        top++;
        printf("Enter the element to be inserted \n");
        scanf("%d", &stack1[top]);
    }
    else{
        printf("Stack Overflow \n");
    }
}

void peek(){
    if(top==-1){
        printf("Stack is empty \n");
    }
    else {
        printf("The topmost value is : %d \n", stack1[top]);
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