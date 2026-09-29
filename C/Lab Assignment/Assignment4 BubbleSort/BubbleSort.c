#include <stdio.h>
#include <stdlib.h>

void display(int arr[], int n){
    for(int i=0;i<n;i++){
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void bubbleSort(int arr[], int n){
    for(int i=0;i<n-1;i++){
        for(int j=0;j<n-i-1;j++){
            if(arr[j]>arr[j+1]){
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

int main(){
    int n;

    printf("Enter the number of Elements: ");
    scanf("%d",&n);

    int arr[n];

    printf("Enter the elements of the array : \n");
    for(int i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }

    printf("Original Array: ");
    display(arr, n);

    bubbleSort(arr, n);

    printf("Sorted Array: ");
    display(arr, n);

    return 0;
}