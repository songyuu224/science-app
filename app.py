import json
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="중학 과학 암기 마스터", page_icon="🧪", layout="centered")

# 클래스카드 스타일의 깔끔한 디자인을 위한 CSS 적용
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        background-color: #4F46E5;
        color: white;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
    }
    .card-container {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 클래스카드 스타일 중학 과학 암기 앱")
st.write("중학교 1~3학년 전 과정 핵심 개념을 플래시카드와 퀴즈로 완벽하게 정복해 보세요!")

# 데이터 로드
@st.cache_data
def load_data():
    try:
        with open("science_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("science_data.json 파일을 찾을 수 없습니다.")
        return []

data = load_data()

if data:
    # 사이드바 설정
    st.sidebar.header("📚 학습 설정")
    selected_grade = st.sidebar.selectbox("학년 선택", ["전체", "1학년", "2학년", "3학년"])
    selected_mode = st.sidebar.radio("학습 모드 선택", ["플래시카드 (용어 암기)", "5지선다 퀴즈", "서술형 테스트"])

    # 필터링
    filtered = data
    if selected_grade != "전체":
        filtered = [d for d in filtered if d.get("grade") == selected_grade]

    mode_map = {
        "플래시카드 (용어 암기)": "card",
        "5지선다 퀴즈": "mcq",
        "서술형 테스트": "short"
    }
    target_type = mode_map[selected_mode]
    filtered = [d for d in filtered if d.get("type") == target_type]

    if not filtered:
        st.info("선택한 조건에 해당하는 문제가 없습니다.")
    else:
        # 세션 인덱스 관리
        if "quiz_idx" not in st.session_state:
            st.session_state.quiz_idx = 0

        idx = st.session_state.quiz_idx % len(filtered)
        item = filtered[idx]

        st.caption(f"📌 [{item.get('grade')}] {item.get('unit')} | 진행도: {idx + 1} / {len(filtered)}")

        # --- 1) 플래시카드 모드 ---
        if target_type == "card":
            st.markdown(f"""
                <div style="padding: 30px; border-radius: 12px; background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); text-align: center; margin-bottom: 20px;">
                    <h3 style="color: #312E81; margin-bottom: 10px;">🎴 암기 용어</h3>
                    <h1 style="color: #1E1B4B; font-size: 2.2rem;">{item['term']}</h1>
                </div>
            """, unsafe_allow_html=True)

            if st.button("💡 뜻/정의 확인하기"):
                if "show_card" not in st.session_state:
                    st.session_state.show_card = True
                else:
                    st.session_state.show_card = not st.session_state.show_card

            if st.session_state.get("show_card", False):
                st.success(f"**정의:** {item['definition']}")

        # --- 2) 5지선다 퀴즈 모드 (상세 오답 피드백 포함) ---
        elif target_type == "mcq":
            with st.container():
                st.markdown(f"#### Q. {item['question']}")
                user_choice = st.radio("정답을 선택하세요:", item['options'], key=f"mcq_{idx}")
                
                if st.button("정답 제출 및 오답 풀이 확인"):
                    choice_num = int(user_choice.split(".")[0])
                    if choice_num == item['answer']:
                        st.success("🎉 정답입니다! 아주 잘하고 있어요!")
                    else:
                        st.error(f"❌ 틀렸습니다! 정답은 **{item['answer']}번**입니다.")
                    
                    # 상세 오답 노트/해설 박스
                    with st.expander("📖 상세 오답 풀이 및 해설 보기", expanded=True):
                        st.info(f"**[해설]**\n\n{item.get('explanation', '해설이 없습니다.')}")

        # --- 3) 서술형 테스트 모드 (모범 답안 및 상세 풀이 제공) ---
        elif target_type == "short":
            with st.container():
                st.markdown(f"#### Q. {item['question']}")
                user_answer = st.text_area("답안을 자유롭게 입력해 보세요:", key=f"short_{idx}")
                
                if st.button("모범 답안 및 상세 해설 확인"):
                    st.warning(f"📝 **모범 답안:** {item['answer']}")
                    
                    with st.expander("📖 상세 채점 기준 및 해설 보기", expanded=True):
                        st.info(f"**[해설]**\n\n{item.get('explanation', '해설이 없습니다.')}")

        st.write("")
        # 이전/다음 이동 버튼
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전 문제"):
                st.session_state.quiz_idx -= 1
                st.session_state.show_card = False
                st.rerun()
        with col2:
            if st.button("다음 문제 ➡️"):
                st.session_state.quiz_idx += 1
                st.session_state.show_card = False
                st.rerun()