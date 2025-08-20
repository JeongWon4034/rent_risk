# --- 1. 라이브러리 ---
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


# -------------------
# 페이지 기본 설정
# -------------------
st.set_page_config(
    page_title="수원시 전세사기 위험 매물 지도",
    page_icon="🏠",
    layout="wide"
)

# -------------------
# 사이드바 메뉴
# -------------------
menu = st.sidebar.radio(
    "메뉴 선택",
    ["📍 지도 보기", "💬 GPT 인터페이스"]
)

# -------------------
# 메인 화면
# -------------------
if menu == "📍 지도 보기":
    st.title("📍 수원시 전세사기 위험 매물 지도")
    st.write("여기에 지도 기능을 추가할 예정입니다.")

elif menu == "💬 GPT 인터페이스":
    st.title("💬 GPT 기반 데이터 분석 인터페이스")
    st.write("추후 확장 예정입니다.")
