#include <stdio.h>

#define SIZE 10

typedef struct Queue{
    int items[SIZE];
    int front;
    int rear;
}Queue;

void innit(Queue *q){
    q->front = 0;
    q->rear = 0;
}

int isFull(Queue *q){ 
    return q->front==(q->rear+1) % SIZE;
}

int isEmpty(Queue *q){
    return q->front==q->rear;
}

void enqueue(Queue *q){
    if(isFull(q)){
        printf("The Queue is Full\n");
        return;
    }
    
    int value;
    printf("Enter the value you want to enqueue : ");
    scanf("%d", &value);
    q->items[q->rear] = value;
    q->rear = (q->rear+1) % SIZE;
}

void dequeue(Queue *q){
    if(isEmpty(q)){
        printf("The Queue is Empty \n");
        return;
    }

    printf("The value deleted is %d \n", q->items[q->front]);
    q->front = (q->front+1) % SIZE;
}

void display(Queue *q){
    if(isEmpty(q)){
        printf("The Queue is Empty \n");
        return;
    }

    printf("The Queue is :\n");
    for(int i=q->front;i!=q->rear;i = (i+1)%SIZE){
        printf("%d ", q->items[i]);
    }
    printf("\n"); 
}

int main(){
    printf ("Press \n 0 -> terminate \n 1 to Enqueue \n 2 to Dequeue \n 3 to Display \n");
    int n=-1;
    Queue q;
    innit(&q);
    while (n!=0){
        scanf("%d", &n);
        switch (n){
            case 0:
                break;
            case 1:
                enqueue(&q);
                break;
            case 2:
                dequeue(&q);
                break;
            case 3:
                display(&q);
                break;
            default:
                printf("Input incorrect");
                break;
        }
    }
}