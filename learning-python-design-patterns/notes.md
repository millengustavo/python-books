# Learning Python Design Patterns

Author: Chetan Giridhar

[Available here](https://www.amazon.com/Learning-Python-Design-Patterns-Second-ebook/dp/B018XYKNOM)

![learning-python-design-patterns](cover.jpg)

# Ch1. Introduction to design patterns

## Understanding object-oriented programming
- Concept of *objects* that have attributes (data members) and procedures (member functions)
- Procedures are responsible for manipulating the attributes
- Objects, which are instances of classes, interact among each other to serve the purpose of an application under development

### Classes
- Define objects in attributes and behaviors (methods)
- Classes consist of constructors that provide the initial state for these objects
- Are like templates and hence can be easily reused

### Methods
- Represent the behavior of the object
- Work on attributes and also implement the desired functionality

## Major aspects of OOP

### Encapsulation
- An object's behavior is kept hidden from the outside world or objects keep their state information private
- Clients can't change the object's internal state by directly acting on them
- Clients request the object by sending requests. Based on the type, objects may respond by changing their internal state using special member functions such as `get` and `set`

### Polymorphism
- Can be of two types:
  - An object provides different implementations of the method based on input parameters
  - The same interface can be used by objects of different types
- In Python polymorphism is a feature built-in for the language (e.g. + operator)

### Inheritance
- Indicates that one class derives (most of) its functionality from the parent class
- An option to reuse functionality defined in the base class and allow independent extensions of the original software implementation
- Creates hierarchy via the relationships among objects of different classes 
- Python supports multiple inheritance (multiple base classes)

### Abstraction
- Provides a simple interface to the clients. Clients can interact with class objects and call methods defined in the interface
- Abstracts the complexity of internal classes with an interface so that the client need not be aware of internal implementations

### Composition
- Combine objects or classes into more complex data structures or software implementations
- An object is used to call member functions in other modules thereby making base functionality available across modules without inheritance

## Object-oriented design principles

### The open/close principle
> **Classes or objects and methods should be open for extension but closed for modifications**

- Make sure you write your classes or modules in a generic way
- Existing classes are not changed reducing the chances of regression
- Helps maintain backward compatibility

### The inversion of control principle
> **High-level modules shouldn't be dependent on low-level modules; they should be dependent on abstractions. Details should depend on abstractions and not the other way round**

- The base module and dependent module should be decoupled with an abstraction layer in between
- The details of your class should represent the abstractions
- The tight coupling of modules is no more prevalent and hence no complexity/rigidity in the system
- Easy to deal with dependencies across modules in a better way

### The interface segregation principle
> **Clients should not be force to depend on interfaces they don't use**

- Forces developers to write thin interfaces and have methods that are specific to the interface
- Helps you not to populate interfaces by adding unintentional methods

### The single responsibility principle
> **A class should have only one reason to change**

- If a class is taking care of two functionalities, it is better to split them
- Functionality = a reason to change
- Whenever there is a change in one functionality, this particular class needs to change, and nothing else
- If a class has multiple functionalities, the dependent classes will have to undergo changes for multiple reasons, which gets avoided

### The substitution principle
> **Derived classes must be able to completely substitute the base classes**

## The concept of design patterns
- Solutions to given problems
- Design patterns are discoveries and not a invention in themselves
- Is about learning from others' successes rather than your own failures!

### Advantages of design patterns
- Reusable across multiple projects
- Architectural level of problems can be solved
- Time-tested and well-proven, which is the experience of developers and architects
- They have reliability and dependence

### Patterns for dynamic languages
Python:
- Types or classes are objects at runtime
- Variables can have type as a value and can be modified at runtime
- Dynamic languages have more flexibility in terms of class restrictions
- Everything is public by default
- Design patterns can be easily implemented in dynamic languages

## Classifying patterns
- Creational
- Structural
- Behavioral

> Classification of patterns is done based primarily on how the objects get created, how classes and objects are structured in a software application, and also covers the way objects interact among themselves

### Creational patterns
- Work on the basis of how objects can be created
- Isolate the details of object creation
- Code is independent of the type of object to be created

### Structural patterns
- Design the structure of objects and classes so that they can compose to achieve larger results
- Focus on simplifying the structure and identifying the relationship between classes and objects
- Focus on class inheritance and composition

### Behavioral patterns
- Concerned with the interaction among objects and responsibilities of objects
- Objects should be able to interact and still be loosely coupled

# Ch2. The singleton design pattern


