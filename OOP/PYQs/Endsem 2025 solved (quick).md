# OOP Endsem 2025, quick solutions

Short answers only. Paper: Endsem 2025-26, CSC-501, 3 hours, 45/60 marks. Attempt any two parts from each question; each part is 4.5/6 marks.

## Q1

> **Question:** How do private, public, and protected access modifiers control data hiding and accessibility in Object-Oriented Programming? Explain their differences with an example, demonstrating access from within and outside a class in C++.

**Answer (a) Access modifiers.** `private`: only inside the class (data hiding). `protected`: the class + derived classes. `public`: everywhere. Default in a `class` is private.

```cpp
class A {
private:   int x = 1;   // hidden
protected: int y = 2;   // kids can see
public:    int z = 3;   // anyone
    void show() { cout << x << y << z; }   // all OK inside
};
class B : public A { void f() { y = 5; /* x = 5; error */ } };
int main() { A a; a.z = 9; /* a.x, a.y: error */ }
```

> **Question:** Design a C++ program for a Restaurant by defining a class named *Order* with the following data members: order id, table number, food items ordered, total payable amount, and the current status of the order (Pending / Preparing / Served / Billed / Cancelled). Member functions: `placeOrder()` inputs and initializes all details (default status = "Pending"); `updateStatus()` modifies the status to one of the allowed values; `generateBill()` displays the complete order details. Implement a menu-driven interface that lets the user invoke any of the member functions.

**Answer (b) Restaurant Order.**

```cpp
#include <iostream>
#include <string>
using namespace std;

class Order {
    int id, table; string items; double amount; string status;
public:
    void placeOrder() {
        cout << "id table items amount: ";
        cin >> id >> table >> items >> amount;   // items as one word, e.g. Pizza,Coke
        status = "Pending";
    }
    void updateStatus() {
        string s; cout << "Pending/Preparing/Served/Billed/Cancelled: "; cin >> s;
        if (s=="Pending"||s=="Preparing"||s=="Served"||s=="Billed"||s=="Cancelled") status = s;
        else cout << "Invalid status\n";
    }
    void generateBill() {
        cout << "Order " << id << ", table " << table << ", items " << items
             << ", amount " << amount << ", status " << status << endl;
    }
};

int main() {
    Order o; int ch;
    do {
        cout << "1 Place  2 Update  3 Bill  4 Exit: "; cin >> ch;
        switch (ch) {
            case 1: o.placeOrder(); break;
            case 2: o.updateStatus(); break;
            case 3: o.generateBill(); break;
        }
    } while (ch != 4);
}
```

> **Question:** Explain the following C++ constructs with example code highlighting their functionality: (i) Inline function, (ii) Dynamic constructor, (iii) Return by reference.

**Answer (c)**
- **Inline function:** the compiler pastes the body at the call site, saving call overhead for tiny functions. `inline int sq(int x) { return x * x; }`
- **Dynamic constructor:** allocates memory with `new` inside the constructor.
  ```cpp
  class Str { char* p; public: Str(const char* s) { p = new char[strlen(s) + 1]; strcpy(p, s); } ~Str() { delete[] p; } };
  ```
- **Return by reference:** returns an alias, so the result can be assigned to.
  ```cpp
  int& bigger(int& a, int& b) { return a > b ? a : b; }
  bigger(x, y) = 0;   // sets the larger of x, y to 0
  ```

## Q2

> **Question:** Implement a class *Date* with three integer data members for day, month and year. Write the code needed so that this driver runs correctly:
>
> ```cpp
> int main() {
>     Date D1(28, 2, 2024);
>     Date D2(31, 12, 2023);
>     cout << "Original D1: " << D1 << endl;
>     cout << "Original D2: " << D2 << endl;
>     ++D1;
>     ++D2;
>     cout << "After Increment D1: " << D1 << endl;
>     cout << "After Increment D2: " << D2 << endl;
>     return 0;
> }
> ```

**Answer (a) Date with `++` and `<<`.**

