# def factorial(n: int) -> int:
#     # 기저 조건 (Base case): 재귀가 멈추는 탈출 조건
#     if n == 0:
#         return 1
#     # 재귀 단계 (Recursive step): 문제를 더 작은 단위로 분할
#     print(f"Calculating factorial({n}), calling factorial({n - 1})")
#     return n * factorial(n - 1)
def factorial(n: int, depth=0) -> int:
    # 기저 조건 (Base case): 재귀가 멈추는 탈출 조건
    if n == 0:
        return 1
    # 재귀 단계 (Recursive step): 문제를 더 작은 단위로 분할
    print (" "*depth, end="")
    print(f"Calculating factorial({n}), calling factorial({n - 1}, {depth+1})")
    return n * factorial(n - 1, depth+1)

def factorial_for(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
        print (" "*i, end="")
        print(f"Calculating factorial({i}), current result: {result}")
    return result

result = factorial(5)
print("Factorial of 5: ", result)

# result = factorial_for(5)
# print(result)