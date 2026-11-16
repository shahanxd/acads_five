# RUN 30 min: OOP Unit 4, Java Classes, Inheritance and Interfaces

Nov 16, 2026 · @shahan

Unit 4 in 30 minutes, written for someone meeting Java for the first time: every idea the paper tests, plus the PYQs that keep coming back, including the Sessional-2 2024 and 2025 Java questions. Every program was compiled and run with JDK 21, and every output shown is the real one.

## How this run works

Read straight through, guessing each answer for ten seconds first. The bold line under an answer is the one to remember. Java reuses Unit 3's C++ ideas with fewer traps.

| What the paper likes | Asked in |
| --- | --- |
| Base class, subclass, an array of objects, print the ones that match a condition | Sessional-2 2024, Java sessional, Endsem 2025 |
| Abstract class vs interface | Sessional-2 2025, Java sessional, Endsems 2022 and 2025 |
| `super` and `this` | Endsems 2021, 2023 and 2025 |
| "What's the output? Does it compile?" | Sessional-2 2024, Endsem 2021 |
| A run-time polymorphism program | Sessional-2 2024, Java sessional |

"Java sessional" is the paper saved as `OOP/PYQs/Makeup 2024.pdf` (its title says "OOPS Sessional 3").

**Shortened from the full 2-hour doc:** the long one-off programs (Fuel\_Monitor, Crushable, payroll) and the repeat Product and Subscriber programs. Each gets a short note with its key lines.

## Stop 1: Java for someone coming from C++

**How a Java program runs.** You write `Hello.java`. The compiler `javac` turns it into **bytecode** (`Hello.class`), an in-between code no real CPU understands. The **JVM** (Java Virtual Machine), a program installed on each computer, reads that bytecode and runs it. Same bytecode, any machine with a JVM.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

Everything in Java lives inside a class, and a public class must sit in a file of the same name. `System.out.println(...)` prints a line, like `cout << ... << endl`.

> **PYQ, Sessional-2 2024 Q1(b), 2 marks.** Explain each keyword in `public static void main(String[] args)`.

**Answer:**

| Word | Meaning |
| --- | --- |
| `public` | Anyone can call it, including the JVM from outside the class |
| `static` | Belongs to the class, so the JVM can call it without making an object first |
| `void` | Returns nothing |
| `main` | The name the JVM looks for as the starting point |
| `String[] args` | An array of the words typed after the program name on the command line |

> **PYQ, Sessional-2 2024 Q1(c), 1 mark.** Differentiate between platform independent and architecture-neutral.

**Answer:** A **platform** is the operating system plus hardware; the **architecture** is the processor design.

|  | Platform independent | Architecture-neutral |
| --- | --- | --- |
| Means | The same `.class` file runs on any OS that has a JVM | Nothing in the language or bytecode depends on the processor: `int` is always 32 bits, `char` 16 bits |
| Comes from | Bytecode plus a JVM for each platform | A fixed language spec; bytecode isn't any CPU's instruction set |
| In C++ | An `.exe` runs only where it was built | `int` can be 16, 32 or 64 bits depending on the machine |

**The big differences from C++:**

|  | C++ | Java |
| --- | --- | --- |
| Functions outside classes | Allowed | Not allowed |
| Where objects live | Stack or heap | Always the heap, made with `new` |
| Pointers | Yes | No, **references** instead |
| Freeing memory | You call `delete` | The **garbage collector** does it |
| Run-time polymorphism | Only with `virtual` | Automatic for every normal method |
| Multiple inheritance of classes | Allowed | Not allowed; interfaces do that job |

**References.** A class-type variable doesn't hold the object; it holds a **reference**, an arrow pointing at the object. Think of a pointer you can't do arithmetic on or `delete`.

```java
Student a = new Student();   // one object, arrow a points at it
Student b = a;               // no copy: b points at the SAME object
b.name = "Riya";             // so a.name is now "Riya" too
```

A reference pointing at nothing holds `null`, and calling a method on it throws a `NullPointerException`.

> **PYQ, Sessional-2 2024 Q1(a)(i), 1 mark.** What's the output? `int arr1[] = {1, 2, 3}; int arr2[] = {1, 2, 3}; if (arr1 == arr2) System.out.println("Same"); else System.out.println("Not same");`

