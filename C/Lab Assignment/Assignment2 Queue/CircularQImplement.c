#include <stdio.h>
#define SIZE 6

typedef struct Queue{
    int items[SIZE];
    int front;
    int rear;
}Queue;

void init(Queue *q){
    q->front = 0;
    q->rear = 0;
}

int isFull(Queue *q){ 
    return q->front==(q->rear+1) % SIZE;
}

int isEmpty(Queue *q){
    return q->front==q->rear;
}

void enqueue(Queue *q, int value){
    if(isFull(q)){
        printf("The Queue is Full\n");
        return;
    }
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
    Queue q;
    init(&q);
    
    enqueue(&q,10);
    enqueue(&q,20);
    enqueue(&q,30);
    enqueue(&q,40);
    enqueue(&q,50);
    
    dequeue(&q);
    dequeue(&q);

    enqueue(&q,60);
    enqueue(&q,70);

    display(&q);
}