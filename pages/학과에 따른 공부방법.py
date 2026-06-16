import streamlit as st
from google import genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="학과별 공부방법 챗봇",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 학과별 공부방법 챗봇")
st.caption("원하는 학과를 입력하면 공부 방법과 준비 전략을 알려드립니다.")

# -----------------------------
# Gemini API 설정
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()
except Exception as e:
    st.error(f"API 설정 오류: {e}")
    st.stop()

# -----------------------------
# 채팅 기록 유지
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "희망 학과를 입력해 주세요.\n"
                "예: 컴퓨터공학과, 간호학과, 심리학과, 기계공학과\n\n"
                "해당 학과 진학을 위한 공부 방법과 준비 전략을 알려드릴게요."
            )
        }
    ]

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("희망 학과를 입력하세요")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        system_prompt = """
당신은 대한민국 고등학생을 위한 진로·학과 상담 전문가입니다.

사용자가 원하는 학과를 입력하면 다음 형식으로 답변하세요.

# 학과 소개

# 고등학교에서 중요한 과목

# 효과적인 공부 방법
- 구체적으로 설명

# 추천 비교과 활동
- 동아리
- 탐구활동
- 독서

# 관련 진로 및 직업

# 추가 조언

친절하고 이해하기 쉽게 작성하세요.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"{system_prompt}\n\n희망 학과: {user_input}"
                        }
                    ]
                }
            ]
        )

        answer = response.text

    except Exception as e:
        answer = (
            "❌ 답변 생성 중 오류가 발생했습니다.\n\n"
            f"오류 내용: {str(e)}\n\n"
            "잠시 후 다시 시도해주세요."
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
