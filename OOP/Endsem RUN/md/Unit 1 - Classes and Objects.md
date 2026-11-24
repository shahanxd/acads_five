# OOP Unit 1: Classes and Objects (C++)

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** a class is a blueprint, an object is the thing built from it, and every feature in this unit is about controlling *how* objects are made, used, shared and destroyed.

**What the endsem asks from here:** one full C++ class program with a real-life scenario (4.5 marks), plus short theory on access specifiers, constructors, inline, static and `this`. The 2025 paper's whole Q1 came from this unit.

Each topic is tagged **Quick** (read once, it's easy marks) or **Slow down** (where people lose marks).

---

## 1. What OOP is, and why it exists · Quick

Imagine a college where every student's marks sit in one big shared Excel sheet that anyone can edit. One wrong click and someone's CGPA is gone. That's **procedural programming**: data lies around in the open, and functions grab and change it.

**Object-oriented programming** fixes this by giving each piece of data an owner. A `Student` object keeps its own marks, and only its own functions are allowed to change them.

**Exam line:** *Object-oriented programming is a paradigm that organises a program around objects, where each object bundles data (attributes) with the functions (methods) that operate on that data.*

The four pillars, each in one line with an example:

| Pillar | Plain meaning | Example |
| --- | --- | --- |
| **Encapsulation** | Data and its functions are packed together, and the data is hidden | `balance` is private; you can only use `deposit()` |
| **Abstraction** | Show what it does, hide how | You call `sort()` without knowing the algorithm |
| **Inheritance** | A new class reuses an old one | `Car` is a `Vehicle`, so it gets wheels for free |
| **Polymorphism** | One name, many behaviours | `area()` works differently for `Circle` and `Square` |

### Structured vs object-oriented development

| Basis | Structured (procedural) | Object-oriented |
| --- | --- | --- |
| Built around | Functions | Objects |
| Design | Top-down: break the task into functions | Bottom-up: find the objects first |
| Data | Global, any function can change it | Hidden inside objects |
| Reuse | Copy-paste functions | Inheritance and templates |
| Change | One change ripples everywhere | Change stays inside one class |
| Example | C | C++, Java |

**Merits of OOP:** reuse (inheritance), security (data hiding), easier maintenance (changes stay local), models the real world naturally, scales to big teams.

**Demerits:** bigger and slightly slower programs, a steeper learning curve, and overkill for tiny programs (you don't need a `Calculator` class to add two numbers).

---

## 2. Class and object · Quick

A **class** is the blueprint, like the architect's drawing of a flat. An **object** is an actual flat built from it. One drawing, many flats, each with its own furniture (data).

**Exam line:** *A class is a user-defined data type that groups data members and member functions. An object is an instance of a class; memory is allocated only when an object is created.*

```cpp
#include <iostream>
using namespace std;

class Student {            // the blueprint
    int roll;              // data members (private by default)
    float marks;
public:
    void set(int r, float m) { roll = r; marks = m; }   // defined inside: automatically inline
    void show();                                        // only declared here
};

void Student::show() {     // defined outside using :: (scope resolution operator)
    cout << roll << " " << marks << endl;
}

int main() {
    Student s1, s2;        // two objects, each with its own roll and marks
    s1.set(1, 88.5);
    s1.show();
}
```

Two ways to define a member function: **inside** the class (short functions; these become inline automatically) or **outside** with `ClassName::function` (the usual way for longer ones).

**Empty class:** a class with no members, `class E {};`. Its objects still take **1 byte**, so that two different objects never share the same address.

---

## 3. Access specifiers and data hiding · Slow down

This exact question was Endsem 2025 Q1(a). Think of a house:

- **private:** your bedroom. Only you (the class itself) can go in.
- **protected:** the family room. You and your kids (derived classes) can go in.
- **public:** the front porch. Anyone can come.

In a `class`, members are **private by default**; in a `struct` they are public by default.

**Data hiding** means keeping data private and letting the outside world touch it only through public functions. Why bother? Because the function can check the value first, so nobody can set `marks = -500`.

> **Endsem 2025 · Q1(a) · 4.5 marks**
> How do private, public, and protected access modifiers control data hiding and accessibility in OOP? Explain their differences with an example, demonstrating access from within and outside a class in C++.

**Answer.**

Access specifiers decide *who* may use a class member. They are the tool that makes data hiding possible: data is kept private, and only chosen functions are made public.

| Specifier | Same class | Derived class | Outside (e.g. `main`) |
| --- | --- | --- | --- |
| `private` | Yes | No | No |
| `protected` | Yes | Yes | No |
| `public` | Yes | Yes | Yes |

```cpp
#include <iostream>
using namespace std;

class Account {
private:
    double balance = 1000;            // hidden: only Account's own functions can touch it
protected:
    int branchCode = 42;              // visible to Account and its children
public:
    void deposit(double amt) {        // public door into the private data
        if (amt > 0) balance += amt;  // inside the class: private is allowed
    }
    double getBalance() { return balance; }
};

class Savings : public Account {
public:
    void showBranch() {
        cout << "Branch: " << branchCode << endl;   // protected: allowed in a child
        // cout << balance;                          // error: private is not inherited access
    }
};

int main() {
    Account a;
    a.deposit(500);                   // public: allowed outside
    cout << a.getBalance() << endl;   // 1500
    // a.balance = 0;                 // error: private
    // a.branchCode = 1;              // error: protected
    Savings s;
    s.showBranch();                   // Branch: 42
}
```

Output: `1500` and `Branch: 42`.

**private hides data from everyone except the class; protected also lets derived classes in; public opens it to all. Keeping data private and exposing public functions is data hiding.**

---

## 4. Inline functions · Quick

A normal function call has a small cost: jump to the function, set up the stack, jump back. For a one-line function, that overhead can cost more than the work itself.

**Exam line:** *An inline function is a function whose body the compiler may substitute at the point of call, removing the function-call overhead. It is requested with the keyword `inline`.*

```cpp
inline int square(int x) { return x * x; }
// cout << square(5);   becomes, in effect,   cout << 5 * 5;
```

It is only a **request**: the compiler ignores it for functions with loops, recursion, `static` variables or big bodies. Member functions defined inside the class are inline automatically.

---

## 5. Constructors and destructors · Slow down

A **constructor** is the "setup crew" that runs automatically the moment an object is born. A **destructor** is the "cleanup crew" that runs when it dies.

**Exam line:** *A constructor is a special member function with the same name as the class and no return type, called automatically when an object is created, to initialise it. A destructor (`~ClassName`) is called automatically when the object goes out of scope, to release resources.*

Rules worth a mark each: same name as the class; no return type (not even `void`); can be overloaded; should be public; a destructor takes no arguments and can't be overloaded.

| Type | What it does | Example |
| --- | --- | --- |
| Default | No arguments | `Point() { x = y = 0; }` |
| Parameterized | Takes values | `Point(int a, int b) { x = a; y = b; }` |
| Copy | Makes a new object from an existing one | `Point(const Point& p) { x = p.x; y = p.y; }` |
| Dynamic | Allocates memory with `new` inside | see below |

**Constructor overloading** = having several of these in one class; the compiler picks one by the arguments you pass.

**Dynamic initialization** = the initial value is worked out at run time, e.g. `Point p(a + b, rand());`.

### Copy constructor: why the parameter must be a reference

If it took the object **by value**, passing the argument would itself need a copy, which calls the copy constructor again, which needs another copy… infinite recursion. So it is always `ClassName(const ClassName& obj)`. This was a 2023 endsem question.

It is called when: an object is initialised from another (`Point b = a;`), an object is passed by value, or an object is returned by value.

### Order of calls

Constructors run in the order objects are created; destructors run in the **reverse** order (last made, first destroyed, like a stack of plates).

> **Endsem 2025 · Q1(c) · 4.5 marks**
> Explain with example code: (i) Inline function, (ii) Dynamic constructor, (iii) Return by reference.

**Answer.**

**(i) Inline function:** the compiler pastes the function body at each call, saving the call overhead. Good for tiny, frequently called functions.

**(ii) Dynamic constructor:** a constructor that allocates memory at run time using `new`, so each object gets exactly the memory it needs. It must be paired with a destructor that frees it with `delete`.

**(iii) Return by reference:** the function returns the variable itself (an alias), not a copy. So the call can even appear on the left of `=`.

```cpp
#include <iostream>
#include <cstring>
using namespace std;

inline int square(int x) { return x * x; }          // (i)

class Name {                                         // (ii)
    char* s;
public:
    Name(const char* t) {
        s = new char[strlen(t) + 1];                 // memory sized at run time
        strcpy(s, t);
    }
    ~Name() { delete[] s; }                          // free it
    void show() { cout << s << endl; }
};

int& bigger(int& a, int& b) { return a > b ? a : b; }   // (iii)

int main() {
    cout << square(5) << endl;     // 25
    Name n("Jamia");
    n.show();                      // Jamia
    int x = 3, y = 7;
    bigger(x, y) = 100;            // assigns to y itself
    cout << x << " " << y << endl; // 3 100
}
```

Output: `25`, `Jamia`, `3 100`.

One warning examiners like: never return a reference to a local variable, since it dies when the function ends.

**Inline removes call overhead, a dynamic constructor allocates memory with new, and return by reference returns the variable itself so it can be assigned to.**

---

## 6. Static members · Slow down

Normal data members are per object: every student has their own `marks`. A **static** data member is shared by the whole class, like the class's notice board. There's only one copy, no matter how many objects exist.

**Exam line:** *A static data member is shared by all objects of a class, has one copy, and must be defined once outside the class. A static member function belongs to the class, can access only static members, and is called as `ClassName::function()` without any object.*

Classic use: counting how many objects exist, by bumping the count in the constructor and dropping it in the destructor.

```cpp
#include <iostream>
using namespace std;

class Vehicle {
    static int count;                    // declaration (one shared copy)
public:
    Vehicle()  { count++; }
    ~Vehicle() { count--; }
    static int getCount() { return count; }   // no 'this', so only static members
};
int Vehicle::count = 0;                  // definition outside the class: required

int main() {
    Vehicle a, b;
    { Vehicle c; cout << Vehicle::getCount() << endl; }   // 3
    cout << Vehicle::getCount() << endl;                   // 2 (c was destroyed)
}
```

Output: `3` then `2`. This is "static data members with constructors and destructors" from the syllabus.

---

## 7. Objects as arguments, returning objects · Quick

Objects can be passed to functions like any variable: **by value** (a copy; changes don't affect the original), **by reference** (the original; cheap and can change it) or **by pointer**. A function can also **return** an object.

```cpp
class Time {
    int h, m;
public:
    Time(int a = 0, int b = 0) : h(a), m(b) {}
    Time add(const Time& t) {            // object as argument
        Time r;                          // object returned
        r.m = m + t.m;
        r.h = h + t.h + r.m / 60;
        r.m %= 60;
        return r;
    }
    void show() { cout << h << ":" << m << endl; }
};
// Time(2,45).add(Time(1,30)).show();   prints 4:15
```

---

## 8. `this`, pointers to objects, arrays of objects · Quick

- **`this`** is a hidden pointer, inside every non-static member function, pointing to the object that called it. Its main use is telling a member apart from a parameter with the same name: `this->x = x;`. Static functions don't have it.
- **Pointer to object:** `Student* p = &s1; p->show();` (use `->` with pointers, `.` with objects). `new` makes an object at run time: `Student* p = new Student;` and later `delete p;`.
- **Array of objects:** `Student s[3];` makes three objects; use `s[i].show()` in a loop. The class needs a default constructor for this.

---

## 9. Scenario program · Slow down

This is the 4.5-mark question you should expect every year. The recipe never changes: private data, public functions, a `switch` menu inside a loop in `main`.

> **Endsem 2025 · Q1(b) · 4.5 marks**
> Design a C++ program for a Restaurant with a class Order with data members: order id, table number, food items ordered, total payable amount, current status (Pending / Preparing / Served / Billed / Cancelled). Member functions: `placeOrder()` inputs all details (default status "Pending"); `updateStatus()` changes status to an allowed value; `generateBill()` displays full order details. Implement a menu-driven interface.

**Answer.**

```cpp
#include <iostream>
#include <string>
using namespace std;

class Order {
    int orderId, tableNo;
    string items;
    double amount;
    string status;
public:
    Order() : orderId(0), tableNo(0), amount(0), status("Pending") {}

    void placeOrder() {
        cout << "Order id: ";        cin >> orderId;
        cout << "Table number: ";    cin >> tableNo;
        cin.ignore();
        cout << "Items ordered: ";   getline(cin, items);
        cout << "Total amount: ";    cin >> amount;
        status = "Pending";          // default status
    }

    void updateStatus() {
        string allowed[] = {"Pending", "Preparing", "Served", "Billed", "Cancelled"};
        string s;
        cout << "New status: ";  cin >> s;
        for (const string& a : allowed)
            if (s == a) { status = s; cout << "Status updated\n"; return; }
        cout << "Invalid status, unchanged\n";
    }

    void generateBill() {
        cout << "\n--- Bill ---\n"
             << "Order id: " << orderId << "\nTable: " << tableNo
             << "\nItems: " << items << "\nAmount: Rs " << amount
             << "\nStatus: " << status << "\n";
    }
};

int main() {
    Order o;
    int choice;
    do {
        cout << "\n1. Place order  2. Update status  3. Generate bill  4. Exit\nChoice: ";
        cin >> choice;
        switch (choice) {
            case 1: o.placeOrder();   break;
            case 2: o.updateStatus(); break;
            case 3: o.generateBill(); break;
            case 4: cout << "Bye\n";  break;
            default: cout << "Invalid choice\n";
        }
    } while (choice != 4);
}
```

Sample run: place order `101`, table `5`, `Paneer Tikka, Naan`, `450`; update to `Served`; generate bill → prints all five fields with status `Served`.

**The marks are in: private data, a constructor setting the default status, validation in updateStatus, and the do-while + switch menu.**

---

## 10. Quick recap

- Class = blueprint, object = instance; memory is allocated per object.
- private / protected / public = me / me and kids / everyone.
- Constructor: same name, no return type, auto-called; destructor `~`, reverse order.
- Copy constructor takes `const X&`, because by value would recurse forever.
- Static member: one shared copy, defined outside; static function has no `this`.
- Inline is a request to paste the body; return by reference returns the variable itself.
- Scenario program = private data + public functions + do-while/switch menu.
