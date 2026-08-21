#include <stdio.h>
#define MAX_SIZE 100

typedef struct Stack {
    int arr[MAX_SIZE];
    int top;
} Stack;

void initialize(Stack* stack) {
    stack->top = -1;
}

int isFull(Stack* stack) {
    return stack->top == MAX_SIZE - 1;
}

int isEmpty(Stack* stack) {
    return stack->top == -1;
}

void push(Stack* stack, int value) {
    if (isFull(stack)) {
        printf("Stack Overflow\n");
        return;
    }
    stack->arr[++stack->top] = value;
}

int pop(Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack Underflow\n");
        return -1;
    }
    return stack->arr[stack->top--];
}

int main() {
    Stack stack;
    initialize(&stack);

    char expression[MAX_SIZE];
    printf("Enter a postfix expression : ");
    fgets(expression, sizeof(expression), stdin);
    
    char* token = strtok(expression, " ");
    while (token != NULL) {
        if (isdigit(token[0])) {
            push(&stack, atoi(token));
        } 
        else {
            int operand2 = pop(&stack);
            int operand1 = pop(&stack);
            int result;

            switch (token[0]) {
                case '+':
                    result = operand1 + operand2;
                    break;
                case '-':
                    result = operand1 - operand2;
                    break;
                case '*':
                    result = operand1 * operand2;
                    break;
                case '/':
                    if (operand2 == 0) {
                        printf("Division by zero error\n");
                        return 1;
                    }
                    result = operand1 / operand2;
                    break;
                case '^':
                    result = 1;
                    for (int i = 0; i < operand2; i++) {
                        result *= operand1;
                    }
                    break;
                default:
                    printf("Invalid operator: %s\n", token);
                    return 1;
            }
            push(&stack, result);
        }
        token = strtok(NULL, " ");
    }

    printf("Result: %d\n", pop(&stack));
    return 0;
}
