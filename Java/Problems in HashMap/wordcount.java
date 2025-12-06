import java.util.*;

public class wordcount {
    public static void main(String[] args) {
        System.out.println("Enter the sentence");
        Scanner sc = new Scanner(System.in);
        String sentence = sc.nextLine().toLowerCase();
        HashMap<String,Integer> wordcount = new HashMap<>();
        String word = "";
        for(int i = 0;i<sentence.length();i++)
        {
            if (sentence.charAt(i)==' '){
                if ( !word.isEmpty()){
                    wordcount.merge(word, 1, Integer::sum);
                    word = "";
                }
            }
            else
            word = word + sentence.charAt(i);
        }
        
        if (!word.isEmpty())
            wordcount.merge(word, 1, Integer::sum);
        
        System.out.println("the words and their word count in the sentence are:");
        
        for(Map.Entry<String,Integer> e: wordcount.entrySet())
        System.out.println(e.getKey() + " " + e.getValue());
    }
}
