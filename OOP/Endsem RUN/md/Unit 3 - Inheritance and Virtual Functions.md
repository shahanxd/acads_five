# OOP Unit 3: Inheritance and Virtual Functions (C++)

*Endsem RUN · about 60 minutes*

**The whole unit in one breath:** inheritance lets a new class reuse an old one ("a Car *is a* Vehicle"), and virtual functions make sure that when you hold a child through a parent pointer, the *child's* version of a function still runs.

**What the endsem asks from here:** a multilevel or multiple inheritance program with constructor chaining (4.5 to 6 marks), the diamond problem / virtual base class (asked in 2021, 2022 and 2025), and theory on virtual functions, abstract classes and binding. The 2025 Q3 also slipped in C++ templates, so they're at the end.

---

## 1. What inheritance is · Quick

You don't write a `Car` class from scratch: a car is a vehicle, so it should automatically get wheels, speed and `start()`, then add its own bits like `airbags`.

**Exam line:** *Inheritance is the mechanism by which a new class (derived/child class) acquires the data members and member functions of an existing class (base/parent class), allowing code reuse and an "is-a" relationship.*

```cpp
class Derived : access-mode Base { ... };
```

### What the access mode does

The access mode (public / protected / private) decides what the inherited members become **inside the child**. Private members of the base are never directly accessible in the child, whatever the mode.

| Base member | `public` inheritance | `protected` inheritance | `private` inheritance |
| --- | --- | --- | --- |
| public | public | protected | private |
| protected | protected | protected | private |
| private | not accessible | not accessible | not accessible |

Easy way to remember: the mode is a **ceiling**. Nothing comes through more open than the mode. Public inheritance is what you'll use 95% of the time.

---

## 2. Five forms of inheritance · Quick

| Form | Shape | Example |
| --- | --- | --- |
| Single | A → B | Vehicle → Car |
| Multiple | A, B → C | Teacher + Researcher → Professor |
| Multilevel | A → B → C | Person → Employee → Manager |
| Hierarchical | A → B, A → C | Shape → Circle, Shape → Square |
| Hybrid | a mix, e.g. hierarchical + multiple | the diamond below |

```cpp
class C : public A, public B { };   // multiple: list the bases with commas
```

---

## 3. Constructors and destructors in a chain · Slow down

When you create a child object, the parent part gets built first, like the ground floor before the first floor. Destruction goes the other way: top floor first.

- **Constructors:** base first, then derived (for multiple inheritance, in the order the bases are *listed* in the class header).
- **Destructors:** reverse order: derived first, then base.
- **Passing values up:** the child's constructor passes arguments to the parent's constructor through the **initializer list**:

```cpp
Derived(int a, int b) : Base(a), y(b) { }
```

If you don't call a base constructor, the base's **default** constructor runs, so it must exist.

> **Endsem 2025 · Q3(b) · 4.5 marks**
> Design a C++ program using multilevel inheritance to manage hotel guest information. Base class Guest has name and phone with functions to input and display. Boarder (from Guest) adds roomNo and tariff with input/display. LongStay (from Boarder) adds contractNo and discountPercent with input/display. Implement both default and parameterized constructors with proper constructor chaining.

**Answer.**

Multilevel means Guest → Boarder → LongStay. "Constructor chaining" means each parameterized constructor passes the parent's share of the values up through its initializer list, and each `display()` calls its parent's `display()` first so nothing is repeated.

```cpp
#include <iostream>
#include <string>
using namespace std;

class Guest {
protected:
    string name, phone;
public:
    Guest() : name("Unknown"), phone("-") { cout << "Guest()\n"; }
    Guest(string n, string p) : name(n), phone(p) { cout << "Guest(n, p)\n"; }
    void input()   { cout << "Name and phone: "; cin >> name >> phone; }
    void display() { cout << "Name: " << name << ", Phone: " << phone << endl; }
};

class Boarder : public Guest {
protected:
    int roomNo;
    double tariff;
public:
    Boarder() : Guest(), roomNo(0), tariff(0) { cout << "Boarder()\n"; }
    Boarder(string n, string p, int r, double t) : Guest(n, p), roomNo(r), tariff(t) {
        cout << "Boarder(...)\n";
    }
    void input()   { Guest::input(); cout << "Room and tariff: "; cin >> roomNo >> tariff; }
    void display() { Guest::display(); cout << "Room: " << roomNo << ", Tariff: " << tariff << endl; }
};

class LongStay : public Boarder {
    int contractNo;
    double discountPercent;
public:
    LongStay() : Boarder(), contractNo(0), discountPercent(0) { cout << "LongStay()\n"; }
    LongStay(string n, string p, int r, double t, int c, double d)
        : Boarder(n, p, r, t), contractNo(c), discountPercent(d) { cout << "LongStay(...)\n"; }
    void input()   { Boarder::input(); cout << "Contract and discount: "; cin >> contractNo >> discountPercent; }
    void display() {
        Boarder::display();
        cout << "Contract: " << contractNo << ", Discount: " << discountPercent << "%"
             << ", Tariff after discount: " << tariff * (1 - discountPercent / 100) << endl;
    }
};

int main() {
    LongStay g("Aman", "9876543210", 204, 3000, 77, 20);
    g.display();
    LongStay blank;            // default chain
    blank.display();
}
```

