import java.io.*;
import java.util.*;

class UniqueNameList
{
    public static void main(String[] args) throws IOException
    {
        BufferedReader read = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter the names of the students");
        HashSet<String> names = new HashSet<>();
        for(int i = 0;i<10;i++)
        {
            names.add(read.readLine());
        }

        // System.out.println("the output:");
        // Iterator IT = names.iterator();
        // while(IT.hasNext())
        // {
        //     System.out.println(IT.next());
        // }

        System.out.println("the output:");
        for (String name : names)
        {
            System.out.println(name);
        }
    }
}