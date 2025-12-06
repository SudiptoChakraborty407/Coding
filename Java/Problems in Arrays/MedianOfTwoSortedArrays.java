import java.util.*;

class MedianOfTwoSortedArrays {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Arr1");
        int m = sc.nextInt();
        int [] nums1 = new int[m];
        for(int i = 0;i<m;i++)
            nums1[i] = sc.nextInt();

        System.out.println("Arr2");
        int n = sc.nextInt();
        int [] nums2 = new int[n];
        for(int i = 0;i<n;i++)
            nums2[i] = sc.nextInt();
        
        int low = 0;
        int high = m;

        while (low <= high) {
            int partitionX = (low + high) / 2;
            int partitionY = (m + n + 1) / 2 - partitionX;

            int maxLeftX = (partitionX == 0) ? Integer.MIN_VALUE : nums1[partitionX - 1];
            int minRightX = (partitionX == m) ? Integer.MAX_VALUE : nums1[partitionX];

            int maxLeftY = (partitionY == 0) ? Integer.MIN_VALUE : nums2[partitionY - 1];
            int minRightY = (partitionY == n) ? Integer.MAX_VALUE : nums2[partitionY];

            if (maxLeftX <= minRightY && maxLeftY <= minRightX) {
                if ((m + n) % 2 == 0) {
                    System.out.println((double) (Math.max(maxLeftX, maxLeftY) + Math.min(minRightX, minRightY)) / 2);
                    break;
                } else {
                    System.out.println((double) Math.max(maxLeftX, maxLeftY));
                    break;
                }
            } else if (maxLeftX > minRightY) {
                high = partitionX - 1;
            } else {
                low = partitionX + 1;
            }
        }
    }
}