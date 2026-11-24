# OOP Unit 4: Java Classes, Inheritance and Interfaces

*Endsem RUN · about 60 minutes*

**The whole unit in one breath:** everything you learnt in C++ (classes, inheritance, overriding, abstract classes) exists in Java with cleaner rules, plus one new idea, the **interface**: a pure "contract" a class promises to follow.

**What the endsem asks from here:** `super` / `this`, abstract class vs interface vs concrete class (asked almost every year), and one Java program with inheritance and a scenario (4.5 to 6 marks). The 2025 paper's whole Q4 came from this unit.

---

## 1. Java for a C++ person · Quick

The differences worth marks:

| C++ | Java |
| --- | --- |
| Pointers, `delete` | No pointers; **garbage collector** frees memory automatically |
| Multiple inheritance of classes | Only **one** parent class; multiple *interfaces* allowed |
| Functions can live outside classes | **Everything** is inside a class |
| Compiled to machine code | Compiled to **bytecode**, run by the JVM: "write once, run anywhere" |
| `virtual` needed for overriding | All non-static, non-final, non-private methods are virtual by default |
| Destructors | No destructors (GC handles it) |

**Why "platform independent":** `javac` turns source into bytecode (`.class`), and any machine with a JVM runs the same bytecode.

**`public static void main(String[] args)`:** `public` so the JVM can call it from outside; `static` so it runs without creating an object; `void` returns nothing; `String[] args` holds command-line arguments.

---

## 2. Classes, objects and constructors · Quick

```java
class Student {
    private int roll;                  // data (fields)
    private String name;

    Student() { this(0, "Unknown"); }  // default constructor calling the other one
    Student(int roll, String name) {   // parameterized
        this.roll = roll;              // this.roll = field, roll = parameter
        this.name = name;
    }
    void show() { System.out.println(roll + " " + name); }
}
// Student s = new Student(1, "Aman");   objects are always made with new
```

**Constructor rules:** same name as the class, no return type, called by `new`. If you write no constructor, Java gives a default one; once you write any constructor, that free default disappears.

**`this`** means "the current object". Two uses: `this.x = x` (field vs parameter with the same name) and `this(...)` (call another constructor of the same class, which must be the first line).

**Access modifiers:** `private` (class only), *default* (no keyword: same package), `protected` (package + subclasses), `public` (everyone).

---

## 3. Inheritance and `super` · Slow down

`class Dog extends Animal` means Dog gets Animal's fields and methods. Java allows only **one** parent class (no diamond problem), but any number of interfaces.

Now, `super`. Think of it as the child's phone line to its parent. `this` means "me"; `super` means "my parent's part of me".

> **Endsem 2025 · Q4(a) · 4.5 marks**
> Discuss the significance of the `super` keyword in Java briefly. Illustrate its usage in calling parent class constructors and methods.

**Answer.**

`super` is a reference to the **immediate parent class** of the current object. It has three uses:

1. **`super(args)`**: calls the parent's constructor, so the parent's fields get set up properly. It must be the **first statement** in the child's constructor. If you don't write it, Java silently inserts `super()` (the no-arg one).
2. **`super.method()`**: calls the parent's version of a method the child has **overridden**, so the child can extend the parent's behaviour instead of rewriting it.
3. **`super.field`**: accesses a parent field hidden by a child field with the same name.

