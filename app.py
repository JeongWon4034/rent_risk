# --- 1. 라이브러리 ---
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# --- 2. 데이터 불러오기 (깃허브 raw URL) ---
url = "https://raw.githubusercontent.com/JeongWon4034/rent_risk/main/dataset_13.csv"
df = pd.read_csv(url, encoding="utf-8-sig")

# 컬럼명 확인 (공백 제거)
df.columns = df.columns.str.strip()
st.write(df.columns.tolist())

# --- 3. 지도 ---
st.title("🏠 전세사기 위험 매물 지도")

# 지도 중심 (수원시청)
m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")

# 마커 클러스터 추가
marker_cluster = MarkerCluster().add_to(m)

# 중복 좌표 제거 (위도+경도 기준)
unique_points = df.drop_duplicates(subset=["위도", "경도"])

# 점 찍기
for _, row in unique_points.iterrows():
    group = df[(df["위도"] == row["위도"]) & (df["경도"] == row["경도"])]

    popup_html = f"<b>{row['단지명']}</b><br>매물 {len(group)}건<br><hr>"
    for _, r in group.iterrows():
        popup_html += f"전세가율: {r['전세가율']}% | 보증금: {r['보증금.만원.']}만원 | 계약유형: {r['계약유형']}<br>"

    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{row['단지명']} (매물 {len(group)}건)"
    ).add_to(marker_cluster)

# Streamlit에 지도 출력
st_data = st_folium(m, width=800, height=600)
