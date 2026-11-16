# RUN 30 min: OOP Unit 3, Inheritance and Virtual Functions

Nov 16, 2026 · @shahan

Unit 3 in 30 minutes: every idea the paper tests, explained from zero, plus the PYQs that keep coming back. Every program was compiled and run with g++, and every output shown is the real one.

## How this run works

Read straight through. Guess each answer for ten seconds before reading it. The bold line under an answer is the one to remember.

| What the paper likes | Asked in |
| --- | --- |
| Base pointer to a derived object: which function runs? | Sessional-2 2021, 2022 and 2023 |
| Constructor chaining down a chain of classes | Sessional-2 2021, Endsems 2021 and 2025, Makeup 2022 |
| Virtual base class (the diamond problem) | Endsems 2021, 2022 and 2025 |

**Shortened from the full 2-hour doc:** the hotel (Endsem 2025), triangle and rectangle (Endsem 2022) and graphics hierarchy (Endsem 2022) programs. Each repeats a skeleton written out in full here, so each gets a short note with its key lines instead.

## Stop 1: Inheritance and access

**Inheritance** means building a new class on top of an existing one. The existing class is the **base class** (parent) and the new one is the **derived class** (child). The child automatically gets the parent's data and functions and adds its own, so the common part is written once. Use it only for "is-a": a Car is a Vehicle, so Car can inherit from Vehicle.

```cpp
class Derived : public Base {    // "public" here is the visibility mode
    // write only the NEW members here
};
```

**Access specifiers** label every member and decide who may use it:

| Specifier | Inside its own class | Inside a derived class | Outside, through an object |
| --- | --- | --- | --- |
| `public` | Yes | Yes | Yes |
| `protected` | Yes | Yes | No |
| `private` | Yes | No | No |

So `protected` is "private, but the kids can see it".

The **visibility mode**, the word after the colon, decides what inherited members become inside the child:

| Member in Base | `public` inheritance | `protected` inheritance | `private` inheritance |
| --- | --- | --- | --- |
| public | public | protected | private |
| protected | protected | protected | private |
| private | not accessible | not accessible | not accessible |

Leave the mode out and a `class` inherits **privately**, so nobody outside can call the inherited functions. That's why you almost always write `public`.

> **PYQ, Endsem 2023 Q3(a)(I), 3 marks.** What are access specifiers? How do they control access to class members, and what is their role in inheritance?

**Answer:** Write the two tables above. The specifier on a base member decides whether the child can see it at all, and the visibility mode in `class D : mode B` decides how visible the inherited members stay inside D. Add one line of code as the example: in `class D : public B`, D's functions can use B's public and protected members, but not its private ones.

**Specifiers decide who can touch a member; the visibility mode decides how visible inherited members stay. Private members are never accessible in the child.**

> **PYQ, Endsem 2023 Q3(c)(II) and (III), 2 marks each.** Base and its public child Derv both have a public func1. How can Derv's func1 call Base's func1? If Base has a protected static member data1, can Derv's func1 use it, and how?

**Answer:** The child's func1 **hides** the parent's, so a plain `func1()` inside Derv means Derv's own. To reach past it, use the **scope resolution operator** `::`, which names the class a member belongs to: `Base::func1()`.

A **static** data member belongs to the class, not to any object, so exactly one copy exists and everyone shares it. It's declared inside the class and defined once outside it. Since data1 is protected, Derv can use that one copy as `data1` or `Base::data1`.

```cpp
#include <iostream>
using namespace std;

class Base {
protected:
    static int data1;
public:
    void func1() { cout << "Base::func1\n"; }
};
int Base::data1 = 10;            // the one shared copy

class Derv : public Base {
public:
    void func1() {
        Base::func1();           // the parent's version
        cout << "Derv::func1, data1 = " << data1 << ", " << Base::data1 << endl;
    }
};

int main() {
    Derv d;
    d.func1();
    return 0;
}
```

```text
Base::func1
Derv::func1, data1 = 10, 10
```

**Call** `Base::func1();` **inside Derv's func1 (a plain** `func1();` **would call itself forever). data1 is usable in Derv as** `data1` **or** `Base::data1`**, both the same single copy.**

