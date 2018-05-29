package sbnhw1;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;

/**
 *
 * @author georgos
 */


// abstract class (no implementation) 
public abstract class Animal implements Stomach
{    
    private final int age;
    private final String name;
    private final String description;
    public final ArrayList<String> foods;
    // we assume a max weight for every animal
    public final float weight_limit;
    
    public Animal(String name, int age, String description, String foods)
    {   
        this.age = age;
        this.name = name;
        this.description = description;
        String[] s = foods.split(" ");
        this.foods = new ArrayList<>(Arrays.asList(s));
        // we assume that an animal cannot eat more than 10 kg of food (this is a not realistic assumption because I could easily)
        this.weight_limit = (float) 10.0;
    }
    
    public int getAge()
    {
        return this.age;
    }
    public String getName()
    {
        return this.name;
    }
    public String getDescription()
    {
        return this.description;
    }
    public String getType()
    {
        return ("animal");
    }
    public ArrayList<String> getFoods()
    {
        return this.foods;
    }
    
    @Override
    public void feedMe(String food, float weight)
    {    
        if (weight > this.weight_limit)
        {      
            System.out.println("Too much food animal!!!");
        }
        if (this.foods.contains(food))
        {
            System.out.println("You can eat " + food + ".");
        }
        else
        {
            System.out.println("Sorry, " + food + " is forbidden for your stomach!!!");
        }
        
    }
}