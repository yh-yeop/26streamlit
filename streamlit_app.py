import streamlit as st
import numpy as np
import random

# -------------------------
# 설정
# -------------------------
SIZE = 10

BLOCKS = [
    np.array([[1]]),
    np.array([[1, 1]]),
    np.array([[1, 1, 1]]),
    np.array([[1, 1],
              [1, 1]]),
    np.array([[1, 1, 1],
              [0, 1, 0]]),
]

# -------------------------
# 초기 상태
# -------------------------
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((SIZE, SIZE), dtype=int)

if "score" not in st.session_state:
    st.session_state.score = 0

if "blocks" not in st.session_state:
    st.session_state.blocks = [random.choice(BLOCKS) for _ in range(3)]

if "selected" not in st.session_state:
    st.session_state.selected = 0

# -------------------------
# 함수
# -------------------------
def can_place(grid, block, x, y):
    h, w = block.shape
    if x + h > SIZE or y + w > SIZE:
        return False
    return np.all(grid[x:x+h, y:y+w] + block <= 1)

def place_block(grid, block, x, y):
    h, w = block.shape
    grid[x:x+h, y:y+w] += block
    return grid

def clear_lines(grid):
    score = 0

    # 행 체크
    for i in range(SIZE):
        if np.all(grid[i, :] == 1):
            grid[i, :] = 0
            score += 10

    # 열 체크
    for j in range(SIZE):
        if np.all(grid[:, j] == 1):
            grid[:, j] = 0
            score += 10

    return grid, score

def game_over(grid, blocks):
    for b in blocks:
        for i in range(SIZE):
            for j in range(SIZE):
                if can_place(grid, b, i, j):
                    return False
    return True

# -------------------------
# UI
# -------------------------
st.title("🧩 Block Blast (Streamlit)")

st.write(f"⭐ Score: {st.session_state.score}")

# -------------------------
# 블록 선택
# -------------------------
cols = st.columns(3)

for i in range(3):
    with cols[i]:
        st.write(f"Block {i}")
        st.write(st.session_state.blocks[i])

        if st.button(f"Select {i}"):
            st.session_state.selected = i

# -------------------------
# 보드 클릭 입력
# -------------------------
st.write("### Board (click cell)")

grid = st.session_state.grid
selected_block = st.session_state.blocks[st.session_state.selected]

for i in range(SIZE):
    cols = st.columns(SIZE)
    for j in range(SIZE):
        cell = grid[i, j]

        label = "⬛" if cell == 0 else "🟩"

        if cols[j].button(label, key=f"{i}-{j}"):
            if can_place(grid, selected_block, i, j):
                grid = place_block(grid, selected_block, i, j)

                grid, gained = clear_lines(grid)
                st.session_state.score += gained

                # 블록 교체
                st.session_state.blocks[st.session_state.selected] = random.choice(BLOCKS)

                st.session_state.grid = grid

# -------------------------
# 게임 오버
# -------------------------
if game_over(st.session_state.grid, st.session_state.blocks):
    st.error("💀 Game Over")
    if st.button("Restart"):
        st.session_state.grid = np.zeros((SIZE, SIZE), dtype=int)
        st.session_state.score = 0
        st.session_state.blocks = [random.choice(BLOCKS) for _ in range(3)]