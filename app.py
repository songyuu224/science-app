import json
import random
import streamlit as st

# 페이지 설정 (와이드 레이아웃)
st.set_page_config(
    page_title="중학 과학 마스터 플랫폼", page_icon="🧪", layout="wide"
)


# 데이터 로드 함수 (캐시 적용)
@st.cache_data
def load_data():
  try:
    with open("science_data.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    return []


data = load_data()

# -------------------------------------------------------------
# 사이드바: 학년 및 단원 필터 (전역 설정)
# -------------------------------------------------------------
st.sidebar.markdown("### 🎛️ 학습 설정")
if not data:
  grades = ["1학년"]
  units = ["데이터 없음"]
else:
  grades = sorted(list(set(item["grade"] for item in data)))
selected_grade = st.sidebar.selectbox("📚 학년 선택", grades)

if data:
  unit_list = sorted(
      list(
          set(
              item["unit"]
              for item in data
              if item["grade"] == selected_grade
          )
      )
  )
  unit_options = ["전체 단원 보기"] + unit_list
else:
  unit_options = ["전체 단원 보기"]
selected_unit = st.sidebar.selectbox("📖 단원 선택", unit_options)

# 데이터 필터링
if not data:
  filtered_data = []
else:
  if selected_unit == "전체 단원 보기":
    filtered_data = [item for item in data if item["grade"] == selected_grade]
  else:
    filtered_data = [
        item
        for item in data
        if item["grade"] == selected_grade and item["unit"] == selected_unit
    ]

# -------------------------------------------------------------
# 메인 화면: 앱을 켰을 때 바로 뜨는 깔끔한 대시보드 메뉴
# -------------------------------------------------------------
st.markdown("## 🧪 중학 과학 복습 & 암기 마스터 플랫폼")
st.markdown(
    "중학교 1~3학년 전 과학 개념을 완벽하게 정리하고, 암기와 실전 문제까지"
    " 한 번에 해결하세요!"
)
st.divider()

# 세션 상태를 이용한 페이지(창) 전환 관리
if "current_page" not in st.session_state:
  st.session_state.current_page = "메인 홈"

# 상단 또는 메인 카드 형태의 네비게이션 버튼 영역
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

with col_m1:
  if st.button("📖 개념 학습", use_container_width=True):
    st.session_state.current_page = "개념 학습"
    st.rerun()
with col_m2:
  if st.button("🎴 암기 플래시카드", use_container_width=True):
    st.session_state.current_page = "암기 파트"
    st.rerun()
with col_m3:
  if st.button("📝 객관식 문제", use_container_width=True):
    st.session_width = "객관식 문제"
    st.session_state.current_page = "객관식 문제"
    st.rerun()
with col_m4:
  if st.button("✍️ 서술형 주관식", use_container_width=True):
    st.session_state.current_page = "서술형 문제"
    st.rerun()
with col_m5:
  if st.button("🏆 실전 테스트", use_container_width=True):
    st.session_state.current_page = "실전 테스트"
    st.rerun()

st.markdown("")  # 여백

# 홈으로 돌아가기 버튼 (상세 페이지 내부용)
if st.session_state.current_page != "메인 홈":
  if st.button("🏠 메인 메뉴로 돌아가기"):
    st.session_state.current_page = "메인 홈"
    st.rerun()
  st.markdown("---")

# -------------------------------------------------------------
# 각 메뉴별 독립된 창(페이지) 렌더링
# -------------------------------------------------------------

if st.session_state.current_page == "메인 홈":
  st.info(
      "👆 위의 메뉴 버튼을 클릭하여 원하는 학습 모드(개념, 암기, 객관식, 서술형,"
      " 실전 테스트)로 바로 이동하세요!"
  )

  st.markdown("### 📊 현재 선택된 학습 정보")
  st.markdown(f"- **선택 학년:** {selected_grade}")
  st.markdown(f"- **선택 단원:** {selected_unit}")
  st.markdown(f"- **등록된 총 학습/문제 데이터 수:** {len(filtered_data)}개")

  st.markdown("---")
  st.markdown("### 💡 선생님의 학습 가이드")
  st.markdown(
      "1. **📖 개념 학습**: 선생님이 꼼꼼하게 정리한 250개 이상의 핵심 용어와"
      " 도식 설명을 먼저 읽어보세요."
  )
  st.markdown(
      "2. **🎴 암기 파트**: 카드를 넘기며 주요 개념과 시각 자료를 반복해서"
      " 암기합니다."
  )
  st.markdown(
      "3. **📝 객관식 / ✍️ 서술형**: 배운 내용을 바탕으로 학교 시험에 자주 나오는"
      " 유형을 풀어봅니다."
  )
  st.markdown(
      "4. **🏆 실전 테스트**: 단원 전체를 종합하여 나의 실력을 최종"
      " 점검합니다."
  )

elif st.session_state.current_page == "개념 학습":
  st.markdown(
      f"## 📖 [{selected_grade} / {selected_unit}] 꼼꼼 핵심 개념 노트"
  )
  st.markdown("중학교 과학에서 반드시 알아야 할 핵심 정의와 원리입니다.")
  st.divider()

  concepts = [item for item in filtered_data if item["type"] == "card"]
  if not concepts:
    st.warning("조건에 맞는 개념 데이터가 없습니다.")
  else:
    for idx, c in enumerate(concepts):
      with st.container():
        st.markdown(f"### 📌 핵심 개념 {idx + 1}: {c['term']}")
        st.success(f"**[개념 및 원리 설명]**\n\n{c['definition']}")
        if "image_description" in c and c["image_description"]:
          st.info(f"🖼️ **[시각 자료 및 도식 해설]**\n\n{c['image_description']}")
        st.markdown("---")

elif st.session_state.current_page == "암기 파트":
  st.markdown(f"## 🎴 [{selected_grade} / {selected_unit}] 암기 플래시카드")
  st.markdown("핵심 용어와 그림 설명을 보며 머릿속에 확실히인쇄하세요!")
  st.divider()

  cards = [item for item in filtered_data if item["type"] == "card"]
  if not cards:
    st.warning("등록된 암기 카드가 없습니다.")
  else:
    if "card_idx" not in st.session_state:
      st.session_state.card_idx = 0
    if st.session_state.card_idx >= len(cards):
      st.session_state.card_idx = 0

    card = cards[st.session_state.card_idx]
    st.markdown(f"**카드 번호:** {st.session_state.card_idx + 1} / {len(cards)}")

    with st.container():
      st.markdown(f"### 💡 용어: {card['term']}")
      st.warning(f"정의:")
      if "image_description" in card and card["image_description"]:
        st.info(f"🖼️ **[그림 도식 설명]**\n\n{card['image_description']}")

    c1, c2 = st.columns(2)
    with c1:
      if st.button("⬅️ 이전 카드 보기"):
        if st.session_state.card_idx > 0:
          st.session_state.card_idx -= 1
          st.rerun()
    with c2:
      if st.button("다음 카드 보기 ➡️"):
        if st.session_state.card_idx < len(cards) - 1:
          st.session_state.card_idx += 1
          st.rerun()

elif st.session_state.current_page == "객관식 문제":
  st.markdown(f"## 📝 [{selected_grade} / {selected_unit}] 객관식 문제 은행")
  st.divider()

  mcqs = [item for item in filtered_data if item["type"] == "mcq"]
  if not mcqs:
    st.warning("등록된 객관식 문제가 없습니다.")
  else:
    for idx, q in enumerate(mcqs):
      st.markdown(f"**Q{idx + 1}. {q['question']}**")
      choice = st.radio(
          f"정답 선택 (Q{idx + 1})",
          options=range(len(q["options"])),
          format_func=lambda x: q["options"][x],
          key=f"mcq_s_{idx}",
      )
      if st.button(f"정답 확인 (Q{idx + 1})", key=f"btn_mcq_{idx}"):
        if choice + 1 == q["answer"]:
          st.success(f"정답입니다! 🎉\n\n**해설:** {q['explanation']}")
        else:
          st.error(
              f"틀렸습니다. 정답은 {q['answer']}번 입니다.\n\n**해설:**"
              f" {q['explanation']}"
          )
      st.markdown("---")

elif st.session_state.current_page == "서술형 문제":
  st.markdown(f"## ✍️ [{selected_grade} / {selected_unit}] 서술형 주관식")
  st.divider()

  shorts = [item for item in filtered_data if item["type"] == "short"]
  if not shorts:
    st.warning("등록된 서술형 문제가 없습니다.")
  else:
    for idx, s in enumerate(shorts):
      st.markdown(f"**S{idx + 1}. {s['question']}**")
      ans = st.text_area(f"답안 작성 (S{idx + 1})", key=f"short_s_{idx}")
      if st.button(f"모범 답안 확인 (S{idx + 1})", key=f"btn_short_{idx}"):
        if ans.strip():
          st.info(f"✨ **모범 답안:** {s['answer']}")
          st.markdown(f"💡 **채점 기준 및 해설:** {s['explanation']}")
        else:
          st.warning("답안을 입력해 주세요!")
      st.markdown("---")

elif st.session_state.current_page == "실전 테스트":
  st.markdown(f"## 🏆 [{selected_grade} / {selected_unit}] 실전 모의고사")
  st.divider()

  tests = [item for item in filtered_data if item["type"] in ["mcq", "short"]]
  if not tests:
    st.warning("테스트 문항이 부족합니다.")
  else:
    for idx, t in enumerate(tests):
      st.markdown(f"**문제 {idx + 1}.** {t['question']}")
      if t["type"] == "mcq":
        for opt in t["options"]:
          st.write(opt)
        st.text_input(
            f"정답 번호 입력 (문제 {idx + 1})", key=f"t_ans_{idx}"
        )
      else:
        st.text_input(
            f"서술형 답안 입력 (문제 {idx + 1})", key=f"t_ans_{idx}"
        )
      st.markdown("---")
    if st.button("🏁 테스트 제출"):
      st.balloons()
      st.success("실전 테스트가 제출되었습니다! 수고하셨습니다. 👏")
