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
# 지도 보기 페이지
# -------------------
if menu == "📍 지도 보기":
    st.title("📍 수원시 전세사기 위험 매물 지도")

    try:
        df = pd.read_csv("dataset_14.csv")

        # 데이터 미리보기
        with st.expander("데이터 미리보기"):
            st.dataframe(df.head())

        # 지도 생성
        m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")
        marker_cluster = MarkerCluster().add_to(m)

        # ✅ 위경도 6자리 반올림
        df["위도_6"] = df["위도"].round(6)
        df["경도_6"] = df["경도"].round(6)

        # ✅ 좌표 그룹핑
        grouped = df.groupby(["위도_6", "경도_6"])

        # ✅ 그룹별 마커 생성
        for (lat, lon), group in grouped:
            info = ""
            for _, row in group.iterrows():
                info += (
                    f"<b>{row['단지명']}</b> | "
                    f"보증금: {row['보증금.만원.']}만원 | "
                    f"전세가율: {row['전세가율']}% | "
                    f"계약유형: {row['계약유형']}<br>"
                )

            folium.Marker(
                location=[lat, lon],
                popup=info
            ).add_to(marker_cluster)

        st_folium(m, width=900, height=600)

    except FileNotFoundError:
        st.error("❌ dataset_14.csv 파일을 찾을 수 없습니다. 앱 폴더에 있는지 확인해주세요.")

# -------------------
# GPT 인터페이스 페이지
# -------------------
elif menu == "💬 GPT 인터페이스":
    st.title("💬 GPT 기반 데이터 분석 인터페이스")
    st.write("추후 확장 예정입니다. (예: 평균 전세가율 질의응답, 위험도 분석 등)")
