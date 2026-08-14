
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def fibonacci(n):
    """피보나치 수열 n개 생성"""
    fibs = [1, 1]
    for i in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

n_terms = 10    
fibs = fibonacci(n_terms)

fig, ax = plt.subplots(figsize=(10, 10))
colors = plt.cm.viridis(np.linspace(0, 1, len(fibs)))

# 방향(direction)별 [호의 중심 코너, 시작각, 끝각, 시작점 코너, 끝점 코너]
# 기하학적으로 유도: 각 정사각형의 대각선 코너쌍이 호의 양 끝점이 되고,
# 나머지 대각선 코너 중 하나가 중심이 되어야 앞뒤 사각형의 호가 정확히 맞물림
ARC_RULE = {
    0: dict(center='TL', t1=270, t2=360, entry='BL', exit='TR'),  # 오른쪽으로 붙는 사각형
    1: dict(center='BL', t1=0,   t2=90,  entry='BR', exit='TL'),  # 위로 붙는 사각형
    2: dict(center='BR', t1=90,  t2=180, entry='TR', exit='BL'),  # 왼쪽으로 붙는 사각형
    3: dict(center='TR', t1=180, t2=270, entry='TL', exit='BR'),  # 아래로 붙는 사각형
}

bbox = None       # 지금까지 쌓인 사각형들 전체의 경계 상자 (x0, y0, x1, y1)
prev_exit = None  # 이전 사각형 호의 끝점 (다음 호의 시작점과 일치해야 함)

for i, f in enumerate(fibs):
    direction = (i - 1) % 4  # 0=오른쪽, 1=위, 2=왼쪽, 3=아래 순으로 반복 회전

    # 1. 새 정사각형 좌표 계산 (기존 bbox의 한 변에 이어 붙임)
    if i == 0:
        sq = (0, 0, f, f)
    else:
        x0, y0, x1, y1 = bbox
        if direction == 0:
            sq = (x1, y0, x1 + f, y0 + f)
        elif direction == 1:
            sq = (x0, y1, x1, y1 + f)
        elif direction == 2:
            sq = (x0 - f, y0, x0, y1)
        elif direction == 3:
            sq = (x0, y0 - f, x1, y0)

    sx0, sy0, sx1, sy1 = sq
    corners = {'BL': (sx0, sy0), 'BR': (sx1, sy0), 'TL': (sx0, sy1), 'TR': (sx1, sy1)}

    # 2. bbox 갱신
    if bbox is None:
        bbox = sq
    else:
        x0, y0, x1, y1 = bbox
        if direction == 0:
            bbox = (x0, y0, sx1, y1)
        elif direction == 1:
            bbox = (x0, y0, x1, sy1)
        elif direction == 2:
            bbox = (sx0, y0, x1, y1)
        elif direction == 3:
            bbox = (x0, sy0, x1, y1)

    # 3. 정사각형 그리기
    rect = patches.Rectangle((sx0, sy0), f, f, linewidth=1.5,
                              edgecolor='black', facecolor=colors[i], alpha=0.6)
    ax.add_patch(rect)
    ax.text(sx0 + f/2, sy0 + f/2, str(f), ha='center', va='center',
             fontsize=11, fontweight='bold')

    # 4. 호(arc) 그리기 - 방향별 규칙에 따라 중심/각도/시작·끝 코너를 결정
    rule = ARC_RULE[direction]
    center = corners[rule['center']]
    entry_coord = corners[rule['entry']]
    exit_coord = corners[rule['exit']]

    # 4-1. 연속성 검증: 이전 호의 끝점 == 이번 호의 시작점
    if prev_exit is not None:
        assert np.allclose(entry_coord, prev_exit), f"호 연결 오류 (square {i})"
    prev_exit = exit_coord

    arc = patches.Arc(center, 2*f, 2*f, angle=0, theta1=rule['t1'], theta2=rule['t2'],
                       color='red', linewidth=2.5)
    ax.add_patch(arc)

# 5. 축 범위 설정 및 저장
x0, y0, x1, y1 = bbox
ax.set_xlim(x0 - 2, x1 + 2)
ax.set_ylim(y0 - 2, y1 + 2)
ax.set_aspect('equal')
ax.set_title('(Fibonacci Spiral)', fontsize=15, fontweight='bold')
ax.axis('off')

plt.tight_layout()
plt.show()
