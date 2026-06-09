import streamlit as st
from google import genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="대학교 학과 추천 챗봇",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 대학교 학과 추천 챗봇")
st.caption("좋아하는 과목이나 관심사를 알려주면 적합한 대학 학과를 추천해드립니다.")

# -----------------------------
# Gemini 설정
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("Secrets에 GEMINI_API_KEY가 설정되어 있지 않습니다.")
    st.stop()
except Exception as e:
    st.error(f"API 초기화 중 오류가 발생했습니다.\n\n{e}")
    st.stop()

# -----------------------------
# 채팅 기록 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "좋아하는 과목이나 관심사를 알려주세요.\n\n"
                "예시:\n"
                "- 수학과 물리\n"
                "- 생명과학과 화학\n"
                "- 컴퓨터와 프로그래밍\n"
                "- 역사와 사회 문제\n"
                "- 디자인과 그림 그리기"
            )
        }
    ]

# -----------------------------
# 이전 채팅 표시
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("좋아하는 과목 또는 관심사를 입력하세요")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("학과를 추천하는 중입니다..."):

            try:
                system_prompt = """
                당신은 대한민국의 진로·진학 전문 상담사입니다.

                사용자가 좋아하는 과목이나 관심사를 말하면:

                1. 추천 학과 3~5개 제시
                2. 각 학과 추천 이유 설명
                3. 해당 학과에서 배우는 내용 설명
                4. 관련 진로 및 직업 예시 제시
                5. 고등학생도 이해하기 쉽게 설명

                답변 형식:

                ## 추천 학과

                ### 1. 학과명
                - 추천 이유:
                - 배우는 내용:
                - 관련 직업:

                마지막에는 한 줄 조언을 제공하세요.
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": f"{system_prompt}\n\n사용자 입력: {user_input}"
                                }
                            ]
                        }
                    ]
                )

                answer = response.text

            except Exception as e:
                answer = (
                    "❌ 답변을 생성하는 중 오류가 발생했습니다.\n\n"
                    f"오류 내용:\n`{str(e)}`\n\n"
                    "잠시 후 다시 시도해주세요."
                )

            st.markdown(answer)

    # 답변 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:

    st.header("⚙️ 메뉴")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "안녕하세요! 😊\n\n"
                    "좋아하는 과목이나 관심사를 알려주시면 "
                    "적합한 대학 학과를 추천해드릴게요."
                )
            }
        ]
        st.rerun()

    st.markdown("---")

    st.subheader("입력 예시")

    st.write("""
    - 수학, 물리
    - 생명과학
    - 컴퓨터 프로그래밍
    - 경제와 투자
    - 그림 그리기
    - 영상 제작
    - 심리학
    - 역사와 사회
    """)
