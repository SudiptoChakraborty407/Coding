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
    struct Node *newNode = malloc(sizeof(struct Node));

    if(!head || !second || !third || !newNode){
        printf("Memory allocation failed \n");
        return 1;
    }

    head->data = 10;
    head->next = second;

    second->data = 20;
    second->next = third;

    third->data = 30;
    third->next = NULL;

    int value, pos;
    printf("Enter the value you want to insert ");
    scanf("%d", &value);
    printf("Enter the position where you want to insert ");
    scanf("%d", &pos);
    newNode->data = value;

    if(pos==1){
        newNode->next = head;
        head = newNode;
    }
    else {
        struct Node *temp = head;
        for(int i=1;i<pos-1;i++){
            temp = temp->next;
        }

        newNode->next = temp->next;
        temp->next = newNode;
    }    

    printf("The linked list is : \n");
    struct Node *temp = head;
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