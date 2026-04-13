import streamlit as st
from rag_chain import load_rag_chain

# -----------------------------------------------
# 페이지 설정
# -----------------------------------------------
st.set_page_config(
    page_title="삼성 메모리카드 매뉴얼 챗봇",
    page_icon="📖",
    layout="centered"
)

st.title("삼성 메모리카드 매뉴얼 챗봇")
st.caption("매뉴얼 기반으로 정확한 답변을 제공합니다.")

# -----------------------------------------------
# RAG 체인 초기화 (최초 1회만 실행)
# -----------------------------------------------
@st.cache_resource
def init_rag_chain():
    return load_rag_chain("data/Samsung_Card_Manual_Korean_1.3.pdf")

rag_chain = init_rag_chain()

# -----------------------------------------------
# 대화 히스토리 초기화
# -----------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------
# 이전 대화 출력
# -----------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------------------------
# 사용자 입력 처리
# -----------------------------------------------
if user_input := st.chat_input("매뉴얼에 대해 궁금한 점을 물어보세요."):

    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # RAG 답변 생성 및 출력
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            answer = rag_chain.invoke(user_input)
        st.markdown(answer)

    # 어시스턴트 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": answer})