**Answer:** `Not same`**.** Arrays are objects, so arr1 and arr2 are two references to two different arrays. `==` on references asks "same object?", not "same contents?". To compare contents, use `java.util.Arrays.equals(arr1, arr2)`, which gives `true`. Strings follow the same rule: compare them with `.equals()`.

> **PYQ, Endsem 2023 Q4(c), 6 marks.** List and explain 3 features that make Java a *completely* object-oriented language.

**Answer:**

1. **Everything lives inside a class.** No global variables or free functions; even `main` is a method. C++ allows a program with no class at all, which makes it a hybrid.
2. **One single class hierarchy.** A class that extends nothing automatically extends `java.lang.Object`, so every object shares methods like `toString()` and `equals()`.
3. **Objects only through** `new` **and references.** No pointers or `delete`; the garbage collector manages memory.

Worth adding: run-time polymorphism is built in. Caveat: the 8 primitive types (`int`, `double` and so on) aren't objects, though each has a wrapper class (`Integer`, `Double`).

> **PYQ, Endsem 2023 Q4(a)(II), 3 marks.** Explain dangling pointer error, memory leak and garbage collection in Java, with code.

**Answer:**

- **Dangling pointer:** a pointer to memory that's already been freed. In C++, `int* p = new int(5); delete p; cout << *p;` reads garbage. **Impossible in Java:** there's no `delete`, and an object is freed only when no reference points to it.
- **Memory leak:** memory you no longer need that never gets freed. Java can still leak if you keep references you don't need:

```java
static ArrayList<int[]> store = new ArrayList<>();
static void handleRequest() {
    store.add(new int[100000]);   // never removed, so it can never be freed
}
```

- **Garbage collection:** the JVM automatically frees objects that no reference can reach.

```java
String s1 = new String("A");
s1 = null;                 // "A" is unreachable, so it can be collected
String s2 = new String("B");
s2 = new String("C");      // "B" is unreachable too
System.gc();               // only a request; the JVM decides when
```

**No** `delete` **means no dangling pointers, useless references still leak, and the GC frees whatever is unreachable.**

## Stop 2: Classes, objects and access

