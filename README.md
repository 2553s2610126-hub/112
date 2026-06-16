import streamlit as st
from google import genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="학과 추천 챗봇",
    page_icon="🎓",
)

st.title("🎓 학과 추천 챗봇")
st.write("좋아하는 과목과 관심사를 입력하면 어울리는 학과를 추천해드립니다.")

# -----------------------------
# API Key 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error(
        "GEMINI_API_KEY를 찾을 수 없습니다. Streamlit Secrets를 확인해주세요."
    )
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
                "좋아하는 과목, 관심 분야, 진로 희망 등을 알려주시면 "
                "어울리는 학과를 추천해드릴게요.\n\n"
                "예시:\n"
                "- 수학과 물리를 좋아해요\n"
                "- 생명과학과 화학에 관심이 있어요\n"
                "- 역사와 글쓰기를 좋아해요"
            ),
        }
    ]

# -----------------------------
# 기존 채팅 표시
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
if prompt := st.chat_input("좋아하는 과목을 입력하세요"):

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("추천 생성 중..."):

            try:
                # 시스템 프롬프트
                system_prompt = """
너는 진로 및 학과 상담 전문가이다.

사용자가 좋아하는 과목, 흥미, 관심사를 분석하여:

1. 적합한 학과 3~5개 추천
2. 추천 이유 설명
3. 해당 학과에서 배우는 내용
4. 관련 직업 예시
5. 고등학생이 준비하면 좋은 과목

을 보기 좋게 정리해서 답변한다.

답변은 친절하고 구체적으로 작성한다.
"""

                # 대화 기록 구성
                history_text = ""

                for m in st.session_state.messages:
                    role = "사용자" if m["role"] == "user" else "AI"
                    history_text += f"{role}: {m['content']}\n"

                full_prompt = (
                    system_prompt
                    + "\n\n"
                    + history_text
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                )

                answer = response.text

            except Exception as e:
                answer = (
                    f"오류가 발생했습니다.\n\n"
                    f"오류 내용: {str(e)}\n\n"
                    f"잠시 후 다시 시도해주세요."
                )

            st.markdown(answer)

    # 답변 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
