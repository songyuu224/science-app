import json
import os
import random
from PIL import Image
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="중학 과학 마스터", page_icon="🧪", layout="wide"
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

# 세션 상태 초기화
if "current_page" not in st.session_state:
  st.session_state.current_page = "메인 홈"
if "is_authenticated" not in st.session_state:
  st.session_state.is_authenticated = False  # 비밀 공간 잠금 상태

# -------------------------------------------------------------
# 사이드바: 학년 및 단원 필터
# -------------------------------------------------------------
st.sidebar.markdown("### 🎛️ 학습 설정")

if not data:
  grades = ["1학년"]
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
# 메인 화면 홈 대시보드
# -------------------------------------------------------------
st.markdown("## 🧪 중학 과학 복습 & 암기 마스터 플랫폼")
st.markdown(
    "중학교 1~3학년 전 과학 개념과 자잘한 암기, 문제 풀이를 한 번에 정복하세요!"
)
st.divider()

# 메인 네비게이션 버튼 영역
col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)

with col_m1:
  if st.button("📖 개념 학습", use_container_width=True):
    st.session_state.current_page = "개념 학습"
    st.rerun()
with col_m2:
  if st.button("🎴 암기 카드", use_container_width=True):
    st.session_state.current_page = "암기 파트"
    st.rerun()
with col_m3:
  if st.button("📝 객관식", use_container_width=True):
    st.session_state.current_page = "객관식 문제"
    st.rerun()
with col_m4:
  if st.button("✍️ 서술형", use_container_width=True):
    st.session_state.current_page = "서술형 문제"
    st.rerun()
with col_m5:
  if st.button("🏆 실전 테스트", use_container_width=True):
    st.session_state.current_page = "실전 테스트"
    st.rerun()
with col_m6:
  if st.button("🔒 Magna", use_container_width=True):
    st.session_state.current_page = "Magna"
    st.rerun()

st.markdown("")

# 상세 페이지 내부의 '메인으로 돌아가기' 버튼
if st.session_state.current_page != "메인 홈":
  if st.button("🏠 메인 메뉴로 돌아가기"):
    st.session_state.current_page = "메인 홈"
    st.rerun()
  st.markdown("---")

# -------------------------------------------------------------
# 각 메뉴별 페이지 렌더링
# -------------------------------------------------------------

if st.session_state.current_page == "메인 홈":
  st.info(
      "👆 상단의 메뉴 버튼을 클릭하여 원하는 학습 창 또는 비밀 공간으로 바로"
      " 이동하세요!"
  )

  st.markdown("### 📊 현재 학습 정보")
  st.markdown(f"- **선택 학년:** {selected_grade}")
  st.markdown(f"- **선택 단원:** {selected_unit}")
  st.markdown(f"- **등록된 총 데이터 수:** {len(filtered_data)}개")

elif st.session_state.current_page == "개념 학습":
  st.markdown(
      f"## 📖 [{selected_grade} / {selected_unit}] 꼼꼼 핵심 개념 & 암기 노트"
  )
  st.divider()

  concepts = [item for item in filtered_data if item["type"] == "card"]
  if not concepts:
    st.warning("등록된 개념 데이터가 없습니다.")
  else:
    for idx, c in enumerate(concepts):
      with st.container():
        st.markdown(f"### 📌 핵심 개념 {idx + 1}: {c['term']}")
        st.success(f"**[개념 및 공식 정리]**\n\n{c['definition']}")
        if "image_description" in c and c["image_description"]:
          st.info(f"🖼️ **[시각 자료 및 상세 해설]**\n\n{c['image_description']}")
        if "image_url" in c and c["image_url"]:
          st.image(c["image_url"], caption=c["term"])
        st.markdown("---")

elif st.session_state.current_page == "암기 파트":
  st.markdown(f"## 🎴 [{selected_grade} / {selected_unit}] 암기 플래시카드")
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
    st.markdown(
        f"**카드 번호:** {st.session_state.card_idx + 1} / {len(cards)}"
    )

    with st.container():
      st.markdown(f"### 💡 키워드: {card['term']}")
      st.warning(f"핵심 내용:")
      if "image_description" in card and card["image_description"]:
        st.info(f"🖼️ **[그림 도식 설명]**\n\n{card['image_description']}")
      if "image_url" in card and card["image_url"]:
        st.image(card["image_url"], caption=card["term"])

    c1, c2 = st.columns(2)
    with c1:
      if st.button("⬅️ 이전 카드"):
        if st.session_state.card_idx > 0:
          st.session_state.card_idx -= 1
          st.rerun()
    with c2:
      if st.button("다음 카드 ➡️"):
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
    if f"rand_mcq_{selected_grade}_{selected_unit}" not in st.session_state:
      shuffled_mcqs = mcqs.copy()
      random.shuffle(shuffled_mcqs)
      st.session_state[f"rand_mcq_{selected_grade}_{selected_unit}"] = (
          shuffled_mcqs
      )

    current_mcqs = st.session_state[
        f"rand_mcq_{selected_grade}_{selected_unit}"
    ]

    for idx, q in enumerate(current_mcqs):
      st.markdown(f"**Q{idx + 1}. {q['question']}**")
      choice = st.radio(
          f"정답 선택 (Q{idx + 1})",
          options=range(len(q["options"])),
          format_func=lambda x: q["options"][x],
          key=f"mcq_s_{selected_unit}_{idx}",
      )
      if st.button(f"정답 확인 (Q{idx + 1})", key=f"btn_mcq_{selected_unit}_{idx}"):
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
    if f"rand_short_{selected_grade}_{selected_unit}" not in st.session_state:
      shuffled_shorts = shorts.copy()
      random.shuffle(shuffled_shorts)
      st.session_state[f"rand_short_{selected_grade}_{selected_unit}"] = (
          shuffled_shorts
      )

    current_shorts = st.session_state[
        f"rand_short_{selected_grade}_{selected_unit}"
    ]

    for idx, s in enumerate(current_shorts):
      st.markdown(f"**S{idx + 1}. {s['question']}**")
      ans = st.text_area(
          f"답안 작성 (S{idx + 1})", key=f"short_s_{selected_unit}_{idx}"
      )
      if st.button(
          f"모범 답안 확인 (S{idx + 1})", key=f"btn_short_{selected_unit}_{idx}"
      ):
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
            f"정답 번호 입력 (문제 {idx + 1})", key=f"t_ans_{selected_unit}_{idx}"
        )
      else:
        st.text_input(
            f"서술형 답안 입력 (문제 {idx + 1})", key=f"t_ans_{selected_unit}_{idx}"
        )
      st.markdown("---")
    if st.button("🏁 테스트 제출"):
      st.balloons()
      st.success("실전 테스트가 제출되었습니다! 수고하셨습니다. 👏")