## Stop 2: Five types of inheritance

Arrows go from child to parent, the way examiners expect them.

```text
 Single      Multilevel     Multiple       Hierarchical        Hybrid

   A             A          A     B             A                 A
   |             |           \   /            / | \              / \
   B             B             C             B  C  D            B   C
                 |                                               \ /
                 C                                                D
```

| Type | What it is | Syntax |
| --- | --- | --- |
| Single | One parent, one child | `class B : public A` |
| Multilevel | A chain: grandparent, parent, child | `class B : public A`, `class C : public B` |
| Multiple | One child, two or more parents | `class C : public A, public B` |
| Hierarchical | One parent, many children | `class B : public A`, `class C : public A` |
| Hybrid | A mix, usually the diamond | Hierarchical plus multiple |

> **Quick check.** `class Result : public Test, public Sports`, where Test and Sports both derive from Student. Which type?

**Hybrid.** Result alone is multiple, and Test and Sports from Student is hierarchical. Together they form the diamond, the trouble in Stop 4.

## Stop 3: Constructors in a chain

A **constructor** is a function with the class's name that runs by itself when an object is created, to set its starting values. A **destructor**, `~ClassName()`, runs by itself when the object dies, to clean up.

A derived object has its parent's part inside it, which fixes the order:

- **Construction: parent first, then child.** Foundation before walls. Multiple parents are built in the order the class header lists them.
- **Destruction: exact reverse.** Demolition starts at the roof.
- **Arguments travel up through the initializer list**, the part after the colon, which runs before the constructor's body. It's the only place a child can call its parent's constructor with arguments.

```cpp
Derived(int x, int y) : Base(x), d(y) { }   // Base gets x, the member d gets y
```

If you skip it, C++ calls the parent's no-argument constructor. If the parent has none, that's a compile error.

> **PYQ, Sessional-2 2021 Q2, 5 marks.** Show how parameters pass from a derived class constructor to the base class constructor, and display the order in which constructors run. Model a real-world scenario with more than 4 classes.

**Answer:** A college staff chain of five classes. Each constructor takes its own value plus everything its parents need, and hands the parents' share up.

```cpp
#include <iostream>
#include <string>
using namespace std;

class Person {
protected:
    string name;
public:
    Person(string n) : name(n) { cout << "1. Person constructor\n"; }
};

class Employee : public Person {
protected:
    int empId;
public:
    Employee(string n, int id) : Person(n), empId(id) { cout << "2. Employee constructor\n"; }
};

class Teacher : public Employee {
protected:
    string subject;
public:
    Teacher(string n, int id, string s) : Employee(n, id), subject(s) {
        cout << "3. Teacher constructor\n";
    }
};

class HOD : public Teacher {
protected:
    string dept;
public:
    HOD(string n, int id, string s, string d) : Teacher(n, id, s), dept(d) {
        cout << "4. HOD constructor\n";
    }
};

class Dean : public HOD {
    string faculty;
public:
    Dean(string n, int id, string s, string d, string f) : HOD(n, id, s, d), faculty(f) {
        cout << "5. Dean constructor\n";
    }
    void show() {
        cout << name << " (" << empId << "), " << subject << ", HOD of " << dept
             << ", Dean of " << faculty << endl;
    }
};

int main() {
    Dean d("Dr. Rao", 101, "Networks", "CSE", "Engineering");
    d.show();
    return 0;
}
```

```text
1. Person constructor
2. Employee constructor
3. Teacher constructor
4. HOD constructor
5. Dean constructor
Dr. Rao (101), Networks, HOD of CSE, Dean of Engineering
```

**Constructors run from the top of the chain down (Person first), and parameters travel up through each initializer list.** Destructors would run in reverse, Dean first.

> **PYQ, Endsem 2021 Q3(a), 6 marks, and Makeup 2022 Q1, 4 marks.** Base class Customer (name, phone). Derive Depositor (accno, balance) from Customer, and Borrower (loan-no, loan-amt) from Depositor. Read and display the details of n customers, with relevant constructors.

**Answer:** A three-level chain. Each `read()` and `display()` first calls the parent's version with `::`, then handles its own members. A Borrower holds all three levels, so an array of n Borrowers stores n complete customers.

