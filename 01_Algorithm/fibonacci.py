def fibonacci(n: int) -> int:
    # 기저 조건
    if n <= 1:
        return n
    # 분기형 재귀 호출
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Fibonacci Sequence : ", fibonacci(10))

for i in range(11):
    print(f"fibonacci({i}) = {fibonacci(i)}")

# finacci  결과의 시각화


