/*
 * Primitive data types are the basic data types that are included in java
 *      Whole numbers: byte, short, int, long 
 *      Decimal numbers: float, double 
 *      Single characters: char 
 *      Boolean values: boolean
 * building blocks of data manip
 * 
 * All data types have a range in which they can exist
 * 
 * Each of these data types are defined by their wrapper class
 * These classes stores information about the primitive that can is not stored in the variable itself
 * e.g. the bounds of acceptable values that a specific data type can take.
 * 
 *  Byte can take up to 1 byte of data in memory and thus contains 8 bits
 *      2^8 possible values (256)
 * 
 *  Short can take up to 2 bytes of data in memory and thus contains 16 bits
 *      2^16 possible values
 * 
 *  int take up to 4 bytes of data in memory and thus contains 32 bits
 *      2^32 possible values
 *      integers can be both negative and positive -> [-(2^32)/2, (2^32)/2]
 *      Exceeding this range through operations result in wraparound errors
 *      Initializing variables that lie outside of this range results in errors that prevent compilation
 *
 *  long can take up to 8 bytes of data in memory and thus contains 64 bits
 *      2^64 possible values      
 * 
 * Because integers are considered to be the standard data type for whole numbers we have to force java 
 * to store a variable as a long we have to add a 'l' or 'L' at the end of the number
 *      
 */
public class primitives {
    public static void main(String[] args) {
        int myIntVal = 10000;
        int myLargeInt = 2189567;
        // Large numbers can be made more readable by introducing underscores, this wont change the value
        int myLargeIntPretty = 2_189_567;
        System.out.println("The large int and the pretty large int are equivalent numbers: " + (myLargeInt==myLargeIntPretty));
        // Byte, Short, Integer and Long are wrapper classes
        System.out.println("The range of the byte data type is: ("+Byte.MIN_VALUE+","+Byte.MAX_VALUE+")");
        System.out.println("The range of the short data type is: ("+Short.MIN_VALUE+","+Short.MAX_VALUE+")");
        System.out.println("The range of the int data type is: ("+Integer.MIN_VALUE+","+Integer.MAX_VALUE+")");
        System.out.println("The range of the long data type is: ("+Long.MIN_VALUE+","+Long.MAX_VALUE+")");
        // Wraparound errors
        System.out.println("Exceeding the minimum bound, i.e. (min-1), results in an underflow and gives us the value: " + (myIntMin-1));
        System.out.println("Exceeding the maximum bound, i.e. (max+1), results in an overflow and gives us the value: " + (myIntMax+1));
        System.out.println("Underflow and overflow are known as wraparounds as the minimum changes to the maximum and viceversa");
        long myFirstLong = 100;
        long myRealFirstLong = 100l;
        System.out.println("The width of the 'myFirstLong' variable is "+myFirstLong.SIZE);
    }
}