```cpp
#include <iostream>
using namespace std;

class Date {
    int d, m, y;
    int days() {
        int md[] = {31,28,31,30,31,30,31,31,30,31,30,31};
        bool leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        return (m == 2 && leap) ? 29 : md[m - 1];
    }
public:
    Date(int dd, int mm, int yy) : d(dd), m(mm), y(yy) {}
    Date& operator++() {
        if (++d > days()) { d = 1; if (++m > 12) { m = 1; y++; } }
        return *this;
    }
    friend ostream& operator<<(ostream& os, const Date& t) {
        return os << t.d << "/" << t.m << "/" << t.y;
    }
};
// main as given: D1 28/2/2024 -> 29/2/2024 (leap), D2 31/12/2023 -> 1/1/2024
```

> **Question:** Explain the situations in which a friend function should take its arguments by reference, and those in which passing by value is more appropriate. Design two classes *Account* and *Loan* for a simple bank transaction system. Each account has a *balance*, and each loan has an *amount* to be deducted. Create a friend function `deductLoan(...)` that directly deducts the loan amount from the account balance.

**Answer (b) Friend: reference vs value.** Pass by **reference** when the friend must change the object (or it's big, to avoid copying). Pass by **value** when it only reads a small object and must not change the original.

```cpp
class Loan;
class Account { double balance; public: Account(double b) : balance(b) {}
    friend void deductLoan(Account&, const Loan&); void show() { cout << balance << endl; } };
class Loan { double amount; public: Loan(double a) : amount(a) {}
    friend void deductLoan(Account&, const Loan&); };
void deductLoan(Account& a, const Loan& l) { a.balance -= l.amount; }   // Account by reference: it changes
int main() { Account a(10000); Loan l(2500); deductLoan(a, l); a.show(); }  // 7500
```

> **Question:** Implement all functions of the following class to perform matrix operations:
>
> ```cpp
> class Matrix {
>     int mat[10][10];
>     int rows, cols;
> public:
>     Matrix();                       // Default constructor
>     Matrix(int r, int c);           // Parameterized constructor
>     void input();                   // Input matrix elements
>     void display();                 // Display matrix
>     Matrix operator*(Matrix &);     // Matrix multiplication
>     Matrix operator~();             // Transpose
>     bool operator==(Matrix &);      // Check equality
> };
> ```

**Answer (c) Matrix.**

```cpp
Matrix::Matrix() : rows(0), cols(0) {}
Matrix::Matrix(int r, int c) : rows(r), cols(c) {}
void Matrix::input() { for (int i=0;i<rows;i++) for (int j=0;j<cols;j++) cin >> mat[i][j]; }
void Matrix::display() { for (int i=0;i<rows;i++) { for (int j=0;j<cols;j++) cout << mat[i][j] << " "; cout << endl; } }
Matrix Matrix::operator*(Matrix& b) {
    if (cols != b.rows) { cout << "Can't multiply\n"; return Matrix(); }   // empty 0x0 matrix
    Matrix r(rows, b.cols);
    for (int i=0;i<rows;i++) for (int j=0;j<b.cols;j++) {
        r.mat[i][j] = 0;
        for (int k=0;k<cols;k++) r.mat[i][j] += mat[i][k] * b.mat[k][j];
    }
    return r;
}
Matrix Matrix::operator~() {
    Matrix t(cols, rows);
    for (int i=0;i<rows;i++) for (int j=0;j<cols;j++) t.mat[j][i] = mat[i][j];
    return t;
}
bool Matrix::operator==(Matrix& b) {
    if (rows != b.rows || cols != b.cols) return false;
    for (int i=0;i<rows;i++) for (int j=0;j<cols;j++) if (mat[i][j] != b.mat[i][j]) return false;
    return true;
}
```

## Q3

> **Question:** Demonstrate the concept of a virtual base class with the help of a suitable program.

**Answer (a) Virtual base class.** Diamond: Test and Sports both inherit Student; Result inherits both, so it'd get two Students. `virtual` keeps one.

```cpp
class Student { protected: int roll = 0; };
class Test   : virtual public Student { protected: int marks = 80; };
class Sports : virtual public Student { protected: int score = 15; };
class Result : public Test, public Sports {
public: void show() { roll = 42; cout << roll << " " << marks + score; }  // no ambiguity
};
```

> **Question:** Design a C++ program using multilevel inheritance to manage hotel guest information. Some customers stay for a short period, while others take long-stay contracts (with some discount). The base class *Guest* has data members *name* and *phone*, with functions to *input* and *display* guest details. The derived class *Boarder* (from Guest) adds *roomNo* and *tariff*, with functions to input and display room details. The derived class *LongStay* (from Boarder) adds *contractNo* and *discountPercent*, with functions to input and display contract details. Implement both default and parameterized constructors with proper constructor chaining.

**Answer (b) Hotel, multilevel with constructor chaining.**

```cpp
class Guest { protected: string name, phone;
public:
    Guest() : name("-"), phone("-") {}
    Guest(string n, string p) : name(n), phone(p) {}
    void input() { cin >> name >> phone; }
    void display() { cout << name << " " << phone << endl; } };

class Boarder : public Guest { protected: int roomNo; double tariff;
public:
    Boarder() : Guest(), roomNo(0), tariff(0) {}
    Boarder(string n, string p, int r, double t) : Guest(n, p), roomNo(r), tariff(t) {}
    void input() { Guest::input(); cin >> roomNo >> tariff; }
    void display() { Guest::display(); cout << roomNo << " " << tariff << endl; } };

class LongStay : public Boarder { int contractNo; double discountPercent;
public:
    LongStay() : Boarder(), contractNo(0), discountPercent(0) {}
    LongStay(string n, string p, int r, double t, int c, double d)
        : Boarder(n, p, r, t), contractNo(c), discountPercent(d) {}
    void input() { Boarder::input(); cin >> contractNo >> discountPercent; }
    void display() { Boarder::display(); cout << contractNo << " " << discountPercent << "%" << endl; } };

int main() { LongStay g("Aman", "98765", 204, 3000, 77, 20); g.display(); }
```

> **Question:** Differentiate between class templates and function templates. Design a template-based C++ function to sort arrays of any data type. It should work for types such as int, float and char, illustrating generic programming.

**Answer (c) Class vs function template.** A **function template** is one generic function (`template<class T> void f(T)`), type usually deduced from arguments. A **class template** is a generic class (`template<class T> class Stack`), type given explicitly (`Stack<int>`). Both are generic programming: one code, many types.

```cpp
template <class T>
void sortArr(T a[], int n) {
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) { T t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; }
}
int main() {
    int x[] = {5, 2, 9};       sortArr(x, 3);
    float y[] = {2.5, 1.1};    sortArr(y, 2);
    char z[] = {'d', 'a', 'c'}; sortArr(z, 3);
}
```

## Q4

> **Question:** Discuss the significance of the *super* keyword in Java briefly. Illustrate its use in calling parent class constructors and methods.

**Answer (a) super.** Reaches the parent: `super(args)` calls the parent constructor (must be the first line), `super.method()` calls the parent's version of an overridden method, `super.field` gets a hidden parent field.

```java
class Person { String name; Person(String n) { name = n; }
    void display() { System.out.println("Name: " + name); } }
class Student extends Person { int roll;
    Student(String n, int r) { super(n); roll = r; }
    void display() { super.display(); System.out.println("Roll: " + roll); } }
```

> **Question:** Differentiate between abstract class, interface, and concrete class, with example code snippets in Java.

**Answer (b) Abstract vs interface vs concrete.**

| | Concrete | Abstract | Interface |
| --- | --- | --- | --- |
| Objects with `new` | Yes | No | No |
| Abstract methods | None | 0 or more | All plain ones (+ default/static) |
| Fields | Any | Any | Only constants |
| Constructors | Yes | Yes | No |
| Inheritance | extends one | extends one | implements many |

```java
interface Drawable { void draw(); }
abstract class Shape implements Drawable { abstract double area(); }
class Square extends Shape { double s = 3;
    double area() { return s * s; }
    public void draw() { System.out.println("Square"); } }
```

> **Question:** Design a Java program to manage premium subscriber information for an online streaming platform, using inheritance. The base class *Subscriber* has *subscriberId* (int) and *name* (String), plus a static data member *platformName* (String). It has a constructor to set ID and name, and a static method `setPlatformName(String name)` to set the platform name for all subscribers. The derived class *PremiumSubscriber* adds *plan* (String) and *monthlyFee* (double), a constructor that initializes all attributes (including inherited ones), and a method to display details of subscribers whose monthlyFee exceeds Rs. 799. In `main()`, first set the platform name with the static method, then create an array of PremiumSubscriber objects with sample data, and display those whose monthly fee is greater than Rs. 799.

**Answer (c) Streaming subscribers.**

```java
class Subscriber {
    protected int subscriberId; protected String name;
    static String platformName;
    Subscriber(int id, String n) { subscriberId = id; name = n; }
    static void setPlatformName(String p) { platformName = p; }
}
class PremiumSubscriber extends Subscriber {
    String plan; double monthlyFee;
    PremiumSubscriber(int id, String n, String p, double f) { super(id, n); plan = p; monthlyFee = f; }
    void displayIfAbove799() {
        if (monthlyFee > 799)
            System.out.println(platformName + " " + subscriberId + " " + name + " " + plan + " " + monthlyFee);
    }
}
class Main {
    public static void main(String[] a) {
        Subscriber.setPlatformName("StreamMax");
        PremiumSubscriber[] s = { new PremiumSubscriber(1, "Aman", "Family", 999),
                                  new PremiumSubscriber(2, "Sara", "Mobile", 499),
                                  new PremiumSubscriber(3, "Kabir", "4K", 1299) };
        for (PremiumSubscriber p : s) p.displayIfAbove799();   // Aman, Kabir
    }
}
```

## Q5

> **Question:** Define Generics in Java and explain how they improve type safety compared with using Object references. Also explain the purpose of this line: `public static <T extends Comparable<T>> void sort_generics(T[] a)`

**Answer (a) Generics.** Generics let a class or method take a type parameter (`List<String>`), so the compiler checks types. With plain `Object` you need casts, and a wrong type only fails at run time (`ClassCastException`); with generics it's a compile error, and no casts are needed.

`public static <T extends Comparable<T>> void sort_generics(T[] a)`: a generic static method for any type T, but **bounded**: T must implement `Comparable<T>`, so the method can call `a[i].compareTo(a[j])` to sort. Works for Integer, String, etc., not for types that can't be compared.

> **Question:** In an online shopping application, the user enters the quantity of items to buy. Users may enter invalid input such as letters or symbols, or leave the field empty, crashing the program. Design a Java program that validates the input using exception handling: prompt for the quantity and use a *try-catch-finally* block. It should catch both *InputMismatchException* and *NumberFormatException* if the quantity is not a valid number, and show a message like "Invalid quantity! Please enter digits only." If the input is valid, display the quantity and finish gracefully.

**Answer (b) Quantity input with exceptions.**

```java
import java.util.*;
class Shop {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            System.out.print("Enter quantity: ");
            String s = sc.nextLine();
            int q = Integer.parseInt(s.trim());          // empty/letters -> NumberFormatException
            System.out.println("Quantity: " + q);
        } catch (InputMismatchException | NumberFormatException e) {
            System.out.println("Invalid quantity! Please enter digits only.");
        } finally {
            sc.close();
            System.out.println("Done.");
        }
    }
}
```

(`InputMismatchException` would come from `sc.nextInt()`; catching both covers either way of reading.)

> **Question:** Design a Java program to simulate a simple bank account system using custom exception handling. Define a class *BankAccount* with a method `withdraw(double amount)` that throws a user-defined *InsufficientBalanceException* when the amount exceeds the available balance. In `main()`, use a *try-catch* block to handle the exception and display suitable messages for both successful and unsuccessful withdrawals.

**Answer (c) Custom exception.**

```java
class InsufficientBalanceException extends Exception {
    InsufficientBalanceException(String m) { super(m); }
}
class BankAccount {
    double balance;
    BankAccount(double b) { balance = b; }
    void withdraw(double amt) throws InsufficientBalanceException {
        if (amt > balance) throw new InsufficientBalanceException("Insufficient balance: " + balance);
        balance -= amt;
        System.out.println("Withdrew " + amt + ", left " + balance);
    }
}
class Main {
    public static void main(String[] a) {
        BankAccount acc = new BankAccount(5000);
        try { acc.withdraw(2000); acc.withdraw(4000); }
        catch (InsufficientBalanceException e) { System.out.println(e.getMessage()); }
    }
}
// Withdrew 2000.0, left 3000.0
// Insufficient balance: 3000.0
```
