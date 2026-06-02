import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="학과 추천 챗봇",
    page_icon="🎓"
)

st.title("🎓 학과 추천 챗봇")
st.write("좋아하는 과목이나 관심사를 말하면 어울리는 학과를 추천해드립니다.")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception:
    st.error("API 키를 불러올 수 없습니다. Secrets 설정을 확인하세요.")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "좋아하는 과목이나 관심사를 알려주세요.\n"
                "예시:\n"
                "- 수학이 좋아\n"
                "- 생명과학과 화학을 좋아해\n"
                "- 컴퓨터 프로그래밍에 관심 있어"
            )
        }
    ]

# 기존 채팅 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("좋아하는 과목을 입력하세요"):

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 대화 기록 구성
        conversation = ""

        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]

            if role == "user":
                conversation += f"학생: {content}\n"
            elif role == "assistant":
                conversation += f"상담사: {content}\n"

        system_prompt = f"""
당신은 대한민국 고등학생을 위한 진로 상담사입니다.

규칙:
1. 사용자가 좋아하는 과목을 분석한다.
2. 적합한 학과를 3~5개 추천한다.
3. 추천 이유를 설명한다.
4. 관련 직업도 알려준다.
5. 친절한 한국어로 답한다.

대화 내용:
{conversation}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=system_prompt
        )

        answer = response.text

    except Exception as e:
        answer = f"""
❌ 오류가 발생했습니다.

오류 내용:
{str(e)}

잠시 후 다시 시도해주세요.
"""

    # 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
