# --- 1. Library Imports ---
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster   # 추가

# --- 2. 데이터 불러오기 (깃허브 raw URL) ---
url = "https://raw.githubusercontent.com/JeongWon4034/rent_risk/main/dataset_12.csv"
df = pd.read_csv(url)

# --- 3. 사이드바 메뉴 ---
st.sidebar.title("📌 메뉴")
page = st.sidebar.radio("페이지 선택", ["지도 보기", "GPT 인터페이스"])

# --- 4. 지도 페이지 ---
if page == "지도 보기":
    st.markdown("""
    <h1 style="font-size:2.2rem; font-weight:700;">🏠 전세사기 위험 매물 지도</h1>
    """, unsafe_allow_html=True)

    # 지도 중심 (수원시청)
    map_center = [37.2636, 127.0286]
    m = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron")

    # 마커 클러스터 추가
    marker_cluster = MarkerCluster().add_to(m)

    # 점 표시 (클러스터에 추가)
    for _, row in df.iterrows():
        popup_text = f"<b>{row['단지명']}</b><br>전세가율: {row['전세가율']}%<br>보증금: {row['보증금.만원.']}만원"
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=popup_text,
            tooltip=row["단지명"]
        ).add_to(marker_cluster)

    # 지도 출력
    st_data = st_folium(m, width=800, height=600)

# --- 5. GPT 페이지 (제목만) ---
elif page == "GPT 인터페이스":
    st.markdown("""
    <h1 style="font-size:2.2rem; font-weight:700;">🤖 GPT 대화 인터페이스</h1>
    """, unsafe_allow_html=True)

    st.info("여기는 GPT 페이지 - 추후 기능 추가 예정")
