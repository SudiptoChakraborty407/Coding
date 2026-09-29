#include <stdio.h>

#define MAX_SIZE 5

typedef struct Queue{
    int items[MAX_SIZE];
    int front;
    int rear;
} Queue;

void init(Queue *q){
    q->front = -1;
    q->rear = 0;
}

int isFull(Queue *q){
    return q->rear==MAX_SIZE;
}

int isEmpty(Queue *q){
    return q->front==q->rear-1;
}

void enqueue(Queue *q, int value){
    if(isFull(q)){
        printf("Queue is Full \n");
        return;
    }
    q->items[q->rear++]=value;
}

void dequeue(Queue *q){
    if(isEmpty(q)){
        printf("Queue is Empty \n");
    }
    q->front++;
}

void display(Queue *q){
    if(isEmpty(q)){
        printf("Queue is Empty \n");
    }
    
    printf("The Queue is : \n");
    for(int i=q->front+1;i<=q->rear-1;i++){
        printf("%d ", q->items[i]);
    }
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