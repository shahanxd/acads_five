# RUN: OOP Unit 4, Java Classes, Inheritance and Interfaces

Nov 16, 2026 · @shahan

All of Unit 4, written for someone meeting Java for the first time, with every Java question from the 2021 to 2025 endsems and the Java sessional solved where it belongs.

## How this run works

Read the idea, try the PYQ on paper, then check the answer right under it. Each question sits in a box, and the line you'd circle in the exam is in bold. Allow about 2 hours.

You already know C++ classes, inheritance and virtual functions from Units 1 to 3. Java uses the same ideas with fewer traps, so this run keeps saying "in C++ this was X, in Java it's Y". If a word shows up that you haven't met, it gets explained right there.

**What the paper likes:**

| Shows up in | Topic |
| --- | --- |
| 3 papers | `super` and `this`, with code |
| 4 papers | Abstract class vs interface (sometimes vs concrete class too) |
| 2 papers | "Will this compile? What's the output?" on a small class hierarchy |
| 4 papers | A full program: a base class, a subclass, an array of objects, print the ones matching a condition |
| 2 papers | Define an interface and implement it in two classes |

Papers used: endsems 2021, 2022, 2023 and 2025, plus the Java sessional saved as `OOP/PYQs/Makeup 2024.pdf` (its title says "OOPS Sessional 3").

**Videos:** Kunal Kushwaha's [Java + DSA playlist](https://www.youtube.com/playlist?list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ) has six OOP videos. For this unit watch OOP 1 (classes, objects, constructors), OOP 2 (packages, static), OOP 3 (inheritance, polymorphism) and OOP 5 (abstract classes, interfaces). The slides are in `OOP/Notes/Unit 4 slides.pdf`.

**About the code:** every program here is complete and runs as written. Every program was compiled and run with JDK 21, and every output shown is the real one. The "won't compile" claims in the PYQ answers were checked against the compiler's actual errors.

## Stop 1: Java for someone coming from C++

**How a Java program runs.** You write `Hello.java`. The compiler `javac` turns it into **bytecode** (`Hello.class`), an in-between code that no real CPU understands. A program called the **JVM** (Java Virtual Machine) is installed on every computer, and it reads the bytecode and runs it. Same bytecode, any machine with a JVM: that's Java's "write once, run anywhere".

The smallest Java program:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

- `public class Hello`: everything in Java lives inside a class. A public class must sit in a file with the same name, `Hello.java`.
- `main` is where the program starts, exactly like `main()` in C++.
- `static` means main belongs to the class itself, so the JVM can call it without first making a `Hello` object.
- `String[] args` holds any words typed after the program name on the command line. You can ignore it.
- `System.out.println(...)` prints and then moves to a new line. It's Java's `cout << ... << endl`.

**The big differences from C++:**

|  | C++ | Java |
| --- | --- | --- |
| Functions outside classes | Allowed | Not allowed. Every method is inside a class |
| Where objects live | Stack or heap | Always the heap, made with `new` |
| Pointers | Yes | No. You get **references** instead (below) |
| Freeing memory | You call `delete` | The **garbage collector** does it for you |
| Run-time polymorphism | Only if you write `virtual` | Automatic for every normal method |
| Multiple inheritance of classes | Allowed | Not allowed. Interfaces do that job (Stop 8) |
| Operator overloading, destructors | Yes | No |

**References.** A variable of a class type doesn't hold the object. It holds a **reference**, an arrow pointing at the object on the heap. Think of it as a pointer you can't do arithmetic on and can't `delete`.

```java
Student a = new Student();   // one object, arrow a points at it
Student b = a;               // no copy made: b points at the SAME object
b.name = "Riya";
System.out.println(a.name);  // prints Riya
```

A reference pointing at nothing holds `null`. Calling a method on `null` throws a `NullPointerException`, Java's clean, catchable error instead of a crash.

> **PYQ, Endsem 2023 Q4(c), 6 marks.** List and explain 3 features of Java that make it a *completely* object-oriented language.

**Answer:**

1. **Everything lives inside a class.** Java has no global variables and no free functions. Even `main` is a method of a class. In C++ you can write a whole program without a single class, which is why C++ is called a hybrid language.
2. **One single class hierarchy.** Every class that doesn't extend anything else automatically extends `java.lang.Object`. So every object in every program shares methods such as `toString()` and `equals()`, and an `Object` reference can point at anything.
3. **Objects only through classes and references.** Objects are always created from a class with `new` and reached only through references. There are no pointers, `struct`s or manual `delete`, and the garbage collector manages memory.

A fourth point worth adding: inheritance and run-time polymorphism are built in. Every normal method is dynamically bound without any `virtual` keyword.

```java
class Point {               // no 'extends' written...
    int x = 3, y = 4;
}
class Demo {
    public static void main(String[] args) {
        Object o = new Point();          // ...yet Point IS-A Object
        System.out.println(o.equals(o)); // method inherited from Object: true
    }
}
```

One honest caveat: Java keeps 8 primitive types (`int`, `char`, `double` and so on) that aren't objects, so purists say it's not 100% pure OO. Each one has a wrapper class (`Integer`, `Character`, `Double`), and Java converts between them automatically.

**Answer: classes for everything, a single root class** `Object`**, and objects only through** `new` **and references (plus built-in polymorphism).**

> **PYQ, Endsem 2023 Q4(a)(II), 3 marks.** Explain the terms *dangling pointer error*, *memory leak* and *garbage collection* in Java with code examples.

**Answer:**

**Dangling pointer:** a pointer that still holds the address of memory that has already been freed. Using it reads garbage or crashes. In C++:

```cpp
int* p = new int(5);
delete p;          // memory given back
cout << *p;        // p now dangles: undefined behaviour
```

This **can't happen in Java**. There's no `delete`, and an object is freed only once no reference points to it. So any reference you still hold always points at a live object, or at `null`.

**Memory leak:** memory you no longer need that never gets freed. In C++ it's a `new` without a `delete`. Java's garbage collector frees unreachable objects, but you can still leak by **keeping references you don't need**:

```java
import java.util.ArrayList;

class Cache {
    static ArrayList<int[]> store = new ArrayList<>();

    static void handleRequest() {
        int[] buffer = new int[100000];
        store.add(buffer);   // never removed, so the GC can never free it
    }
}
```

Every call adds 400 KB that stays reachable through `store`, so memory grows until the program dies with `OutOfMemoryError`.

**Garbage collection:** the JVM automatically finds objects that no reference can reach and frees their memory. An object becomes eligible when its reference is set to `null`, when the reference is pointed elsewhere, or when the method that created it ends.

```java
class GCDemo {
    public static void main(String[] args) {
        String s1 = new String("A");
        s1 = null;                  // "A" unreachable -> eligible
        String s2 = new String("B");
        s2 = new String("C");       // "B" unreachable -> eligible
        System.gc();                // only a request; the JVM decides when
    }
}
```

**Answer: Java has no dangling pointers (no** `delete`**), still leaks if you keep useless references, and frees unreachable objects through the garbage collector.**

## Stop 2: Classes, objects and access specifiers

A **class** is a blueprint. It lists the **fields** (the data each object carries, like roll number and name) and the **methods** (what the object can do). An **object** is one real thing built from that blueprint with `new`.

```java
class Student {
    int rollNo;          // fields
    String name;

    void display() {     // method
        System.out.println(rollNo + " - " + name);
    }
}

class StudentDemo {
    public static void main(String[] args) {
        Student s1 = new Student();   // make an object, s1 refers to it
        s1.rollNo = 101;              // the dot reaches inside the object
        s1.name = "Asha";
        s1.display();                 // prints: 101 - Asha
    }
}
```

Two small Java rules that C++ doesn't have:

- **Fields get default values.** Numbers start at 0, `boolean` at `false`, and references at `null`. A C++ field would hold garbage.
- **Local variables don't.** A variable declared inside a method must be given a value before you read it, or the program won't compile.

