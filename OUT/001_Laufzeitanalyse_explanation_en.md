# Algorithms and Complexity Theory

## 1. Big-O Notation (Time complexity)

### 1.1 Definition of Big-O Notation

**Definition/Description**:  
Big-O notation is a mathematical notation that describes the upper bound of an algorithm's time or space complexity. It is used to measure the worst-case scenario, providing an estimate of the amount of time or resources required by an algorithm.

For example, consider a simple sorting algorithm that takes n elements as input and has a running time proportional to n^2. In this case, we can say that the time complexity of the algorithm is O(n^2).

### 1.2 Understanding Big-O Notation

**Mathematical Formula**:  
$$ T(n) = O(f(n)) \iff \exists c > 0, n_0 \geq 0 : 0 \leq T(n) \leq cf(n) \quad \forall n \geq n_0 $$

This formula states that an algorithm's time complexity is in the order of f(n) if there exists a constant c and a positive integer n_0 such that the running time is less than or equal to c times f(n) for all inputs greater than or equal to n_0.

## Terminology

* **Time complexity**: The amount of time an algorithm takes to complete, usually expressed as a function of the input size.
* **Space complexity**: The amount of memory an algorithm uses, also expressed as a function of the input size.

### 1.3 Examples of Algorithms with Big-O Notation

**Code**:  
```python
def find_smallest(lst):
    smallest = lst[0]
    for i in range(1, len(lst)):
        if lst[i] < smallest:
            smallest = lst[i]
    return smallest
```

This algorithm has a time complexity of O(n) because it needs to iterate through the entire list once.

**Code**:  
```python
def find_smallest_diff(nums):
    min_diff = float('inf')
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            diff = abs(nums[i] - nums[j])
            if diff < min_diff:
                min_diff = diff
    return min_diff
```

This algorithm has a time complexity of O(n^2) because it needs to iterate through the list twice.

## 2. Simplified Knapsack Problem

### 2.1 Definition and Example

**Definition/Description**:  
The simplified knapsack problem is a classic problem in computer science where we need to find the optimal way to pack items of different weights into a knapsack of limited capacity.

Consider an example with two items: Item A weighs 10 units and has a value of $100, while Item B weighs 20 units and has a value of $200. The knapsack can hold up to 30 units of weight. We need to find the optimal combination of items that maximizes the total value.

### 2.2 Mathematical Formulation

**Mathematical Formula**:  
$$ \max \sum_{i=1}^n v_i x_i $$

subject to:

$$ \sum_{i=1}^n w_i x_i \leq W $$

where $v_i$ is the value of item i, $w_i$ is the weight of item i, and $x_i$ is a binary variable indicating whether item i is included in the solution.

## 3. Programming a Simplified Knapsack Problem

### 3.1 Example Code

**Code**:  
```python
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i-1] <= j:
                dp[i][j] = max(dp[i-1][j], values[i-1] + dp[i-1][j-weights[i-1]])
            else:
                dp[i][j] = dp[i-1][j]

    return dp[n][capacity]
```

This code uses dynamic programming to solve the simplified knapsack problem.