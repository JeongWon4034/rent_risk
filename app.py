# --- 1. 라이브러리 임포트 ---
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
import openai

# ✅ OpenAI API Key (Streamlit Cloud secrets 사용)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- 2. 페이지 세팅 ---
st.set_page_config(
    layout="wide", 
    page_title="수원시 전세사기 위험 매물 지도", 
    page_icon="💰"
)

st.markdown("""
<div style="background:#f8f9fa; padding:1rem; border-radius:12px; text-align:center;">
    <h1 style="margin:0; font-size:2rem; font-weight:700; color:#333;">
        💰 수원시 전세사기 위험 매물 분석 & GPT 상담
    </h1>
</div>
""", unsafe_allow_html=True)

# --- 3. 데이터 로드 ---
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_14.csv")

    # 숫자 변환
    df["전세가율"] = pd.to_numeric(df["전세가율"], errors="coerce")
    df["보증금.만원."] = pd.to_numeric(df["보증금.만원."], errors="coerce")
    df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
    df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

    # NaN 좌표 제거
    df = df.dropna(subset=["위도", "경도"])

    # 중복 좌표 처리
    df["위도_6"] = df["위도"].round(6)
    df["경도_6"] = df["경도"].round(6)

    return df

df = load_data()
grouped = df.groupby(["위도_6", "경도_6"])

# --- 4. 메인 화면 (지도 + GPT 상담 나란히) ---
col1, col2 = st.columns([2, 1])

# 🗺️ 지도
with col1:
    st.subheader("🗺️ 수원시 전세사기 위험 매물 지도")

    m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    for (lat, lon), group in grouped:
        if pd.isna(lat) or pd.isna(lon):
            continue
        info = "<br>".join(
            f"<b>{row['단지명']}</b> | 보증금: {row['보증금.만원.']}만원 "
            f"| 전세가율: {row['전세가율']}% | 계약유형: {row['계약유형']}"
            for _, row in group.iterrows()
        )
        folium.Marker(location=[lat, lon], popup=info).add_to(marker_cluster)

    st_folium(m, width=750, height=600)

# 🤖 GPT 상담
with col2:
    st.subheader("🤖 GPT 상담 서비스")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 입력 폼
    with st.form("chat_form"):
        user_input = st.text_area("궁금한 점을 입력하세요", "")
        submitted = st.form_submit_button("상담 요청")

    if submitted and user_input:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 전세사기 예방 전문가입니다. 법적·실무적 조언을 쉽고 정확하게 해주세요."},
                    {"role": "user", "content": user_input}
                ]
            )
            gpt_reply = response.choices[0].message.content.strip()
            st.session_state["messages"].append({"role": "user", "content": user_input})
            st.session_state["messages"].append({"role": "assistant", "content": gpt_reply})
        except Exception as e:
            st.error(f"❌ GPT 호출 실패: {e}")

    # 대화 기록 출력
    if st.session_state["messages"]:
        st.markdown("### 💬 상담 내역")
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.markdown(f"**🙋‍♂️ 사용자:** {msg['content']}")
            else:
                st.markdown(f"**🤖 GPT:** {msg['content']}")
