
import os
import base64
import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 생성
client =

# 페이지 설정
st.set_page_config(  page_title="텍스트 음성 변환기", page_icon="🤖"   )
st.title(  '텍스트를 음성으로 변환 하겠습니'   )

# 텍스트 입력
text = st.text_area(
    "읽을 텍스트를 입력하세요",
    "안녕하세요. OpenAI 텍스트 음성 변환 실습입니다."
)

# 버튼
if st.button(   '변환하기'   ):
    if text.strip() == "":
        st.warning(   '변환할 텍스트를 입력 하세요'   )
    else:
        
         sys_role = """
            당신은 텍스트를 발랄하고 즐겁게 읽어 주는 초등학생 입니다.
            입력된 문장의 뜻을 유지하되, 초등학생처럼 발랄하고 귀여운 말투로 자연스럽게 바꾸어 말하세요.
            """

            # 프롬프트 구성
            prompt = """
            다음 문장을 음성으로 변환 하세요.
           
            """
        
        # TTS 생성
        speech = client.chat.completions.create(
            model= "tts-1",
            voice= 'nova',
            input=[{"role": "system", "content": sys_role},
                    {"role": "user", "content": prompt}]
        )
        audio_bytes =

        # 음성 출력
        st.markdown("### 🔊 음성 재생")
        st.audio(speech.content, format="audio/mp3")
