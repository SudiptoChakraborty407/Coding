import java.util.*;

public class VowelCount {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a sentence to check for vowels");
        String str = sc.nextLine();
        HashMap <Character, Integer> map = new HashMap<>();
        map.put('a',0);
        map.put('e',0);
        map.put('i',0);
        map.put('o',0);
        map.put('u',0);
        String lstr = str.toLowerCase();
        for(int i = 0;i<lstr.length(); i++)
        {
            char c = str.charAt(i);
            if (map.containsKey(c))
                map.put(c,map.get(c)+1);
        }
        System.out.println("the vowel counts:");
        for(Map.Entry<Character,Integer> e : map.entrySet())
        {
            System.out.println(e.getKey() + " " + e.getValue());
        }
    }
}
