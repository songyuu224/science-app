import json
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="중학교 과학 마스터 플래시카드 & 문제 은행",
    page_icon="🧪",
    layout="wide",
)


# 데이터 로드 함수
@st.cache_data
def load_data():
  try:
    with open("science_data.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    return []


data = load_data()

st.title("🧪 중학교 과학 소단원별 암기 카드 & 문제 은행")
st.markdown(
    "원하는 **학년**과 **소단원**을 선택하여 암기 카드(그림 설명 포함)와 객관식·서술형 문제를"
    " 학습해 보세요!"
)

if not data:
  st.error(
      "❌ `science_data.json` 파일을 찾을 수 없습니다. 파일을 프로젝트 폴더에"
      " 업로드해 주세요."
  )
else:
  # 학년 목록 추출
  grades = sorted(list(set(item["grade"] for item in data)))
  selected_grade = st.sidebar.selectbox("학년 선택", grades)

  # 선택된 학년에 해당하는 단원 목록 추출
  units = sorted(
      list(
          set(
              item["unit"]
              for item in data
              if item["grade"] == selected_grade
          )
      )
  )
  selected_unit = st.sidebar.selectbox("소단원 선택", units)

  # 사이드바 학습 모드 선택
  mode = st.sidebar.radio(
      "학습 모드 선택", ["🎴 암기 파트 (플래시카드 & 그림)", "📝 문제 은행 (객관식/서술형)"]
  )

  # 필터링된 데이터
  filtered_data = [
      item
      for item in data
      if item["grade"] == selected_grade and item["unit"] == selected_unit
  ]

  # -------------------------------------------------------------
  # 1. 암기 파트 (플래시카드 + 그림 설명)
  # -------------------------------------------------------------
  if mode == "🎴 암기 파트 (플래시카드 & 그림)":
    st.header(f"🎴 {selected_unit} - 암기 플래시카드")
    st.markdown(
        "핵심 개념과 **그림/도식 설명**을 통해 직관적으로 개념을 암기해"
        " 보세요."
    )
    st.divider()

    cards = [item for item in filtered_data if item["type"] == "card"]

    if not cards:
      st.info("이 단원에 등록된 암기 카드가 없습니다.")
    else:
      for idx, card in enumerate(cards):
        with st.container():
          st.subheader(f"카드 {idx + 1}. {card['term']}")
          st.info(f"💡 핵심 정의:")

          # 🖼️ 새로 추가된 그림 설명 표시 부분
          if "image_description" in card and card["image_description"]:
            st.warning(f"🖼️ **[그림으로 이해하기]**\n\n{card['image_description']}")

          # 실제 이미지 URL이 있는 경우 이미지 렌더링
          if "image_url" in card and card["image_url"]:
            st.image(
                card["image_url"],
                caption=card["term"],
                use_column_width=True,
            )

          st.markdown("---")

  # -------------------------------------------------------------
  # 2. 문제 은행 (객관식 & 서술형)
  # -------------------------------------------------------------
  elif mode == "📝 문제 은행 (객관식/서술형)":
    st.header(f"📝 {selected_unit} - 문제 풀기")
    st.markdown("객관식과 서술형 문제를 풀며 실력을 점검해 보세요.")
    st.divider()

    # 객관식 문제들
    mcqs = [item for item in filtered_data if item["type"] == "mcq"]
    if mcqs:
      st.subheader("📌 객관식 문제")
      for idx, q in enumerate(mcqs):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")

        # 보기 출력
        user_choice = st.radio(
            f"정답을 선택하세요 (Q{idx + 1})",
            options=range(len(q["options"])),
            format_func=lambda x: q["options"][x],
            key=f"mcq_{selected_unit}_{idx}",
        )

        # 정답 확인 버튼
        if st.button(f"정답 확인 (Q{idx + 1})", key=f"btn_mcq_{selected_unit}_{idx}"):
          if user_choice + 1 == q["answer"]:
            st.success(f"정답입니다! 🎉\n\n**해설:** {q['explanation']}")
          else:
            st.error(
                f"틀렸습니다. 정답은 {q['answer']}번 입니다.\n\n**해설:**"
                f" {q['explanation']}"
            )
        st.markdown("---")

    # 서술형 문제들
    shorts = [item for item in filtered_data if item["type"] == "short"]
    if shorts:
      st.subheader("✍️ 서술형 문제")
      for idx, s in enumerate(shorts):
        st.markdown(f"**S{idx + 1}. {s['question']}**")

        user_answer = st.text_area(
            f"답안을 작성하세요 (S{idx + 1})", key=f"short_{selected_unit}_{idx}"
        )

        if st.button(
            f"모범 답안 확인 (S{idx + 1})", key=f"btn_short_{selected_unit}_{idx}"
        ):
          if user_answer.strip():
            st.info(f"✨ **모범 답안:** {s['answer']}")
            st.markdown(f"💡 **채점 기준 및 해설:** {s['explanation']}")
          else:
            st.warning("답안을 먼저 입력해 주세요!")
        st.markdown("---")