```cpp
#include <iostream>
#include <string>
using namespace std;

class Customer {
protected:
    string name, phone;
public:
    Customer(string n = "", string p = "") : name(n), phone(p) {}
    void read() { cout << "Name and phone: "; cin >> name >> phone; }
    void display() { cout << "Name: " << name << ", Phone: " << phone << endl; }
};

class Depositor : public Customer {
protected:
    int accNo;
    double balance;
public:
    Depositor(string n = "", string p = "", int a = 0, double b = 0)
        : Customer(n, p), accNo(a), balance(b) {}
    void read() {
        Customer::read();
        cout << "Account number and balance: "; cin >> accNo >> balance;
    }
    void display() {
        Customer::display();
        cout << "Account: " << accNo << ", Balance: " << balance << endl;
    }
};

class Borrower : public Depositor {
    int loanNo;
    double loanAmt;
public:
    Borrower(string n = "", string p = "", int a = 0, double b = 0, int l = 0, double amt = 0)
        : Depositor(n, p, a, b), loanNo(l), loanAmt(amt) {}
    void read() {
        Depositor::read();
        cout << "Loan number and amount: "; cin >> loanNo >> loanAmt;
    }
    void display() {
        Depositor::display();
        cout << "Loan: " << loanNo << ", Amount: " << loanAmt << endl;
    }
};

int main() {
    int n;
    cout << "How many customers? "; cin >> n;
    Borrower* list = new Borrower[n];
    for (int i = 0; i < n; i++) list[i].read();
    for (int i = 0; i < n; i++) { cout << "\nCustomer " << i + 1 << endl; list[i].display(); }
    delete[] list;
    return 0;
}
```

With n = 1 and input `Ali 999 5 2000 77 50000`, the display part prints:

```text
Customer 1
Name: Ali, Phone: 999
Account: 5, Balance: 2000
Loan: 77, Amount: 50000
```

**The chain is** `Borrower(...) : Depositor(n, p, a, b)` **and** `Depositor(...) : Customer(n, p)`**. Every constructor has default arguments because** `new Borrower[n]` **needs one it can call with no arguments.**

**Same pattern, Endsem 2025 Q3(b), 4.5 marks:** Guest (name, phone) → Boarder (roomNo, tariff) → LongStay (contractNo, discountPercent), each with input and display. Write it like the bank. It asks for separate default and parameterized constructors, so write both at each level:

```cpp
LongStay() : Boarder(), contractNo(0), discountPercent(0) {}
LongStay(string n, string p, int r, double t, int c, double d)
    : Boarder(n, p, r, t), contractNo(c), discountPercent(d) {}
```

## Stop 4: Ambiguity and virtual base classes

**Ambiguity** means the compiler finds two equally good matches for a name and refuses to guess. Multiple inheritance causes it in two ways.

- **Same name in two parents.** A and B both have `show()`, and C inherits both, so `c.show()` won't compile. Fix: name the parent, `c.A::show()`, or give C its own `show()`.
- **The diamond.** Test and Sports both inherit Student, and Result inherits both. Result now holds **two copies** of Student, one per path, so `roll` is ambiguous. Two birth certificates for one kid.

**The fix is a virtual base class:** write `virtual` where the middle classes inherit Student. Every path then shares one Student, and the most derived class (Result) builds it.

```text
          Student
         /       \
  virtual         virtual
      Test        Sports
         \       /
          Result      <- one Student inside, not two
```

> **PYQ, Endsem 2025 Q3(a), 4.5 marks; Endsem 2022 Q3(b), 6 marks; Endsem 2021 Q3(c), 6 marks.** When does ambiguity arise in multiple inheritance, and how is it resolved? What are virtual base classes and why do they matter? Demonstrate with a program.

**Answer:** The two cases above. The first is fixed with `::`. The second is fixed with a virtual base class, which keeps one shared copy of the grandparent, saves memory and removes the ambiguity.

