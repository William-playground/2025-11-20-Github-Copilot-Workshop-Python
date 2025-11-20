"""
Fibonacci数列に関する関数を提供するモジュール

このモジュールはFibonacci数列を生成・計算するための各種関数を提供します。
"""


def fibonacci(n):
    """
    Fibonacci数列のn番目の数を返す関数（再帰的実装）
    
    Fibonacci数列は以下のように定義されます：
    - F(0) = 0
    - F(1) = 1
    - F(n) = F(n-1) + F(n-2) (n >= 2)
    
    Args:
        n (int): 取得したいFibonacci数列の位置（0から始まる）
        
    Returns:
        int: n番目のFibonacci数
        
    Raises:
        ValueError: nが負の数の場合
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
        >>> fibonacci(10)
        55
        
    Note:
        この実装は再帰的なため、大きな数に対しては効率が悪くなります。
        大きな数を扱う場合は、fibonacci_iterative()を使用することを推奨します。
    """
    if n < 0:
        raise ValueError("nは0以上の整数である必要があります")
    
    if n <= 1:
        return n
    
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_iterative(n):
    """
    Fibonacci数列のn番目の数を返す関数（反復的実装）
    
    この実装は再帰を使用せず、反復処理でFibonacci数を計算します。
    大きな数に対しても効率的に動作します。
    
    Args:
        n (int): 取得したいFibonacci数列の位置（0から始まる）
        
    Returns:
        int: n番目のFibonacci数
        
    Raises:
        ValueError: nが負の数の場合
        
    Examples:
        >>> fibonacci_iterative(0)
        0
        >>> fibonacci_iterative(1)
        1
        >>> fibonacci_iterative(5)
        5
        >>> fibonacci_iterative(10)
        55
        >>> fibonacci_iterative(50)
        12586269025
        
    Note:
        この実装は時間計算量O(n)、空間計算量O(1)で動作します。
    """
    if n < 0:
        raise ValueError("nは0以上の整数である必要があります")
    
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def fibonacci_sequence(n):
    """
    0からn番目までのFibonacci数列を生成する関数
    
    Args:
        n (int): 生成するFibonacci数列の最後の位置
        
    Returns:
        list: 0からn番目までのFibonacci数のリスト
        
    Raises:
        ValueError: nが負の数の場合
        
    Examples:
        >>> fibonacci_sequence(0)
        [0]
        >>> fibonacci_sequence(5)
        [0, 1, 1, 2, 3, 5]
        >>> fibonacci_sequence(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        
    Note:
        この関数は内部的にfibonacci_iterative()を使用しているため、
        大きな数に対しても効率的に動作します。
    """
    if n < 0:
        raise ValueError("nは0以上の整数である必要があります")
    
    sequence = []
    for i in range(n + 1):
        sequence.append(fibonacci_iterative(i))
    
    return sequence


def is_fibonacci_number(num):
    """
    与えられた数がFibonacci数かどうかを判定する関数
    
    数学的性質を利用して判定します：
    ある数nがFibonacci数である ⇔ 5*n^2 + 4 または 5*n^2 - 4 が完全平方数
    
    Args:
        num (int): 判定したい数
        
    Returns:
        bool: Fibonacci数の場合True、そうでない場合False
        
    Examples:
        >>> is_fibonacci_number(0)
        True
        >>> is_fibonacci_number(1)
        True
        >>> is_fibonacci_number(5)
        True
        >>> is_fibonacci_number(10)
        False
        >>> is_fibonacci_number(55)
        True
        
    Note:
        この実装は負の数に対してはFalseを返します。
    """
    if num < 0:
        return False
    
    import math
    
    def is_perfect_square(n):
        """完全平方数かどうかを判定する補助関数"""
        root = int(math.sqrt(n))
        return root * root == n
    
    # 5*n^2 + 4 または 5*n^2 - 4 が完全平方数かをチェック
    return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)


if __name__ == "__main__":
    # 使用例
    print("Fibonacci数列のデモンストレーション")
    print("=" * 50)
    
    # 個別の値を取得
    print("\n■ 個別のFibonacci数:")
    for i in [0, 1, 5, 10, 15]:
        print(f"fibonacci({i}) = {fibonacci_iterative(i)}")
    
    # 数列を生成
    print("\n■ Fibonacci数列（0〜10）:")
    print(fibonacci_sequence(10))
    
    # Fibonacci数の判定
    print("\n■ Fibonacci数の判定:")
    test_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 21, 55, 100]
    for num in test_numbers:
        result = "○" if is_fibonacci_number(num) else "×"
        print(f"{num:3d}: {result}")
