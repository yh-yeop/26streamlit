import streamlit as st
import pygame
import numpy as np
import time

# -------------------
# 초기 설정
# -------------------

WIDTH = 800
HEIGHT = 400

GRAVITY = 0.7
JUMP_POWER = -12
MOVE_SPEED = 5

# -------------------
# 상태 저장
# -------------------

if "x" not in st.session_state:
    st.session_state.x = 100

if "y" not in st.session_state:
    st.session_state.y = 300

if "vy" not in st.session_state:
    st.session_state.vy = 0

if "jumping" not in st.session_state:
    st.session_state.jumping = False

# -------------------
# 입력
# -------------------

st.title("🕹️ Streamlit Mini Platformer")

col1, col2, col3 = st.columns(3)

left = col1.button("⬅️ Left")
jump = col2.button("⬆️ Jump")
right = col3.button("➡️ Right")

# -------------------
# 이동 처리
# -------------------

if left:
    st.session_state.x -= MOVE_SPEED

if right:
    st.session_state.x += MOVE_SPEED

# 점프
if jump and not st.session_state.jumping:
    st.session_state.vy = JUMP_POWER
    st.session_state.jumping = True

# -------------------
# 물리 처리
# -------------------

st.session_state.vy += GRAVITY
st.session_state.y += st.session_state.vy

# 바닥 충돌
GROUND = 300

if st.session_state.y >= GROUND:
    st.session_state.y = GROUND
    st.session_state.vy = 0
    st.session_state.jumping = False

# -------------------
# pygame 렌더링
# -------------------

pygame.init()

surface = pygame.Surface((WIDTH, HEIGHT))

# 배경
surface.fill((30, 30, 40))

# 바닥
pygame.draw.rect(surface, (100, 200, 100), (0, 350, WIDTH, 50))

# 플레이어
pygame.draw.rect(
    surface,
    (50, 200, 255),
    (
        st.session_state.x,
        st.session_state.y,
        50,
        50
    )
)

# numpy 변환
frame = pygame.surfarray.array3d(surface)
frame = np.transpose(frame, (1, 0, 2))

# 출력
st.image(frame)

# 좌표 표시
st.write(f"X: {st.session_state.x}")
st.write(f"Y: {st.session_state.y:.1f}")