**Access specifiers** decide who may touch a member. Java has four levels, one more than C++, because of **packages**. A package is a named group of related classes, like a folder (Stop 10).

| Specifier | Same class | Same package | Subclass in another package | Anywhere else |
| --- | --- | --- | --- | --- |
| `private` | Yes | No | No | No |
| *(none)*, called default or package-private | Yes | Yes | No | No |
| `protected` | Yes | Yes | Yes | No |
| `public` | Yes | Yes | Yes | Yes |

Two traps if you think in C++:

- In a C++ class, no keyword means `private`. In Java, no keyword means "anyone in the same package".
- Java's `protected` is wider than C++'s, because it also opens the member to the whole package.

The usual design is **encapsulation**: keep fields `private` and expose small `public` methods. A **getter** returns a field and a **setter** changes it after checking the value. Then no one outside can put the object into a nonsense state.

> **PYQ, Endsem 2021 Q1(c)(i), 3 marks.** Differentiate among private, public and protected members of a class. Give a suitable example illustrating accessibility / non-accessibility of each using a class and an object in C++ / Java.

**Answer:**

|  | private | protected | public |
| --- | --- | --- | --- |
| Inside its own class | Yes | Yes | Yes |
| In a subclass | No | Yes | Yes |
| Through an object, from outside | No | Only from the same package | Yes |
| Typical use | Data you hide | Data meant for subclasses | The class's interface to the world |

```java
class Account {
    private int pin = 1234;          // only Account itself
    protected double balance = 500;  // Account, its subclasses, same package
    public String owner = "Asha";    // everyone

    void show() {                    // inside the class: all three work
        System.out.println(owner + " " + balance + " " + pin);
    }
}

class Savings extends Account {
    void test() {
        System.out.println(owner);    // OK: public
        System.out.println(balance);  // OK: protected, Savings is a subclass
        // System.out.println(pin);   // ERROR: pin has private access in Account
    }
}

class Main {
    public static void main(String[] args) {
        Account a = new Account();
        System.out.println(a.owner);    // OK: public
        System.out.println(a.balance);  // OK only because Main is in the same package
        // System.out.println(a.pin);   // ERROR: private
        a.show();
    }
}
```

Output:

```text
Asha
500.0
Asha 500.0 1234
```

**Answer: private = class only, protected = class + subclasses (+ package in Java), public = everyone.**

> **PYQ, Endsem 2022 Q4(a), 6 marks.** Define a class `Fuel_Monitor` that checks the fuel left in a vehicle after travelling a certain distance. It has an instance variable `tank_capacity` for the initial tank size and `efficiency` for the vehicle's efficiency, and `fuel_in_tank` set to zero. Include a method that returns the tank size and the fuel in the tank, a method `add_fuel` that works out how much fuel can be filled given the fuel already there and the capacity, and a method `drive_distance` that returns how far the vehicle can go on the fuel available. Embed it in a test program with appropriate use of public, private and protected.

**Answer:** An **instance variable** is just a non-static field: each object gets its own copy. Efficiency is taken in km per litre.

```java
class FuelMonitor {
    private double tankCapacity;      // litres; nobody outside may change it
    private double efficiency;        // km per litre
    protected double fuelInTank = 0;  // starts empty; subclasses may read it

    public FuelMonitor(double tankCapacity, double efficiency) {
        this.tankCapacity = tankCapacity;
        this.efficiency = efficiency;
    }

    public double getTankSize()   { return tankCapacity; }
    public double getFuelInTank() { return fuelInTank; }

    // fills only up to the brim; returns how much actually went in
    public double addFuel(double litres) {
        double space = tankCapacity - fuelInTank;
        double added = Math.min(litres, space);
        fuelInTank += added;
        return added;
    }

    // how far we can go on what is in the tank
    public double driveDistance() {
        return fuelInTank * efficiency;
    }

    // actually drive; returns the fuel left afterwards
    public double drive(double km) {
        double needed = km / efficiency;
        if (needed > fuelInTank) {
            System.out.println("Not enough fuel for " + km + " km");
            return fuelInTank;
        }
        fuelInTank -= needed;
        return fuelInTank;
    }
}

class FuelTest {
    public static void main(String[] args) {
        FuelMonitor car = new FuelMonitor(40, 15);   // 40 L tank, 15 km/L
        System.out.println("Tank size: " + car.getTankSize() + " L");
        System.out.println("Added: " + car.addFuel(25) + " L");
        System.out.println("Added: " + car.addFuel(30) + " L");   // only 15 L fits
        System.out.println("Fuel in tank: " + car.getFuelInTank() + " L");
        System.out.println("Can drive: " + car.driveDistance() + " km");
        car.drive(150);                                         // uses 10 L
        System.out.println("Fuel left: " + car.getFuelInTank() + " L");
        // car.tankCapacity = 100;   // ERROR: private
    }
}
```

Output:

```text
Tank size: 40.0 L
Added: 25.0 L
Added: 15.0 L
Fuel in tank: 40.0 L
Can drive: 600.0 km
Fuel left: 30.0 L
```

Why each specifier: capacity and efficiency are `private` because they're fixed facts about the car. `fuelInTank` is `protected` so a subclass, say `TruckMonitor`, can read it. The methods are `public` because they are how the outside world uses the class.

**Answer: private data, a protected fuel level, public get/add/drive methods, and** `addFuel` **adds** `min(asked, capacity - fuel)`**.**

## Stop 3: Constructors and this

A **constructor** is a special method that runs by itself the moment `new` creates an object. Its job is to give the new object its starting values. It has the class's name and **no return type, not even** `void`.

The kinds, all in one class:

- **No-argument constructor:** takes nothing and sets fixed starting values.
- **Parameterized constructor:** takes values, so each object can start differently.
- **Constructor overloading:** several constructors in one class with different parameter lists. Java picks the one whose parameters match what you pass to `new`.

```java
class Rectangle {
    int length, breadth;

    Rectangle() {                 // no-argument
        this(1, 1);               // reuse the 2-argument constructor
    }
    Rectangle(int side) {         // one argument: a square
        this(side, side);
    }
    Rectangle(int length, int breadth) {   // parameterized
        this.length = length;     // field = parameter
        this.breadth = breadth;
    }
    int area() { return length * breadth; }
}

class RectangleDemo {
    public static void main(String[] args) {
        Rectangle r1 = new Rectangle();       // 1 x 1
        Rectangle r2 = new Rectangle(5);      // 5 x 5
        Rectangle r3 = new Rectangle(4, 6);   // 4 x 6
        System.out.println(r1.area() + " " + r2.area() + " " + r3.area());   // 1 25 24
    }
}
```

`this` means "the object this code is running on right now". It has two jobs here.

1. `this.length` **vs** `length`**.** When a parameter has the same name as a field, the plain name means the parameter. `this.length` means the field. Write `length = length;` instead and the parameter gets copied onto itself, so the field silently stays 0.
2. `this(...)` calls another constructor of the same class, so the setup code lives in one place. It must be the **first line** of the constructor.

**The default constructor trap.** If you write no constructor at all, Java quietly adds an empty no-argument one. The moment you write any constructor, that free one is gone. So a class with only `Rectangle(int, int)` makes `new Rectangle()` a compile error. Endsem 2021 tests exactly this (Stop 5).

**Rules to quote:**

- Same name as the class, and no return type.
- Called automatically by `new`. You can't call it like a normal method.
- Not inherited and can't be overridden. A subclass reaches its parent's constructor through `super(...)` (Stop 5).
- Can't be `abstract`, `static` or `final`.
- Java has no destructors, because the garbage collector frees memory. It has no built-in copy constructor either, though you can write one, such as `Rectangle(Rectangle r)`.

## Stop 4: static and final

`static` **= belongs to the class, not to any one object.** A normal field has a separate copy inside every object. A static field has exactly one copy that all objects share, like a notice board in a classroom instead of a notebook per student.

