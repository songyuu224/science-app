import json
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="중학교 과학 마스터 & 개념 학습", page_icon="🧪", layout="wide"
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

st.title("🧪 중학교 과학 학습 플랫폼 (개념 · 암기 · 문제)")
st.markdown(
    "원하는 **학년**과 **소단원**을 선택한 뒤, **[개념 파트]**로 기초를 잡고,"
    " **[암기 파트]**와 **[문제 은행]**으로 실력을 완성해 보세요!"
)

if not data:
  st.error(
      "❌ `science_data.json` 파일을 찾을 수 없습니다. 프로젝트 폴더에"
      " JSON 파일이 있는지 확인해 주세요."
  )
else:
  # 학년 목록 추출
  grades = sorted(list(set(item["grade"] for item in data)))
  selected_grade = st.sidebar.selectbox("학년 선택", grades)

  # 선택된 학년에 해당하는 소단원 목록 추출
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

  # 사이드바 학습 모드 선택 (개념 파트 명시적 추가)
  mode = st.sidebar.radio(
      "학습 모드 선택",
      [
          "📖 개념 파트 (핵심 정리 & 도식)",
          "🎴 암기 파트 (플래시카드 & 그림 설명)",
          "📝 문제 은행 (객관식 / 서술형)",
      ],
  )

  # 필터링된 데이터
  filtered_data = [
      item
      for item in data
      if item["grade"] == selected_grade and item["unit"] == selected_unit
  ]

  # -------------------------------------------------------------
  # 1. 📖 개념 파트 (핵심 정리 및 개념 이해)
  # -------------------------------------------------------------
  if mode == "📖 개념 파트 (핵심 정리 & 도식)":
    st.header(f"📖 [{selected_unit}] - 개념 파트")
    st.markdown("이 소단원에서 반드시 알아야 할 **핵심 개념과 기초 정의**입니다.")
    st.divider()

    # card 타입 데이터에서 개념 정의를 뽑아와서 개념 노트 형태로 출력
    concepts = [item for item in filtered_data if item["type"] == "card"]

    if not concepts:
      st.info("이 단원에 등록된 개념 데이터가 없습니다.")
    else:
      for idx, c in enumerate(concepts):
        with st.container():
          st.subheader(f"📌 핵심 개념 {idx + 1}. {c['term']}")
          st.success(f"**[개념 및 정의]**\n\n{c['definition']}")

          # 그림/도식 설명이 함께 제공되도록 연동
          if "image_description" in c and c["image_description"]:
            st.info(f"🖼️ **[개념 도식 및 그림 설명]**\n\n{c['image_description']}")

          if "image_url" in c and c["image_url"]:
            st.image(c["image_url"], caption=c["term"], use_column_width=True)

          st.markdown("---")

  # -------------------------------------------------------------
  # 2. 🎴 암기 파트 (플래시카드 + 그림 설명)
  # -------------------------------------------------------------
  elif mode == "🎴 암기 파트 (플래시카드 & 그림 설명)":
    st.header(f"🎴 [{selected_unit}] - 암기 파트")
    st.markdown("개념을 확실히 내 것으로 만들기 위한 **암기 플래시카드**입니다.")
    st.divider()

    cards = [item for item in filtered_data if item["type"] == "card"]

    if not cards:
      st.info("이 단원에 등록된 암기 카드가 없습니다.")
    else:
      for idx, card in enumerate(cards):
        with st.container():
          st.subheader(f"🎴 암기 카드 {idx + 1}. {card['term']}")
          st.warning(f"💡 정의:")

          if "image_description" in card and card["image_description"]:
            st.info(f"🖼️ **[그림으로 이해하기]**\n\n{card['image_description']}")

          if "image_url" in card and card["image_url"]:
            st.image(
                card["image_url"],
                caption=card["term"],
                use_column_width=True,
            )

          st.markdown("---")

  # -------------------------------------------------------------
  # 3. 📝 문제 은행 (객관식 & 서술형)
  # -------------------------------------------------------------
  elif mode == "📝 문제 은행 (객관식 / 서술형)":
    st.header(f"📝 [{selected_unit}] - 문제 은행")
    st.markdown("객관식과 서술형 문제를 풀며 실력을 점검해 보세요.")
    st.divider()

    # 객관식 문제들
    mcqs = [item for item in filtered_data if item["type"] == "mcq"]
    if mcqs:
      st.subheader("📌 객관식 문제")
      for idx, q in enumerate(mcqs):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")

        user_choice = st.radio(
            f"정답을 선택하세요 (Q{idx + 1})",
            options=range(len(q["options"])),
            format_func=lambda x: q["options"][x],
            key=f"mcq_{selected_unit}_{idx}",
        )

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
