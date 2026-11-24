# OOP Endsem 2025, Solved

**Paper:** B.Tech (CE) Sem V, Object Oriented Programming (CSC-501 / CEN-504 Old), 3 hours, 45/60 marks. Attempt any two parts from each question; each part is 4.5/6 marks.

Every question of the 2025 endsem paper, solved. The same answers sit inside the unit docs at the topic they belong to; the unit is named under each question so you can jump there for the explanation.

---

## Question 1

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

*Taught in Unit 1.*

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

*Taught in Unit 1.*

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

*Taught in Unit 1.*

---

## Question 2

> **Endsem 2025 · Q2(a) · 4.5 marks**
> Implement a class Date with three integer data members for day, month and year, so that this driver runs correctly:
> `Date D1(28, 2, 2024); Date D2(31, 12, 2023);` print both, then `++D1; ++D2;` and print both again.

**Answer.**

The paper only needs a constructor, prefix `++` and `<<`. But look at the dates: they're traps. 28/2/2024 is in a **leap year**, so the next day is 29/2, and 31/12/2023 must roll over the **year**. A lazy `d++` gives 29/2 by luck and 32/12/2023, which loses most of the marks.

```cpp
#include <iostream>
using namespace std;

class Date {
    int d, m, y;
    bool leap() const { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }
    int daysInMonth() const {
        int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        return (m == 2 && leap()) ? 29 : days[m - 1];
    }
public:
    Date(int a, int b, int c) : d(a), m(b), y(c) {}
    Date& operator++() {                       // prefix ++
        if (++d > daysInMonth()) {
            d = 1;
            if (++m > 12) { m = 1; y++; }
        }
        return *this;
    }
    friend ostream& operator<<(ostream& out, const Date& t) {   // friend: left side is cout
        return out << t.d << "/" << t.m << "/" << t.y;
    }
};

int main() {
    Date D1(28, 2, 2024);
    Date D2(31, 12, 2023);
    cout << "Original D1: " << D1 << endl;
    cout << "Original D2: " << D2 << endl;
    ++D1;
    ++D2;
    cout << "After Increment D1: " << D1 << endl;
    cout << "After Increment D2: " << D2 << endl;
    return 0;
}
```

Output:

```
Original D1: 28/2/2024
Original D2: 31/12/2023
After Increment D1: 29/2/2024
After Increment D2: 1/1/2024
```

**`<<` is a friend that returns `ostream&` so it can chain; `++` is a member with no argument that handles month-end, year-end and leap years.**

*Taught in Unit 2.*

> **Endsem 2025 · Q2(b) · 4.5 marks**
> Explain when a friend function should take arguments by reference and when passing by value is more appropriate. Design classes Account (balance) and Loan (amount) and a friend function `deductLoan(...)` that directly deducts the loan amount from the account balance.

**Answer.**

