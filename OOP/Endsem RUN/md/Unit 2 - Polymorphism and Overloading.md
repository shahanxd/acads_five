# OOP Unit 2: Polymorphism and Overloading (C++)

*Endsem RUN · about 60 minutes*

**The whole unit in one breath:** overloading lets you teach C++ that `+`, `==`, `<<` or `[]` should mean something sensible for *your* class, so `d1 + d2` works on dates just like it works on ints.

**What the endsem asks from here:** "Here is a `main()`. Write the class so it runs." Every year. The 2025 paper's whole Q2 was this unit: a Date with `++` and `<<`, a friend function, and a Matrix with `*`, `~`, `==`.

**The one skill:** read the `main()` first and list every operator it uses. Each one is a function you must write.

---

## 1. Polymorphism · Quick

Polymorphism means **one name, many forms**. You say "open" to a door, a bottle and a laptop, and each does its own version of open.

**Exam line:** *Polymorphism is the ability of the same function or operator name to behave differently depending on the data or object it works on.*

| | Compile-time (static, early binding) | Run-time (dynamic, late binding) |
| --- | --- | --- |
| How | Function overloading, operator overloading | Virtual functions (Unit 3) |
| Decided by | Argument types, at compile time | Actual object type, while running |
| Speed | Faster | Slightly slower (vtable lookup) |

**Function overloading** = same name, different parameter list (number or types). Return type alone does **not** count.

```cpp
int    area(int s)            { return s * s; }        // square
int    area(int l, int b)     { return l * b; }        // rectangle
double area(double r)         { return 3.14 * r * r; } // circle
```

---

## 2. How operator overloading works · Slow down

Here's the secret: an operator is just a function with a funny name. When you write `a + b` for objects, C++ quietly calls `a.operator+(b)`.

**Exam line:** *Operator overloading gives an existing C++ operator an additional meaning for user-defined types, by defining a function named `operator<symbol>`.*

```cpp
ReturnType operator+(const ClassName& other);   // inside the class
```

**How many arguments?** The left operand is the object itself (`this`), so:

| Operator kind | As a member | As a friend |
| --- | --- | --- |
| Unary (`++`, `-`, `~`) | 0 arguments | 1 argument |
| Binary (`+`, `==`, `*`) | 1 argument | 2 arguments |

**Rules (each is a 1-mark point):**

- Can't overload: `::` `.` `.*` `?:` `sizeof`
- Must be members: `=` `[]` `()` `->`
- `<<` and `>>` must be **friends** (or non-members), because the left side is `cout`, which isn't your object.
- You can't invent new operators, change precedence, or change how many operands an operator takes.
- At least one operand must be a user-defined type (you can't redefine `int + int`).

---

## 3. Unary operators, and the `++` problem · Slow down

`++x` (prefix) and `x++` (postfix) are the same symbol, so how does C++ tell them apart? With a hack: the **postfix** version takes a dummy `int` parameter that's never used. This is the "limitation of overloading `++` and `--`" in the syllabus.

```cpp
Counter& operator++()     { ++count; return *this; }               // prefix: change, then return self
Counter  operator++(int)  { Counter old = *this; ++count; return old; }  // postfix: return the OLD value
```

Prefix returns a reference (the updated object); postfix returns a copy of the old value, which is why postfix is slightly slower.

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

---

## 4. Binary operators: arithmetic, relational, assignment · Slow down

The pattern for any binary operator, as a member: take the right operand as `const&`, build a result, return it.

```cpp
#include <iostream>
using namespace std;

class Product {
    int price;
public:
    Product(int p = 0) : price(p) {}
    Product operator+(const Product& o) const { return Product(price + o.price); }  // arithmetic
    bool operator>(const Product& o)  const { return price > o.price; }             // relational
    bool operator==(const Product& o) const { return price == o.price; }
    Product& operator=(const Product& o) { price = o.price; return *this; }       // assignment
    void display() const { cout << "Price: " << price << endl; }
};

int main() {
    Product p1(1000), p2(500), p4(1000);
    Product p3 = p1 + p2;
    p3.display();                                 // Price: 1500
    if (p1 > p2)  cout << "p1 costs more\n";
    if (p1 == p4) cout << "p1 equals p4\n";
}
```

Relational operators return `bool`. Assignment returns `*this` by reference so `a = b = c` works. (You only *need* to write `=` yourself when the class owns a pointer; otherwise the default copies fine.)

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

---

## 5. Subscript `[]`, and `new` / `delete` · Quick

`operator[]` lets your object be indexed like an array. Return a **reference** so it works on both sides of `=`, and add a bounds check (that's usually the point of the question).

```cpp
int& operator[](int i) {
    if (i < 0 || i >= size) { cout << "Index out of range\n"; exit(1); }
    return arr[i];
}
// a[2] = 50;  cout << a[2];
```

`new` and `delete` can be overloaded too, usually to log or track memory:

```cpp
void* operator new(size_t size) { cout << "Allocating " << size << " bytes\n"; return malloc(size); }
void  operator delete(void* p)  { cout << "Freeing\n"; free(p); }
```

---

## 6. Overloading through friend functions · Slow down

A **friend function** is not a member, but the class gives it permission to read private data. Think of it as giving a trusted friend a spare key to your house.

**Exam line:** *A friend function is a non-member function declared with the keyword `friend` inside a class; it can access the class's private and protected members, and is called like a normal function, without an object.*

When do you need one for overloading?

1. **`<<` and `>>`**, because the left operand is `cout`/`cin`.
2. When the **left operand isn't your object**: `2 * c` can't be a member of your class, since `2` is an int. A friend `operator*(int, const C&)` handles it.
3. When **one function needs private data of two classes** (like `deductLoan` below).

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

---

## 7. Data conversion between types · Slow down

Three directions. Learn which tool goes with which, since that is the whole question.

| Conversion | Tool | Example |
| --- | --- | --- |
| Basic → class | One-argument **constructor** | `Temp t = 300;` calls `Temp(float)` |
| Class → basic | **Conversion operator** `operator float()` | `float f = t;` |
| Class A → class B | Constructor in B taking A, **or** `operator B()` in A | `B b = a;` |

A conversion operator has **no return type** written and **no arguments**: its name already says what it returns.

```cpp
#include <iostream>
using namespace std;

class TempK {
    float k;
public:
    TempK(float v) : k(v) {}             // basic -> class
    operator float() const { return k; } // class -> basic
};

int main() {
    TempK t = 300;          // constructor
    float f = t;            // conversion operator
    TempK t2(102);
    f = t2;                 // operator float
    t2 = f;                 // constructor makes a temporary TempK
    cout << f << endl;      // 102
}
```

---

## 8. Memory leaks · Quick

A **memory leak** happens when memory taken with `new` is never given back with `delete`, so the program keeps eating RAM. Classic causes: a missing destructor in a class that uses `new`, losing the only pointer to a block, or using `delete` instead of `delete[]` for arrays.

**Tracing leaks:** count allocations and frees (for example by overloading `new`/`delete` to print or count), or use tools like Valgrind and AddressSanitizer. **Fix:** every `new` gets a matching `delete`, ideally in a destructor (or use smart pointers like `unique_ptr`).

---

## 9. Quick recap

- `a + b` is really `a.operator+(b)`. Member binary = 1 argument, friend binary = 2.
- Postfix `++` takes a dummy `int` and returns the old value.
- `<<` / `>>` must be friends and return the stream by reference.
- Can't overload `::` `.` `.*` `?:` `sizeof`.
- Basic→class: constructor. Class→basic: `operator type()`. Class→class: either.
- Friend arguments: by reference to modify, by value or const reference to read.
