package sbnhw1;

/**
 *
 * @author georgos
 */
public class Omnivor extends Animal{
    
    public Omnivor(String name, int age, String description, String foods) {
        super(name, age, description, foods);
    } 
    @Override
    public String getType()
    {
        return ("omnivor");
    }
    @Override
    public void feedMe(String food, float weight)
    {    
        if (weight > weight_limit)
        {
            System.out.println("Too much food animal!!!");
        } else {      
        }
        if (true)
        {
            System.out.println("Top! You can eat " + food + " and every other food.");
        }
    }
    
}
