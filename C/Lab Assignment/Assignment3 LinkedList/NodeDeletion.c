#include <stdio.h>
#include <stdlib.h>

struct Node{
    int data;
    struct Node *next;
};

int main(){
    struct Node *head = malloc(sizeof(struct Node));
    struct Node *second = malloc(sizeof(struct Node));
    struct Node *third = malloc(sizeof(struct Node));
    struct Node *deleteNode = malloc(sizeof(struct Node));

    if(!head || !second || !third || !deleteNode){
        printf("Memory allocation failed \n");
        return 1;
    }

    head->data = 10;
    head->next = second;

    second->data = 20;
    second->next = third;

    third->data = 30;
    third->next = NULL;
    
    struct Node *temp = head;

    int pos;
    printf("Enter the position which you want to delete ");
    scanf("%d", &pos);
    if(pos==1){
        deleteNode = head;
        head = head->next;
    }
    else {
        for(int i=1;i<pos-1;i++){
            temp = temp->next;
        }

        deleteNode = temp->next;
        temp-> next = deleteNode->next;
    }
    free(deleteNode);


    printf("The linked list is : \n");
    temp = head;
    while(temp!=NULL){
        printf("%d ", temp->data);
        temp=temp->next;
    }

    temp = head;
    while(temp!=NULL){
        struct Node *next = temp->next;
        free(temp);
        temp = next;
    }
}