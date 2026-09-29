    #include <stdio.h>
#include <stdlib.h>

int main(){
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
            if(arr[j]>arr[pos])
                pos = j;
        }

        int temp = arr[i];
        arr[i] = arr[pos];
        arr[pos] = temp;
    }

    printf("The elements of the array are: \n");
    for(int i=0;i<n;i++){
        printf("%d ", arr[i]);
    }

    return 0;
}