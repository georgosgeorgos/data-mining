package sbnhw1;
import java.util.List;
import java.util.Arrays;
/**
 *
 * @author georgos
 */
public class Herbivor extends Animal {

    public Herbivor(String name, int age, String description, String foods) {
        super(name, age, description, foods);
    }

    @Override
    public String getType()
    {
        return ("herbivor");
    }
}