Output:

```
Guest(n, p)
Boarder(...)
LongStay(...)
Name: Aman, Phone: 9876543210
Room: 204, Tariff: 3000
Contract: 77, Discount: 20%, Tariff after discount: 2400
Guest()
Boarder()
LongStay()
Name: Unknown, Phone: -
Room: 0, Tariff: 0
Contract: 0, Discount: 0%, Tariff after discount: 0
```

The print lines inside the constructors prove the chain runs **Guest → Boarder → LongStay**.

**Each parameterized constructor hands the parent's arguments up through the initializer list; each display calls the parent's display first.**

---

## 4. The diamond problem and virtual base classes · Slow down

Picture this family tree: `Student` at the top, `Test` and `Sports` both inherit from it, and `Result` inherits from both `Test` and `Sports`. That's a diamond.

Problem: `Result` now gets **two copies** of `Student` (one through each parent). Writing `roll` inside `Result` is **ambiguous**: which copy's `roll`? It's like a child with two copies of the same grandfather's surname, and nobody knows which to use.

**Fix:** make the middle classes inherit `virtual`ly. Then only **one** shared copy of `Student` exists.

**Exam line:** *A virtual base class is a base class declared with the keyword `virtual` in the inheritance list (`class B : virtual public A`), which ensures that only one copy of its members is inherited by a class that derives from it through multiple paths, removing the ambiguity of the diamond problem.*

> **Endsem 2025 · Q3(a) · 4.5 marks**
> Demonstrate the concept of virtual base class with the help of a suitable program.

**Answer.**

```cpp
#include <iostream>
using namespace std;

class Student {                                // grandparent
protected:
    int roll;
public:
    void setRoll(int r) { roll = r; }
};

class Test : virtual public Student {          // virtual: share Student
protected:
    int marks;
public:
    void setMarks(int m) { marks = m; }
};

class Sports : virtual public Student {        // virtual: share Student
protected:
    int score;
public:
    void setScore(int s) { score = s; }
};

class Result : public Test, public Sports {    // gets ONE Student
public:
    void show() {
        cout << "Roll: " << roll << endl;      // no ambiguity
        cout << "Total: " << marks + score << endl;
    }
};

int main() {
    Result r;
    r.setRoll(42);
    r.setMarks(80);
    r.setScore(15);
    r.show();
}
```

Output: `Roll: 42`, `Total: 95`.

Without `virtual` in `Test` and `Sports`, the line `cout << roll` fails to compile with "reference to 'roll' is ambiguous", because `Result` would hold two `roll`s.

```
        Student
        /     \
   Test         Sports      (both: virtual public Student)
        \     /
        Result               -> one shared Student
```

**`virtual` in the middle classes makes the grandparent's members appear only once in the bottom class, so there's no ambiguity.**

(Another fix for simple name clashes in multiple inheritance is the scope operator: `Test::roll`. But that still keeps two copies; only `virtual` removes the duplicate.)

---

## 5. Base pointers, and why virtual functions exist · Slow down

C++ lets a **base-class pointer point to a derived object**: `Shape* s = new Circle;`. Handy, because one array of `Shape*` can hold circles, squares, everything.

But there's a catch. Without `virtual`, `s->draw()` calls **Shape's** `draw`, because the compiler only looks at the pointer's type. That's called **early (static) binding**.

Mark the function `virtual`, and C++ waits until run time, checks what the pointer *actually* points to, and calls **Circle's** `draw`. That's **late (dynamic) binding**, and it's what run-time polymorphism means.

**Exam line:** *A virtual function is a member function declared with `virtual` in the base class and redefined (overridden) in derived classes; when called through a base pointer or reference, the version run is chosen at run time by the type of the actual object.*

```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    virtual void draw() { cout << "Shape\n"; }
    void info()         { cout << "I am a shape\n"; }   // not virtual
};
class Circle : public Shape {
public:
    void draw() override { cout << "Circle\n"; }
    void info()          { cout << "I am a circle\n"; }
};

int main() {
    Shape* s = new Circle;
    s->draw();   // Circle        (virtual: late binding)
    s->info();   // I am a shape  (not virtual: early binding)
    delete s;
}
```

How it works under the hood (a 1-line bonus): each class with virtual functions has a **vtable** (table of function addresses), and each object carries a hidden **vptr** to its class's vtable.

| Early (static) binding | Late (dynamic) binding |
| --- | --- |
| Decided at compile time | Decided at run time |
| By pointer/variable type | By actual object type |
| Normal functions, overloading | Virtual functions |
| Faster | Slightly slower (vtable lookup) |

