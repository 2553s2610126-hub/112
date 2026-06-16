import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="학과별 진로 추천",
    page_icon="🎓"
)

st.title("🎓 학과별 진로 추천")
st.write("관심 있는 학과를 입력하면 관련 진로를 추천해드립니다.")

# API 연결
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ GEMINI_API_KEY를 불러오지 못했습니다.")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력창
user_input = st.chat_input("예: 컴퓨터공학과, 간호학과, 심리학과")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # 대화 기록 생성
        history = ""
        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "AI"
            history += f"{role}: {msg['content']}\n"

        prompt = f"""
당신은 고등학생을 위한 진로 상담 전문가입니다.

사용자가 입력한 학과를 바탕으로 아래 형식대로 친절하게 설명해주세요.

### 1. 학과 소개
간단히 설명

### 2. 관련 직업 (5개 이상)

### 3. 필요한 역량

### 4. 추천 자격증

### 5. 대학 생활에서 하면 좋은 활동

### 6. 고등학생 때 준비하면 좋은 것

### 7. 한줄 조언

대답은 이해하기 쉽게 작성하세요.

대화 내용:
{history}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        answer = response.text

    except Exception:
        answer = """
⚠️ 현재 AI 응답을 가져오지 못했습니다.

잠시 후 다시 시도해주세요.
"""

    # AI 답변 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

# 사이드바
with st.sidebar:
    st.header("📚 추천 학과")

    examples = [
        "컴퓨터공학과",
        "간호학과",
        "심리학과",
        "교육학과",
        "경영학과",
        "화학공학과",
        "디자인학과",
        "수의학과"
    ]

    for major in examples:
        st.write("•", major)

    st.divider()

    if st.button("🗑️ 대화 기록 초기화"):
        st.session_state.messages = []
        st.rerun()
