import java.util.*;

public class SumTwoNumArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of integers you want to input");
        int n = sc.nextInt();
        System.out.println("Enter the target Sum");
        int sum = sc.nextInt();
        System.out.println("enter the elements of the array");
        Map<Integer,Integer> arr = new HashMap<>();
        for(int i=0;i<n;i++)
        {
            int x = sc.nextInt();
            int num = sum-x;
            if (arr.containsKey(num))
            {
                System.out.println(num + " with index " + arr.get(num) + " and " + x + " with index " + i);
            }
            arr.put(x, i);
        }
    }
}
