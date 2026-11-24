# OOP Unit 5: Exception Handling and Generics in Java

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** exceptions are Java's way of saying "something went wrong, here's an object describing it, deal with it", and generics are Java's way of writing one class or method that works for any type while still catching type mistakes at compile time.

**What the endsem asks from here:** a try-catch-finally program for bad input, a custom exception program, and generics theory (why generics, bounded types, wildcards, type erasure). The 2025 paper's whole Q5 came from here. No old RUN doc covered this unit, so everything here is new.

---

## Part A: Exception handling

## 1. What an exception is · Quick

You're driving and a tyre bursts. You don't just stop existing; you pull over, handle it, and continue. An **exception** is the program's burst tyre: an unexpected event *during execution* (dividing by zero, a missing file, letters typed where a number was expected).

Without handling, Java prints a stack trace and the program **crashes**. With handling, you catch the problem and keep running.

**Exam line:** *An exception is an event that occurs during program execution and disrupts the normal flow of instructions. In Java, an exception is an object of a class derived from `Throwable`, which is created and "thrown" when the error occurs and can be "caught" and handled.*

**Error vs exception:** an `Error` (like `OutOfMemoryError`) is serious and usually not recoverable; an `Exception` is something the program can reasonably handle.

## 2. The hierarchy · Quick

"All exceptions in Java are objects" (a 2023 question): every exception is an instance of a class, so it carries a message (`getMessage()`) and a stack trace.

```
                Throwable
               /         \
           Error        Exception
                       /         \
            IOException     RuntimeException
         (checked)          /        |        \
                ArithmeticException  NullPointerException  ArrayIndexOutOfBoundsException
                                     NumberFormatException (via IllegalArgumentException)
```

| Checked exceptions | Unchecked exceptions |
| --- | --- |
| Checked by the **compiler**: you must catch or declare them | Not checked at compile time |
| Subclasses of `Exception` but not `RuntimeException` | `RuntimeException` and its subclasses |
| `IOException`, `FileNotFoundException`, `SQLException` | `ArithmeticException`, `NullPointerException`, `NumberFormatException` |
| Usually outside your control (file, network) | Usually programming mistakes |

## 3. The five keywords · Slow down

| Keyword | Job | Analogy |
| --- | --- | --- |
| `try` | Wraps code that might fail | "I'll attempt this" |
| `catch` | Handles a specific exception type | "If that went wrong, do this instead" |
| `finally` | Runs **always**, exception or not | Switching off the stove, whatever happened |
| `throw` | Actually throws one exception object | Raising your hand to report a problem |
| `throws` | In a method header: "this method may throw these" | A warning label on the box |

```java
try {
    int x = 10 / 0;                                  // throws ArithmeticException
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage()); // Error: / by zero
} finally {
    System.out.println("Always runs");
}
```

Rules worth a mark: one `try` can have many `catch` blocks, and they're checked **top to bottom**, so put the **specific** ones before general ones like `Exception`. Since Java 7, one catch can handle several types: `catch (A | B e)`. `finally` runs even if the try has a `return`; it's skipped only if the JVM exits (`System.exit`).

**`throw` vs `throws`:** `throw new X("msg")` is a statement inside a method that throws one object; `throws X, Y` goes in the method signature and declares what may come out.

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

## 4. Custom exceptions · Slow down

Java's built-in exceptions don't know your business rules. "Insufficient balance" isn't a Java error, it's *your* rule. So you make your own exception class.

**How:** extend `Exception` (checked, so callers must handle it) or `RuntimeException` (unchecked). Pass the message to `super(message)`.

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

---

## Part B: Generics

## 5. Why generics exist · Slow down

Before generics (Java 1.4), a list stored plain `Object`s. You could put a `String` and an `Integer` in the same list, and the mistake only showed up **at run time**, when you cast the wrong one and got a `ClassCastException`. Like a pharmacy where every bottle is labelled "medicine": you find out it's the wrong one only after swallowing.

Generics put a **type label on the container**. `ArrayList<String>` can hold only Strings, and the compiler rejects anything else **before the program ever runs**.

**Exam line:** *Generics allow classes, interfaces and methods to take a type parameter (such as `<T>`), so the same code works for many types while the compiler enforces type safety and removes the need for explicit casts.*

```java
// Without generics: compiles, crashes at run time
List list = new ArrayList();
list.add("hello");
list.add(10);
String s = (String) list.get(1);      // ClassCastException at RUN time

// With generics: the mistake is caught at COMPILE time
List<String> names = new ArrayList<>();
names.add("hello");
// names.add(10);                     // compile error
String t = names.get(0);              // no cast needed
```

