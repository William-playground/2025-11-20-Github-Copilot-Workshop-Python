def fibonacci(n):
    """Fibonacci数列を計算する関数
    
    指定された個数のFibonacci数列を計算して、リストとして返します。
    Fibonacci数列は、最初の2つの数が0と1で、それ以降の各数が
    直前の2つの数の和となる数列です（0, 1, 1, 2, 3, 5, 8, 13, ...）。
    
    Args:
        n (int): 生成するFibonacci数列の項数
    
    Returns:
        list: Fibonacci数列を格納したリスト
            - n <= 0 の場合は空のリスト []
            - n == 1 の場合は [0]
            - n == 2 の場合は [0, 1]
            - n >= 3 の場合は n 個の要素を持つリスト
    
    Examples:
        >>> fibonacci(0)
        []
        >>> fibonacci(1)
        [0]
        >>> fibonacci(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    Note:
        この関数は反復的なアプローチを使用しているため、
        大きな n の値に対しても効率的に動作します。
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_value = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_value)
    
    return fib_sequence
