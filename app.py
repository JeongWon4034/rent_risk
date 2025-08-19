# --- 1. Library Imports ---
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from pyproj import Transformer
import os
import ast
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- 제목 부분 ---
st.markdown("""
<div class="premium-header">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🏠 전세사기 위험 매물 지도</h1>
</div>
""", unsafe_allow_html=True)


##############################  🖥️ 페이지 설정 ##############################

# 🎨 스타일 정의
st.markdown("""
<style>
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-top: 2rem;
    }

    .metric-box {
        flex: 1;
        margin: 0 1rem;
        padding: 2rem;
        background: #f4f6fa;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.3s ease;
    }

    .metric-box:hover {
        transform: translateY(-5px);
    }

    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)


# ✅ 박스 4개 (더미 값)
num_sources = 128
num_detections = 64
num_types = 5
success_rate = 87.5

st.markdown(f"""
<div class="metric-container">
    <div class="metric-box">
        <div class="metric-title">수원시 전세 </div>
        <div class="metric-value">{num_sources}개소</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">⚠️ 현재 매물 갯수</div>
        <div class="metric-value">{num_detections}건</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">📊 오늘의 날씨</div>
        <div class="metric-value">{num_types}종</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">📈 분석 성공률</div>
        <div class="metric-value">{success_rate:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)


##################################################################3
# --- 지도 생성 ---
# 지도 중심 (예: 수원시청 근처 위도, 경도)
map_center = [37.2636, 127.0286]
m = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron")

# --- 원형 마커 추가 예시 ---
# (lat, lon, 위험도) 데이터 예시
sample_data = [
    {"lat": 37.25814177, "lon": 126.9523229, "label": "안전 매물", "risk": "low"},
    {"lat": 37.25452283, "lon": 126.9615656, "label": "주의 매물", "risk": "mid"},
    {"lat": 37.2500, "lon": 127.0200, "label": "위험 매물", "risk": "high"},
]

for d in sample_data:
    color = "blue" if d["risk"] == "low" else "orange" if d["risk"] == "mid" else "red"
    folium.CircleMarker(
        [d["lat"], d["lon"]],
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(f"{d['label']}", max_width=200),
        tooltip=f"{d['label']}"
    ).add_to(m)

# --- Streamlit에 지도 띄우기 ---
st_folium(m, width='100%', height=650)