**Three benefits:** (1) type safety at compile time, (2) no casting, (3) code reuse: one `Box<T>` for every type.

## 6. Generic classes and generic methods · Quick

```java
class Box<T> {                         // generic class: T is decided when you create it
    private T item;
    void set(T item) { this.item = item; }
    T get() { return item; }
}

class Util {
    static <T> void show(T[] arr) {    // generic method: <T> goes before the return type
        for (T x : arr) System.out.print(x + " ");
        System.out.println();
    }
}

public class Main {
    public static void main(String[] args) {
        Box<Integer> b = new Box<>();  // diamond <> : type inferred from the left side
        b.set(42);
        System.out.println(b.get());   // 42
        Util.show(new String[]{"a", "b"});   // T inferred as String
        Util.show(new Integer[]{1, 2, 3});   // T inferred as Integer
    }
}
```

Type parameter naming: `T` type, `E` element, `K` key, `V` value, `N` number. Generics work only with **reference types**, so `Box<int>` is illegal; use `Box<Integer>` (autoboxing converts automatically).

**Types of generics (syllabus list):** generic classes, generic interfaces (`interface Comparable<T>`), generic methods, and generic constructors.

**Type inference:** the compiler works out `T` for you, from the arguments (`Util.show(...)`) or from the variable's type (`new Box<>()`, the "diamond").

## 7. Bounded types · Slow down

Sometimes "any type" is too loose. To sort things, you must be able to compare them. So you say: "T can be any type, **as long as** it is comparable". That's a **bounded type parameter**, written with `extends` (which here means "is or implements").

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

## 8. Generics, inheritance and subtypes · Quick

A surprising rule: even though `Integer` is a subtype of `Number`, **`List<Integer>` is NOT a subtype of `List<Number>`**.

Why? If it were, you could do `List<Number> nums = intList; nums.add(3.5);` and now a `Double` sits inside a list of Integers. Java blocks this to keep type safety. That's what wildcards solve.

## 9. Wildcards · Slow down

The wildcard `?` means "some unknown type".

| Wildcard | Meaning | Use it to | Example |
| --- | --- | --- | --- |
| `<?>` | Any type | Only read as `Object` | `void printAll(List<?> l)` |
| `<? extends T>` | T or any **subclass** (upper bound) | **Read** T's out | `double sum(List<? extends Number> l)` works for `List<Integer>` and `List<Double>` |
| `<? super T>` | T or any **superclass** (lower bound) | **Add** T's in | `void fill(List<? super Integer> l)` accepts `List<Number>` |

Memory trick (PECS): **P**roducer **E**xtends, **C**onsumer **S**uper. If the list *gives* you items, use `extends`; if you *put* items in, use `super`.

```java
static double sum(List<? extends Number> list) {
    double s = 0;
    for (Number n : list) s += n.doubleValue();
    return s;
}
// sum(List.of(1, 2, 3)) -> 6.0     sum(List.of(1.5, 2.5)) -> 4.0
```

## 10. Type erasure · Quick

Generics exist **only at compile time**. After checking types, the compiler **erases** them: `T` becomes `Object` (or its bound, e.g. `Comparable`), and casts are inserted automatically. At run time, `List<String>` and `List<Integer>` are the same class, `List`.

**Exam line:** *Type erasure is the process by which the Java compiler removes generic type information after compile-time checking, replacing type parameters with their bounds (or `Object`) and inserting casts, so generic code runs on the JVM without new classes per type.*

**Consequences (good 1-mark points):** you can't do `new T()`, can't create `new T[10]`, can't use primitives as type arguments, and `instanceof List<String>` is illegal. It exists for **backward compatibility** with pre-generics Java code.

---

## 11. Quick recap

- Exception = an object describing a run-time error; unhandled means a crash.
- Checked (compiler forces handling: `IOException`) vs unchecked (`RuntimeException` family).
- try / catch (specific first) / finally (always) / throw (one object) / throws (declaration).
- Custom exception: `class X extends Exception { X(String m) { super(m); } }`.
- Generics: type errors at compile time, no casts, reuse.
- `<T extends Comparable<T>>` = bounded: T must be comparable.
- `List<Integer>` is not a `List<Number>`; use `? extends` to read, `? super` to write.
- Type erasure: generic types vanish after compilation (T → Object or its bound).