# 🔒 비밀 개인 공간 페이지 (영구 저장 폴더 연동, 회전/확대/삭제 기능 포함)
elif st.session_state.current_page == "Magna":
  st.markdown("## 🔒 Area Magna")
  st.markdown(
      "이곳은 과학 내용과 상관없이 나 혼자만의 메모와 사진을 영구 보관하는"
      " 공간입니다."
  )
  st.divider()

  if not st.session_state.is_authenticated:
    st.warning("⚠️ 보호된 공간입니다. 6자리 비밀번호를 입력해 주세요.")
    input_pw = st.text_input(
        "6자리 비밀번호 입력", type="password", max_chars=6
    )

    if st.button("잠금 해제"):
      if input_pw == "123456":  # 원하는 6자리 비밀번호로 변경 가능
        st.session_state.is_authenticated = True
        st.success("잠금이 해제되었습니다!")
        st.rerun()
      else:
        st.error("비밀번호 6자리가 틀렸습니다!")
  else:
    st.success("🔓 잠금이 해제되었습니다.")
    if st.button("🔒 다시 잠그기"):
      st.session_state.is_authenticated = False
      st.rerun()

    st.markdown("---")
    st.markdown("### 🖼️ 영구 보관 사진 갤러리")

    # 사진을 안전하게 저장할 폴더 자동 생성
    PHOTO_DIR = "secret_photos"
    os.makedirs(PHOTO_DIR, exist_ok=True)

    # 새로운 사진 업로드 기능
    uploaded_files = st.file_uploader(
        "새로운 사진을 업로드하면 폴더에 영구 저장됩니다",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True,
    )

    if uploaded_files:
      for file in uploaded_files:
        file_path = os.path.join(PHOTO_DIR, file.name)
        # 파일을 서버 폴더에 영구 기록
        with open(file_path, "wb") as f:
          f.write(file.getbuffer())
      st.success("새로운 사진이 영구 보관함에 저장되었습니다! 🎉")

    # 폴더에 저장되어 있는 모든 사진 목록 불러오기
    saved_photos = sorted(os.listdir(PHOTO_DIR))
    saved_photos = [
        p for p in saved_photos if p.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if saved_photos:
      selected_name = st.selectbox(
          "📁 보관된 사진 중 확인하고 싶은 사진을 선택하세요", saved_photos
      )
      file_path = os.path.join(PHOTO_DIR, selected_name)

      rot_key = f"rot_{selected_name}"
      if rot_key not in st.session_state:
        st.session_state[rot_key] = 0

      zoom_key = f"zoom_{selected_name}"
      if zoom_key not in st.session_state:
        st.session_state[zoom_key] = 100

      c_r1, c_r2, c_r3, c_r4 = st.columns([1, 1, 1, 2])
      with c_r1:
        if st.button("↺ 왼쪽 90도"):
          st.session_state[rot_key] = (st.session_state[rot_key] - 90) % 360
      with c_r2:
        if st.button("↻ 오른쪽 90도"):
          st.session_state[rot_key] = (st.session_state[rot_key] + 90) % 360
      with c_r3:
        if st.button("🗑️ 사진 삭제"):
          os.remove(file_path)
          st.success("사진이 삭제되었습니다.")
          st.rerun()

      # 확대 비율 조절 슬라이더
      zoom_percent = st.slider(
          "🔍 사진 확대 비율 조절 (%)",
          min_value=50,
          max_value=300,
          value=100,
          step=10,
          key=zoom_key,
      )

      # PIL을 이용한 회전 및 확대 처리
      image = Image.open(file_path)
      current_rotation = st.session_state[rot_key]
      if current_rotation != 0:
        image = image.rotate(current_rotation, expand=True)

      if zoom_percent != 100:
        w, h = image.size
        new_w = int(w * (zoom_percent / 100))
        new_h = int(h * (zoom_percent / 100))
        image = image.resize((new_w, new_h))

      st.image(
          image,
          caption=f"{selected_name} (회전: {current_rotation}°, 확대: {zoom_percent}%)",
          width=int(700 * (zoom_percent / 100)),
      )
    else:
      st.info("저장된 사진이 없습니다. 위에서 사진을 업로드해 보세요!")

    st.markdown("---")
    st.markdown("### 📝 비밀 메모장")
    st.text_area(
        "여기에 자유롭게 내용을 적어보세요.",
        height=200,
        placeholder="내용을 입력하세요...",
    )
    if st.button("임시 저장"):
      st.info("메모가 입력되었습니다.")
