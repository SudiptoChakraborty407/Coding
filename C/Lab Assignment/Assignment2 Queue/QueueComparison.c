#include <stdio.h>

#define MAX_SIZE 100

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

void enqueue(Queue *q){
    if(isFull(q)){
        printf("Queue is Full");
        return;
    }
    
    int value;
    printf("Enter the value you want to Enqueue: ");
    scanf("%d", &value);
    q->items[q->rear++]=value;
}

int dequeue(Queue *q){
    if(isEmpty(q)){
        printf("Queue is Empty");
        return -99999999;
    }

    return q->items[++q->front];
}

void display(Queue *q){
    if(isEmpty(q)){
        printf("Queue is Empty");
        return;
    }
    
    printf("The Queue is : \n");
    for(int i=q->front+1;i<q->rear;i++){
        printf("%d ", q->items[i]);
    }
}

void compare(Queue *q1, Queue *q2){

    if (q1->rear-q1->front!=q2->rear-q2->front){
        printf("The queues aren't similar");
        return;
    }
    int j = q2->front+1;
    for(int i = q1->front+1;i<q1->rear;i++){
        if(q1->items[i]!=q2->items[j++]){
            printf("The queue aren't similar ");
            return;
        }
    }
    printf("The queue are similar");
}

int main(){
    printf ("Press \n 0 -> terminate operations on current queue \n 1 to Enqueue \n 2 to Dequeue \n 3 to Display \n");
    int n=-1;
    Queue q1;
    init(&q1);
    while (n!=0){
        scanf("%d", &n);
        switch (n){
            case 0:
                break;
            case 1:
                enqueue(&q1);
                break;
            case 2:
                printf("The dequed value is : %d \n", dequeue(&q1));
                break;
            case 3:
                display(&q1);
                break;
            default:
                printf("Input incorrect");
                break;
        }
    }

    printf ("Press \n 0 -> terminate operations on current queue \n 1 to Enqueue \n 2 to Dequeue \n 3 to Display \n");
    n=-1;
    Queue q2;
    init(&q2);
    while (n!=0){
        scanf("%d", &n);
        switch (n){
            case 0:
                break;
            case 1:
                enqueue(&q2);
                break;
            case 2:
                printf("The dequed value is : %d \n", dequeue(&q2));
                break;
            case 3:
                display(&q2);
                break;
            default:
                printf("Input incorrect");
                break;
        }
    }

    compare(&q1,&q2);
}