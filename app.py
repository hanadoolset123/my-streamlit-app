
import os
import streamlit as st
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# JSON 구조
class MovieRec(BaseModel):
    title: str = Field(description="추천 영화 제목")
    year: int | None = Field(default=None, description="개봉 연도")
    reason: str = Field(description="추천 이유(2~3문장)")
    tags: list[str] = Field(description="키워드 3개")

# 체인 생성 캐싱 (앱 시작 시 딱 한 번만 실행됨)
@st.cache_resource
def create_movie_chain():
    s_msg = "당신은 영화 전문가입니다. 사용자가 원하는 장르의 최신 영화를 추천합니다."
    h_msg = "{genre} 장르의 최신 영화 1편을 추천하세요. JSON 스키마에 맞춰 답하세요."
    messages = [("system", s_msg), ("human", h_msg)]
    prompt = ChatPromptTemplate.from_messages(messages)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    return prompt | llm.with_structured_output(MovieRec)

# Streamlit UI
st.set_page_config(page_title="🎬 AI Movie Rec", page_icon="🍿")
st.title("🎬 영화 추천")

genre = st.selectbox("장르 선택", ["공상과학", "액션", "드라마", "코미디", "스릴러", "공포", "로맨스"])

if st.button("추천 받기", type="primary"):
    with st.spinner(f"📡 {genre} 영화 정보를 가져오는 중..."):
        chain = create_movie_chain()
        response = chain.invoke({"genre": genre})

    st.subheader(f"🎥 추천: {response.title} ({response.year})")
    st.info(response.reason)
    st.write(f"🏷️ {' '.join([f'#{t}' for t in response.tags])}")

    with st.expander("DEBUG: 원본 데이터"):
        st.json(response.model_dump())
