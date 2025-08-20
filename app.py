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
        df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
        df["경도"] = pd.to_numeric(df["경도"], errors="coerce")
        df = df.dropna(subset=["위도", "경도"])
        df["위도_6"] = df["위도"].round(6)
        df["경도_6"] = df["경도"].round(6)
        grouped = df.groupby(["위도_6", "경도_6"])

        # 지도 생성
        m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")
        marker_cluster = MarkerCluster().add_to(m)

        for (lat, lon), group in grouped:
            if pd.isna(lat) or pd.isna(lon):
                continue
            info = "<br>".join(
                f"<b>{row['단지명']}</b> | 보증금: {row['보증금.만원.']}만원 | 전세가율: {row['전세가율']}% | 계약유형: {row['계약유형']}"
                for _, row in group.iterrows()
            )
            folium.Marker(location=[lat, lon], popup=info).add_to(marker_cluster)

        # ✅ 좌우 레이아웃
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📊 위험 매물 현황 요약")
            st.metric("총 매물 수", len(df))
            st.metric("평균 전세가율", round(df["전세가율"].mean(), 2))
            st.metric("최대 전세가율", df["전세가율"].max())

            with st.expander("데이터 미리보기"):
                st.dataframe(df.head(10))

        with col2:
            st.subheader("🗺️ 지도")
            st_folium(m, width=800, height=600)

    except Exception as e:
        st.error(f"에러 발생: {e}")


# -------------------
# GPT 인터페이스 페이지
# -------------------
elif menu == "💬 GPT 인터페이스":
    st.title("💬 GPT 기반 데이터 분석 인터페이스")
    st.write("추후 확장 예정입니다. (예: 평균 전세가율 질의응답, 위험도 분석 등)")
