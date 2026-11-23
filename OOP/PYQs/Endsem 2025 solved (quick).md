# OOP Endsem 2025, quick solutions

Short answers only. Attempt any two parts per question.

## Q1

**(a) Access modifiers.** `private`: only inside the class (data hiding). `protected`: the class + derived classes. `public`: everywhere. Default in a `class` is private.

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

**(b) Restaurant Order.**

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

**(c)**
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

**(a) Date with `++` and `<<`.**

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

**(b) Friend: reference vs value.** Pass by **reference** when the friend must change the object (or it's big, to avoid copying). Pass by **value** when it only reads a small object and must not change the original.

```cpp
class Loan;
class Account { double balance; public: Account(double b) : balance(b) {}
    friend void deductLoan(Account&, const Loan&); void show() { cout << balance << endl; } };
class Loan { double amount; public: Loan(double a) : amount(a) {}
    friend void deductLoan(Account&, const Loan&); };
void deductLoan(Account& a, const Loan& l) { a.balance -= l.amount; }   // Account by reference: it changes
int main() { Account a(10000); Loan l(2500); deductLoan(a, l); a.show(); }  // 7500
```

**(c) Matrix.**

```cpp
Matrix::Matrix() : rows(0), cols(0) {}
Matrix::Matrix(int r, int c) : rows(r), cols(c) {}
void Matrix::input() { for (int i=0;i<rows;i++) for (int j=0;j<cols;j++) cin >> mat[i][j]; }
void Matrix::display() { for (int i=0;i<rows;i++) { for (int j=0;j<cols;j++) cout << mat[i][j] << " "; cout << endl; } }
Matrix* Matrix::operator*(Matrix& b) {
    if (cols != b.rows) return nullptr;              // can't multiply
    Matrix* r = new Matrix(rows, b.cols);
    for (int i=0;i<rows;i++) for (int j=0;j<b.cols;j++) {
        r->mat[i][j] = 0;
        for (int k=0;k<cols;k++) r->mat[i][j] += mat[i][k] * b.mat[k][j];
    }
    return r;                                       // caller deletes it
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

**(a) Virtual base class.** Diamond: Test and Sports both inherit Student; Result inherits both, so it'd get two Students. `virtual` keeps one.

```cpp
class Student { protected: int roll = 0; };
class Test   : virtual public Student { protected: int marks = 80; };
class Sports : virtual public Student { protected: int score = 15; };
class Result : public Test, public Sports {
public: void show() { roll = 42; cout << roll << " " << marks + score; }  // no ambiguity
};
```

**(b) Hotel, multilevel with constructor chaining.**

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

**(c) Class vs function template.** A **function template** is one generic function (`template<class T> void f(T)`), type usually deduced from arguments. A **class template** is a generic class (`template<class T> class Stack`), type given explicitly (`Stack<int>`). Both are generic programming: one code, many types.

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

**(a) super.** Reaches the parent: `super(args)` calls the parent constructor (must be the first line), `super.method()` calls the parent's version of an overridden method, `super.field` gets a hidden parent field.

```java
class Person { String name; Person(String n) { name = n; }
    void display() { System.out.println("Name: " + name); } }
class Student extends Person { int roll;
    Student(String n, int r) { super(n); roll = r; }
    void display() { super.display(); System.out.println("Roll: " + roll); } }
```

**(b) Abstract vs interface vs concrete.**

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

**(c) Streaming subscribers.**

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

**(a) Generics.** Generics let a class or method take a type parameter (`List<String>`), so the compiler checks types. With plain `Object` you need casts, and a wrong type only fails at run time (`ClassCastException`); with generics it's a compile error, and no casts are needed.

`public static <T extends Comparable<T>> void sort_generics(T[] a)`: a generic static method for any type T, but **bounded**: T must implement `Comparable<T>`, so the method can call `a[i].compareTo(a[j])` to sort. Works for Integer, String, etc., not for types that can't be compared.

**(b) Quantity input with exceptions.**

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

**(c) Custom exception.**

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
