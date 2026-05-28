import streamlit as st
from streamlit_keyup import st_keyup
import pygame
import numpy as np

# -------------------------
# 설정
# -------------------------
WIDTH, HEIGHT = 800, 400
GROUND = 320

GRAVITY = 0.8
JUMP_POWER = -14
MOVE_SPEED = 6

# -------------------------
# 상태
# -------------------------
if "x" not in st.session_state:
    st.session_state.x = 100

if "y" not in st.session_state:
    st.session_state.y = GROUND

if "vy" not in st.session_state:
    st.session_state.vy = 0

if "on_ground" not in st.session_state:
    st.session_state.on_ground = True

# -------------------------
# 키 입력 (핵심)
# -------------------------
key = st_keyup("키 입력 (← → ↑ or A/D/W)")

# -------------------------
# 입력 처리
# -------------------------
if key in ["ArrowLeft", "a", "A"]:
    st.session_state.x -= MOVE_SPEED

if key in ["ArrowRight", "d", "D"]:
    st.session_state.x += MOVE_SPEED

if key in ["ArrowUp", "w", "W", " "]:
    if st.session_state.on_ground:
        st.session_state.vy = JUMP_POWER
        st.session_state.on_ground = False

# -------------------------
# 물리
# -------------------------
st.session_state.vy += GRAVITY
st.session_state.y += st.session_state.vy

if st.session_state.y >= GROUND:
    st.session_state.y = GROUND
    st.session_state.vy = 0
    st.session_state.on_ground = True

# -------------------------
# 렌더링 (pygame surface)
# -------------------------
pygame.init()
surface = pygame.Surface((WIDTH, HEIGHT))

surface.fill((20, 20, 30))

# 바닥
pygame.draw.rect(surface, (80, 200, 120), (0, GROUND + 50, WIDTH, 80))

# 플레이어
pygame.draw.rect(
    surface,
    (80, 180, 255),
    (st.session_state.x, st.session_state.y, 40, 40)
)

# 변환
frame = pygame.surfarray.array3d(surface)
frame = np.transpose(frame, (1, 0, 2))

st.image(frame)

# 상태
st.write("입력된 키:", key)
st.write({
    "x": st.session_state.x,
    "y": st.session_state.y,
    "vy": st.session_state.vy
})