```cpp
#include <iostream>
using namespace std;

class Student {
protected:
    int roll;
public:
    Student() : roll(0) { cout << "Student constructor\n"; }
    void setRoll(int r) { roll = r; }
};

class Test : virtual public Student {       // virtual here
protected:
    int marks;
public:
    void setMarks(int m) { marks = m; }
};

class Sports : virtual public Student {     // and here
protected:
    int score;
public:
    void setScore(int s) { score = s; }
};

class Result : public Test, public Sports {
public:
    void show() {
        cout << "Roll " << roll << ", total " << marks + score << endl;  // no ambiguity
    }
};

int main() {
    Result r;
    r.setRoll(42);
    r.setMarks(80);
    r.setScore(15);
    r.show();
    return 0;
}
```

```text
Student constructor
Roll 42, total 95
```

**"Student constructor" prints once: one Student inside Result. Without the two** `virtual` **keywords,** `roll` **is ambiguous and the program doesn't compile.**

## Stop 5: Base pointers and virtual functions

A **pointer** holds an object's address. A base-class pointer can hold the address of a derived object, because a Dog **is an** Animal. Everything in this stop builds on that.

The catch: normally C++ picks the function by the **pointer's type**, so `p->sound()` runs Animal's version even when the object is a Dog. Mark the base function `virtual` and C++ picks by the **object's actual type**, while the program runs.

```cpp
class Animal { public: virtual void sound() { cout << "..."; } };
class Dog : public Animal { public: void sound() { cout << "Woof"; } };

Animal* p = new Dog;
p->sound();     // Woof with virtual, ... without it
```

A child redefining a parent's function with the same name and parameters is **overriding** it. Writing `override` after the child's function makes the compiler check that it really overrides something.

**Underneath:** each class with virtual functions gets a **vtable**, a hidden table of its virtual functions' addresses. Every object carries a hidden pointer to its class's vtable, and a virtual call is looked up there at run time.

> **PYQ, Sessional-2 2022 Q3(b), 1 mark.** Explain pointers to derived class objects.

**Answer:** A base pointer can hold a derived object's address, `Base* p = &d;`. Through it you reach only what Base declares. Non-virtual calls run Base's versions, and virtual calls run the object's versions. A `Derived*` can't point at a plain Base object without a cast.

> **PYQ, Sessional-2 2023 Q1(a), 1 mark.** Inheritance enables run-time polymorphism. Justify.

**Answer:** **Run-time polymorphism** means one call, many behaviours, chosen while the program runs. Inheritance supplies both halves: the base declares the common interface as virtual functions, and each child overrides them. Since a base pointer can point at any child object, the same call `p->f()` runs a different function per object. **No inheritance, no base pointer to a derived object, no run-time polymorphism.**

> **PYQ, Endsem 2023 Q3(c)(I), 2 marks.** Differentiate late (dynamic) and early (static) binding, with at least two differences.

**Answer:** **Binding** means connecting a function call to the body that will run.

| Basis | Early (static) binding | Late (dynamic) binding |
| --- | --- | --- |
| Resolved at | Compile time | Run time |
| Decided by | Pointer or reference type | Actual object type |
| Used for | Normal functions, overloading | Virtual functions |
| Speed | Faster, a direct call | Slightly slower, a vtable lookup |

> **PYQ, Endsem 2021 Q3(b), 6 marks, and Makeup 2022 Q4, 3 marks.** Differentiate method overriding and method overloading with a program in C++.

**Answer:** **Overloading** is several functions in one class sharing a name but taking different parameters; the compiler picks by the arguments. **Overriding** is a child redefining a parent's function with the same signature (name and parameter types).

| Basis | Overloading | Overriding |
| --- | --- | --- |
| Where | Same class | Base and derived class |
| Signature | Must differ in parameters | Must be the same |
| Binding | Compile time | Run time, when virtual |
| Inheritance needed | No | Yes |

```cpp
#include <iostream>
using namespace std;

class Calc {
public:
    int add(int a, int b) { return a + b; }               // overloading:
    double add(double a, double b) { return a + b; }      // same name, different parameters
    virtual void show() { cout << "Calc\n"; }
    virtual ~Calc() {}
};

class SciCalc : public Calc {
public:
    void show() override { cout << "SciCalc\n"; }         // overriding: same signature
};

int main() {
    Calc c;
    cout << c.add(2, 3) << " " << c.add(2.5, 3.5) << endl;
    Calc* p = new SciCalc;
    p->show();
    delete p;
    return 0;
}
```

