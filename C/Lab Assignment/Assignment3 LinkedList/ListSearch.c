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
    printf("The linked list is : \n");
    temp = head;
    while(temp!=NULL){
        printf("%d ", temp->data);
        temp=temp->next;
    }
    
    int value;
    printf("Enter the value to be searched : ");
    scanf("%d", &value);
    temp=head;

    int i=1;
    while(temp->data!=value){
        i++;
        temp = temp->next;
    }

    if(temp==NULL){
        printf("Value not found \n");
        return 1;
    }
    else
        printf("Value found at position %d \n", i);

    
    freeList(head);
}