A **class** is a blueprint listing **fields** (each object's data) and **methods** (what it can do). An **object** is one real thing built from it with `new`, and the dot reaches inside it: `s1.name = "Asha";`. Unlike C++, **fields get default values** (0, `false` or `null`), but a local variable must be set before it's read.

**Access specifiers** have four levels in Java, one more than C++, because of **packages**: named groups of related classes, like folders (Stop 10).

| Specifier | Same class | Same package | Subclass in another package | Anywhere else |
| --- | --- | --- | --- | --- |
| `private` | Yes | No | No | No |
| *(none)*: default, or package-private | Yes | Yes | No | No |
| `protected` | Yes | Yes | Yes | No |
| `public` | Yes | Yes | Yes | Yes |

Two C++ traps: no keyword means "same package", not private, and `protected` also opens the member to the whole package. The usual design is **encapsulation**: `private` fields, plus small `public` **getters** (return a field) and **setters** (change it after checking the value).

> **PYQ, Endsem 2021 Q1(c)(i), 3 marks.** Differentiate private, public and protected members, with an example of what is and isn't accessible.

**Answer:** private = its own class only; protected = its class, subclasses, and (in Java) the same package; public = everyone.

```java
class Account {
    private int pin = 1234;          // only Account itself
    protected double balance = 500;  // Account, its subclasses, same package
    public String owner = "Asha";    // everyone
}

class Savings extends Account {
    void test() {
        System.out.println(owner);    // OK: public
        System.out.println(balance);  // OK: protected, and Savings is a subclass
        // System.out.println(pin);   // ERROR: pin has private access in Account
    }
}
```

**private = class only, protected = class + subclasses (+ package in Java), public = everyone.**

**Endsem 2022 Q4(a), 6 marks (Fuel\_Monitor), in short:** make `tankCapacity` and `efficiency` private (fixed facts about the car), `fuelInTank` protected and starting at 0, and the methods public. The getters return the tank size and fuel. `addFuel(litres)` adds `Math.min(litres, tankCapacity - fuelInTank)`, so the tank never overflows, and returns the amount added. `driveDistance()` returns `fuelInTank * efficiency`.

## Stop 3: Constructors and this

A **constructor** runs by itself the moment `new` creates an object, to give it starting values. It has the class's name and **no return type, not even** `void`. Several constructors with different parameter lists is **constructor overloading**, and Java picks the one that matches what you pass.

```java
class Rectangle {
    int length, breadth;

    Rectangle() { this(1, 1); }                 // no-argument: reuse the 2-argument one
    Rectangle(int side) { this(side, side); }   // a square
    Rectangle(int length, int breadth) {        // parameterized
        this.length = length;                   // field = parameter
        this.breadth = breadth;
    }
}
```

`this` means "the object this code is running on". Two jobs:

1. `this.length` **vs** `length`**.** When a parameter shares a field's name, the plain name means the parameter. Write `length = length;` and the field silently stays 0.
2. `this(...)` calls another constructor of the same class. It must be the **first line**.

**The default constructor trap.** Write no constructor and Java adds an empty no-argument one for free. Write any constructor and that free one is gone, so `new Rectangle()` would fail if only `Rectangle(int, int)` existed.

Constructors aren't inherited and can't be overridden. Java has no destructors (the garbage collector handles memory).

## Stop 4: static and final

`static` **means it belongs to the class, not to any one object.** A normal field has a copy inside every object; a static field has one copy that all objects share, like a classroom notice board instead of a notebook per student. A **static method** is called as `ClassName.method()` with no object, so it can't use `this` or plain instance fields.

`final` **means it can't change any more:**

- a **final variable** is set once, then it's a constant;
- a **final method** can't be overridden;
- a **final class** can't be extended (`String` is final).

`static final double PI = 3.14159;` gives one shared copy that never changes: Java's constant.

> **PYQ, Java sessional Q2(b).** Differentiate between final and static.

**Answer:**

|  | `static` | `final` |
| --- | --- | --- |
| Core meaning | Belongs to the class, shared | Can't change once set |
| On a variable | One copy for all objects | Assigned once, then constant |
| On a method | Called without an object, no `this` | Can't be overridden |
| On a class | Only on nested classes | Can't be extended |

```java
class Student {
    static int count = 0;                 // one shared counter
    static final String COLLEGE = "JMI";  // shared constant
    final int rollNo;                     // each student's own, fixed once set
    String name;

    Student(int rollNo, String name) {
        this.rollNo = rollNo;
        this.name = name;
        count++;
    }

    static void showCount() {             // no object needed
        System.out.println("Students: " + count);
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
        // a.rollNo = 5;                  // ERROR: cannot assign a value to final variable rollNo
    }
}
```

```text
1 Asha JMI
2 Ravi JMI
Students: 2
```

**static = one shared copy belonging to the class; final = can't change (variable), be overridden (method) or be extended (class).**

**Endsem 2021 Q4(b), 6 marks**, asks for super, static and final with code snippets: use this program for static and final, and Stop 5's Person and Student program for super.

## Stop 5: Inheritance and super

**Inheritance** builds a new class on an existing one with `extends`. The old class is the **superclass** (parent), the new one the **subclass** (child), and the child gets the parent's fields and methods plus its own. It models **IS-A**: a BedRoom is a Room.

```java
class Room {
    int length, breadth;
    Room(int x, int y) { length = x; breadth = y; }
    int area() { return length * breadth; }
}

class BedRoom extends Room {
    int height;
    BedRoom(int x, int y, int z) {
        super(x, y);              // let Room set length and breadth
        height = z;
    }
    int volume() { return length * breadth * height; }
}
// new BedRoom(14, 12, 10): area() = 168 (inherited), volume() = 1680
```

**Types:** single, multilevel and hierarchical are allowed. **Multiple inheritance of classes is banned**: if A and B both had `show()` and C extended both, `c.show()` would be ambiguous (Unit 3's diamond problem). Interfaces give the useful part without that (Stop 8). The child can't name the parent's private fields and doesn't inherit constructors.

`super` means "the parent part of this object". Three uses:

1. `super(args)` calls the parent's constructor, and must be the **first line**.
2. `super.method()` runs the parent's version of an overridden method.
3. `super.field` reaches a parent field hidden by a child field of the same name.

**Constructor chaining:** making a child object runs constructors **top-down**, grandparent first. If you don't write `super(...)`, Java inserts `super()` with no arguments, and if the parent has no no-argument constructor, that's a compile error.

> **PYQ, Endsem 2025 Q4(a), 4.5 marks.** Discuss the significance of `super`, showing its use in calling parent constructors and methods.

**Answer:** `super` lets a child reuse its parent: the parent sets up its own fields (even private ones), and the child extends a method instead of rewriting it. `@Override` is an **annotation**, a note telling the compiler "I mean to override", so a misspelt name becomes an error.

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

```text
Person constructor
Student constructor
Name: Asha
Roll no: 101
```

`super(...)` **(first line) runs the parent constructor,** `super.method()` **the parent's version of a method, and** `super.field` **a hidden parent field.** Remove `super(name)` and it won't compile, since Person has no no-argument constructor.

> **PYQ, Endsem 2023 Q4(a)(I), 3 marks.** What is the use of `this` and `super`? Illustrate.

**Answer:**

|  | `this` | `super` |
| --- | --- | --- |
| Refers to | The current object | The parent part of the current object |
| Field | `this.x`: own field, when a parameter is also x | `super.x`: parent's field hidden by a child field |
| Method | `this.m()`: own method | `super.m()`: parent's version |
| Constructor | `this(...)`: another constructor of this class | `super(...)`: the parent's constructor |

Both `this(...)` and `super(...)` must be the first line, so a constructor uses only one, and neither works in a static method. Stop 3's Rectangle and the Student above are the examples.

> **PYQ, Endsem 2021 Q4(c), 6 marks.** Use these classes and justify:

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

> (i) Car doesn't compile. Why, and how do you fix it? (ii) Once fixed, output of `Car audi = new Car(); Car.drive();`? (iii) Output of `Car porsche = new Car(2, 4); porsche.drive();`? (iv) Output of `Vehicle v = new Vehicle(18); v.drive(); v.numOfDoors = 2;`?

**Answer:**

**(i)** `super(w)` isn't the first statement, and Java requires it there. Move it up: `public Car(int d, int w) { super(w); numOfDoors = d; }`. (Java 25 relaxed this rule, but exams assume classic Java.)

**(ii) Neither line compiles, so there's no output.** Car has only `Car(int, int)`, so there's no free `Car()`. And `drive` is an instance method, which needs an object; calling it on the class gives "non-static method drive() cannot be referenced from a static context".

**(iii)** `Driving a car`. The porsche has 2 doors and 4 wheels, and Car's own `drive()` runs.

**(iv)** **Compile error**: Vehicle has no field `numOfDoors`, because a parent knows nothing about its child's fields. Without that line, it prints `Driving a vehicle`.

**(i) super must come first; (ii) compile errors; (iii)** `Driving a car`**; (iv) compile error on numOfDoors.**

> **PYQ, Sessional-2 2024 Q2, 5 marks.** Class Employee with employee\_id and employee\_name. Subclass Salary adds designation and monthly\_salary. Give (a) constructors, (b) a method that displays employees earning more than Rs. 20,000, (c) a main that stores employees in an array and demonstrates it.

**Answer:** `Salary[] staff = { ... }` is an **array of references**, one arrow per object. `for (Salary s : staff)` is the **for-each loop**: "for each s in staff".

```java
class Employee {
    protected int employeeId;
    protected String employeeName;

    Employee(int employeeId, String employeeName) {
        this.employeeId = employeeId;
        this.employeeName = employeeName;
    }
}

class Salary extends Employee {
    private String designation;
    private double monthlySalary;

    Salary(int employeeId, String employeeName, String designation, double monthlySalary) {
        super(employeeId, employeeName);         // Employee sets id and name
        this.designation = designation;
        this.monthlySalary = monthlySalary;
    }

    void displayIfAbove20000() {
        if (monthlySalary > 20000)
            System.out.println(employeeId + " | " + employeeName + " | "
                               + designation + " | Rs. " + monthlySalary);
    }
}

class SalaryDemo {
    public static void main(String[] args) {
        Salary[] staff = {
            new Salary(1, "Asha", "Manager", 45000),
            new Salary(2, "Ravi", "Clerk", 18000),
            new Salary(3, "Meera", "Engineer", 32000),
            new Salary(4, "Kabir", "Intern", 20000)
        };
        System.out.println("Employees earning more than Rs. 20,000:");
        for (Salary s : staff)
            s.displayIfAbove20000();
    }
}
```

```text
Employees earning more than Rs. 20,000:
1 | Asha | Manager | Rs. 45000.0
3 | Meera | Engineer | Rs. 32000.0
```

Kabir earns exactly 20,000, which isn't *more than* 20,000, so he's left out. Graders like a boundary case.

`super(id, name)` **in the subclass constructor, and a filter method on** `monthlySalary > 20000`**.**

**Same program, two more papers:**

- **Java sessional Q1:** Product (id, name) → subclass with `category` and `monthly_sales`; the filter is `monthlySales > 100`.
- **Endsem 2025 Q4(c), 4.5 marks:** Subscriber (id, name) → PremiumSubscriber (plan, monthlyFee); the filter is `monthlyFee > 799`. The extra is a **static** `platformName`, the same for every subscriber, set once through the class:

```java
static String platformName;                        // in Subscriber
static void setPlatformName(String platform) { platformName = platform; }
// in main, before making the array:
Subscriber.setPlatformName("StreamMax");
```

## Stop 6: Overriding, overloading and dynamic binding

**Polymorphism** means "many forms": one method name, different behaviour. Java has two kinds.

- **Compile-time = overloading:** one class, several methods with the same name but different parameters. The compiler picks one from the arguments. A different return type alone doesn't count.
- **Run-time = overriding:** a subclass rewrites an inherited method with the same name and parameters. The version is picked while the program runs.

**Overriding rules:**

1. Same name and parameters; the return type is the same or **covariant** (a subclass of the original).
2. Access can't get stricter: `public` can't become `private`.
3. `final` methods can't be overridden, and `private` ones aren't inherited.
4. `static` methods are **hidden**, not overridden: the reference type decides which runs.

**Upcasting:** a parent-type reference may point at a child object, since a Circle IS-A Shape: `Shape s = new Circle(2);`. Then **dynamic binding** (or **dynamic method dispatch**) kicks in:

- the **reference type** decides what you're *allowed* to call (the compiler checks this);
- the **object type** decides *which version* runs (the JVM decides this).

In C++ this needed `virtual`; in Java every normal method works this way.

> **PYQ, Sessional-2 2024 Q1(a)(ii), 1 mark.** What's the output?

```java
class X {
    static void method() { System.out.println("Static Method in X"); }
}
class Y extends X {
    static void method() { System.out.println("Static Method in Y"); }
}
public class TestDemo {
    public static void main(String[] args) {
        X obj = new Y();
        obj.method();
    }
}
```

**Answer:** `Static Method in X`**.** A static method belongs to the class, so it isn't overridden, only **hidden**. The call is fixed at compile time by the reference type, X, whatever object `obj` holds. Remove both `static` words and it prints `Static Method in Y`, because then it's real overriding.

> **PYQ, Sessional-2 2024 Q3, 5 marks.** Base class Customer has `getDiscount()` giving a default discount (0%). Subclasses: RegularCustomer (10%), PremiumCustomer (20%), VIPCustomer (30%). Use run-time polymorphism to apply the right discount by the actual customer type and compute the final price.

**Answer:** Each subclass overrides `getDiscount()`. One `finalPrice()` in the base calls it, and dynamic binding runs the right version for the actual object.

```java
class Customer {
    double getDiscount() { return 0; }              // default: no discount
    String type() { return "Customer"; }
    double finalPrice(double amount) {
        return amount - amount * getDiscount() / 100;   // runs the object's getDiscount()
    }
}

class RegularCustomer extends Customer {
    @Override double getDiscount() { return 10; }
    @Override String type() { return "Regular"; }
}

class PremiumCustomer extends Customer {
    @Override double getDiscount() { return 20; }
    @Override String type() { return "Premium"; }
}

class VIPCustomer extends Customer {
    @Override double getDiscount() { return 30; }
    @Override String type() { return "VIP"; }
}

class Shop {
    public static void main(String[] args) {
        Customer[] customers = { new Customer(), new RegularCustomer(),
                                 new PremiumCustomer(), new VIPCustomer() };
        double bill = 1000;
        for (Customer c : customers)
            System.out.println(c.type() + ": " + c.getDiscount() + "% off, pays Rs. "
                               + c.finalPrice(bill));
    }
}
```

```text
Customer: 0.0% off, pays Rs. 1000.0
Regular: 10.0% off, pays Rs. 900.0
Premium: 20.0% off, pays Rs. 800.0
VIP: 30.0% off, pays Rs. 700.0
```

**One** `Customer` **reference type, four objects: dynamic binding picks each subclass's** `getDiscount()` **at run time.**

> **PYQ, Endsem 2021 Q3(b), 6 marks.** Differentiate method overriding and overloading with a program in C++ or Java.

**Answer:**

|  | Overloading | Overriding |
| --- | --- | --- |
| Where | One class | Parent and child class |
| Parameters | **Different** | **Same** |
| Return type | May differ (not enough on its own) | Same, or covariant |
| Decided at | Compile time | Run time |
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
        System.out.println(c.add(2, 3));
        System.out.println(c.add(2.5, 1.5));
        System.out.println(c.add(1, 2, 3));
        Animal a = new Dog();          // parent reference, child object
        a.sound();                     // picked at run time
    }
}
```

```text
5
4.0
6
Bark
```

> **PYQ, Endsem 2023 Q3(c)(I), 2 marks.** Differentiate late (dynamic) and early (static) binding.

**Answer:** **Binding** connects a method call to the body that will run.

|  | Early (static) | Late (dynamic) |
| --- | --- | --- |
| When | Compile time | Run time |
| Decided by | Reference type | Actual object type |
| Used for | Overloaded, static, private, final methods | Overridden methods |
| Speed | Faster | Slightly slower, a run-time lookup |

## Stop 7: Abstract classes and methods

Some classes are too general to exist on their own: you never draw "a shape", you draw a circle. Java marks these `abstract`.

- An **abstract class** can't be turned into objects (`new Shape()` is an error); it exists to be inherited.
- An **abstract method** has no body, just a signature ending in `;`: a promise that every real subclass will write it. In C++ terms, it's a pure virtual function.
- A **concrete** class or method is a normal one, everything filled in.

**Rules:** a class with even one abstract method must be abstract. It can still have fields, constructors (run through `super(...)`) and concrete methods. Its references are fine: `Shape s = new Circle(2);`. A subclass must implement every abstract method or be abstract itself. An abstract method can't be `private`, `static` or `final`, since each blocks overriding.

> **PYQ, Endsem 2021 Q4(a), 6 marks.** What is the only effect of `abstract` on a class? What are the two main effects of declaring a method abstract? Then use these classes:

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

> (i) Whale compiles but Cat doesn't. Why, and how do you fix it? (ii) Is `Mammal m = new Whale();` valid? (iii) Output of `Whale w = new Whale(); w.breathe(); w.nurse(); Mammal m = w; m.breathe(); m.nurse();`?

**Answer:**

**On a class:** the only effect is that it **can't be instantiated**. **On a method:** (1) it has **no body**, and (2) it **forces the class to be abstract** and every concrete subclass to override it.

**(i)** Cat's `nurse(int t)` takes a parameter, so it's an **overload**, not an override. Cat still has the bodiless `nurse()` but isn't abstract, so it fails. Fix: add `public void nurse() { ... }`, or declare Cat abstract.

**(ii) Valid.** A Mammal reference can point at any concrete subclass object; a Whale IS-A Mammal.

**(iii)** w and m point at the same Whale, so Whale's methods run both times, and `super.breathe()` adds Mammal's line:

```text
Whale is breathing
Mammal is breathing
Whale is nursing
Whale is breathing
Mammal is breathing
Whale is nursing
```

**Cat fails because** `nurse(int)` **overloads instead of overriding. The upcast is valid, and the output is these 6 lines.**

**Java sessional Q3 (payroll), in short:** four employee types, each paid differently: a textbook abstract method. Make `abstract class Employee` with `abstract double earnings();`. Salaried returns a fixed salary, Commissioned returns `rate * grossSales`, Hourly pays 1.5x past 40 hours, and Base + Commission extends Commissioned and reuses it:

```java
double earnings() {                                  // HourlyEmployee
    if (hours <= 40) return wage * hours;
    return 40 * wage + (hours - 40) * wage * 1.5;    // overtime at 1.5x
}
double earnings() { return baseSalary + super.earnings(); }   // BasePlusCommissionEmployee
```

Loop over an `Employee[]` printing `e.earnings()`, and dynamic binding picks each type's rule. A wage of 20 for 50 hours gives 800 + 300 = 1100.

## Stop 8: Interfaces

An **interface** is a list of methods a class promises to provide, with no say in *how*. It's a job description: the interface says **what**, and each implementing class says **how**.

```java
interface Student {
    int MAX_MARKS = 100;     // a constant: automatically public static final
    void study();            // automatically public abstract
}
```

**Inside an interface:** methods without bodies (automatically `public abstract`) and constants (automatically `public static final`). Since Java 8, also `default` methods (with a body, inherited unless overridden) and `static` methods. **Not allowed:** constructors, normal fields, or `new Student()`.

**Implementing:** a class signs up with `implements` and must write every method as `public`, since an override can't lower the access. Skip one and the class must be abstract.

**Interface references:** a variable of interface type can point at an object of *any* class that implements it, and dynamic binding runs that object's method. That's the syllabus's "accessing implementations through interface references".

**Multiple inheritance, the Java way:** extend one class, implement any number of interfaces: `class Duck extends Bird implements Flyable, Swimmable`. No diamond problem, because abstract methods have no bodies to clash: if two interfaces both list `move()`, one `move()` satisfies both.

**Extending interfaces:** `interface Teacher extends Student { void teach(); }`, so a class implementing Teacher must write `study()` and `teach()`. An interface may extend several: `interface C extends A, B`.

**Keywords:** class to class `extends`, interface to interface `extends`, class to interface `implements`.

> **PYQ, Endsem 2022 Q4(c), 6 marks.** Define an interface with a method to calculate perimeter. Implement it in classes Circle and Rectangle with suitable fields and methods, and test them in main.

**Answer:** `printf` prints formatted text: `%.2f` is a number rounded to 2 decimals, and `%n` is a newline.

```java
interface Perimeter {
    double perimeter();                      // public abstract, automatically
}

