import streamlit as st
import pygame
import numpy as np
import time

pygame.init()

WIDTH, HEIGHT = 400, 300

x = st.slider("공 위치", 0, WIDTH, 100)

surface = pygame.Surface((WIDTH, HEIGHT))

surface.fill((0, 0, 0))

pygame.draw.circle(surface, (0, 255, 255), (x, 150), 30)

img = pygame.surfarray.array3d(surface)
img = np.transpose(img, (1, 0, 2))

st.image(img)