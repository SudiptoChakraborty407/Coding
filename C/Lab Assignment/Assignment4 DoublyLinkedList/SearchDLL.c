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

void search(Node *head, int data){
    Node *temp = head;
    int position = 1;

    while(temp!=NULL){
        if(temp->data==data){
            printf("Element found at position %d\n", position);
            return;
        }

        temp=temp->next;
        position++;
    }

    printf("Element not present in the list\n");
}

int main(){
    Node *head = createList();

    printf("\nDoubly Linked List: ");
    display(head);

    int data;

    printf("Enter the element you want to search: ");
    scanf("%d", &data);

    search(head, data);

    freelist(head);

    return 0;
}