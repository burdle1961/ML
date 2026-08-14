def binary_search(arr: list, target: int, low: int, high: int) -> int:

    print (f">>> {low} ~ {high}  ", end="")

    # 탐색 실패 (교차점 발생)
    if low > high:
        return -1
    
    mid = (low + high) // 2
    
    # 탐색 성공
    if arr[mid] == target:
        return mid
    # 목표값이 중간값보다 작으면 왼쪽 구간 재귀 탐색
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    # 목표값이 중간값보다 크면 오른쪽 구간 재귀 탐색
    else:
        return binary_search(arr, target, mid + 1, high)

# 예시 데이터: 반드시 정렬된 배열이어야 함
# data = [2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91]

# 정렬되지 않은 데이터를 이용하면 정확한 결과를 보장할 수 없음
data = [56, 16, 72, 12, 2, 23, 91, 10, 8, 42, 38]
res = data.sort()  # 정렬되지 않은 배열을 정렬
print(res)
# 테스트 케이스들
test_targets = [23, 2, 91, 100, 16]

print(f"배열: {data}")
print(f"배열 길이: {len(data)}\n")

for target in test_targets:
    result = binary_search(data, target, 0, len(data) - 1)
    print()
    if result != -1:
        print(f"target={target:>3} -> 인덱스 {result}에서 발견 (arr[{result}]={data[result]})")
    else:
        print(f"target={target:>3} -> 탐색 실패 (배열에 존재하지 않음)")
