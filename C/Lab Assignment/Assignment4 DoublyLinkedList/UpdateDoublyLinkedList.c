#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    int data;
    struct Node *prev;
    struct Node *next;
}Node;

Node *createNode(int data){
    Node *newNode = malloc(sizeof(Node));
    newNode->data = data;
    newNode->next=NULL;
    newNode->prev=NULL;
    return newNode;
}

void freelist(Node *head){
    Node *temp = head;
    while (temp!=NULL){
        Node *next = temp->next;
        free(temp);
        temp = next;
    }
}

void display(Node *head){
    Node *temp = head;
    while(temp!=NULL){
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

Node *createList(){
    printf("Enter the value of Head: ");
    int data;
    scanf("%d", &data);
    Node *head = createNode(data);

    printf("Enter the number of nodes: ");
    int n;
    scanf("%d", &n);
    printf("Enter the data of the Nodes : \n");

    Node *temp = head;
    for(int i=1;i<=n;i++){
        scanf("%d", &data);
        Node *newNode = createNode(data);
        newNode->prev = temp;
        temp->next = newNode;
        temp = newNode;
    }

    return head;
}

void update(Node *head, int position, int data){
    if(position<1){
        printf("Invalid position\n");
        return;
    }

    Node *temp = head;

    for(int i=1; temp!=NULL && i<position; i++)
        temp=temp->next;

    if(temp==NULL){
        printf("Position more than number of nodes\n");
        return;
    }

    temp->data=data;
}

int main(){
    Node *head = createList();

    printf("\nOriginal Doubly Linked List: ");
    display(head);

    int position, data;

    printf("Enter the position you want to update: ");
    scanf("%d", &position);

    printf("Enter the new data: ");
    scanf("%d", &data);

    update(head, position, data);

    printf("Updated Doubly Linked List: ");
    display(head);

    freelist(head);

    return 0;
}