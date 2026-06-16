import streamlit as st

try:
    from google import genai
except ImportError:
    st.error("google-genai 라이브러리가 설치되지 않았습니다.")
    st.stop()


# 페이지 설정
st.set_page_config(
    page_title="진로 고민 상담소",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 진로 고민 상담소")
st.write("진로와 학과 선택에 대한 고민을 AI와 함께 이야기해보세요.")

# API Key 확인
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# 입력
major = st.text_input(
    "희망 학과 (선택)",
    placeholder="예: 컴퓨터공학과"
)

concern = st.text_area(
    "진로 고민 (선택)",
    placeholder="예: 성적이 부족한데 컴퓨터공학과에 진학할 수 있을까요?"
)

if st.button("상담 받기", type="primary"):

    if not major.strip() and not concern.strip():
        st.warning("희망 학과 또는 고민 내용을 입력해주세요.")
        st.stop()

    prompt = f"""
당신은 친절한 진로 상담 전문가입니다.

희망 학과:
{major if major else "입력 없음"}

진로 고민:
{concern if concern else "입력 없음"}

다음 형식으로 한국어로 답변하세요.

1. 고민 분석
2. 학과 관련 조언
3. 지금부터 준비할 것
4. 추천 활동
5. 응원 메시지

학생이 이해하기 쉽고 구체적으로 작성하세요.
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        st.success("상담 결과")

        if response.text:
            st.markdown(response.text)
        else:
            st.warning("답변을 생성하지 못했습니다.")

    except Exception as e:
        st.error("AI 상담 중 오류가 발생했습니다.")
        st.error(str(e))

st.divider()

with st.expander("💡 활용 예시"):
    st.write("""
    희망 학과: 컴퓨터공학과

    고민:
    수학 성적이 부족한데 컴퓨터공학과를 가고 싶어요.
    지금부터 무엇을 준비하면 좋을까요?
    """)
