import json
import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="중학 과학 복습 & 암기 마스터", page_icon="🧪", layout="wide"
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

# 사진 속 타이틀 및 설명 레이아웃 반영
st.markdown("### 🧪 중학 과학 복습&암기")
st.markdown(
    "암기부터 객관식·서술형 문제 및 실전 테스트까지 완벽 대비할 수 있는 학습"
    " 공간입니다."
)
st.divider()

if not data:
  st.error(
      "❌ `science_data.json` 파일을 찾을 수 없습니다. 프로젝트 폴더에"
      " 데이터 파일을 업로드해 주세요."
  )
else:
  # 학년 선택
  grades = sorted(list(set(item["grade"] for item in data)))
  selected_grade = st.sidebar.selectbox("📚 학년 선택", grades)

  # 선택된 학년에 해당하는 단원 목록 추출 ('전체 단원 보기' 옵션 포함)
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
  selected_unit = st.sidebar.selectbox("📖 단원 선택", unit_options)

  # 사진 속 학습 모드 구성에 '개념 학습' 모드 추가 확장
  mode = st.sidebar.radio(
      "🎯 학습 모드 선택",
      [
          "📖 개념 학습 (용어 & 원리)",
          "🎴 암기 (플래시카드 & 그림)",
          "📝 객관식 문제 (오답 반복)",
          "✍️ 서술형 문제 (오답 반복)",
          "🏆 실전 테스트",
      ],
  )

  # 데이터 필터링 (전체 단원 보기 지원)
  if selected_unit == "전체 단원 보기":
    filtered_data = [item for item in data if item["grade"] == selected_grade]
  else:
    filtered_data = [
        item
        for item in data
        if item["grade"] == selected_grade and item["unit"] == selected_unit
    ]

  # -------------------------------------------------------------
  # 1. 📖 개념 학습 모드 (새로 추가된 개념 파트)
  # -------------------------------------------------------------
  if mode == "📖 개념 학습 (용어 & 원리)":
    st.header(
        f"📖 [{selected_grade} / {selected_unit}] - 핵심 개념 및 용어 정리"
    )
    st.markdown(
        "문제와 암기 카드에 나오는 핵심 용어와 과학적 원리를 먼저 탄탄하게"
        " 익혀보세요."
    )
    st.divider()

    concept_items = [item for item in filtered_data if item["type"] == "card"]

    if not concept_items:
      st.info("해당 조건에 일치하는 개념 데이터가 없습니다.")
    else:
      for idx, c in enumerate(concept_items):
        with st.container():
          st.subheader(f"💡 핵심 용어 및 개념 {idx + 1}: {c['term']}")
          st.success(f"**[개념 정의]**\n\n{c['definition']}")

          if "image_description" in c and c["image_description"]:
            st.info(f"🖼️ **[원리 도식 및 그림 설명]**\n\n{c['image_description']}")

          if "image_url" in c and c["image_url"]:
            st.image(c["image_url"], caption=c["term"], use_column_width=True)

          st.markdown("---")

  # -------------------------------------------------------------
  # 2. 🎴 암기 모드 (플래시카드 & 그림 설명)
  # -------------------------------------------------------------
  elif mode == "🎴 암기 (플래시카드 & 그림)":
    st.header(f"🎴 [{selected_grade} / {selected_unit}] - 암기 플래시카드")
    st.markdown(
        "카드를 넘기며 주요 개념과 도식 설명을 반복해서 시각적으로 암기하세요."
    )
    st.divider()

    cards = [item for item in filtered_data if item["type"] == "card"]

    if not cards:
      st.info("등록된 암기 카드가 없습니다.")
    else:
      # 세션 상태로 카드 번호 관리
      if "card_index" not in st.session_state:
        st.session_state.card_index = 0

      if st.session_state.card_index >= len(cards):
        st.session_state.card_index = 0

      card = cards[st.session_state.card_index]

      st.markdown(
          f"단원: (카드 {st.session_state.card_index + 1} /"
          f" {len(cards)})"
      )

      with st.container():
        st.subheader(f"🎴 {card['term']}")
        st.warning(f"정의:")

        if "image_description" in card and card["image_description"]:
          st.info(f"🖼️ **[그림으로 이해하기]**\n\n{card['image_description']}")

        if "image_url" in card and card["image_url"]:
          st.image(card["image_url"], caption=card["term"], use_column_width=True)

      col1, col2 = st.columns(2)
      with col1:
        if st.button("⬅️ 이전 카드"):
          if st.session_state.card_index > 0:
            st.session_state.card_index -= 1
            st.rerun()
      with col2:
        if st.button("다음 카드 ➡️"):
          if st.session_state.card_index < len(cards) - 1:
            st.session_state.card_index += 1
            st.rerun()

  # -------------------------------------------------------------
  # 3. 📝 객관식 문제 모드 (오답 반복 포함)
  # -------------------------------------------------------------
  elif mode == "📝 객관식 문제 (오답 반복)":
    st.header(f"📝 [{selected_grade} / {selected_unit}] - 객관식 문제 은행")
    st.divider()

    mcqs = [item for item in filtered_data if item["type"] == "mcq"]

    if not mcqs:
      st.info("등록된 객관식 문제가 없습니다.")
    else:
      for idx, q in enumerate(mcqs):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")

        user_choice = st.radio(
            f"정답 선택 (Q{idx + 1})",
            options=range(len(q["options"])),
            format_func=lambda x: q["options"][x],
            key=f"mcq_ui_{selected_unit}_{idx}",
        )

        if st.button(
            f"정답 및 해설 확인 (Q{idx + 1})", key=f"btn_mcq_chk_{idx}"
        ):
          if user_choice + 1 == q["answer"]:
            st.success(f"정답입니다! 🎉\n\n**해설:** {q['explanation']}")
          else:
            st.error(
                f"오답입니다. 정답은 {q['answer']}번 입니다.\n\n**해설:**"
                f" {q['explanation']}"
            )
        st.markdown("---")

  # -------------------------------------------------------------
  # 4. ✍️ 서술형 문제 모드 (오답 반복 포함)
  # -------------------------------------------------------------
  elif mode == "✍️ 서술형 문제 (오답 반복)":
    st.header(f"✍️ [{selected_grade} / {selected_unit}] - 서술형 주관식")
    st.divider()

    shorts = [item for item in filtered_data if item["type"] == "short"]

    if not shorts:
      st.info("등록된 서술형 문제가 없습니다.")
    else:
      for idx, s in enumerate(shorts):
        st.markdown(f"**S{idx + 1}. {s['question']}**")

        user_answer = st.text_area(
            f"서술형 답안 작성 (S{idx + 1})", key=f"short_ui_{selected_unit}_{idx}"
        )

        if st.button(
            f"모범 답안 및 채점 기준 확인 (S{idx + 1})", key=f"btn_short_chk_{idx}"
        ):
          if user_answer.strip():
            st.info(f"✨ **모범 답안:** {s['answer']}")
            st.markdown(f"💡 **해설 및 채점 기준:** {s['explanation']}")
          else:
            st.warning("답안을 먼저 입력해 주세요!")
        st.markdown("---")

  # -------------------------------------------------------------
  # 5. 🏆 실전 테스트 모드
  # -------------------------------------------------------------
  elif mode == "🏆 실전 테스트":
    st.header(f"🏆 [{selected_grade} / {selected_unit}] - 실전 모의고사")
    st.markdown("단원별 학습한 내용을 종합하여 테스트를 진행합니다.")
    st.divider()

    test_items = [
        item for item in filtered_data if item["type"] in ["mcq", "short"]
    ]

    if not test_items:
      st.info("테스트용 문항이 부족합니다.")
    else:
      score = 0
      total = len(test_items)

      for idx, t in enumerate(test_items):
        st.markdown(f"**문제 {idx + 1}.** {t['question']}")
        if t["type"] == "mcq":
          for opt in t["options"]:
            st.write(opt)
          ans = st.text_input(
              f"정답 번호 입력 (문제 {idx + 1})", key=f"test_ans_{idx}"
          )
          if ans.strip().isdigit() and int(ans.strip()) == t["answer"]:
            score += 1
        else:
          st.text_input(f"서술형 답안 입력 (문제 {idx + 1})", key=f"test_ans_{idx}")
        st.markdown("---")

      if st.button("🏁 테스트 제출 및 결과 보기"):
        st.balloons()
        st.success(
            f"테스트가 완료되었습니다! 총 {total}개 문항 중 객관식 기준"
            f" 정답률을 확인하세요."
        )