- **Static field:** shared data, such as a counter of how many objects exist. Read it as `ClassName.field`.
- **Static method:** called as `ClassName.method()` with no object. It can't use `this` or plain instance fields, because there's no object for them to belong to. `main` is static for exactly this reason.
- **Static block:** `static { ... }` runs once, when the class is first loaded, and is used for one-time setup.

`final` **= "can't change any more".** What exactly can't change depends on where you put it:

- **Final variable:** gets a value once, then it's a constant. A final field must be set by the end of the constructor.
- **Final method:** subclasses can't override it.
- **Final class:** no class can extend it. `String` is final, so nobody can make a fake `String`.

The two are often used together. `static final double PI = 3.14159;` gives one shared copy that never changes, which is Java's way of writing a constant.

> **PYQ, Java sessional (Makeup 2024 file) Q2(b).** Differentiate between final and static in Java.

**Answer:**

|  | `static` | `final` |
| --- | --- | --- |
| Core meaning | Belongs to the class and is shared | Can't be changed after it's set |
| On a variable | One copy shared by all objects | Assigned once, then a constant |
| On a method | Called without an object, can't use `this` | Can't be overridden by a subclass |
| On a class | Only allowed on nested classes | Can't be extended |
| Memory | Created once, when the class loads | No effect on memory |

```java
class Student {
    static int count = 0;                 // one shared counter
    static final String COLLEGE = "JMI";  // shared constant
    final int rollNo;                     // each student's own, fixed once set
    String name;

    Student(int rollNo, String name) {
        this.rollNo = rollNo;             // a final field is set exactly once
        this.name = name;
        count++;
    }

    static void showCount() {             // no object needed
        System.out.println("Students: " + count);
        // System.out.println(name);      // ERROR: no object, so whose name?
    }

    final void show() {                   // subclasses can't override this
        System.out.println(rollNo + " " + name + " " + COLLEGE);
    }
}

class StaticFinalDemo {
    public static void main(String[] args) {
        Student a = new Student(1, "Asha");
        Student b = new Student(2, "Ravi");
        a.show();
        b.show();
        Student.showCount();
        // a.rollNo = 5;                  // ERROR: cannot assign to final rollNo
    }
}
```

Output:

```text
1 Asha JMI
2 Ravi JMI
Students: 2
```

**Answer: static means one shared copy that belongs to the class; final means it can't change (variable), be overridden (method) or be extended (class).**

## Stop 5: Inheritance and super

**Inheritance** builds a new class on top of an existing one. The new class gets the old one's fields and methods for free and adds its own. The old class is the **superclass** (parent, base) and the new one is the **subclass** (child, derived). Java uses the keyword `extends`.

It models an **IS-A** relationship. A `BedRoom` IS-A `Room`, so a bedroom has everything a room has, plus a height. If the sentence "X is a Y" sounds wrong, inheritance is the wrong tool.

```java
class Room {
    int length, breadth;
    Room(int x, int y) { length = x; breadth = y; }
    int area() { return length * breadth; }
}

class BedRoom extends Room {      // BedRoom IS-A Room
    int height;
    BedRoom(int x, int y, int z) {
        super(x, y);              // let Room set length and breadth
        height = z;
    }
    int volume() { return length * breadth * height; }
}

class InherTest {
    public static void main(String[] args) {
        BedRoom r = new BedRoom(14, 12, 10);
        System.out.println("Area = " + r.area());      // inherited method: 168
        System.out.println("Volume = " + r.volume());  // own method: 1680
    }
}
```

**Types of inheritance in Java:**

| Type | Shape | Allowed with classes? |
| --- | --- | --- |
| Single | B extends A | Yes |
| Multilevel | C extends B, B extends A | Yes |
| Hierarchical | B and C both extend A | Yes |
| Multiple | C extends A **and** B | **No**. Only through interfaces |
| Hybrid | A mix that includes multiple | Only through interfaces |

Why no multiple inheritance? Say A and B both have a `show()` and C extends both. Then `c.show()` is ambiguous. That's the **diamond problem**, which C++ patches with virtual base classes (Unit 3). Java simply bans it for classes. Interfaces (Stop 8) give you the useful part without the ambiguity.

**What the subclass gets:** the public and protected members, plus default ones if it's in the same package. Private fields still exist inside the object, but the subclass can't name them and has to go through the parent's methods. Constructors are **not** inherited.

`super` means "the parent-class part of this object". It has three uses:

1. `super(args)` calls the parent's constructor. It must be the **first line** of the child's constructor.
2. `super.method()` runs the parent's version of a method the child has overridden.
3. `super.field` reaches the parent's field when the child has a field with the same name.

**Constructor chaining.** Making a child object runs the constructors **top-down**: grandparent first, then parent, then child. The house is built from the foundation up. If you don't write `super(...)`, Java silently inserts `super()` with no arguments. If the parent has no no-argument constructor, that's a compile error.

```java
class A { A() { System.out.println("A"); } }
class B extends A { B() { System.out.println("B"); } }   // super() inserted for you
class C extends B { C() { System.out.println("C"); } }
// new C();  prints A, then B, then C
```

> **PYQ, Endsem 2025 Q4(a), 4.5 marks.** Discuss the significance of the `super` keyword in Java briefly. Illustrate its usage in calling parent class constructors and methods.

**Answer:** `super` lets a subclass reuse its parent instead of copying it.

- **Calling the parent's constructor** lets the parent set up its own fields, including private ones the child can't touch.
- **Calling the parent's method** lets the child extend a behaviour rather than replace it.
- **Reaching a hidden field** gets the parent's field when a child field has the same name.

`@Override` in the code below is an **annotation**, a note to the compiler that says "I mean to override a parent method". If you misspell the name, you get an error instead of a silent new method.

```java
class Person {
    String name;
    Person(String name) {
        this.name = name;
        System.out.println("Person constructor");
    }
    void display() {
        System.out.println("Name: " + name);
    }
}

class Student extends Person {
    int rollNo;
    Student(String name, int rollNo) {
        super(name);              // parent constructor, first line
        this.rollNo = rollNo;
        System.out.println("Student constructor");
    }
    @Override
    void display() {
        super.display();          // parent's version first
        System.out.println("Roll no: " + rollNo);
    }
}

class SuperDemo {
    public static void main(String[] args) {
        Student s = new Student("Asha", 101);
        s.display();
    }
}
```

Output:

```text
Person constructor
Student constructor
Name: Asha
Roll no: 101
```

Remove `super(name)` and it no longer compiles. Java would insert `super()`, but `Person` has no no-argument constructor.

**Answer:** `super(...)` **(first line) runs the parent constructor,** `super.method()` **runs the parent's version of an overridden method, and** `super.field` **reaches a hidden parent field.**

> **PYQ, Endsem 2023 Q4(a)(I), 3 marks.** What is the use of `this` and `super` keywords in Java? Illustrate with an example.

**Answer:**

|  | `this` | `super` |
| --- | --- | --- |
| Refers to | The current object | The parent-class part of the current object |
| Field | `this.x`: own field, when a parameter is also called x | `super.x`: parent's field, when hidden by a child field |
| Method | `this.m()`: own method | `super.m()`: parent's version of an overridden method |
| Constructor | `this(...)`: another constructor of the same class | `super(...)`: the parent's constructor |

Both `this(...)` and `super(...)` must be the first line, so a constructor can use only one of them. Neither works inside a static method, since there's no current object there.

```java
class Animal {
    String sound = "...";
    Animal() { System.out.println("Animal created"); }
}

class Dog extends Animal {
    String sound = "Woof";        // hides Animal's sound
    String name;

    Dog() { this("Tommy"); }      // this(): the other Dog constructor
    Dog(String name) {
        super();                  // super(): Animal's constructor
        this.name = name;         // this.name: the field, not the parameter
    }
    void show() {
        System.out.println(name + " says " + this.sound + ", parent field: " + super.sound);
    }
}

class ThisSuperDemo {
    public static void main(String[] args) {
        new Dog().show();
    }
}
```

