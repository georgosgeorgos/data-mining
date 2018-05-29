package sbnhw1;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Scanner;
import org.apache.lucene.queryparser.classic.ParseException;

/**
 *
 * @author georgos
 */
public class SBNHW1 
{
    /**
     * @param args
     * @throws java.io.IOException
     * @throws org.apache.lucene.queryparser.classic.ParseException
     */ 
    public static void main(String[] args) throws IOException, ParseException 
    {
        // read input
        try (Scanner reader = new Scanner(System.in)) 
        {
            // store names of data files
            ArrayList<String> arrayList = SBNHW1.data();
            // create one instance for every type (omnivor, carnivor, herbivor)
            System.out.println("ANIMALS");
            System.out.println();
            
            for (String string : arrayList)
            {
                String[] s = string.split(";");
                String name = s[0];
                int age = Integer.parseInt(s[1]);
                String description = s[2];
                String foods = s[3];
                String type = s[4];
                
                if (type != null)
                switch (type) 
                {
                    case "h":
                        // instance of animal with stomach interface
                        Herbivor h = new Herbivor(name, age, description, foods);
                        // print some results about foods and weights
                        SBNHW1.print(h, reader);
                        break;
                    case "o":
                        Omnivor o = new Omnivor(name, age, description, foods);
                        SBNHW1.print(o, reader);
                        break;
                    case "c":
                        Carnivor c = new Carnivor(name, age, description, foods);
                        SBNHW1.print(c, reader);
                        break;
                    default:
                        break;
                }
            }
            // run lucene to build an index and perform a simple OR boolean query
            System.out.println("LUCENE");
            System.out.println();
            SBNHW1.lucene();
        }
    }
    
    private static void print(Animal animal, Scanner reader) 
    {    
        System.out.println("name: " + animal.getName());
        System.out.println("type: " + animal.getType());
        System.out.println("age: " + animal.getAge());
        System.out.println("description: " + animal.getDescription());
        System.out.println();
        String food;
        String w;
        
        
        System.out.println("Enter a food or press Enter for default(food:fish, weight:10.0): (choose between meat, fish, vegetable, fruit)");
        food = reader.nextLine();
        if (food.equals(""))
        {
            food = "fish";
        }
        System.out.println("Enter a weight:");
        w = reader.nextLine();
        float weight;
        
        try{weight = Float.valueOf(w);}
        catch (java.lang.NumberFormatException e){weight = (float) 10.0;}
        
        System.out.println("food: " + food + ", quantity: " + weight);
        System.out.println();
        animal.feedMe(food, weight);
        System.out.println("--------------------------------");
        System.out.println();
    }
    
    private static void lucene() throws IOException, ParseException
    {
        Lucene luc = new Lucene();
        Path path = Paths.get("./index/write.lock");
        if (Files.notExists(path)) 
        {
            System.out.println("create index");
            // create index if not present
            luc.createIndex();
            
        }
        else
        {
            System.out.println("index exists");
        }
        String string;
        
        try (Scanner reader = new Scanner(System.in)) 
        {
            System.out.println("Enter a word or press Enter for default(lion): (for example lion)");
            string = reader.nextLine();
            if (string.equals(""))
            {
            string = "lion";
            }
        }
        // search
        luc.searchIndex(string);
    }
    
    private static ArrayList<String> data() throws FileNotFoundException, IOException
    {
        ArrayList<String> arrayList = new ArrayList<>();
        File folder = new File("src/sbnhw1/data");
        File[] listOfFiles;
        listOfFiles = folder.listFiles();
        
        for (File file : listOfFiles) 
        {
            FileInputStream fstream = new FileInputStream(file);
            InputStreamReader reader = new InputStreamReader(fstream);
            
            try (BufferedReader br = new BufferedReader(reader)) 
            {
                String line;
                while ((line = br.readLine()) != null) 
                {
                    arrayList.add(line);
                }
            }
        }
        return (arrayList);
    }
}