```text
5 6
SciCalc
```

> **PYQ, Sessional-2 2021 Q1, 5 marks.** Use virtual functions to achieve run-time polymorphism, modelling a real-world scenario.

**Answer:** A payment system. The checkout loop holds only `Payment*` pointers and never needs to know which kind it has.

```cpp
#include <iostream>
using namespace std;

class Payment {
protected:
    double amount;
public:
    Payment(double a) : amount(a) {}
    virtual void pay() { cout << "Generic payment of " << amount << endl; }
    virtual ~Payment() {}
};

class UPI : public Payment {
public:
    UPI(double a) : Payment(a) {}
    void pay() override { cout << "Paid " << amount << " by UPI, no fee" << endl; }
};

class Card : public Payment {
public:
    Card(double a) : Payment(a) {}
    void pay() override { cout << "Paid " << amount * 1.02 << " by card, with 2% fee" << endl; }
};

int main() {
    Payment* p[3] = { new UPI(500), new Card(1000), new UPI(250) };
    for (int i = 0; i < 3; i++) p[i]->pay();       // which pay()? decided at run time
    for (int i = 0; i < 3; i++) delete p[i];
    return 0;
}
```

```text
Paid 500 by UPI, no fee
Paid 1020 by card, with 2% fee
Paid 250 by UPI, no fee
```

**One loop, one call,** `p[i]->pay()`**, three behaviours. That's run-time polymorphism.**

> **PYQ, Sessional-2 2022 Q2, 4 marks.** A bookshop sells books and tapes, both derived from media (title, price). Book adds pages, tape adds playing time. Each has read() and show(), virtual in the base. Process the objects through base-class pointers.

**Answer:** The Payment skeleton again. Each child's `read()` and `show()` call Media's version first, then add their own field.

```cpp
#include <iostream>
#include <string>
using namespace std;

class Media {
protected:
    string title;
    float price;
public:
    virtual void read() { cout << "Title and price: "; cin >> title >> price; }
    virtual void show() { cout << "Title: " << title << ", Price: " << price << endl; }
    virtual ~Media() {}
};

class Book : public Media {
    int pages;
public:
    void read() override { Media::read(); cout << "Pages: "; cin >> pages; }
    void show() override { Media::show(); cout << "Pages: " << pages << endl; }
};

class Tape : public Media {
    float playTime;
public:
    void read() override { Media::read(); cout << "Playing time (min): "; cin >> playTime; }
    void show() override { Media::show(); cout << "Playing time: " << playTime << " min" << endl; }
};

int main() {
    Media* list[2] = { new Book, new Tape };
    for (int i = 0; i < 2; i++) list[i]->read();
    cout << endl;
    for (int i = 0; i < 2; i++) list[i]->show();   // Book::show, then Tape::show
    for (int i = 0; i < 2; i++) delete list[i];
    return 0;
}
```

With input `Cpp 450 300 Songs 120 60`, the show loop prints:

```text
Title: Cpp, Price: 450
Pages: 300
Title: Songs, Price: 120
Playing time: 60 min
```

**Same skeleton, Endsem 2022 Q3(c)(ii), 3 marks:** base `shape` stores `double x, y`, sets them with `get_data(double a, double b)` and has `virtual void display_area()`. `triangle` overrides it to print `0.5 * x * y` and `rectangle` prints `x * y`. Through `shape* p`, `get_data(10, 5)` then gives 25 and 50.

## Stop 6: Pure virtual functions and abstract classes

A **pure virtual function** has no body in the base class, just `= 0`: `virtual double area() = 0;`. It means "every child must define this; I have no sensible default". A class with at least one is an **abstract class**:

- You **can't create objects** of it.
- You **can** have pointers and references to it, and that's the whole point.
- A child that doesn't override every pure virtual function is abstract too.
- It can still have data members, constructors and normal functions.

Think of a job description: nobody hires the description, they hire a person who fits it.

