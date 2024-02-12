class ClassLoaderExample {
    public static void main(String args[]){
        Class c = ClassLoaderExample.class;
        System.out.println(c.getClassLoader());
        //output: jdk.internal.loader.ClassLoaders$AppClassLoader@33909752
        //Uses the application classloader (AppClassLoader)
        System.out.println(String.class.getClassLoader());
        //output: null
        //String is included into the standard library rt.jar and will be loaded by the bootstrap classloader
        //null is returned because it is a builtin class
    }
} 