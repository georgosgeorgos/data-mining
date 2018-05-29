package sbnhw1;

import java.util.Arrays;
import java.util.List;

/**
 *
 * @author georgos
 */
public class Carnivor extends Animal {

    public Carnivor(String name, int age, String description, String foods) {
        super(name, age, description, foods);
    }
    
    @Override
    public String getType()
    {
        return ("carnivor");
    }
}