> **PYQ, Sessional-2 2022 Q3(a), 1 mark.** Explain pure virtual functions with an example.

**Answer:** A virtual function declared with `= 0` and no body in the base, such as `virtual double area() = 0;` in Shape. Every **concrete** child (one you can make objects of) must define it, and Shape becomes abstract.

> **PYQ, Endsem 2023 Q3(a)(II), 3 marks.** Explain abstract classes, virtual and pure virtual functions. How do they enable run-time polymorphism? Give a simple example.

**Answer:**

| Term | Meaning |
| --- | --- |
| Virtual function | Marked `virtual`, so a call through a base pointer runs the child's version |
| Pure virtual function | Virtual, with `= 0` and no body; every concrete child must override it |
| Abstract class | Has at least one pure virtual function, so no objects of it exist |

The abstract class fixes a common interface and each child overrides it. Code written against `Base*` then runs the right version for whatever object it gets, chosen at run time through the vtable. The next PYQ is the example.

> **PYQ, Endsem 2023 Q3(b), 6 marks.** Abstract class Shape: protected name, public print, public pure virtual area, a 1-argument constructor. Rectangle (public child): length, width, a 3-argument constructor passing name to Shape in the initializer list, overriding print and area. Square (public child of Rectangle): a 2-argument constructor (side, name) passing them to Rectangle. What does the given main print?

**Answer:**

```cpp
#include <iostream>
#include <string>
using namespace std;

class Shape {
protected:
    string name;
public:
    Shape(string n) : name(n) {}
    virtual void print() { cout << "Shape: " << name << endl; }
    virtual double area() = 0;
    virtual ~Shape() {}
};

class Rectangle : public Shape {
protected:
    double length, width;
public:
    Rectangle(double l, double w, string n) : Shape(n), length(l), width(w) {}
    void print() override {
        cout << name << " with length " << length << " and width " << width << endl;
    }
    double area() override {
        cout << "Area of " << name << " = " << length * width << endl;
        return length * width;
    }
};

class Square : public Rectangle {
    double side;
public:
    Square(double s, string n) : Rectangle(s, s, n), side(s) {}
    void print() override { cout << name << " with side " << side << endl; }
    double area() override {
        cout << "Area of " << name << " = " << side * side << endl;
        return side * side;
    }
};

int main() {
    Shape* myShape = new Rectangle(4, 2, "Rectangle");
    Rectangle* myRectangle = new Square(5, "Square");
    myShape->area();
    myShape->print();
    myRectangle->area();
    myRectangle->print();
    delete myShape;
    delete myRectangle;
    return 0;
}
```

```text
Area of Rectangle = 8
Rectangle with length 4 and width 2
Area of Square = 25
Square with side 5
```

**Every call runs the actual object's version, because print and area are virtual.** The question doesn't say print is virtual. If it isn't, `myShape->print()` prints `Shape: Rectangle` instead, so add that as a one-line note.

> **PYQ, Sessional-2 2023 Q1(b), 1 mark.** Class Element: no data members, `void print()` (virtual) and `double norm()` (pure virtual), a default constructor and destructor. Can you create an Element object?

**Answer:**

```cpp
class Element {
public:
    Element() {}
    virtual ~Element() {}
    virtual void print() { cout << "Element" << endl; }
    virtual double norm() = 0;          // pure virtual
};
```

**No. norm() is pure virtual, so Element is abstract and** `Element e;` **is a compile error.** `Element* p;` **is fine.**

> **PYQ, Sessional-2 2023 Q1(c), 3 marks.** Class PointND, a public child of Element, with one data member, a pointer to double. Give a default constructor, a constructor that copies a double array of size aSize, and a destructor.

**Answer:** print and norm need the size, so state that assumption and add `size`. The **norm** of a point is its distance from the origin, the square root of the sum of squares.

