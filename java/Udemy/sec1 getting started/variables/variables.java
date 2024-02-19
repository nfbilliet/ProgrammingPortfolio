/*
 * Java is a case sensitive language meaning that uppercase and lowercase impact how we write code
 * 'Int a' is not equivalent to 'int a'
 * 
 * Variables can only be declared once and will result in an error when we try to redefine it
 */

public class variables {
    public static void main(String args[]){
        int myFirstNum = 5;
        double mySecondNum = 5.5;
        System.out.println("The variable 'myFirstNum' contains the value :");
        System.out.println(myFirstNum);
        myFirstNum = myFirstNum*2;
        System.out.println("The variable 'myFirstNum' contains the following value after modification:");
        System.out.println(myFirstNum);
        System.out.println("The variable 'mySecondNum' contains the value:");
        System.out.println(mySecondNum);
        System.out.println("Adding 2 variables of different types together results in :");
        System.out.println(myFirstNum+mySecondNum);
    }
}
