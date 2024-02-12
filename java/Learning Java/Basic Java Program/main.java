/*
 * In order to run the java program we need to compile the class Basic using the command prompt
 * 'javac fname.java'. This command will generate an class file in the directory 'className.class'
 * which can be executed using the 'java className' command in the command line. If multiple classes are 
 * defined in a java file multiple class files will be generated when compiling the java file
 */


class Basic {
    /*
     * the public keyword indicates that this is a class that is visible throughout the entire scope
     * Static is a keyword that indicates that there is no need to create an object to invoke the method which allows us to save memory
     * String[] args or String args[] are command line prompt 
     * System is a class where out is an object of the PrintStream class where println is a method of the object
     */
    public static void main(String[] args){
        System.out.println("Hello World");
    }
}

class Simple {
    /*
     * the public keyword indicates that this is a class that is visible throughout the entire scope
     * Static is a keyword that indicates that there is no need to create an object to invoke the method which allows us to save memory
     * String[] args or String args[] are command line prompt 
     * System is a class where out is an object of the PrintStream class where println is a method of the object
     */
    public static void main(String args[]){
        System.out.println("Hello World");
    }
}