class Circle implements Perimeter {
    private double radius;
    Circle(double radius) { this.radius = radius; }
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
        Rectangle r = new Rectangle(4, 5);
        System.out.printf("Rectangle area %.1f%n", r.area());
        Perimeter[] shapes = { new Circle(7), r };    // interface references
        for (Perimeter p : shapes)
            System.out.printf("Perimeter %.2f%n", p.perimeter());
    }
}
```

```text
Rectangle area 20.0
Perimeter 43.98
Perimeter 18.00
```

`interface Perimeter { double perimeter(); }`**, implemented as public methods (2πr and 2(l + w)), called through** `Perimeter` **references.**

**Endsem 2023 Q4(b), 6 marks (Crushable), in short:** interface `Crushable` with `crush()`, implemented by `Circle`, where `crush()` returns 4 random circles whose areas add up to the original. Area grows with the *square* of the radius, so split the **area**, not the radius. Pick 4 random weights from 1 to 10, call their sum S, and size each piece by its weight. Each piece then gets its share of the area, and the shares add up to exactly 1:

```latex
\begin{aligned}
r_i &= r\sqrt{\frac{w_i}{S}} \\
A_i &= \pi r_i^2 = \pi r^2 \cdot \frac{w_i}{S} \\
\sum_{i=1}^{4} A_i &= \pi r^2 \cdot \frac{w_1 + w_2 + w_3 + w_4}{S} = \pi r^2
\end{aligned}
```

```java
public Circle[] crush() {
    Random rand = new Random();                       // import java.util.Random;
    int[] w = new int[4];
    int sum = 0;
    for (int i = 0; i < 4; i++) { w[i] = rand.nextInt(10) + 1; sum += w[i]; }
    Circle[] circleArray = new Circle[4];
    for (int i = 0; i < 4; i++)
        circleArray[i] = new Circle(radius * Math.sqrt((double) w[i] / sum));
    return circleArray;
}
```

`(double)` matters: without it, `3 / 20` is integer division and gives 0.

## Stop 9: Abstract class vs interface vs concrete class

The picture to keep:

- A **concrete class** is a finished product: every method has a body, so you can make objects.
- An **abstract class** is a half-built house for one *family* of classes: shared walls (fields, constructor, common methods) are up, and some rooms are left for each child.
- An **interface** is a certificate like "can fly" or "can be printed": no walls at all, just the promise, and any class from any family can earn several.

> **PYQ, Sessional-2 2025 Q3, 4 marks; Endsem 2025 Q4(b), 4.5 marks; Java sessional Q2(a).** Discuss the similarities and differences between abstract class and interface (Endsem 2025 adds concrete class), with their purpose, usage and key characteristics, and example code.

**Answer:**

**Similarities (abstract class and interface):**

- Neither can be instantiated with `new`.
- Both can declare abstract methods that subclasses or implementers must write.
- Both work as reference types for run-time polymorphism: `Shape s = new Square(...)`, `Drawable d = new Square(...)`.
- Both are tools for **abstraction**: showing *what* is done and hiding *how*.
- Both can have static methods, and both can have methods with bodies (an interface through `default` methods, since Java 8).

**Differences:**

|  | Concrete class | Abstract class | Interface |
| --- | --- | --- | --- |
| Declared as | `class A` | `abstract class A` | `interface A` |
| Objects with `new` | Yes | No | No |
| Abstract methods | None | Zero or more | All plain methods (plus `default` and `static` ones) |
| Fields | Any | Any | Only `public static final` constants |
| Constructors | Yes | Yes, run through `super(...)` | No |
| Inherited with | `extends`, one parent | `extends`, one parent | A class `implements` many |
| Method access | Any | Any (abstract ones not private) | `public` |
| Purpose | A complete, usable type | A common base sharing code and state | A capability shared across unrelated classes |

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

```text
Drawing a red square
red shape, area 9.0
```

Shape doesn't write `draw()`, which is allowed only because Shape is abstract; the job passes down to Square.

**Abstract class: a partial base for one family, shared through** `extends`**. Interface: a public contract that any number of unrelated classes can** `implements`**.**

> **PYQ, Endsem 2022 Q4(b)(ii), 3 marks.** Discuss the criteria for choosing an interface or an abstract class, with an example.

**Answer:** **Abstract class** when the classes are a close IS-A family sharing fields or code, or need a constructor or non-public members. **Interface** when unrelated classes share one capability, when a class must be several types at once, or to fix *what* and leave *how* to each class. Example: every vehicle has a registration number and refuels the same way, so `abstract class Vehicle` with a shared `refuel()`. Cars and phones are unrelated but both trackable, so `interface Trackable { String location(); }`, implemented by both.

## Stop 10: Packages, and throw vs throws

Both were asked in Java papers, so here they are briefly.

A **package** is a named group of related classes stored as a folder of the same name. `java.util.Random` is the class Random in the package `java.util`.

> **PYQ, Endsem 2022 Q4(b)(i), 3 marks.** Benefits of packages, and the steps to create and use one.

**Answer:** **Benefits:** no name clashes (`java.util.Date` vs `java.sql.Date`), better organisation, package-level access control, and easy reuse through `import`.

**Steps:**

1. Write `package mypack;` as the **first line** of the file.
2. Make the class and the methods others need `public`.
3. Compile with `javac -d . Calculator.java`, which creates the folder `mypack` with `Calculator.class` inside.
4. In another program, write `import mypack.Calculator;` (or `import mypack.*;`).

```java
// File: Calculator.java
package mypack;