```cpp
#include <iostream>
#include <cmath>
using namespace std;

// class Element from Q1(b) goes here

class PointND : public Element {
    double* data;
    int size;
public:
    PointND() : data(nullptr), size(0) {}
    PointND(const double arr[], int aSize) : size(aSize) {
        data = new double[size];                     // its own copy of the values
        for (int i = 0; i < size; i++) data[i] = arr[i];
    }
    ~PointND() { delete[] data; }
    void print() override {
        cout << "(";
        for (int i = 0; i < size; i++) cout << data[i] << (i < size - 1 ? ", " : "");
        cout << ")" << endl;
    }
    double norm() override {
        double s = 0;
        for (int i = 0; i < size; i++) s += data[i] * data[i];
        return sqrt(s);
    }
};

int main() {
    double someData[3] = {1, 2, 3};
    Element* anElementPtr = new PointND(someData, 3);
    anElementPtr->print();
    cout << anElementPtr->norm() << endl;
    delete anElementPtr;
    return 0;
}
```

```text
(1, 2, 3)
3.74166
```

That's the square root of 14. **PointND must override norm(), or it stays abstract.**

> **PYQ, Sessional-2 2023 Q2(a), 2.5 marks.** Does `Element* anElementPtr = new PointND(someData, 3); delete anElementPtr;` compile and run cleanly in C++? What about similar code in Java?

**Answer:** **C++: it compiles, but runs cleanly only if Element's destructor is virtual.** If it isn't, `delete` runs only `~Element()`, PointND's array is never freed (a **memory leak**), and formally it's **undefined behaviour**, meaning C++ promises nothing. The virtual `~Element()` above fixes it.

**Java: this exact code won't compile**, since Java has no pointers and no `delete`. You'd write `Element e = new PointND(someData, 3);`, and the garbage collector (Java's automatic memory cleaner) frees the object once nothing refers to it, so the leak can't happen.

## Stop 7: Virtual destructors and the rules

Delete a derived object through a base pointer when the base destructor isn't virtual, and only the base destructor runs, so whatever the child allocated is never freed. A **virtual destructor** makes `delete` start at the real object's destructor and work up the chain. **If a class has any virtual function, give it a virtual destructor.**

> **PYQ, Sessional-2 2022 Q3(c), 1 mark.** Explain the virtual destructor with an example.

**Answer:**

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual ~Base() { cout << "Base destructor\n"; }
};

class Derived : public Base {
    int* arr;
public:
    Derived() { arr = new int[100]; }
    ~Derived() { delete[] arr; cout << "Derived destructor\n"; }
};

int main() {
    Base* p = new Derived;
    delete p;
    return 0;
}
```

```text
Derived destructor
Base destructor
```

**Without** `virtual`**, only "Base destructor" prints and the 100 ints leak.** Constructors can't be virtual; destructors can and should be.

> **PYQ, Endsem 2022 Q3(c)(i), 3 marks.** What are pure virtual functions? What rules apply to virtual functions?

**Answer:** Pure virtual functions are in Stop 6. The rules:

1. It must be a **member** of a class, not static and not a friend.
2. You call it through a **base pointer or reference** for run-time behaviour. Called on an object directly, it binds at compile time.
3. Base and child prototypes must be **identical** (name, parameters, const). Anything else is a new function, not an override.
4. It must be **defined** in the base, unless it's pure (`= 0`).
5. **Constructors can't be virtual**; destructors can.
6. Once virtual, it **stays virtual** in every child, keyword or not.
7. A base pointer can point to a child object, not the other way round.
8. If a child doesn't redefine it, the base version runs.

**Same skeleton, Endsem 2022 Q3(a), 6 marks (graphics hierarchy):** abstract Figure with children Close and Open, then Polygon and Ellipse from Close, Line and Polyline from Open, and three Polygon objects. Draw the tree first, since it's worth marks on its own:

```text
                  Figure (abstract)
                 /                 \
            Close                   Open
           /     \                 /    \
     Polygon    Ellipse         Line   Polyline
```

Figure gets `virtual void draw() = 0;` and a virtual destructor. Close and Open don't override draw, so **they stay abstract too**, and only the four leaf classes can have objects. Each leaf overrides draw. Give every class a constructor and destructor that print a line, exactly like the Stop 3 chain, and main makes `Polygon triangle(3), rectangle(4), pentagon(5);` and calls `draw()` on each through a `Figure*`.

That's Unit 3. If you can write the virtual base class program and the bank chain without looking, you've covered most of three endsems' Q3. Top up the tea.
