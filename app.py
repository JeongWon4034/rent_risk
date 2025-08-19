# --- 1. Library Imports ---
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 2. 데이터 불러오기 (깃허브 raw URL) ---
url = "https://raw.githubusercontent.com/JeongWon4034/rent_risk/main/dataset_10.csv"
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

    # 중복 좌표 제거
    unique_points = df.drop_duplicates(subset=["위도", "경도"])

    # 점 표시
    for _, row in unique_points.iterrows():
        popup_text = f"<b>{row['단지명']}</b><br>위도: {row['위도']}<br>경도: {row['경도']}"
        folium.CircleMarker(
            location=[row["위도"], row["경도"]],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=popup_text,
            tooltip=row["단지명"]
        ).add_to(m)

    # 지도 출력 + 클릭 이벤트
    st_data = st_folium(m, width=800, height=600)

    # 사이드바: 매물 정보 표시
    st.sidebar.markdown("### 📋 선택된 매물 정보")

    if st_data["last_clicked"] is not None:
        lat = round(st_data["last_clicked"]["lat"], 6)
        lon = round(st_data["last_clicked"]["lng"], 6)

        selected_group = df[(df["위도"].round(6) == lat) & (df["경도"].round(6) == lon)]

        if not selected_group.empty:
            danji = selected_group.iloc[0]["단지명"]
            st.sidebar.write(f"**{danji} 매물 {len(selected_group)}건**")

            for _, r in selected_group.iterrows():
                st.sidebar.write(
                    f"- 전세가율: {r['전세가율']} / 보증금: {r['보증금.만원.']} / 계약유형: {r['계약유형']}"
                )
        else:
            st.sidebar.write("해당 좌표의 매물 정보를 찾을 수 없습니다.")

# --- 5. GPT 페이지 (제목만) ---
elif page == "GPT 인터페이스":
    st.markdown("""
    <h1 style="font-size:2.2rem; font-weight:700;">🤖 GPT 대화 인터페이스</h1>
    """, unsafe_allow_html=True)

    st.info("여기는 GPT 페이지입니다. 추후 기능이 추가될 예정입니다.")
