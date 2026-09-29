#include <stdio.h>
#include <stdlib.h>

int main(){
    int countComparison = 0, countSwap = 0;
    int n, j;

    printf("Enter the number of Elements: ");
    scanf("%d",&n);

    int arr[n];

    printf("Enter the elements of the array : \n");
    for(int i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }

    int pos;
    for(int i=0;i<n-1;i++){
        pos = i;

        for(int j=i+1;j<n;j++){
            countComparison++;

            if(arr[j]<arr[pos])
                pos = j;
        }

        if(pos!=i){
            int temp = arr[i];
            arr[i] = arr[pos];
            arr[pos] = temp;
            countSwap++;
        }
    }

    printf("The elements of the array are: \n");
    for(int i=0;i<n;i++){
        printf("%d ", arr[i]);
    }

    printf("\nTotal number of comparisons: %d\n", countComparison);
    printf("Total number of swaps: %d\n", countSwap);

    return 0;
}