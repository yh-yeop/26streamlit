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

if "last_action" not in st.session_state:
    st.session_state.last_action = None


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


def new_blocks():
    return [random.choice(BLOCKS) for _ in range(3)]


# -----------------------
# UI
# -----------------------
st.title("🧩 Block Blast UX+ (Streamlit)")

st.write(f"⭐ Score: {st.session_state.score}")

# -----------------------
# 블록 선택
# -----------------------
cols = st.columns(3)

for i in range(3):
    with cols[i]:
        st.write(f"Block {i}")

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
# 좌표 선택 (shadow 핵심)
# -----------------------
st.subheader("🎯 Placement Preview")

row = st.selectbox("Row", list(range(N)))
col = st.selectbox("Col", list(range(N)))

grid = st.session_state.grid
block = st.session_state.blocks[st.session_state.selected]

valid = can_place(grid, block, row, col)

st.write("Preview:")

# shadow grid 생성
shadow = grid.copy()

for i in range(block.shape[0]):
    for j in range(block.shape[1]):
        x = row + i
        y = col + j
        if x < N and y < N:
            shadow[x][y] = 2 if valid else 3  # 2 = valid shadow, 3 = invalid shadow


# -----------------------
# 렌더 (CSS 개선)
# -----------------------
html = """
<style>
.board {
    display: grid;
    grid-template-columns: repeat(10, 26px);
    gap: 2px;
}
.cell {
    width: 26px;
    height: 26px;
    border-radius: 4px;
}
.empty { background: #2b2b2b; }
.filled { background: #4fc3f7; }
.shadow_ok { background: #ff6b6b; opacity: 0.4; }
.shadow_bad { background: #b00020; opacity: 0.4; }
</style>

<div class="board">
"""

for i in range(N):
    for j in range(N):
        v = shadow[i][j]

        if v == 1:
            html += '<div class="cell filled"></div>'
        elif v == 2:
            html += '<div class="cell shadow_ok"></div>'
        elif v == 3:
            html += '<div class="cell shadow_bad"></div>'
        else:
            html += '<div class="cell empty"></div>'

html += "</div>"

st.markdown(html, unsafe_allow_html=True)


# -----------------------
# Place 버튼 (핵심 UX)
# -----------------------
if st.button("🟢 PLACE BLOCK"):
    if valid:
        grid = place(grid, block, row, col)
        grid, gain = clear_lines(grid)

        st.session_state.grid = grid
        st.session_state.score += gain

        # 🔥 핵심: 블록 자동 새로고침
        st.session_state.blocks[st.session_state.selected] = random.choice(BLOCKS)

        st.session_state.last_action = "placed"
        st.rerun()
    else:
        st.warning("❌ Cannot place block here")


# -----------------------
# 게임 오버
# -----------------------
def game_over(grid, blocks):
    for b in blocks:
        for i in range(N):
            for j in range(N):
                if can_place(grid, b, i, j):
                    return False
    return True


if game_over(st.session_state.grid, st.session_state.blocks):
    st.error("💀 GAME OVER")
    if st.button("Restart"):
        st.session_state.grid = np.zeros((N, N), dtype=int)
        st.session_state.score = 0
        st.session_state.blocks = new_blocks()
        st.rerun()