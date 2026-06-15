import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="학과 추천 챗봇",
    page_icon="🎓"
)

st.title("🎓 학과 추천 챗봇")
st.write("좋아하는 과목을 입력하면 추천 학과와 공부 방법을 알려드립니다.")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error("API 키를 불러올 수 없습니다. Secrets 설정을 확인하세요.")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 좋아하는 과목을 알려주면 추천 학과와 공부 방법을 알려드릴게요."
        }
    ]

# 기존 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("예: 수학과 과학을 좋아해요"):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        system_prompt = """
        당신은 대한민국 고등학생을 위한 진로·학과 상담 전문가입니다.

        사용자가 좋아하는 과목이나 관심사를 말하면:

        1. 적합한 학과 3~5개 추천
        2. 추천 이유 설명
        3. 해당 학과 진학을 위한 공부 방법
        4. 고등학교 때 준비하면 좋은 활동
        5. 관련 직업

        형식을 보기 좋게 마크다운으로 작성하세요.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"{system_prompt}\n\n사용자: {prompt}"
        )

        answer = response.text

    except Exception as e:
        answer = f"""
❌ 오류가 발생했습니다.

오류 내용:
`{str(e)}`

잠시 후 다시 시도해주세요.
"""

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
