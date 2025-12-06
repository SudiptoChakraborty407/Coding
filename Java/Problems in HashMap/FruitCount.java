import java.util.*;

public class FruitCount {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the names of fruits, enter 0 to stop");
        String fruit;
        HashMap<String, Integer> fruits = new HashMap<>();
        while(true)
        {
            fruit = sc.next().toLowerCase();
            if(fruit.equals("0"))
                break;
            fruits.merge(fruit, 1, Integer::sum);
        }

        sc.close();

        for(Map.Entry<String,Integer> e: fruits.entrySet())
        {
            System.out.println(e.getKey() + " " + e.getValue());
        }
    }
}
