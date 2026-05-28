import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="수학 계산기", page_icon="🧮")

st.title("🧮 간단한 수학 계산기")

menu = st.sidebar.selectbox(
    "기능 선택",
    ["함수 계산", "원 넓이", "직사각형 넓이", "삼각형 넓이"]
)

# 함수 계산
if menu == "함수 계산":
    st.header("📈 함수 계산")
    
    x = st.number_input("x 값을 입력하세요", value=1.0)
    
    result = x**2 + 2*x + 1
    
    st.write("계산식:")
    st.latex(r"f(x) = x^2 + 2x + 1")
    
    st.success(f"결과: {result}")

    # -------------------------
    # 그래프 추가 부분
    # -------------------------
    
    # x 범위 생성
    x_vals = np.linspace(-10, 10, 400)
    
    # 함수 계산
    y_vals = x_vals**2 + 2*x_vals + 1
    
    # 그래프 생성
    fig, ax = plt.subplots()
    
    ax.plot(x_vals, y_vals, label="f(x)")
    
    # 현재 입력한 x 위치 표시
    ax.scatter(x, result, color="red", s=100, label="현재 값")
    
    ax.set_title("함수 그래프")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    
    ax.grid(True)
    ax.legend()
    
    st.pyplot(fig)

# 원 넓이
elif menu == "원 넓이":
    st.header("⭕ 원의 넓이")
    
    r = st.number_input("반지름 입력", min_value=0.0, value=1.0)
    
    area = math.pi * r * r
    
    st.latex(r"A = \pi r^2")
    st.success(f"원의 넓이: {area:.2f}")

# 직사각형 넓이
elif menu == "직사각형 넓이":
    st.header("▭ 직사각형 넓이")
    
    width = st.number_input("가로", min_value=0.0, value=1.0)
    height = st.number_input("세로", min_value=0.0, value=1.0)
    
    area = width * height
    
    st.latex(r"A = w \times h")
    st.success(f"직사각형 넓이: {area:.2f}")

# 삼각형 넓이
elif menu == "삼각형 넓이":
    st.header("🔺 삼각형 넓이")
    
    base = st.number_input("밑변", min_value=0.0, value=1.0)
    height = st.number_input("높이", min_value=0.0, value=1.0)
    
    area = (base * height) / 2
    
    st.latex(r"A = \frac{1}{2}bh")
    st.success(f"삼각형 넓이: {area:.2f}")