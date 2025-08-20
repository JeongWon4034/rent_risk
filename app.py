import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# --- 데이터 불러오기 ---
url = "https://raw.githubusercontent.com/JeongWon4034/rent_risk/main/dataset_12.csv"
df = pd.read_csv(url)

# --- 메뉴 ---
st.sidebar.title("📌 메뉴")
page = st.sidebar.radio("페이지 선택", ["지도 보기", "GPT 인터페이스"])

if page == "지도 보기":
    st.markdown("<h1>🏠 전세사기 위험 매물 지도</h1>", unsafe_allow_html=True)

    # 지도 초기 위치: 수원시청
    map_center = [37.2636, 127.0286]
    m = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    # 중복 좌표 제거
    unique_points = df.drop_duplicates(subset=["위도", "경도"])

    for _, row in unique_points.iterrows():
        group = df[(df["위도"] == row["위도"]) & (df["경도"] == row["경도"])]

        # 팝업 HTML
        popup_html = f"<b>{str(row['단지명'])}</b><br>매물 {len(group)}건<br><hr>"
        for _, r in group.iterrows():
            popup_html += (
                f"전세가율: {str(r['전세가율'])}% | "
                f"보증금: {str(r['보증금.만원.'])}만원 | "
                f"계약유형: {str(r['계약유형'])}<br>"
            )

        # 마커 추가
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{str(row['단지명'])} (매물 {len(group)}건)"
        ).add_to(marker_cluster)

    st_folium(m, width=800, height=600)

elif page == "GPT 인터페이스":
    st.markdown("<h1>🤖 GPT 대화 인터페이스</h1>", unsafe_allow_html=True)
    st.info("여기는 GPT 페이지 - 추후 기능 추가 예정")
