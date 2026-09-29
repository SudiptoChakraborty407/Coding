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

void insertAtBeginning(Node **head, int data){
    Node *newNode = createNode(data);

    if(*head==NULL){
        *head = newNode;
        return;
    }

    newNode->prev=NULL;
    newNode->next=*head;
    (*head)->prev=newNode;
    *head = newNode;
}

void insertAtEnd(Node **head, int data){
    Node *newNode = createNode(data);

    if(*head==NULL){
        *head = newNode;
        return;
    }

    Node *temp = *head;
    while(temp->next!=NULL)
        temp = temp->next;

    temp->next=newNode;
    newNode->prev=temp;
}

void insert(Node **head, int data, int position){

    if(position<1){
        printf("Invalid position\n");
        return;
    }

    if(position==1){
        insertAtBeginning(head, data);
        return;
    }

    Node *newNode = createNode(data);
    Node *temp = *head;

    for(int i=1; temp != NULL && i<position-1; i++)
        temp=temp->next;
    
    if(temp==NULL){
        printf("Position more than number of nodes\n");
        free(newNode);
        return;
    }

    if(temp->next==NULL){
        insertAtEnd(head, data);
        free(newNode);
        return;
    }

    newNode->prev = temp;
    newNode->next = temp->next;
    temp->next = newNode;
    newNode->next->prev = newNode;

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

void deleteAtBeginning(Node **head){
    if(*head==NULL){
        printf("List is empty\n");
        return;
    }

    Node *temp = *head;
    *head = (*head)->next;

    if(*head!=NULL)
        (*head)->prev=NULL;

    free(temp);
}

void deleteAtEnd(Node **head){
    if(*head==NULL){
        printf("List is empty\n");
        return;
    }

    Node *temp = *head;

    while(temp->next!=NULL)
        temp=temp->next;

    if(temp->prev==NULL){
        *head=NULL;
    }
    else{
        temp->prev->next=NULL;
    }

    free(temp);
}

void delete(Node **head, int position){
    if(position<1){
        printf("Invalid position\n");
        return;
    }
    
    if(position==1){
        deleteAtBeginning(head);
        return;
    }

    Node *temp = *head;

    for(int i=1; temp!=NULL && i<position; i++)
        temp=temp->next;

    if(temp==NULL){
        printf("Position more than number of nodes\n");
        return;
    }

    if(temp->next==NULL){
        deleteAtEnd(head);
        return;
    }

    temp->prev->next=temp->next;
    temp->next->prev=temp->prev;

    free(temp);
}

int main(){
    Node *head = createList();
    
    printf("\nEnter: \n0 to terminate the program \n1 for Insert \n2 for Delete \n3 to Display\n");

    int c, data, pos;
    scanf("%d", &c);

    while(c!=0){
        switch(c){
            case 1:
                printf("Enter the value of the data and the position you want to insert: \n");
                scanf("%d", &data);
                scanf("%d", &pos);
                insert(&head, data, pos);
                break;

            case 2:
                printf("Enter the position you want to delete: \n");
                scanf("%d", &pos);
                delete(&head, pos);
                break;

            case 3:
                printf("The Doubly Linked List is: ");
                display(head);
                break;

            default:
                printf("Invalid choice\n");
        }

        printf("\nEnter your choice: ");
        scanf("%d", &c);
    }

    freelist(head);

    return 0;
}