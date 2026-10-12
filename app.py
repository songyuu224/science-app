import json
import random
import streamlit as st

# 페이지 기본 설정 (모바일 최적화)
st.set_page_config(
    page_title="중학 과학 완벽 암기장",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 커스텀 CSS (폰트 및 클래스카드 스타일 UI)
st.markdown(
    """
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {
            font-family: 'Pretendard', sans-serif !important;
        }
        
        .main-title {
            font-size: 26px;
            font-weight: 800;
            color: #1E293B;
            text-align: center;
            margin-bottom: 5px;
        }
        
        .sub-title {
            font-size: 14px;
            color: #64748B;
            text-align: center;
            margin-bottom: 25px;
        }
        
        .card-box {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
        
        .card-term {
            font-size: 28px;
            font-weight: 700;
            color: #0284c7;
            margin-bottom: 15px;
        }
        
        .card-def {
            font-size: 18px;
            color: #334155;
            line-height: 1.6;
        }
        
        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
            height: 48px;
            width: 100%;
        }
    </style>
""",
    unsafe_allow_html=True,
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

# 헤더 타이틀
st.markdown(
    '<p class="main-title">🧪 중학 과학 끝판왕 암기장</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-title">학년별 단원 선택 · 랜덤 플래시카드 · 스마트 오답 반복'
    ' 퀴즈</p>',
    unsafe_allow_html=True,
)

if not data:
  st.error("⚠️ `science_data.json` 파일을 찾을 수 없거나 데이터가 비어 있습니다.")
else:
  # 사이드바 설정 (학년 및 모드 선택)
  st.sidebar.header("🎯 학습 설정")

  grades = sorted(list(set(item["grade"] for item in data)))
  selected_grade = st.sidebar.selectbox("학년 선택", grades)

  units_in_grade = sorted(
      list(
          set(
              item["unit"]
              for item in data
              if item["grade"] == selected_grade
          )
      )
  )
  selected_unit = st.sidebar.selectbox(
      "단원 선택", ["전체 단원 보기"] + units_in_grade
  )

  mode = st.sidebar.radio(
      "학습 모드 선택",
      ["🃏 플래시카드 (랜덤 암기)", "📝 퀴즈 (랜덤 5지선다 & 서술형 + 오답 반복)"],
  )

  # 데이터 필터링
  if selected_unit == "전체 단원 보기":
    filtered_data = [item for item in data if item["grade"] == selected_grade]
  else:
    filtered_data = [
        item
        for item in data
        if item["grade"] == selected_grade and item["unit"] == selected_unit
    ]

  if not filtered_data:
    st.warning("해당 조건에 등록된 문제가 아직 없습니다.")
  else:
    # -------------------------------------------------------------------------
    # 1. 플래시카드 모드 (랜덤 섞기 적용)
    # -------------------------------------------------------------------------
    if mode == "🃏 플래시카드 (랜덤 암기)":
      # 학년이나 단원이 바뀔 때마다 카드를 무작위로 섞음
      if "shuffled_cards" not in st.session_state or st.session_state.get(
          "current_card_filter"
      ) != (selected_grade, selected_unit):
        cards = [item for item in filtered_data if item["type"] == "card"]
        random.shuffle(cards)
        st.session_state.shuffled_cards = cards
        st.session_state.card_idx = 0
        st.session_state.show_definition = False
        st.session_state.current_card_filter = (selected_grade, selected_unit)

      cards = st.session_state.shuffled_cards

      if not cards:
        st.info("이 조건에는 등록된 플래시카드가 없습니다.")
      else:
        if st.session_state.card_idx >= len(cards):
          st.session_state.card_idx = 0

        current_card = cards[st.session_state.card_idx]

        st.markdown(
            f"**[{selected_grade} / {current_card['unit']}]** (카드"
            f" {st.session_state.card_idx + 1} / {len(cards)})"
        )

        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card-term">{current_card["term"]}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.show_definition:
          st.markdown(
              f'<div class="card-def">{current_card["definition"]}</div>',
              unsafe_allow_html=True,
          )
        else:
          st.markdown(
              '<div style="color: #94a3b8; font-size: 15px;">👆 아래 버튼을'
              " 눌러 뜻을 확인하세요</div>",
              unsafe_allow_html=True,
          )
        st.markdown("</div>", unsafe_allow_html=True)

        if not st.session_state.show_definition:
          if st.button("🔍 뜻 확인하기"):
            st.session_state.show_definition = True
            st.rerun()
        else:
          if st.button("🙈 뜻 숨기기"):
            st.session_state.show_definition = False
            st.rerun()

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
          if st.button("⬅️ 이전"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(
                cards
            )
            st.session_state.show_definition = False
            st.rerun()
        with col2:
          if st.button("🔀 카드 섞기"):
            random.shuffle(cards)
            st.session_state.card_idx = 0
            st.session_state.show_definition = False
            st.rerun()
        with col3:
          if st.button("다음 ➡️"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(
                cards
            )
            st.session_state.show_definition = False
            st.rerun()

    # -------------------------------------------------------------------------
    # 2. 퀴즈 모드 (랜덤 출제 + 틀린 문제 무한 반복)
    # -------------------------------------------------------------------------
    else:
      quiz_items = [
          item for item in filtered_data if item["type"] in ["mcq", "short"]
      ]

      if not quiz_items:
        st.info("이 조건에는 등록된 퀴즈 문제가 없습니다.")
      else:
        # 학년/단원이 바뀌면 문제를 랜덤하게 섞어서 큐 생성
        if "quiz_queue" not in st.session_state or st.session_state.get(
            "current_grade_unit_quiz"
        ) != (selected_grade, selected_unit):
          shuffled_quiz = list(quiz_items)
          random.shuffle(shuffled_quiz)
          st.session_state.quiz_queue = shuffled_quiz
          st.session_state.original_quiz_count = len(quiz_items)
          st.session_state.current_grade_unit_quiz = (
              selected_grade,
              selected_unit,
          )
          st.session_state.quiz_score = 0
          st.session_state.submitted = False

        queue = st.session_state.quiz_queue
        total_orig = st.session_state.original_quiz_count

        if len(queue) == 0:
          st.success("🎉 대단합니다! 모든 문제를 완벽하게 맞추셨습니다!")
          if st.button("🔄 다시 풀기 (새로 섞기)"):
            new_shuffled = list(quiz_items)
            random.shuffle(new_shuffled)
            st.session_state.quiz_queue = new_shuffled
            st.session_state.submitted = False
            st.rerun()
        else:
          current_q = queue[0]
          solved_count = total_orig - len(queue)

          st.progress(solved_count / total_orig)
          st.markdown(
              f"**남은 문제:** {len(queue)}문제 | **맞춘 누적 횟수:"
              f"** {st.session_state.quiz_score}"
          )
          st.markdown(f"### [{current_q['unit']}]")
          st.markdown(f"**Q. {current_q['question']}**")

          # 5지선다 객관식
          if current_q["type"] == "mcq":
            user_choice = st.radio(
                "정답을 선택하세요:",
                current_q["options"],
                key=f"q_{current_q['question']}_{len(queue)}",
            )

            if not st.session_state.submitted:
              if st.button("정답 제출하기"):
                selected_num = int(user_choice.split(".")[0])
                st.session_state.submitted = True
                st.session_state.is_correct = (
                    selected_num == current_q["answer"]
                )
                st.rerun()
            else:
              if st.session_state.is_correct:
                st.success("정답입니다! 👏 깔끔하게 맞추셨네요!")
                if st.button("다음 문제로 ➡️"):
                  st.session_state.quiz_queue.pop(0)
                  st.session_state.quiz_score += 1
                  st.session_state.submitted = False
                  st.rerun()
              else:
                st.error(
                    f"오답입니다. 🥲 정답은 **{current_q['answer']}번**입니다."
                )
                st.info(f"💡 **해설**: {current_q['explanation']}")
                if st.button(
                    "🔄 틀린 문제 다시 도전하기 (맞출 때까지 반복!)"
                ):
                  wrong_item = st.session_state.quiz_queue.pop(0)
                  st.session_state.quiz_queue.append(wrong_item)
                  st.session_state.submitted = False
                  st.rerun()

          # 서술형/단답형
          elif current_q["type"] == "short":
            user_input = st.text_input(
                "정답을 적어주세요:",
                key=f"short_{current_q['question']}_{len(queue)}",
            )

            if not st.session_state.submitted:
              if st.button("정답 제출하기"):
                st.session_state.submitted = True
                clean_input = user_input.strip().replace(" ", "")
                clean_answer = str(current_q["answer"]).strip().replace(" ", "")
                st.session_state.is_correct = clean_input == clean_answer
                st.rerun()
            else:
              if st.session_state.is_correct:
                st.success("정답입니다! 👏 완벽해요!")
                if st.button("다음 문제로 ➡️"):
                  st.session_state.quiz_queue.pop(0)
                  st.session_state.quiz_score += 1
                  st.session_state.submitted = False
                  st.rerun()
              else:
                st.error(
                    f"아쉽네요! 정답은 **'{current_q['answer']}'** 입니다."
                )
                st.info(f"💡 **해설**: {current_q['explanation']}")
                if st.button(
                    "🔄 틀린 문제 다시 도전하기 (맞출 때까지 반복!)"
                ):
                  wrong_item = st.session_state.quiz_queue.pop(0)
                  st.session_state.quiz_queue.append(wrong_item)
                  st.session_state.submitted = False
                  st.rerun()