**Pass by reference** when the function must **change** the original object (here, the account's balance), or when the object is large and copying it would waste time and memory. Use `const&` if it only reads a large object.

**Pass by value** when the function only **reads** a small object and must not touch the original, because it works on a private copy. A wrong change can't leak back to the caller.

So in `deductLoan`, the `Account` goes **by reference** (its balance must really drop), while the `Loan` is only read, so it can go by value or, better, by `const` reference.

```cpp
#include <iostream>
using namespace std;

class Loan;                                   // forward declaration: Account mentions Loan first

class Account {
    double balance;
public:
    Account(double b) : balance(b) {}
    friend void deductLoan(Account& a, const Loan& l);
    void show() const { cout << "Balance: " << balance << endl; }
};

class Loan {
    double amount;
public:
    Loan(double a) : amount(a) {}
    friend void deductLoan(Account& a, const Loan& l);
};

void deductLoan(Account& a, const Loan& l) {   // friend of both: reads both privates
    if (l.amount <= a.balance) a.balance -= l.amount;
    else cout << "Insufficient balance\n";
}

int main() {
    Account acc(10000);
    Loan emi(2500);
    deductLoan(acc, emi);
    acc.show();                               // Balance: 7500
}
```

If `Account` were passed by value, the function would subtract from a copy, and the real balance would stay 10000. That's the bug the question is testing.

**By reference to modify (Account&), by value or const reference to only read (Loan); the friend is declared in both classes so it can reach both balances.**

*Taught in Unit 2.*

> **Endsem 2025 · Q2(c) · 4.5 marks**
> Implement all functions of this class: `int mat[10][10]; int rows, cols;` with `Matrix()`, `Matrix(int r, int c)`, `void input()`, `void display()`, `Matrix operator*(Matrix&)` (multiplication), `Matrix operator~()` (transpose), `bool operator==(Matrix&)` (equality).

**Answer.**

Three ideas carry the marks: multiplication needs **A's columns = B's rows**, and the result is rows(A) × cols(B); transpose swaps `[i][j]` into `[j][i]`; equality checks the **sizes first**, then every element.

```cpp
#include <iostream>
using namespace std;

class Matrix {
    int mat[10][10];
    int rows, cols;
public:
    Matrix() : rows(0), cols(0) {}
    Matrix(int r, int c) : rows(r), cols(c) {
        for (int i = 0; i < r; i++)
            for (int j = 0; j < c; j++) mat[i][j] = 0;   // zero it, so += below is safe
    }
    void input() {
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++) cin >> mat[i][j];
    }
    void display() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) cout << mat[i][j] << " ";
            cout << "\n";
        }
    }
    Matrix operator*(Matrix& b) {
        if (cols != b.rows) { cout << "Cannot multiply\n"; return Matrix(); }
        Matrix r(rows, b.cols);
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < b.cols; j++)
                for (int k = 0; k < cols; k++)
                    r.mat[i][j] += mat[i][k] * b.mat[k][j];
        return r;
    }
    Matrix operator~() {
        Matrix t(cols, rows);
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++) t.mat[j][i] = mat[i][j];
        return t;
    }
    bool operator==(Matrix& b) {
        if (rows != b.rows || cols != b.cols) return false;
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++)
                if (mat[i][j] != b.mat[i][j]) return false;
        return true;
    }
};

int main() {
    Matrix A(2, 2), B(2, 2);
    A.input();             // 1 2 3 4
    B.input();             // 5 6 7 8
    Matrix C = A * B;
    C.display();           // 19 22 / 43 50
    Matrix T = ~A;
    T.display();           // 1 3 / 2 4
    cout << (A == B ? "Equal" : "Not equal") << endl;
}
```

Check by hand:

```latex
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix} = \begin{bmatrix} 1\cdot5+2\cdot7 & 1\cdot6+2\cdot8 \\ 3\cdot5+4\cdot7 & 3\cdot6+4\cdot8 \end{bmatrix} = \begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}
```

**A × B = [[19, 22], [43, 50]], ~A = [[1, 3], [2, 4]], and A == B is false.**

*Taught in Unit 2.*

---

## Question 3

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

*Taught in Unit 3.*

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

*Taught in Unit 3.*

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

*Taught in Unit 3.*

---

## Question 4

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

*Taught in Unit 4.*

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

*Taught in Unit 4.*

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

*Taught in Unit 4.*

---

## Question 5

> **Endsem 2025 · Q5(a) · 4.5 marks**
> Define Generics in Java and explain how they improve type safety compared with using Object references. Also explain the purpose of: `public static <T extends Comparable<T>> void sort_generics(T[] a)`.

**Answer.**

**Generics** let a class, interface or method take a type as a parameter, like `ArrayList<String>`, so one piece of code works for many types.

**Type safety vs `Object`:** with `Object` references, anything can be stored, so the compiler can't check; you must cast when reading, and a wrong type fails only at **run time** with `ClassCastException`. With generics, the compiler knows the exact type, rejects wrong types at **compile time**, and no casts are needed.

**The line, piece by piece:**

| Part | Meaning |
| --- | --- |
| `public static` | Callable from anywhere without creating an object |
| `<T extends Comparable<T>>` | Declares a type parameter T, **bounded**: T must implement `Comparable<T>`, i.e. objects of T can be compared with each other |
| `void` | Returns nothing; it sorts the array in place |
| `sort_generics(T[] a)` | Takes an array of any such T |

**Purpose:** one sorting method that works for `Integer[]`, `String[]`, `Double[]` or any class that implements `Comparable`, because the bound guarantees that `a[i].compareTo(a[j])` exists. Passing an array of a non-comparable type is rejected **at compile time**.

```java
public class GenericSort {
    public static <T extends Comparable<T>> void sort_generics(T[] a) {
        for (int i = 0; i < a.length - 1; i++)
            for (int j = 0; j < a.length - 1 - i; j++)
                if (a[j].compareTo(a[j + 1]) > 0) {       // allowed only because of the bound
                    T t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                }
    }
    public static void main(String[] args) {
        Integer[] n = {5, 2, 9, 1};
        String[]  s = {"pear", "apple", "mango"};
        sort_generics(n);
        sort_generics(s);
        System.out.println(java.util.Arrays.toString(n));   // [1, 2, 5, 9]
        System.out.println(java.util.Arrays.toString(s));   // [apple, mango, pear]
    }
}
```

**Generics move type errors from run time to compile time and remove casts; the bound `T extends Comparable<T>` lets one method sort any type whose objects can be compared.**

*Taught in Unit 5.*

> **Endsem 2025 · Q5(b) · 4.5 marks**
> In an online shopping app, users enter the quantity of items to buy. They may enter alphabets, symbols, or leave it empty, which crashes the program. Design a Java program that validates the input using exception handling: prompt for the quantity, use a try-catch-finally block, catch both `InputMismatchException` and `NumberFormatException` for invalid numbers, show "Invalid quantity! Please enter digits only." for bad input, and for valid input display the quantity and finish gracefully.

**Answer.**

Which exception fires depends on how you read the input:

- `sc.nextInt()` throws **`InputMismatchException`** if the next token isn't an int (e.g. `abc`).
- `Integer.parseInt(text)` throws **`NumberFormatException`** if the text isn't a valid int, including the **empty string** (when the user just presses Enter).

Reading the whole line and parsing it handles the empty case, and catching both types covers either way of reading, exactly as the question asks.

```java
import java.util.InputMismatchException;
import java.util.Scanner;

public class QuantityInput {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            System.out.print("Enter quantity: ");
            String line = sc.nextLine().trim();          // "" if the user just hits Enter
            int qty = Integer.parseInt(line);            // "abc", "5$", "" -> NumberFormatException
            if (qty <= 0) throw new NumberFormatException("not positive");
            System.out.println("Quantity entered: " + qty);
        } catch (InputMismatchException | NumberFormatException e) {
            System.out.println("Invalid quantity! Please enter digits only.");
        } finally {
            sc.close();                                  // runs in every case
            System.out.println("Thank you for shopping.");
        }
    }
}
```

Runs:

| Input | Output |
| --- | --- |
| `5` | Quantity entered: 5 / Thank you for shopping. |
| `abc` | Invalid quantity! Please enter digits only. / Thank you for shopping. |
| `@#` | Invalid quantity! Please enter digits only. / Thank you for shopping. |
| *(empty)* | Invalid quantity! Please enter digits only. / Thank you for shopping. |

**try holds the risky read and parse, one multi-catch handles both exception types with the required message, and finally closes the Scanner whatever happens.**

*Taught in Unit 5.*

> **Endsem 2025 · Q5(c) · 4.5 marks**
> Design a Java program to simulate a simple bank account system using custom exception handling. Define a class BankAccount with a method `withdraw(double amount)` that throws a user-defined `InsufficientBalanceException` when the amount exceeds the available balance. In `main()`, use a try-catch block to handle it and display suitable messages for both successful and unsuccessful withdrawals.

**Answer.**

```java
class InsufficientBalanceException extends Exception {      // custom, checked
    InsufficientBalanceException(String message) {
        super(message);                                     // stored for getMessage()
    }
}

class BankAccount {
    private double balance;
    BankAccount(double balance) { this.balance = balance; }

    void withdraw(double amount) throws InsufficientBalanceException {   // declares it
        if (amount > balance)
            throw new InsufficientBalanceException(
                "Withdrawal of Rs " + amount + " failed: balance is only Rs " + balance);
        balance -= amount;
        System.out.println("Withdrawn Rs " + amount + ". Remaining balance: Rs " + balance);
    }
}

public class Main {
    public static void main(String[] args) {
        BankAccount acc = new BankAccount(5000);
        double[] requests = {2000, 4000, 1000};
        for (double amt : requests) {
            try {
                acc.withdraw(amt);
            } catch (InsufficientBalanceException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}
```

Output:

```
Withdrawn Rs 2000.0. Remaining balance: Rs 3000.0
Error: Withdrawal of Rs 4000.0 failed: balance is only Rs 3000.0
Withdrawn Rs 1000.0. Remaining balance: Rs 2000.0
```

The failed withdrawal doesn't crash the program; the next one still goes through. That's the whole point of handling.

**Extend Exception, pass the message to super, `throw` it inside withdraw (declared with `throws`), and catch it in main.**

*Taught in Unit 5.*