public class Calculator {
    public int add(int a, int b) { return a + b; }
}
```

```java
// File: UsePack.java, next to the mypack folder
import mypack.Calculator;

class UsePack {
    public static void main(String[] args) {
        System.out.println(new Calculator().add(4, 5));   // 9
    }
}
```

An **exception** is an object Java creates when something goes wrong at run time. Uncaught, it stops the program; `try { ... } catch (SomeException e) { ... }` catches it so the program carries on. A **checked** exception (like `IOException`) must be caught or declared; an **unchecked** one (like `ArithmeticException`) needn't be.

> **PYQ, Java sessional Q2(c).** Differentiate between throw and throws.

**Answer:**

|  | `throw` | `throws` |
| --- | --- | --- |
| What | A statement that raises an exception now | A clause in a method header that declares exceptions |
| Where | Inside the method body | After the parameter list |
| Followed by | One exception **object**: `throw new X("msg");` | Exception **class names**: `throws IOException, SQLException` |
| Purpose | Signal an error | Warn callers to catch or pass it on |

```java
class AgeException extends Exception {        // our own checked exception
    AgeException(String msg) { super(msg); }
}

class Voter {
    static void checkAge(int age) throws AgeException {           // throws: the warning
        if (age < 18)
            throw new AgeException("Age " + age + " is below 18");  // throw: the act
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

```text
Age 20: can vote
Caught: Age 15 is below 18
```

`throw` **raises one exception object inside a method;** `throws` **in the header declares what the method may pass to its caller.**

That's Unit 4. If you can write the Employee and Salary program and the abstract class vs interface table from memory, you've covered the two most-asked Java questions. Give the cat a scratch.