**Rules for virtual functions:** must be members (not static, not friend); accessed through a base pointer or reference to get polymorphism; the override must have the same signature; constructors can't be virtual, but destructors can (and often should be); if not overridden, the base version is used.

---

## 6. Overriding vs overloading · Quick

| | Overloading | Overriding |
| --- | --- | --- |
| Where | Same class (same scope) | Base and derived class |
| Signature | Must differ | Must be the same |
| Binding | Compile time | Run time (with `virtual`) |
| Purpose | Same action on different inputs | Child changes parent's behaviour |

---

## 7. Pure virtual functions and abstract classes · Slow down

Sometimes the base class has no sensible version of a function. What's the `area()` of a generic "Shape"? There's no answer. So you declare it with `= 0`, which says: "every child **must** provide this".

**Exam line:** *A pure virtual function is a virtual function with no body in the base class, declared as `virtual void f() = 0;`. A class with at least one pure virtual function is an abstract class: it cannot be instantiated, and serves only as a base whose derived classes must override the pure virtual functions.*

```cpp
#include <iostream>
using namespace std;

class Shape {                                   // abstract
public:
    virtual double area() = 0;                  // pure virtual
    virtual ~Shape() {}
};
class Rect : public Shape {
    double l, b;
public:
    Rect(double x, double y) : l(x), b(y) {}
    double area() override { return l * b; }
};
class Circle : public Shape {
    double r;
public:
    Circle(double x) : r(x) {}
    double area() override { return 3.14159 * r * r; }
};

int main() {
    // Shape s;                                 // error: cannot create an abstract object
    Shape* shapes[] = { new Rect(4, 2), new Circle(1) };
    for (Shape* s : shapes) { cout << s->area() << endl; delete s; }
}
```

Output: `8` then `3.14159`. One loop, different behaviour per object: that's run-time polymorphism in one picture.

If a derived class doesn't override every pure virtual function, it is abstract too.

---

## 8. Virtual destructors · Quick

If you `delete` a child object through a base pointer and the base destructor **isn't** virtual, only the base destructor runs. The child's destructor never runs, so anything it allocated leaks.

```cpp
class Base { public: virtual ~Base() { cout << "~Base\n"; } };
class Derived : public Base {
    int* p = new int[100];
public:
    ~Derived() { delete[] p; cout << "~Derived\n"; }
};
// Base* b = new Derived; delete b;   prints ~Derived then ~Base (only because ~Base is virtual)
```

**Rule:** any class meant to be used polymorphically should have a virtual destructor.

---

## 9. Templates (asked in 2025 Q3c) · Quick

A **template** lets you write code once and use it with any type. The compiler generates a separate version for each type you actually use.

> **Endsem 2025 · Q3(c) · 4.5 marks**
> Differentiate between class templates and function templates. Design a template-based C++ function to sort arrays of any data type, working for int, float and char, illustrating generic programming.

**Answer.**

| | Function template | Class template |
| --- | --- | --- |
| What it makes generic | One function | A whole class (data + functions) |
| Syntax | `template <class T> void f(T x)` | `template <class T> class Stack { T a[10]; };` |
| Type given | Usually **deduced** from the arguments: `f(5)` | Written explicitly: `Stack<int> s;` |
| Example | `swap`, `max`, `sort` | `Stack<T>`, `Array<T>`, `Pair<T1, T2>` |

Both are **generic programming**: one piece of code that works for many types, with type checking at compile time.

```cpp
#include <iostream>
using namespace std;

template <class T>
void sortArray(T a[], int n) {                 // bubble sort for any type with <
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1 - i; j++)
            if (a[j + 1] < a[j]) { T t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; }
}

template <class T>
void print(T a[], int n) {
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    cout << endl;
}

int main() {
    int   x[] = {5, 2, 9, 1};        sortArray(x, 4); print(x, 4);
    float y[] = {2.5f, 1.1f, 3.3f};  sortArray(y, 3); print(y, 3);
    char  z[] = {'d', 'a', 'c', 'b'}; sortArray(z, 4); print(z, 4);
}
```

Output: `1 2 5 9`, `1.1 2.5 3.3`, `a b c d`.

**A function template generalises one function and deduces T from the call; a class template generalises a class and needs `<type>` written out. One `sortArray<T>` sorts ints, floats and chars.**

---

## 10. Quick recap

- Access mode is a ceiling; base private members are never directly accessible.
- Constructors: base → derived (pass args via the initializer list). Destructors: reverse.
- Diamond = two copies of the grandparent; `virtual` inheritance keeps one.
- Base pointer + virtual function = late binding = the child's version runs.
- `= 0` makes a pure virtual function; any class with one is abstract (no objects).
- Polymorphic base class → virtual destructor.
- Function template: T deduced. Class template: `Name<type>` written.