Its significance: it enables **reuse** (no duplicating the parent's setup code) and correct **constructor chaining** (parent part initialised before the child part).

```java
class Person {
    String name;
    Person(String name) {
        this.name = name;
        System.out.println("Person constructor");
    }
    void display() { System.out.println("Name: " + name); }
}

class Student extends Person {
    int roll;
    Student(String name, int roll) {
        super(name);                       // 1. parent constructor, first line
        this.roll = roll;
        System.out.println("Student constructor");
    }
    @Override
    void display() {
        super.display();                   // 2. parent's version of the method
        System.out.println("Roll: " + roll);
    }
}

public class Main {
    public static void main(String[] args) {
        Student s = new Student("Aman", 42);
        s.display();
    }
}
```

Output:

```
Person constructor
Student constructor
Name: Aman
Roll: 42
```

**`super(...)` calls the parent constructor (first line only); `super.method()` calls the parent's overridden method; `super.field` reaches a hidden parent field.**

---

## 4. Polymorphism: overriding and dynamic binding · Slow down

**Overriding:** the child writes a method with the **same name and parameters** as the parent's, to change its behaviour. Use `@Override` so the compiler catches typos.

**Dynamic binding (dynamic method dispatch):** a parent reference can hold a child object, and the method that runs is chosen at **run time** by the object, not the reference type. Same idea as C++ virtual functions, but automatic.

```java
class Payment {
    void pay(double amt) { System.out.println("Paying " + amt); }
}
class UPI extends Payment {
    @Override void pay(double amt) { System.out.println("UPI: " + amt); }
}
class Card extends Payment {
    @Override void pay(double amt) { System.out.println("Card: " + amt + " + 2% fee"); }
}

public class Main {
    public static void main(String[] args) {
        Payment[] list = { new UPI(), new Card(), new Payment() };
        for (Payment p : list) p.pay(100);   // UPI: 100.0 / Card: 100.0 + 2% fee / Paying 100.0
    }
}
```

**Rules:** you can't override `final`, `static` or `private` methods; the overriding method can't be *less* accessible; constructors are never overridden.

| | Overloading | Overriding |
| --- | --- | --- |
| Where | Same class | Parent and child |
| Parameters | Must differ | Must match |
| Decided | Compile time | Run time |

---

## 5. Abstract classes and methods · Quick

Same idea as C++ pure virtual functions, but with a keyword.

**Exam line:** *An abstract class is declared with `abstract`; it cannot be instantiated and may contain abstract methods (declared without a body) as well as normal methods. A subclass must implement all abstract methods, or itself be declared abstract.*

```java
abstract class Shape {
    String name;
    Shape(String name) { this.name = name; }   // abstract classes CAN have constructors
    abstract double area();                    // no body
    void print() { System.out.println(name + " area = " + area()); }
}
class Circle extends Shape {
    double r;
    Circle(double r) { super("Circle"); this.r = r; }
    double area() { return Math.PI * r * r; }
}
// new Shape("x");  -> error: Shape is abstract
```

---

## 6. Interfaces · Slow down

An interface is a **contract**. It says *what* a class must be able to do, not *how*. Think of a USB port standard: any device that follows it plugs in, whether it's a mouse or a pen drive.

**Exam line:** *An interface is a reference type declared with `interface` that contains abstract methods (implicitly `public abstract`) and constants (implicitly `public static final`); since Java 8 it may also have `default` and `static` methods. A class uses `implements` to promise it provides all the interface's methods.*

```java
interface Payable {
    double RATE = 0.18;                  // a constant: public static final
    double total(double amt);            // public abstract
}
interface Printable { void print(); }

class Bill implements Payable, Printable {      // one class, many interfaces
    public double total(double amt) { return amt + amt * RATE; }
    public void print() { System.out.println("Bill printed"); }
}

interface SmartPayable extends Payable {        // an interface extending another
    void refund();
}

public class Main {
    public static void main(String[] args) {
        Payable p = new Bill();                 // access through an interface reference
        System.out.println(p.total(100));       // 118.0
    }
}
```

The four syllabus points, each one line:

- **Defining:** `interface Name { ... }`.
- **Implementing:** `class X implements Name` and write every method as `public`.
- **Accessing through an interface reference:** `Payable p = new Bill();` then `p.total()` runs Bill's version (dynamic binding).
- **Extending:** `interface B extends A` (an interface can extend *many* interfaces).

---

## 7. Abstract class vs interface vs concrete class · Slow down

This table is worth full marks on its own; it was asked in 2025, in Sessional-2 2025, and in 2022.

> **Endsem 2025 · Q4(b) · 4.5 marks**
> Differentiate between abstract class, interface, and concrete class with example code snippets in Java.

**Answer.**

A **concrete class** is a normal, complete class: every method has a body and you can create objects. An **abstract class** is a partly finished class: it can't be instantiated and may leave some methods abstract. An **interface** is a pure contract of methods a class promises to implement.

| Feature | Concrete class | Abstract class | Interface |
| --- | --- | --- | --- |
| Keyword | `class` | `abstract class` | `interface` |
| Objects with `new` | Yes | No | No |
| Abstract methods | None | Zero or more | All normal methods are abstract (plus `default`/`static` since Java 8) |
| Fields | Any | Any (instance variables allowed) | Only `public static final` constants |
| Constructors | Yes | Yes | No |
| Inherited with | `extends` (one) | `extends` (one) | `implements` (many) |
| Use when | You need a complete, usable type | Related classes share code and state | Unrelated classes share a capability |

```java
interface Drawable {                       // interface: only the contract
    void draw();
}

abstract class Shape implements Drawable { // abstract: part shared, part left open
    String name;
    Shape(String name) { this.name = name; }
    abstract double area();                // child must write this
    void describe() { System.out.println(name + " with area " + area()); }
}

class Square extends Shape {               // concrete: everything filled in
    double side;
    Square(double side) { super("Square"); this.side = side; }
    double area() { return side * side; }
    public void draw() { System.out.println("Drawing a square"); }
}

public class Main {
    public static void main(String[] args) {
        Square s = new Square(3);          // only the concrete class can be created
        s.draw();                          // Drawing a square
        s.describe();                      // Square with area 9.0
        // new Shape("x");                 // error: abstract
        // new Drawable();                 // error: interface
    }
}
```

**Concrete = complete and instantiable; abstract = partly done, shares code, single inheritance; interface = pure contract, constants only, multiple implementation.**

---

## 8. `static` and `final` · Quick

- **`static`** = belongs to the class, shared by all objects (like C++ static). A static method can't use `this` or non-static members. Called as `ClassName.method()`.
- **`final`** = can't change. A `final` variable is a constant, a `final` method can't be overridden, and a `final` class can't be extended (e.g. `String`).

---

## 9. Scenario program · Slow down

> **Endsem 2025 · Q4(c) · 4.5 marks**
> Design a Java program for premium subscribers of a streaming platform. Base class Subscriber has subscriberId (int), name (String), a static platformName (String), a constructor for ID and name, and a static method `setPlatformName(String name)`. PremiumSubscriber extends Subscriber, adds plan (String) and monthlyFee (double), a constructor initialising everything (including inherited fields), and a method to display details of subscribers whose monthlyFee exceeds Rs. 799. In `main()`, set the platform name using the static method, create an array of PremiumSubscriber objects with sample data, and display those with fee > 799.

**Answer.**

What the marker looks for: `static` field + `static` setter called with the **class name**; `super(id, name)` in the child constructor; an array of objects; a loop with the `> 799` check.

```java
class Subscriber {
    protected int subscriberId;
    protected String name;
    protected static String platformName;          // shared by every subscriber

    Subscriber(int subscriberId, String name) {
        this.subscriberId = subscriberId;
        this.name = name;
    }
    static void setPlatformName(String name) {    // static: called without an object
        platformName = name;
    }
}

class PremiumSubscriber extends Subscriber {
    private String plan;
    private double monthlyFee;

    PremiumSubscriber(int id, String name, String plan, double monthlyFee) {
        super(id, name);                           // inherited fields via super
        this.plan = plan;
        this.monthlyFee = monthlyFee;
    }
    void displayIfAbove799() {
        if (monthlyFee > 799)
            System.out.println(platformName + " | ID " + subscriberId + " | " + name
                               + " | " + plan + " | Rs " + monthlyFee);
    }
}

public class Main {
    public static void main(String[] args) {
        Subscriber.setPlatformName("StreamMax");
        PremiumSubscriber[] subs = {
            new PremiumSubscriber(101, "Aman",  "Family 4K", 999),
            new PremiumSubscriber(102, "Sara",  "Mobile",    499),
            new PremiumSubscriber(103, "Kabir", "Ultra HD",  1299),
            new PremiumSubscriber(104, "Zoya",  "Basic",     799)
        };
        System.out.println("Subscribers paying more than Rs 799:");
        for (PremiumSubscriber p : subs) p.displayIfAbove799();
    }
}
```

Output:

```
Subscribers paying more than Rs 799:
StreamMax | ID 101 | Aman | Family 4K | Rs 999.0
StreamMax | ID 103 | Kabir | Ultra HD | Rs 1299.0
```

Zoya pays exactly 799, which is not *more than* 799, so she's correctly left out. That boundary is a nice detail to point out in the exam.

**Static platform name set once through the class, super() for the inherited fields, and a loop printing only fees above 799.**

---

## 10. Quick recap

- Java: one parent class, many interfaces; GC instead of `delete`; methods are virtual by default.
- `this` = current object / other constructor; `super` = parent constructor / parent method / parent field.
- `super(...)` must be the first line of a constructor.
- Parent reference + child object = dynamic binding.
- Abstract class: can't instantiate, can have constructors, fields and normal methods.
- Interface: contract, constants only, `implements`, many allowed, can `extend` other interfaces.
- `static` = shared by the class; `final` = can't change / override / extend.
