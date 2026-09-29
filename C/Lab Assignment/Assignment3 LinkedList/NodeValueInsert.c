#include <stdio.h>
#include <stdlib.h>

struct Node{
    int data;
    struct Node *next;
};

void freeList (struct Node *head){
    struct Node *temp = head;
    while(temp!=NULL){
        struct Node *next = temp->next;
        free(temp);
        temp = next;
    }
}

int initialize(struct Node *head){
    struct Node *temp = NULL;
    if(head==NULL){
        printf("Memory allocation failed \n");
        return 1;
    }

    int n;
    printf("Enter the number of nodes : ");
    scanf("%d", &n);

    if(n<=0){
        printf("invalid number of nodes");
        return 1;
    }

    printf("Enter the value of head : ");
    scanf("%d", &head->data);

    head->next = NULL;
    temp = head;

    printf("Enter the values of node : \n");
    for(int i=2; i<=n;i++){
        struct Node *newNode = malloc(sizeof(struct Node));

        if(newNode==NULL){
            printf("Memory allocation failed \n");
            return 1;
        }

        scanf("%d", &newNode->data);

        temp->next = newNode;
        newNode->next = NULL;
        temp =  newNode;
    }
    return 0;
}

int main(){
    struct Node *head = malloc(sizeof(struct Node));
    struct Node *temp = NULL;
    if(initialize(head)!=0){
        return 1;
    };
    
    struct Node *insert = malloc(sizeof(struct Node));
    int value;
    printf("Enter the value you want to insert ");
    scanf("%d", &insert->data);
    printf("Enter the value you want to insert this before ");
    scanf("%d", &value);

    
    if(value==head->data){
        insert->next=head;
        head = insert;
    }
    else {
        temp=head;
        while(temp->next!=NULL && temp->next->data!=value){
            temp=temp->next;
        }
        if(temp->next==NULL){
            printf("Value was not found \n");
            free(insert);
            freeList(head);
            return 1;
        }
        insert->next=temp->next;
        temp->next=insert;
    }

    printf("The linked list is : \n");
    temp = head;
    while(temp!=NULL){
        printf("%d ", temp->data);
        temp=temp->next;
    }
    freeList(head);
}

