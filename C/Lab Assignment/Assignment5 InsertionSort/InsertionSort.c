#include <stdio.h>
#include <stdlib.h>

int main(){
    int countComparison = 0, countShift = 0;
    int n, j;

    printf("Enter the number of Elements: ");
    scanf("%d",&n);

    int arr[n];

    printf("Enter the elements of the array : \n");
    for(int i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }

    for(int i=1;i<n;i++){
        for(j=0;j<i;j++){
            countComparison++;

            if(arr[j]>arr[i]){
                break;
            }
        }

        int temp = arr[i];

        for(int k=i;k>j;k--){
            arr[k] = arr[k-1];
            countShift++;
        }

        arr[j] = temp;
    }

    printf("The elements of the array are: \n");
    for(int i=0;i<n;i++){
        printf("%d ", arr[i]);
    }

    printf("\nTotal number of comparisons: %d\n", countComparison);
    printf("Total number of shifts: %d\n", countShift);

    return 0;
}