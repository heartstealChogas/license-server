import streamlit as st
import hashlib

# ==========================================
# 🔐 관리자 설정 (blog.py와 똑같아야 함)
# ==========================================
SECRET_SALT = "My_Success_Key_2025!@#" 
ACCESS_PASSWORD = "trend2025"  # 구매자들에게 알려줄 공통 비밀번호
# ==========================================

st.set_page_config(page_title="Trend Extractor License", page_icon="🔐")

st.title("🔐 정품 라이선스 발급")
st.markdown("판매자에게 받은 **접속 비밀번호**와 프로그램의 **제품 ID**를 입력하세요.")

with st.form("keygen"):
    user_pw = st.text_input("1. 접속 비밀번호", type="password")
    pid = st.text_input("2. 제품 ID (예: A1B2-C3D4)")
    submit = st.form_submit_button("키 발급받기")

if submit:
    if user_pw != ACCESS_PASSWORD:
        st.error("❌ 접속 비밀번호가 틀렸습니다.")
    elif not pid or len(pid) < 5:
        st.warning("⚠️ 올바른 제품 ID를 입력해주세요.")
    else:
        try:
            # 암호화 (blog.py와 동일 로직)
            text = f"{pid.strip().upper()}{SECRET_SALT}"
            key = hashlib.md5(text.encode()).hexdigest()
            
            st.success("✅ 발급 완료!")
            st.code(key, language="text")
            st.info("위 키를 복사해서 프로그램에 입력하세요.")
        except:
            st.error("오류 발생")