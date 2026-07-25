# 3658. GCD of Odd and Even Sums

**Topic:** Math

**Difficulty:** Easy

**Language:** Python

**Problem Link: https://leetcode.com/problems/gcd-of-odd-and-even-sums/ **

---

## Problem

You are given an integer n. Your task is to compute the GCD (greatest common divisor) of two values:

sumOdd: the sum of the smallest n positive odd numbers.

sumEven: the sum of the smallest n positive even numbers.

Return the GCD of sumOdd and sumEven.

---

## My Thought Process
Firstly I went through the problem statement and then I declared 2 variables **o** and **e** for odd sum and the even sum respectively. After that I focused on 
finding the formula to calculate the sums, for that i first recalled the formula to calculate the sum of an AP (Arithmetic Progression) i.e. Sn = n/2 * [2a + (n-1)d]
Using this I figured out the final formula i.e. o=n**2 and e=n*(n+1). Then I focused on the way to calculate the GCD of these sum and I decided to go with the Eucledian 
algorithm as it computes the GCD in logarithmic time.

---

## Algorithm
1. Declare the variable **o** for the odd sum using the formula ** o=n**2 **.
2. Declare the variable **e** for the even sum using the formula ** e=n*(n+1) **.
3. Apply the Euclidean Algorithm:

   - While `e` is not zero:
     - Store `e` temporarily.
     - Replace `e` with `o % e`.
     - Replace `o` with the previous value of `e`.
4. Return the absolute value of `o`, which is the GCD.



---

## Complexity Analysis

Time Complexity: **O(log n)**

Space Complexity: **O(1)**

---

## What I Learned
- The sum of the first `n` odd numbers is always `n²`.
- The sum of the first `n` even numbers is `n(n+1)`.
- Always double check your formulas before the implementation.
- Looking for mathematical patterns can simplify a problem significantly.
- The Euclidean Algorithm is an efficient way to compute the GCD.

---

## Mistakes that I made
I used the wrong formula for calculating the odd and even sum and this wasted a lot of my time.

---
## Key Takeaway

Not every problem requires simulation. Before writing loops, check whether a mathematical pattern or formula can simplify the solution. Combining mathematical 
observations with an efficient algorithm like the Euclidean Algorithm can greatly reduce the implementation complexity.

---
## Solution

```python
class Solution(object):
    def gcdOfOddEvenSums(self, n):
        """
        :type n: int
        :rtype: int
        """

        o = n ** 2
        e = n * (n + 1)

        while e:
            o, e = e, o % e

        return abs(o)
```
        
        
```
