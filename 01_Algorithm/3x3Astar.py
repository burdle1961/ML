# 3x3 퍼즐 A* 알고리즘 구현

import heapq

# 목표 상태 (1부터 8까지 정렬되고 마지막이 빈칸인 상태)
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class PuzzleNode:
    def __init__(self, board, g, parent=None, move="시작"):
        self.board = tuple(board)
        self.parent = parent
        self.g = g  # 시작부터 현재까지 이동한 횟수 (현재 Step)
        self.move = move  # 이동 방향
        # self.h = self.calculate_manhattan()
        self.h = self.calculate_misplaced() # 제자리에 있지 않은 타일의 개수
        self.f = self.g + self.h # 총 예상 비용

    def calculate_manhattan(self): # 맨하튼 거리 계산
        distance = 0
        for i, val in enumerate(self.board):
            if val != 0:
                curr_r, curr_c = i // 3, i % 3
                target_idx = GOAL.index(val)
                target_r, target_c = target_idx // 3, target_idx % 3
                distance += abs(curr_r - target_r) + abs(curr_c - target_c)
        return distance
    
    def calculate_misplaced(self):
        """휴리스틱: 제자리에 있지 않은 타일의 개수 (0 제외)"""
        count = 0
        for i in range(9):
            if self.board[i] != 0 and self.board[i] != GOAL[i]:
                count += 1
        return count

    def get_neighbors(self):
        neighbors = []
        z = self.board.index(0)
        r, c = z // 3, z % 3
        moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]
        for dr, dc, direction in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_board = list(self.board)
                nz = nr * 3 + nc
                new_board[z], new_board[nz] = new_board[nz], new_board[z]
                neighbors.append(PuzzleNode(new_board, self.g + 1, self, direction))
        return neighbors

    def __lt__(self, other):
        # Heap은 f가 작은 순서대로 꺼내며, f가 같으면 g가 큰 것(더 깊이 탐색한 것)을 우선시할 수 있음
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

def print_step_by_step(final_node):
    """최종 경로를 역추적하여 전/후 상태와 Step 수를 출력"""
    path = []
    curr = final_node
    while curr:
        path.append(curr)
        curr = curr.parent
    path.reverse()

    print("\n" + "="*60)
    print(f"{'최종 해결 경로 상세 안내':^55}")
    print("="*60)

    for i in range(1, len(path)):
        prev = path[i-1]
        now = path[i]
        
        # 이동 전(prev.g)과 이동 후(now.g) Step 표시
        print(f"\n[STEP {prev.g} -> {now.g}] 방향: {now.move}")
        print(f"{' <이동 전 (Step ' + str(prev.g) + ')> ':^20}    {' <이동 후 (Step ' + str(now.g) + ')> ':^20}")
        
        for r in range(3):
            before_row = list(prev.board[r*3 : (r+1)*3])
            after_row = list(now.board[r*3 : (r+1)*3])
            print(f"      {before_row}         --->         {after_row}")
        print("-" * 60)

def solve_puzzle(start_board):
    open_list = []
    heapq.heappush(open_list, PuzzleNode(start_board, 0))
    # visited에 해당 상태에 도달한 '최소 비용 g'를 기록
    visited = {tuple(start_board): 0}
    
    revisit_count = 0 # 재방문(지름길 발견) 횟수

    while open_list:
        current = heapq.heappop(open_list)

        if current.board == GOAL:
            print(f"\n최적 경로 발견! (지름길 갱신 횟수: {revisit_count})")
            print_step_by_step(current)
            return

        for neighbor in current.get_neighbors():
            # [핵심 로직] 이미 가본 길인데, 지금 경로가 더 짧다면?
            if neighbor.board in visited:
                if neighbor.g < visited[neighbor.board]:
                    print(f"\n[지름길 발견!] 상태 {neighbor.board[:3]}...의 기존 Step {visited[neighbor.board]}을 {neighbor.g}로 갱신합니다.")
                    print(f"{neighbor.board} --> {neighbor}")
                    revisit_count += 1
                    visited[neighbor.board] = neighbor.g
                    heapq.heappush(open_list, neighbor)
            
            # 처음 가보는 길이라면
            elif neighbor.board not in visited:
                visited[neighbor.board] = neighbor.g
                heapq.heappush(open_list, neighbor)

# 인버전 (퍼즐 판을 1차원으로 펼쳤을 때(빈칸 0은 제외), 어떤 숫자가 자기보다 뒤에 있는 더 작은 숫자보다 앞에 나오는 쌍의 개수)
# 타일의 좌우 이동 (인버전 수 변화 없음), 상하 이동 (인버전 수 변화 있, 짝수 많큼 변함) --> 인버전의 홀짝성은 변하지 않음.
# 목표 상태는 인버전이 짝수 --> 즉, 초기도 짝수이어야 목표 상태에 도달 가능. (홀수 상태 --> 짝수 상태롤 변화되지 않음.)
# 3x3 퍼즐에서만 적용됨.

def is_solvable(board):
    flat_board = [num for num in board if num != 0]
    inversions = 0
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1
    return inversions % 2 == 0

if __name__ == "__main__":
    # 해결 가능한 초기 상태 예시
    # initial_state = [8, 1, 2, 0, 4, 6, 5, 7, 3]
    initial_state = [1, 2, 3, 4, 8, 0, 7, 6, 5]    
    
    print(f"입력 보드: {initial_state}")
    
    if not is_solvable(initial_state):
        print("결과: 이 퍼즐은 해결 불가능합니다.")
    else:
        print("결과: 해결 가능. 탐색 시작...")
        solve_puzzle(initial_state)