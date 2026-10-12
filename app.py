import json
import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="중학 과학 완벽 암기장",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 클래스카드 스타일 부드러운 전환 애니메이션 CSS 강화
st.markdown(
    """
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {
            font-family: 'Pretendard', sans-serif !important;
        }
        
        /* 부드러운 카드 및 문제 전환 애니메이션 */
        @keyframes classcardFade {
            0% { opacity: 0; transform: translateY(12px) scale(0.98); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .anim-card {
            animation: classcardFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        .main-title {
            font-size: 28px;
            font-weight: 800;
            color: #0f172a;
            text-align: center;
            margin-bottom: 2px;
        }
        
        .sub-title {
            font-size: 14px;
            color: #64748b;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .card-box {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 2px solid #cbd5e1;
            border-radius: 20px;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }
        
        .card-term {
            font-size: 32px;
            font-weight: 700;
            color: #0284c7;
            margin-bottom: 15px;
        }
        
        .card-def {
            font-size: 19px;
            color: #334155;
            line-height: 1.6;
        }
        
        .stButton>button {
            border-radius: 12px;
            font-weight: 600;
            height: 50px;
            width: 100%;
            transition: all 0.2s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .control-panel {
            background-color: #f1f5f9;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 25px;
            border: 1px solid #e2e8f0;
        }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
  try:
    with open("science_data.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    return []


data = load_data()

st.markdown('<p class="main-title">🧪 중학 과학 클래스카드</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">암기부터 객관식·서술형 문제 및 실전 테스트까지 완벽'
    " 대비</p>",
    unsafe_allow_html=True,
)

if not data:
  st.error("⚠️ `science_data.json` 파일을 찾을 수 없습니다.")
else:
  # 메인 화면 접근성 최적화 패널
  st.markdown('<div class="control-panel">', unsafe_allow_html=True)
  col_a, col_b = st.columns(2)

  with col_a:
    grades = sorted(list(set(item["grade"] for item in data)))
    selected_grade = st.selectbox("📚 학년 선택", grades)

  units_in_grade = sorted(
      list(
          set(
              item["unit"]
              for item in data
              if item["grade"] == selected_grade
          )
      )
  )
  with col_b:
    selected_unit = st.selectbox(
        "📖 단원 선택", ["전체 단원 보기"] + units_in_grade
    )

  # 용어 변경 반영 (암기, 객관식 문제, 서술형 문제, 실전 테스트)
  mode = st.radio(
      "🎯 학습 모드 선택",
      [
          "🃏 암기",
          "📝 객관식 문제 (오답 반복)",
          "✍️ 서술형 문제 (오답 반복)",
          "🏆 실전 테스트",
      ],
      horizontal=True,
  )
  st.markdown("</div>", unsafe_allow_html=True)

  if selected_unit == "전체 단원 보기":
    filtered_data = [item for item in data if item["grade"] == selected_grade]
  else:
    filtered_data = [
        item
        for item in data
        if item["grade"] == selected_grade and item["unit"] == selected_unit
    ]

  if not filtered_data:
    st.warning("해당 조건에 등록된 학습 내용이 없습니다.")
  else:
    st.markdown('<div class="anim-card">', unsafe_allow_html=True)

    # 1. 암기 모드
    if mode == "🃏 암기":
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
        st.info("이 조건에는 등록된 암기 카드가 없습니다.")
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
          if st.button("⬅️ 이전 카드"):
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
          if st.button("다음 카드 ➡️"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(
                cards
            )
            st.session_state.show_definition = False
            st.rerun()

    # 2. 객관식 문제 모드 (오답 반복)
    elif mode == "📝 객관식 문제 (오답 반복)":
      quiz_items = [item for item in filtered_data if item["type"] == "mcq"]

      if not quiz_items:
        st.info("이 조건에는 등록된 객관식 문제가 없습니다.")
      else:
        if "quiz_queue_mcq" not in st.session_state or st.session_state.get(
            "current_filter_mcq"
        ) != (selected_grade, selected_unit):
          shuffled = list(quiz_items)
          random.shuffle(shuffled)
          st.session_state.quiz_queue_mcq = shuffled
          st.session_state.orig_count_mcq = len(quiz_items)
          st.session_state.current_filter_mcq = (selected_grade, selected_unit)
          st.session_state.score_mcq = 0
          st.session_state.sub_mcq = False

        queue = st.session_state.quiz_queue_mcq
        total = st.session_state.orig_count_mcq

        if len(queue) == 0:
          st.success("🎉 완벽합니다! 이 단원의 객관식을 모두 마스터하셨습니다!")
          if st.button("🔄 객관식 문제 다시 풀기"):
            new_s = list(quiz_items)
            random.shuffle(new_s)
            st.session_state.quiz_queue_mcq = new_s
            st.session_state.sub_mcq = False
            st.rerun()
        else:
          current_q = queue[0]
          solved = total - len(queue)
          st.progress(solved / total)
          st.markdown(
              f"**남은 문제:** {len(queue)}개 | **맞춘 누적 횟수:**"
              f" {st.session_state.score_mcq}"
          )
          st.markdown(f"### [{current_q['unit']}]")
          st.markdown(f"**Q. {current_q['question']}**")

          user_choice = st.radio(
              "정답을 선택하세요:",
              current_q["options"],
              key=f"mcq_{current_q['question']}_{len(queue)}",
          )

          if not st.session_state.sub_mcq:
            if st.button("정답 제출하기"):
              selected_num = int(user_choice.split(".")[0])
              st.session_state.sub_mcq = True
              st.session_state.is_corr_mcq = (
                  selected_num == current_q["answer"]
              )
              st.rerun()
          else:
            if st.session_state.is_corr_mcq:
              st.success("정답입니다! 👏 깔끔하게 맞추셨네요!")
              if st.button("다음 문제로 ➡️"):
                st.session_state.quiz_queue_mcq.pop(0)
                st.session_state.score_mcq += 1
                st.session_state.sub_mcq = False
                st.rerun()
            else:
              st.error(f"오답입니다. 🥲 정답은 **{current_q['answer']}번**입니다.")
              st.info(f"💡 **해설**: {current_q['explanation']}")
              if st.button("🔄 틀린 문제 다시 도전하기 (맞출 때까지 반복!)"):
                wrong = st.session_state.quiz_queue_mcq.pop(0)
                st.session_state.quiz_queue_mcq.append(wrong)
                st.session_state.sub_mcq = False
                st.rerun()

    # 3. 서술형 문제 모드 (오답 반복)
    elif mode == "✍️ 서술형 문제 (오답 반복)":
      short_items = [item for item in filtered_data if item["type"] == "short"]

      if not short_items:
        st.info("이 조건에는 등록된 서술형 문제가 없습니다.")
      else:
        if "quiz_queue_short" not in st.session_state or st.session_state.get(
            "current_filter_short"
        ) != (selected_grade, selected_unit):
          shuffled = list(short_items)
          random.shuffle(shuffled)
          st.session_state.quiz_queue_short = shuffled
          st.session_state.orig_count_short = len(short_items)
          st.session_state.current_filter_short = (selected_grade, selected_unit)
          st.session_state.score_short = 0
          st.session_state.sub_short = False

        queue = st.session_state.quiz_queue_short
        total = st.session_state.orig_count_short

        if len(queue) == 0:
          st.success(
              "🎉 완벽합니다! 이 단원의 서술형 문제를 모두 정복하셨습니다!"
          )
          if st.button("🔄 서술형 문제 다시 풀기"):
            new_s = list(short_items)
            random.shuffle(new_s)
            st.session_state.quiz_queue_short = new_s
            st.session_state.sub_short = False
            st.rerun()
        else:
          current_q = queue[0]
          solved = total - len(queue)
          st.progress(solved / total)
          st.markdown(
              f"**남은 문제:** {len(queue)}개 | **맞춘 누적 횟수:**"
              f" {st.session_state.score_short}"
          )
          st.markdown(f"### [{current_q['unit']}]")
          st.markdown(f"**Q. {current_q['question']}**")

          user_input = st.text_input(
              "정답을 입력하세요:",
              key=f"short_input_{current_q['question']}_{len(queue)}",
          )

          if not st.session_state.sub_short:
            if st.button("정답 제출하기"):
              st.session_state.sub_short = True
              clean_input = user_input.strip().replace(" ", "")
              clean_answer = str(current_q["answer"]).strip().replace(" ", "")
              st.session_state.is_corr_short = clean_input == clean_answer
              st.rerun()
          else:
            if st.session_state.is_corr_short:
              st.success("정답입니다! 👏 완벽해요!")
              if st.button("다음 문제로 ➡️"):
                st.session_state.quiz_queue_short.pop(0)
                st.session_state.score_short += 1
                st.session_state.sub_short = False
                st.rerun()
            else:
              st.error(f"아쉽네요! 정답은 **'{current_q['answer']}'** 입니다.")
              st.info(f"💡 **해설**: {current_q['explanation']}")
              if st.button("🔄 틀린 문제 다시 도전하기 (맞출 때까지 반복!)"):
                wrong = st.session_state.quiz_queue_short.pop(0)
                st.session_state.quiz_queue_short.append(wrong)
                st.session_state.sub_short = False
                st.rerun()

    # 4. 실전 테스트 모드
    elif mode == "🏆 실전 테스트":
      test_items = [
          item for item in filtered_data if item["type"] in ["mcq", "short"]
      ]

      if not test_items:
        st.info("실전 테스트에 출제할 문제가 부족합니다.")
      else:
        if "test_started" not in st.session_state or st.session_state.get(
            "test_filter"
        ) != (selected_grade, selected_unit):
          st.session_state.test_started = False
          st.session_state.test_filter = (selected_grade, selected_unit)

        if not st.session_state.test_started:
          st.markdown(
              "### 📝 실전 테스트 모드 안내\n- 선택한 단원의 문제 중"
              " 무작위로 최대 5문제가 출제됩니다.\n- 제한 없이 쭉 풀고 난 뒤"
              " **최종 점수와 오답 노트**를 확인할 수 있습니다!"
          )
          if st.button("🚀 테스트 시작하기"):
            selected_tests = random.sample(
                test_items, min(5, len(test_items))
            )
            st.session_state.test_questions = selected_tests
            st.session_state.test_answers = {}
            st.session_state.test_submitted = False
            st.session_state.test_started = True
            st.rerun()
        else:
          questions = st.session_state.test_questions

          if not st.session_state.test_submitted:
            st.markdown("### ✍️ 테스트 진행 중...")
            user_responses = {}

            for idx, q in enumerate(questions):
              st.markdown(
                  f"**문제 {idx + 1}. [{q['unit']}] {q['question']}**"
              )
              if q["type"] == "mcq":
                ans = st.radio(
                    "보기 선택",
                    q["options"],
                    key=f"test_mcq_{idx}",
                    label_visibility="collapsed",
                )
                user_responses[idx] = int(ans.split(".")[0])
              else:
                ans = st.text_input(
                    "정답 입력",
                    key=f"test_short_{idx}",
                    label_visibility="collapsed",
                )
                user_responses[idx] = ans.strip().replace(" ", "")
              st.markdown("---")

            if st.button("🏁 테스트 채점하기"):
              st.session_state.test_answers = user_responses
              st.session_state.test_submitted = True
              st.rerun()
          else:
            st.markdown("### 📊 실전 테스트 채점 결과")
            score = 0
            questions = st.session_state.test_questions
            user_ans = st.session_state.test_answers

            for idx, q in enumerate(questions):
              user_val = user_ans.get(idx)
              if q["type"] == "mcq":
                is_ok = user_val == q["answer"]
                correct_str = f"{q['answer']}번"
              else:
                correct_str = str(q["answer"])
                is_ok = user_val == correct_str.replace(" ", "")

              if is_ok:
                score += 1
                st.success(
                    f"문제 {idx + 1}: 정답! 🎉 (제출한 답: {user_val})"
                )
              else:
                st.error(
                    f"문제 {idx + 1}: 오답 🥲 (제출한 답: {user_val} / 정답:"
                    f" {correct_str})"
                )
                st.info(f"💡 해설: {q['explanation']}")

            total_q = len(questions)
            st.markdown(
                f"### 🎯 최종 점수: {score} / {total_q} 점"
                f" ({int(score/total_q*100)}점)"
            )

            if st.button("🔄 테스트 다시 풀기"):
              st.session_state.test_started = False
              st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
