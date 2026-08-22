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
        return -99999999;
    }
    
    printf("The Queue is : \n");
    for(int i=q->front+1;i<q->rear;i++){
        printf("%d ", q->items[i]);
    }
    printf("\n");
}

void find(Queue *q){
    int largest = q->items[q->front+1];
    int smallest = largest;
    for(int i=q->front+1;i<=q->rear;i++){
        if (largest<q->items[i])
            largest = q->items[i];
        if (smallest>q->items[i])
            smallest = q->items[i];
    }
    printf("The smallest item in the Queue is %d while the largest item is %d \n", smallest, largest);
}

int main(){
    printf ("Press \n 0 -> terminate \n 1 to Enqueue \n 2 to Dequeue \n 3 to Display \n 4 to show largest and smallest \n");
    int n=-1;
    Queue q;
    init(&q);
    while (n!=0){
        scanf("%d", &n);
        switch (n){
            case 0:
                break;
            case 1:
                enqueue(&q);
                break;
            case 2:
                printf("The dequed value is : %d \n", dequeue(&q));
                break;
            case 3:
                display(&q);
                break;
            case 4:
                find(&q);
                break;
            default:
                printf("Input incorrect");
                break;
        }
    }
}