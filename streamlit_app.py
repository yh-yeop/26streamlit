import streamlit as st
import numpy as np
import random

# -----------------------
# 설정
# -----------------------
N = 10

BLOCKS = [
    np.array([[1]]),
    np.array([[1, 1]]),
    np.array([[1, 1, 1]]),
    np.array([[1, 1],
              [1, 1]]),
    np.array([[1, 0],
              [1, 1]]),
]

# -----------------------
# 상태
# -----------------------
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((N, N), dtype=int)

if "score" not in st.session_state:
    st.session_state.score = 0

if "blocks" not in st.session_state:
    st.session_state.blocks = [random.choice(BLOCKS) for _ in range(3)]

if "selected" not in st.session_state:
    st.session_state.selected = 0


# -----------------------
# 로직
# -----------------------
def can_place(grid, block, x, y):
    h, w = block.shape
    if x + h > N or y + w > N:
        return False
    return np.all(grid[x:x+h, y:y+w] + block <= 1)


def place(grid, block, x, y):
    h, w = block.shape
    grid[x:x+h, y:y+w] += block
    return grid


def clear_lines(grid):
    score = 0

    for i in range(N):
        if np.all(grid[i, :] == 1):
            grid[i, :] = 0
            score += 10

    for j in range(N):
        if np.all(grid[:, j] == 1):
            grid[:, j] = 0
            score += 10

    return grid, score


def game_over(grid, blocks):
    for b in blocks:
        for i in range(N):
            for j in range(N):
                if can_place(grid, b, i, j):
                    return False
    return True


# -----------------------
# UI
# -----------------------
st.title("🧩 Block Blast PRO (Streamlit Edition)")
st.write(f"⭐ Score: {st.session_state.score}")

# -----------------------
# 블록 선택 UI
# -----------------------
cols = st.columns(3)

for i in range(3):
    with cols[i]:
        st.write(f"Block {i}")

        # 블록 미리보기 (예쁘게)
        b = st.session_state.blocks[i]
        preview = ""
        for r in b:
            for c in r:
                preview += "🟦" if c else "⬜"
            preview += "<br>"

        st.markdown(preview, unsafe_allow_html=True)

        if st.button(f"Select {i}"):
            st.session_state.selected = i


# -----------------------
# 클릭 좌표 선택 방식 (핵심)
# -----------------------
st.subheader("🎯 Place Block")

row = st.selectbox("Row", list(range(N)))
col = st.selectbox("Col", list(range(N)))

if st.button("Place"):
    grid = st.session_state.grid
    block = st.session_state.blocks[st.session_state.selected]

    if can_place(grid, block, row, col):
        grid = place(grid, block, row, col)

        grid, gain = clear_lines(grid)
        st.session_state.score += gain

        st.session_state.blocks[st.session_state.selected] = random.choice(BLOCKS)

        st.session_state.grid = grid


# -----------------------
# 보드 UI (핵심: HTML로 렌더링)
# -----------------------
st.subheader("🧱 Board")

html = """
<style>
.board {
    display: grid;
    grid-template-columns: repeat(10, 25px);
    gap: 2px;
}
.cell {
    width: 25px;
    height: 25px;
    border-radius: 4px;
}
.filled {
    background: #4fc3f7;
}
.empty {
    background: #2b2b2b;
}
</style>

<div class="board">
"""

grid = st.session_state.grid

for i in range(N):
    for j in range(N):
        if grid[i][j]:
            html += '<div class="cell filled"></div>'
        else:
            html += '<div class="cell empty"></div>'

html += "</div>"

st.markdown(html, unsafe_allow_html=True)


# -----------------------
# 게임 오버
# -----------------------
if game_over(st.session_state.grid, st.session_state.blocks):
    st.error("💀 GAME OVER")
    if st.button("Restart"):
        st.session_state.grid = np.zeros((N, N))
        st.session_state.score = 0
        st.session_state.blocks = [random.choice(BLOCKS) for _ in range(3)]