Output:

```text
Animal created
Tommy says Woof, parent field: ...
```

**Answer:** `this` **points to the current object (own field, method or constructor);** `super` **points to its parent part (parent's field, method or constructor).**

> **PYQ, Endsem 2021 Q4(b), 6 marks.** Show the use of the following keywords of Java with example code snippets: (i) super (ii) static (iii) final.

**Answer:**

- **super:** calls the parent's constructor, method or field (above).
- **static:** a member that belongs to the class and is shared by all objects (Stop 4).
- **final:** a constant variable, a method that can't be overridden, or a class that can't be extended (Stop 4).

One program shows all three:

```java
class Shape {
    static int count = 0;            // static: one counter for all shapes
    final double PI = 3.14159;       // final variable: a constant
    String name;

    Shape(String name) { this.name = name; count++; }

    final void id() {                // final method: can't be overridden
        System.out.println("Shape #" + count);
    }
}

class Circle extends Shape {
    double r;
    Circle(double r) {
        super("circle");             // super: parent constructor
        this.r = r;
    }
    double area() { return PI * r * r; }
}

final class Util {                   // final class: can't be extended
    static int square(int x) { return x * x; }   // static method
}

class KeywordDemo {
    public static void main(String[] args) {
        Circle c = new Circle(2);
        System.out.println(c.name + " " + c.area());
        c.id();
        System.out.println(Util.square(5));
        System.out.println(Shape.count);
        // c.PI = 3;                 // ERROR: final
        // class MyUtil extends Util {}   // ERROR: Util is final
    }
}
```

Output:

```text
circle 12.56636
Shape #1
25
1
```

**Answer: super reaches the parent, static means shared by the class, and final means fixed (constant variable, non-overridable method, non-extendable class).**

> **PYQ, Endsem 2021 Q4(c), 6 marks.** Use these classes. Justify your answers.

```java
public class Vehicle {
    public int numOfWheels;
    public Vehicle(int x) { numOfWheels = x; }
    public void drive() { System.out.println("Driving a vehicle"); }
}
public class Car extends Vehicle {
    public int numOfDoors;
    public Car(int d, int w) {
        numOfDoors = d;
        super(w);
    }
    public void drive() { System.out.println("Driving a car"); }
}
```

> (i) The Car class does not compile. Why? How can it be corrected? (ii) Assume it's corrected. Output of `Car audi = new Car(); Car.drive();`? (iii) Output of `Car porsche = new Car(2, 4); porsche.drive();`? (iv) Output of `Vehicle v = new Vehicle(18); v.drive(); v.numOfDoors = 2;`?

**Answer:**

**(i)** `super(w)` is not the first statement of the constructor, and Java demands it there. There's a second problem underneath: with no `super(...)` on the first line, Java inserts `super()`, but `Vehicle` only has `Vehicle(int)`. The fix is to move the call up:

```java
public Car(int d, int w) {
    super(w);          // first line now
    numOfDoors = d;
}
```

A bonus line for the curious: Java 25 added "flexible constructor bodies", which allow a field assignment like `numOfDoors = d;` before `super(w)`, so the original Car would compile there. Exams assume classic Java (8 to 21), where `super(...)` must come first, so answer as above.

**(ii) Neither line compiles, so there's no output.**

- `new Car()`: Car declares only `Car(int, int)`, so Java gives it no free no-argument constructor.
- `Car.drive()`: `drive` is an instance method, so it needs an object. Calling it through the class name gives "non-static method drive() cannot be referenced from a static context".
- If you add `Car() { super(4); numOfDoors = 4; }` and call `audi.drive()`, it prints `Driving a car`.

**(iii)** `porsche` gets 2 doors and 4 wheels, and Car's own `drive()` runs. Output: `Driving a car`.

**(iv)** `v.drive()` would print `Driving a vehicle`. But `v.numOfDoors = 2;` is a **compile error**, because `Vehicle` has no field `numOfDoors`. A parent knows nothing about its child's fields. Since one line fails, the program doesn't run at all. Delete that line and it prints `Driving a vehicle`.

**Answer: (i)** `super(w)` **must come first; (ii) compile errors (no** `Car()`**, and** `drive` **isn't static); (iii)** `Driving a car`**; (iv) compile error on** `numOfDoors`**, otherwise** `Driving a vehicle`**.**

> **PYQ, Java sessional (Makeup 2024 file) Q1.** Write a Java program to create a class `Product` with product id and name. Extend it to a subclass with `category` and `monthly_sales`. Implement (a) appropriate constructors, (b) a method to find and display the products with monthly sales greater than 100 units, (c) a main method that creates an array to store product details and demonstrates the functionality.

**Answer:** `SalesProduct[] items = { ... }` makes an **array of references**, one arrow per product. `for (SalesProduct p : items)` is the **for-each loop**, read as "for each p in items".

```java
class Product {
    protected int productId;
    protected String name;

    Product(int productId, String name) {
        this.productId = productId;
        this.name = name;
    }
}

class SalesProduct extends Product {
    private String category;
    private int monthlySales;

    SalesProduct(int productId, String name, String category, int monthlySales) {
        super(productId, name);          // Product sets id and name
        this.category = category;
        this.monthlySales = monthlySales;
    }

    void displayIfBestSeller() {
        if (monthlySales > 100) {
            System.out.println(productId + " | " + name + " | " + category + " | " + monthlySales);
        }
    }
}

class ProductDemo {
    public static void main(String[] args) {
        SalesProduct[] items = {
            new SalesProduct(1, "Notebook", "Stationery", 250),
            new SalesProduct(2, "Desk Lamp", "Electronics", 80),
            new SalesProduct(3, "Pen Pack", "Stationery", 140),
            new SalesProduct(4, "Headphones", "Electronics", 95)
        };
        System.out.println("Products selling more than 100 units a month:");
        for (SalesProduct p : items) {
            p.displayIfBestSeller();
        }
    }
}
```

Output:

```text
Products selling more than 100 units a month:
1 | Notebook | Stationery | 250
3 | Pen Pack | Stationery | 140
```

**Answer: subclass constructor passes id and name up with** `super(...)`**; the filter method prints only items with** `monthlySales > 100`**.**

> **PYQ, Endsem 2025 Q4(c), 4.5 marks.** Design a Java program for premium subscribers of a streaming platform. Base class `Subscriber` has `subscriberId` (int), `name` (String), a static data member `platformName`, a constructor for ID and name, and a static method `setPlatformName(String name)`. Derived class `PremiumSubscriber` adds `plan` (String) and `monthlyFee` (double), a constructor for all attributes, and a method to display subscribers whose `monthlyFee` exceeds Rs. 799. In `main`, set the platform name with the static method, create an array of `PremiumSubscriber` objects, and display those paying more than Rs. 799.

**Answer:** `platformName` is static because the platform is the same for every subscriber, so it's stored once and set once through the class.

```java
class Subscriber {
    protected int subscriberId;
    protected String name;
    static String platformName;              // one copy for everyone

    Subscriber(int subscriberId, String name) {
        this.subscriberId = subscriberId;
        this.name = name;
    }

    static void setPlatformName(String platform) {
        platformName = platform;
    }
}

class PremiumSubscriber extends Subscriber {
    private String plan;
    private double monthlyFee;

    PremiumSubscriber(int subscriberId, String name, String plan, double monthlyFee) {
        super(subscriberId, name);           // parent sets id and name
        this.plan = plan;
        this.monthlyFee = monthlyFee;
    }

    void displayIfAbove799() {
        if (monthlyFee > 799) {
            System.out.println(platformName + " | " + subscriberId + " | " + name
                               + " | " + plan + " | Rs. " + monthlyFee);
        }
    }
}

class StreamingDemo {
    public static void main(String[] args) {
        Subscriber.setPlatformName("StreamMax");   // static: called on the class
        PremiumSubscriber[] subs = {
            new PremiumSubscriber(101, "Aman", "Family", 999.0),
            new PremiumSubscriber(102, "Sara", "Mobile", 499.0),
            new PremiumSubscriber(103, "Kabir", "4K Ultra", 1299.0),
            new PremiumSubscriber(104, "Meera", "Standard", 799.0)
        };
        System.out.println("Subscribers paying more than Rs. 799:");
        for (PremiumSubscriber s : subs) {
            s.displayIfAbove799();
        }
    }
}
```

Output:

```text
Subscribers paying more than Rs. 799:
StreamMax | 101 | Aman | Family | Rs. 999.0
StreamMax | 103 | Kabir | 4K Ultra | Rs. 1299.0
```

Meera pays exactly 799, which doesn't *exceed* 799, so she's left out. Graders like seeing a boundary case handled.

**Answer: a static** `platformName` **set once through** `Subscriber.setPlatformName`**,** `super(id, name)` **in the subclass constructor, and a filter on** `monthlyFee > 799`**.**

## Stop 6: Overriding, overloading and dynamic binding

**Polymorphism** means "many forms": one method name, different behaviour depending on the situation. Java has two kinds.

- **Compile-time polymorphism = method overloading.** One class has several methods with the same name but different parameter lists, such as `add(int, int)` and `add(double, double)`. The compiler looks at the arguments and picks one before the program ever runs. A different return type alone doesn't count as overloading.
- **Run-time polymorphism = method overriding.** A subclass writes its own version of a method it inherited, with the same name and the same parameters. Which version runs is decided while the program runs.

**Overriding rules** (straight from the slides, examiners love these):

1. Same name and same parameter types. The return type is the same, or a **covariant** type, meaning a subclass of the original return type.
2. Access can't get stricter. A `public` method can't be overridden as `private`.
3. A `final` method can't be overridden.
4. A `private` method isn't inherited, so it can't be overridden.
5. A `static` method is **hidden**, not overridden: the reference type decides which one runs, not the object.
6. Different parameters make it overloading, not overriding.
7. The child can still call the parent's version with `super.method()`.

**Upcasting.** A parent-type reference may point at a child object, because a Circle IS-A Shape: `Shape s = new Circle(2);`

**Dynamic binding** (also called late binding or **dynamic method dispatch**): when you call an overridden method through such a reference, Java looks at the **actual object** at run time and runs that object's version. Remember the split:

- The **reference type** decides what you're *allowed* to call. The compiler checks this.
- The **object type** decides *which version* runs. The JVM decides this.

In C++ you only got this if you wrote `virtual`. In Java every normal instance method behaves this way automatically.

```java
class Shape {
    double area() { return 0.0; }
}
class Rectangle extends Shape {
    double l, b;
    Rectangle(double l, double b) { this.l = l; this.b = b; }
    @Override double area() { return l * b; }
}
class Circle extends Shape {
    double r;
    Circle(double r) { this.r = r; }
    @Override double area() { return Math.PI * r * r; }
}

class DispatchDemo {
    public static void main(String[] args) {
        Shape s;                  // one parent reference...
        s = new Rectangle(4, 5);
        System.out.println(s.area());   // ...Rectangle's area runs: 20.0
        s = new Circle(2);
        System.out.println(s.area());   // ...now Circle's: 12.566370614359172
    }
}
```

Same line, `s.area()`, two different methods. That's the whole point.

> **PYQ, Endsem 2021 Q3(b), 6 marks.** Differentiate between method overriding and method overloading with the help of a suitable program in C++ / Java.

**Answer:**

|  | Overloading | Overriding |
| --- | --- | --- |
| Where | Within one class | Between a parent and a child class |
| Name and parameters | Same name, **different** parameters | Same name, **same** parameters |
| Return type | May differ (but that alone isn't enough) | Same, or covariant |
| Decided at | Compile time (static binding) | Run time (dynamic binding) |
| Kind of polymorphism | Compile-time | Run-time |
| Inheritance needed | No | Yes |
| static, final, private methods | Can be overloaded | Can't be overridden |

```java
class Calculator {
    int add(int a, int b)          { return a + b; }       // overloading:
    double add(double a, double b) { return a + b; }       // same name,
    int add(int a, int b, int c)   { return a + b + c; }   // different parameters
}

class Animal {
    void sound() { System.out.println("Some sound"); }
}
class Dog extends Animal {
    @Override
    void sound() { System.out.println("Bark"); }           // overriding: same signature
}

class PolyDemo {
    public static void main(String[] args) {
        Calculator c = new Calculator();
        System.out.println(c.add(2, 3));       // picked at compile time
        System.out.println(c.add(2.5, 1.5));
        System.out.println(c.add(1, 2, 3));

        Animal a = new Dog();                  // parent reference, child object
        a.sound();                             // picked at run time
    }
}
```

Output:

```text
5
4.0
6
Bark
```

**Answer: overloading = same name, different parameters, one class, resolved at compile time; overriding = same signature in a subclass, resolved at run time on the actual object.**

> **PYQ, Endsem 2023 Q3(c)(I), 2 marks.** Differentiate between late (or dynamic) binding and early (or static) binding, giving at least two differences.

**Answer:** **Binding** means connecting a method call in your code to the actual method body that will run.

|  | Early (static) binding | Late (dynamic) binding |
| --- | --- | --- |
| When | Compile time | Run time |
| Decided by | Type of the reference | Type of the actual object |
| Used for | Overloaded, static, private and final methods (non-virtual in C++) | Overridden methods (virtual in C++) |
| Speed | Faster, no lookup | Slightly slower, needs a lookup at run time |
| Gives you | Compile-time polymorphism | Run-time polymorphism |

In `Shape s = new Circle(2); s.area();`, the compiler can't know which `area()` to use, since `s` might hold any shape. So it's bound late, to `Circle.area()`.

**Answer: early binding is fixed at compile time from the reference type; late binding is chosen at run time from the actual object.**

## Stop 7: Abstract classes and methods

Some classes describe an idea that is too general to exist on its own. You never draw "a shape". You draw a circle or a rectangle. Java models this with `abstract`.

- An **abstract class** is marked `abstract` and **can't be turned into objects** (`new Shape()` is an error). It exists only to be inherited.
- An **abstract method** has no body, just a signature ending in `;`. It's a promise that every real subclass will write this method.
- A **concrete method** is a normal method with a body, and a **concrete class** is a normal class you *can* make objects of.

In C++ terms, an abstract method is a pure virtual function (`virtual double area() = 0;`), and an abstract class is any class with at least one of them. Java just uses a keyword.

**Rules:**

1. A class with even one abstract method must itself be declared `abstract`.
2. An abstract class may still have fields, constructors, concrete methods and static methods. It may even have zero abstract methods.
3. You can't create its objects, but you **can** have its references: `Shape s = new Circle(2);`
4. A subclass must implement every inherited abstract method, or be declared abstract itself.
5. An abstract method can't be `private`, `static` or `final`, since each of those blocks overriding. Constructors can't be abstract.
6. Its constructor still runs, called through `super(...)` when a subclass object is built.

```java
abstract class Shape {
    abstract double area();          // abstract: no body
    void describe() {                // concrete: has a body
        System.out.println("Every shape has an area calculation.");
    }
}

class Rectangle extends Shape {
    private double length, breadth;
    Rectangle(double length, double breadth) { this.length = length; this.breadth = breadth; }
    @Override double area() { return length * breadth; }
}

class Circle extends Shape {
    private double radius;
    Circle(double radius) { this.radius = radius; }
    @Override double area() { return Math.PI * radius * radius; }
}

class ShapeDemo {
    public static void main(String[] args) {
        Shape s = new Rectangle(4, 3);   // abstract reference, concrete object
        System.out.println(s.area());    // 12.0
        s = new Circle(2);
        System.out.println(s.area());    // 12.566370614359172
        s.describe();                    // inherited concrete method
        // Shape x = new Shape();        // ERROR: Shape is abstract
    }
}
```

> **PYQ, Endsem 2021 Q4(a), 6 marks.** What is the only effect that the `abstract` keyword has on a class? What are the two main effects of declaring a method abstract? Then use these classes and justify your answers:

```java
public abstract class Mammal {
    public void breathe() { System.out.println("Mammal is breathing"); }
    public abstract void nurse();
}
public class Cat extends Mammal {
    public void breathe() { System.out.println("Cat is breathing"); }
    public void nurse(int t) { System.out.println("Cat is nursing"); }
}
public class Whale extends Mammal {
    public void breathe() {
        System.out.println("Whale is breathing");
        super.breathe();
    }
    public void nurse() { System.out.println("Whale is nursing"); }
}
```

> (i) The Whale class compiles fine, but Cat does not. Why not? How can it be fixed? (ii) Is `Mammal m = new Whale();` valid? (iii) What is the output of `Whale w = new Whale(); w.breathe(); w.nurse(); Mammal m = w; m.breathe(); m.nurse();`?

**Answer:**

**Effect on a class:** its only effect is that the class **can't be instantiated**, so `new Mammal()` is illegal. Everything else (fields, constructors, concrete methods) works as usual.

**Effects on a method:**

1. It has **no body**, just a declaration. The implementation is left to subclasses.
2. It **forces the class to be abstract**, and forces every concrete subclass to override it.

**(i)** Cat's `nurse(int t)` takes a parameter, so it's an **overload**, not an override of `nurse()`. Cat still inherits the abstract `nurse()` with no body, yet Cat isn't marked abstract, so it doesn't compile. Whale's `nurse()` matches exactly, so Whale is fine. Fix it either way:

```java
public void nurse() { System.out.println("Cat is nursing"); }   // add a real override
// or: declare Cat itself abstract
```

**(ii) Yes, it's valid.** You can't create a `Mammal` object, but a `Mammal` reference may point to any concrete subclass object. A Whale IS-A Mammal, so this is upcasting.

**(iii)** `w` and `m` point at the same Whale object. Dynamic binding runs Whale's versions both times, and `super.breathe()` adds Mammal's line.

```text
Whale is breathing
Mammal is breathing
Whale is nursing
Whale is breathing
Mammal is breathing
Whale is nursing
```

`m.nurse()` compiles because `Mammal` declares `nurse()`. At run time it executes Whale's body.

**Answer: abstract class = can't be instantiated; abstract method = no body + must be overridden (forcing an abstract class). Cat fails because** `nurse(int)` **overloads instead of overriding. The upcast is valid. Output is the 6 lines above.**

> **PYQ, Java sessional (Makeup 2024 file) Q3.** A company pays its employees weekly. There are 4 types: Salaried (fixed salary regardless of hours), Hourly (paid by the hour, with 1.5x pay for every hour beyond 40 in a week), Commissioned (a percentage of their sales), and Base + Commission (a subclass of Commissioned: base salary plus commission). Write a Java program that calculates the salaries.

**Answer:** Every employee has earnings, but each type computes them differently. That's a textbook abstract method: `Employee` declares `earnings()` and each subclass fills it in.

The class tree:

```text
Employee (abstract)
├── SalariedEmployee
├── HourlyEmployee
└── CommissionEmployee
    └── BasePlusCommissionEmployee
```

`printf` prints formatted text: `%s` is filled with a string, `%.2f` with a number rounded to 2 decimals, and `%n` is a newline.

```java
abstract class Employee {
    protected String name;
    Employee(String name) { this.name = name; }
    abstract double earnings();      // each type pays differently
    abstract String type();
}

class SalariedEmployee extends Employee {
    private double weeklySalary;
    SalariedEmployee(String name, double weeklySalary) {
        super(name);
        this.weeklySalary = weeklySalary;
    }
    double earnings() { return weeklySalary; }   // hours don't matter
    String type() { return "Salaried"; }
}

class HourlyEmployee extends Employee {
    private double wage, hours;
    HourlyEmployee(String name, double wage, double hours) {
        super(name);
        this.wage = wage;
        this.hours = hours;
    }
    double earnings() {
        if (hours <= 40) return wage * hours;
        return 40 * wage + (hours - 40) * wage * 1.5;   // overtime at 1.5x
    }
    String type() { return "Hourly"; }
}

class CommissionEmployee extends Employee {
    private double grossSales, rate;
    CommissionEmployee(String name, double grossSales, double rate) {
        super(name);
        this.grossSales = grossSales;
        this.rate = rate;
    }
    double earnings() { return rate * grossSales; }
    String type() { return "Commission"; }
}

class BasePlusCommissionEmployee extends CommissionEmployee {
    private double baseSalary;
    BasePlusCommissionEmployee(String name, double grossSales, double rate, double baseSalary) {
        super(name, grossSales, rate);
        this.baseSalary = baseSalary;
    }
    @Override
    double earnings() { return baseSalary + super.earnings(); }   // base + commission
    @Override
    String type() { return "Base + Commission"; }
}

class Payroll {
    public static void main(String[] args) {
        Employee[] staff = {
            new SalariedEmployee("Riya", 800),
            new HourlyEmployee("Arjun", 20, 50),       // 10 hours of overtime
            new HourlyEmployee("Sam", 15, 30),         // no overtime
            new CommissionEmployee("Neha", 10000, 0.06),
            new BasePlusCommissionEmployee("Vikram", 5000, 0.04, 300)
        };
        double total = 0;
        for (Employee e : staff) {                     // dynamic binding picks each earnings()
            System.out.printf("%s (%s): Rs. %.2f%n", e.name, e.type(), e.earnings());
            total += e.earnings();
        }
        System.out.printf("Total weekly payroll: Rs. %.2f%n", total);
    }
}
```

Output:

```text
Riya (Salaried): Rs. 800.00
Arjun (Hourly): Rs. 1100.00
Sam (Hourly): Rs. 450.00
Neha (Commission): Rs. 600.00
Vikram (Base + Commission): Rs. 500.00
Total weekly payroll: Rs. 3450.00
```

Check Arjun by hand: 40 x 20 = 800, plus 10 x 20 x 1.5 = 300, total 1100. Vikram: 0.04 x 5000 = 200, plus 300 base, total 500.

**Answer: an abstract** `Employee` **with abstract** `earnings()`**, four concrete pay rules (base + commission reuses** `super.earnings()`**), and one loop over** `Employee[]` **that dynamic binding sorts out.**

## Stop 8: Interfaces

An **interface** is a list of methods that a class promises to provide, with no say in *how*. Think of it as a job description: it lists what the job needs ("must be able to `print()`") and each class that takes the job decides how to do it. The interface says **what**, and the implementing class says **how**.

```java
interface Student {
    int MAX_MARKS = 100;     // a constant: automatically public static final
    void study();            // automatically public abstract
    void attendClass();
}
```

**What can go inside an interface:**

- **Methods without a body.** These are automatically `public abstract`, so you don't write those words.
- **Fields**, which are automatically `public static final`, meaning constants. They must get a value right where they're declared.
- From Java 8: `default` **methods** (with a body, which implementing classes inherit unless they override) and `static` **methods**. From Java 9: private helper methods.
- **Not allowed:** constructors, normal instance fields, or `new Student()`.

A top-level interface is either `public` (usable from any package, and it must live in its own file) or has no keyword (usable only inside its package).

**Implementing.** A class signs the contract with `implements` and must write every method. It must declare each one `public`, because the interface method is public and an override can't lower its access. Skip one, and the class must be declared abstract.

```java
interface Callback {
    void callback(int param);
}

class Client implements Callback {
    public void callback(int p) {                 // public is required
        System.out.println("callback called with " + p);
    }
}

class AnotherClient implements Callback {
    public void callback(int p) {
        System.out.println("Another version of callback");
        System.out.println("p squared is " + (p * p));
    }
}

class TestIface {
    public static void main(String[] args) {
        Callback c = new Client();      // interface reference
        c.callback(42);
        c = new AnotherClient();        // same reference, different class
        c.callback(42);
    }
}
```

Output:

```text
callback called with 42
Another version of callback
p squared is 1764
```

**Accessing implementations through interface references.** That's the `Callback c` above. A variable of interface type can point at an object of *any* class that implements it, and dynamic dispatch runs that object's method. Code written against `Callback` works with classes that don't even exist yet.

**Multiple inheritance, the Java way.** A class may extend only one class but implement any number of interfaces:

```java
class Duck extends Bird implements Flyable, Swimmable { ... }
```

There's no diamond problem here. Interfaces carry no object state, and an abstract method has no body to clash with. If two interfaces both list `move()`, the class writes one `move()` and it satisfies both.

**Extending interfaces.** One interface can inherit another with `extends`, and an interface may extend several at once (`interface C extends A, B`). A class that implements the child must write the methods of the whole chain.

```java
interface Student { void study(); void attendClass(); }
interface Teacher extends Student { void teach(); }   // gets study and attendClass too

class SchoolTeacher implements Teacher {
    public void study()       { System.out.println("Student studies."); }
    public void attendClass() { System.out.println("Student attends class."); }
    public void teach()       { System.out.println("Teacher teaches students."); }
}
```

**Keyword cheat line:** class to class is `extends`, interface to interface is `extends`, and class to interface is `implements`.

> **PYQ, Endsem 2022 Q4(c), 6 marks.** Define an interface in Java that contains a method to calculate the perimeter of an object. Define two classes `Circle` and `Rectangle` with suitable fields and methods. Implement the interface `perimeter` in these classes. Write an appropriate `main()` to create an object of each class and test all the methods.

**Answer:**

```java
interface Perimeter {
    double perimeter();                      // public abstract, automatically
}

class Circle implements Perimeter {
    private double radius;
    Circle(double radius) { this.radius = radius; }
    double getRadius() { return radius; }
    public double perimeter() { return 2 * Math.PI * radius; }
}

class Rectangle implements Perimeter {
    private double length, width;
    Rectangle(double length, double width) { this.length = length; this.width = width; }
    double area() { return length * width; }
    public double perimeter() { return 2 * (length + width); }
}

class PerimeterTest {
    public static void main(String[] args) {
        Circle c = new Circle(7);
        Rectangle r = new Rectangle(4, 5);
        System.out.printf("Circle radius %.1f, perimeter %.2f%n", c.getRadius(), c.perimeter());
        System.out.printf("Rectangle area %.1f, perimeter %.2f%n", r.area(), r.perimeter());

        Perimeter[] shapes = { c, r };       // interface references
        for (Perimeter p : shapes)
            System.out.printf("%.2f%n", p.perimeter());
    }
}
```

Output:

```text
Circle radius 7.0, perimeter 43.98
Rectangle area 20.0, perimeter 18.00
43.98
18.00
```

Check: 2 x 3.14159 x 7 = 43.98 and 2 x (4 + 5) = 18.

**Answer:** `interface Perimeter { double perimeter(); }`**, implemented as** `public` **methods in** `Circle` **(2πr) and** `Rectangle` **(2(l + w)), and called through** `Perimeter` **references.**

> **PYQ, Endsem 2023 Q4(b), 6 marks.** Define a public interface `Crushable` with a single function `crush`. Define a public class `Circle` with attribute `radius` that implements `Crushable`. `crush` should return an array of 4 `Circle` objects of random radius such that the total area equals the area of the original circle. (Hints: `Circle circleArray[] = new Circle[Array_Length];` `import java.util.Random;` `int rand_int1 = rand.nextInt(10);` gives an integer from 0 to 9.)

**Answer:** Area grows with the *square* of the radius, so you can't just split the radius into 4 random parts. Split the **area** instead. Draw 4 random weights, give piece *i* the share wᵢ/S of the area (S = sum of weights), then work back to its radius:

```latex
\begin{aligned}
A_i &= \pi r^2 \cdot \frac{w_i}{S} \\
\pi r_i^2 &= \pi r^2 \cdot \frac{w_i}{S} \\
r_i &= r\sqrt{\frac{w_i}{S}}
\end{aligned}
```

The shares add up to 1, so the pieces add up to the original area:

```latex
\sum_{i=1}^{4} A_i = \pi r^2 \cdot \frac{w_1 + w_2 + w_3 + w_4}{S} = \pi r^2
```

The weights use `nextInt(10) + 1` (1 to 10), because a weight of 0 would make a circle of radius 0. A public type must live in a file of its own name, hence two files.

```java
// File: Crushable.java
public interface Crushable {
    Circle[] crush();
}
```

```java
// File: Circle.java
import java.util.Random;

public class Circle implements Crushable {
    private double radius;

    public Circle(double radius) { this.radius = radius; }
    public double getRadius() { return radius; }
    public double area() { return Math.PI * radius * radius; }

    public Circle[] crush() {
        Random rand = new Random();
        int[] w = new int[4];
        int sum = 0;
        for (int i = 0; i < 4; i++) {
            w[i] = rand.nextInt(10) + 1;          // random weight 1..10
            sum += w[i];
        }
        Circle[] circleArray = new Circle[4];
        for (int i = 0; i < 4; i++) {
            circleArray[i] = new Circle(radius * Math.sqrt((double) w[i] / sum));
        }
        return circleArray;
    }

    public static void main(String[] args) {
        Circle big = new Circle(10);
        double total = 0;
        for (Circle c : big.crush()) {
            System.out.printf("radius %.4f, area %.4f%n", c.getRadius(), c.area());
            total += c.area();
        }
        System.out.printf("Sum of pieces: %.4f%n", total);
        System.out.printf("Original area: %.4f%n", big.area());
    }
}
```

`(double) w[i] / sum` turns the weight into a decimal first. Without it, `3 / 20` is integer division and gives 0.

One possible run (the radii change every time, the totals never do). Here the weights came out 3, 7, 1 and 9:

```text
radius 3.8730, area 47.1239
radius 5.9161, area 109.9557
radius 2.2361, area 15.7080
radius 6.7082, area 141.3717
Sum of pieces: 314.1593
Original area: 314.1593
```

**Answer: split the area by random weights and set each radius to r√(wᵢ/S); the 4 areas then always sum to πr².**

## Stop 9: Abstract class vs interface vs concrete class

The one picture to keep in your head:

- A **concrete class** is a finished product. Every method has a body, so you can make objects of it.
- An **abstract class** is a half-built house. The shared walls are up (fields, constructor, common methods) and some rooms are left for each owner to finish. It's for a *family* of related classes.
- An **interface** is a certificate such as "can fly" or "can be printed". It holds no walls at all, just the promise, and any class from any family can earn it, even several at once.

> **PYQ, Endsem 2025 Q4(b), 4.5 marks.** Differentiate between abstract class, interface and concrete class with example code snippets in Java.

**Answer:**

|  | Concrete class | Abstract class | Interface |
| --- | --- | --- | --- |
| Declared as | `class A` | `abstract class A` | `interface A` |
| Objects with `new` | Yes | No | No |
| Abstract methods | None allowed | Zero or more | Every plain method (plus `default` and `static` ones since Java 8) |
| Fields | Any | Any | Only `public static final` constants |
| Constructors | Yes | Yes, run through `super(...)` | No |
| How it's inherited | `extends`, one parent class | `extends`, one parent class | A class `implements` many; an interface `extends` many |
| Method access | Any | Any (abstract ones not private) | `public` |
| Use it for | A complete, usable type | A common base with shared code and state | A capability shared across unrelated classes |

All three in one program:

```java
interface Drawable {                         // interface: just the promise
    void draw();
}

abstract class Shape implements Drawable {   // abstract: shared state + code
    protected String color;
    Shape(String color) { this.color = color; }
    abstract double area();                  // left for subclasses
    void info() { System.out.println(color + " shape, area " + area()); }
}

class Square extends Shape {                 // concrete: everything filled in
    private double side;
    Square(String color, double side) { super(color); this.side = side; }
    double area() { return side * side; }
    public void draw() { System.out.println("Drawing a " + color + " square"); }
}

class Demo {
    public static void main(String[] args) {
        Square sq = new Square("red", 3);    // only the concrete class can be created
        sq.draw();
        sq.info();
        Drawable d = sq;                     // interface reference: fine
        Shape s = sq;                        // abstract-class reference: fine
        // new Shape("blue");  new Drawable();   // both ERRORS
    }
}
```

Output:

```text
Drawing a red square
red shape, area 9.0
```

`Shape` claims to implement `Drawable` without writing `draw()`. That's allowed only because `Shape` is abstract, so the job passes down to `Square`.

**Answer: concrete = complete and instantiable; abstract = partial (state + some abstract methods), not instantiable, single inheritance; interface = pure contract of public methods and constants, many per class.**

> **PYQ, Java sessional (Makeup 2024 file) Q2(a).** Differentiate between abstract class and interface.

**Answer:**

| Feature | Abstract class | Interface |
| --- | --- | --- |
| Main purpose | Common base with partial implementation | Contract the class must follow |
| Keyword to use it | `extends` | `implements` (interfaces `extends` each other) |
| Methods | Abstract and concrete | Abstract by default; `default` and `static` since Java 8 |
| Variables | Instance variables, any access | Only `public static final` constants |
| Constructors | Yes | No |
| Multiple inheritance | A class extends only one | A class implements many |
| Access modifiers | Any (subject to overriding rules) | Methods implicitly `public` |
| Best for | Closely related classes sharing state | Unrelated classes sharing a capability |
| Example | `abstract class Shape { abstract double area(); }` | `interface Printable { void print(); }` |

**Answer: an abstract class shares code and state with one family through** `extends`**; an interface fixes a public contract that any number of classes can** `implements`**.**

> **PYQ, Endsem 2022 Q4(b)(ii), 3 marks.** Discuss the criteria for applying the concept of interface and abstract class in Java. Take an appropriate programming example to support your criteria.

**Answer:**

**Use an abstract class when:**

- the classes are closely related (a true IS-A family) and share fields or code;
- you need a constructor, non-public members, or fields that change per object;
- you want to ship common behaviour once and let subclasses fill in only the parts that differ.

**Use an interface when:**

- unrelated classes should share one capability (like `Comparable`, `Runnable`, `Printable`);
- a class needs to be several types at once, which is the only multiple inheritance Java allows;
- you want to fix *what* must be done and leave *how* entirely to each class.

Example: every vehicle has a registration number and fuel and refuels the same way. That's shared state and code, so it's an abstract class. Being trackable on a map applies to cars and to phones, which are unrelated, so it's an interface.

```java
abstract class Vehicle {
    protected String regNo;
    protected double fuel;
    Vehicle(String regNo) { this.regNo = regNo; }
    void refuel(double litres) { fuel += litres; }   // shared code
    abstract int wheels();                           // differs per vehicle
}

interface Trackable {
    String location();
}

class Car extends Vehicle implements Trackable {
    Car(String regNo) { super(regNo); }
    int wheels() { return 4; }
    public String location() { return "Car " + regNo + " at Okhla"; }
}

class Phone implements Trackable {                 // not a vehicle, still trackable
    public String location() { return "Phone at Jamia Nagar"; }
}

class Fleet {
    public static void main(String[] args) {
        Car c = new Car("DL3C1234");
        c.refuel(20);
        System.out.println(c.regNo + ": " + c.wheels() + " wheels, " + c.fuel + " L");
        Trackable[] things = { c, new Phone() };
        for (Trackable t : things) System.out.println(t.location());
    }
}
```

Output:

```text
DL3C1234: 4 wheels, 20.0 L
Car DL3C1234 at Okhla
Phone at Jamia Nagar
```

**Answer: abstract class for a related family that shares state and code; interface for a capability that unrelated classes share, or when a class must be several types at once.**

## Stop 10: Packages, and throw vs throws

Neither is in the Unit 4 syllabus line, but both were asked in Java papers, so here they are.

**A package** is a named group of related classes and interfaces, stored as a folder of the same name. Java's own `ArrayList` and `Random` live in the package `java.util`, which is why you write `import java.util.Random;`.

> **PYQ, Endsem 2022 Q4(b)(i), 3 marks.** What are the benefits of using packages? Write down the steps in creating a package and using it in a Java program with an example.

**Answer:**

**Benefits:**

- **No name clashes:** two classes can share a name in different packages, like `java.util.Date` and `java.sql.Date`.
- **Organisation:** related classes sit together, so code is easier to find and maintain.
- **Access control:** default (package-private) members are visible inside the package and hidden outside it.
- **Reuse:** one `import` line brings a tested class into any program.

**Steps:**

1. Write `package mypack;` as the **first line** of the source file.
2. Make the class and the methods others need `public`, or they stay invisible outside the package.
3. Compile with `javac -d . Calculator.java`. The `-d .` flag creates the folder `mypack` and puts `Calculator.class` inside it.
4. In another program, `import mypack.Calculator;` (or `import mypack.*;` for everything).
5. Compile and run that program from the folder that contains `mypack`.

```java
// File: Calculator.java
package mypack;

public class Calculator {
    public int add(int a, int b)      { return a + b; }
    public int multiply(int a, int b) { return a * b; }
}
```

```java
// File: UsePack.java (next to the mypack folder)
import mypack.Calculator;

class UsePack {
    public static void main(String[] args) {
        Calculator c = new Calculator();
        System.out.println(c.add(4, 5));       // 9
        System.out.println(c.multiply(4, 5));  // 20
    }
}
```

```bash
javac -d . Calculator.java
javac UsePack.java
java UsePack
```

**Answer: packages prevent name clashes, organise code, add package-level access control and allow reuse. Create one with** `package name;` **on line 1, compile with** `-d .`**, then** `import` **it.**

**Exceptions in one paragraph** (full treatment in Unit 5): an **exception** is an object Java creates when something goes wrong while the program runs, such as dividing by zero or bad input. If nothing catches it, the program stops with an error message. `try { ... } catch (SomeException e) { ... }` catches it and lets the program carry on. A **checked** exception (like `IOException`) is one the compiler forces you to either catch or declare. An **unchecked** one (like `ArithmeticException`) it doesn't.

> **PYQ, Java sessional (Makeup 2024 file) Q2(c).** Differentiate between throw and throws.

**Answer:**

|  | `throw` | `throws` |
| --- | --- | --- |
| What it is | A statement that raises an exception right now | A clause in a method header that declares exceptions |
| Where | Inside the method body | After the parameter list |
| Followed by | One exception **object**: `throw new X("msg");` | One or more exception **class names**: `throws IOException, SQLException` |
| Purpose | Signal an error | Warn callers that they must catch or pass on these exceptions |
| Needed for | Any exception | Checked exceptions (optional for unchecked) |

```java
class AgeException extends Exception {        // our own checked exception
    AgeException(String msg) { super(msg); }
}

class Voter {
    static void checkAge(int age) throws AgeException {        // throws: the warning
        if (age < 18)
            throw new AgeException("Age " + age + " is below 18");   // throw: the act
        System.out.println("Age " + age + ": can vote");
    }

    public static void main(String[] args) {
        try {
            checkAge(20);
            checkAge(15);
            checkAge(30);          // never reached: the exception jumps to catch
        } catch (AgeException e) {
            System.out.println("Caught: " + e.getMessage());
        }
    }
}
```

Output:

```text
Age 20: can vote
Caught: Age 15 is below 18
```

**Answer:** `throw` **raises one exception object inside a method;** `throws` **in the method header declares which exceptions the method may pass to its caller.**
