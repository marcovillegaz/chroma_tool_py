class atributtes, are attributes inherentes of a class, all objects defined as 
a class will have the same class atributtes. 
instance attribites 

a class has properties (attributes) and behaviors (methods). An instance refers
 to a specific occurrence of a class. When you create an object from a class,
you are creating an instance of that class.

__dict__ method return all the attributs that belong to the class or any instance

to refer to class attributes you use the name of the class:
    MyClass.ClassAttribute 
    
__repr__ is a method used to return an unambiguous string representation of an 
object that can be used to reproduce the same object when fed to the eval() 
function. It is most commonly used for debugging, so it is important that the 
representation is information-rich and explicit.


**Class Method**\
The built-in fun*ction decorator @classmethod is an expression that is evaluated 
just after the definition of your function. The result of such a evaluation 
casts a shadow over your function definition. Similar to how an instance method 
receives the instance, a class method also takes the class as an implicit first 
argument.

```
class ClassName(object):
    @classmethod
    def method(cls, arg1, arg2, ...):
       ....
       return cls
```


**Static methods**\
 static method is a method that is tied to the class instead of the class's object. It is not possible to pass an implicit first argument to a static method. The class state cannot be accessed or changed by this method. It is present in a class because having the method in a class makes sense. It returns a Static method for the function

 ```
    class ClassName(object):
    @staticmethod
    def method(arg1, arg2, ...):
       ....
       return val 
 ```

 **Static methods vs Class methods**\
 Static methods are typically unaware of the class state. They are utility methods that operate on some parameters after receiving them. On the other hand, class must be a parameter for class methods