import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 🔐 보안 설정 (blog.py와 똑같아야 함)
# ==========================================
SECRET_SALT = "My_Success_Key_2025!@#" 
# ==========================================

st.set_page_config(page_title="라이선스 발급 센터", page_icon="🎫")

st.title("🎫 1회용 라이선스 키 발급")
st.markdown("구매하신 **쿠폰 번호**와 프로그램의 **제품 ID**를 입력하세요.")

# 구글 시트 연결 설정
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("license_form"):
    coupon_code = st.text_input("1. 쿠폰 번호", placeholder="예: COUPON-001")
    product_id = st.text_input("2. 제품 ID", placeholder="예: A1B2-C3D4")
    
    submit = st.form_submit_button("키 발급받기")

if submit:
    if not coupon_code or not product_id:
        st.warning("⚠️ 쿠폰 번호와 제품 ID를 모두 입력해주세요.")
    else:
        try:
            # 1. 엑셀 데이터 읽어오기 (캐시 없이 즉시 읽기)
            df = conn.read(worksheet="Sheet1", ttl=0)
            
            # 2. 입력값 정리
            clean_coupon = coupon_code.strip()
            clean_pid = product_id.strip().upper()
            
            # 3. 쿠폰 찾기
            mask = df['Code'] == clean_coupon
            
            if not df[mask].empty:
                idx = df[mask].index[0]
                status = df.at[idx, 'Status']
                saved_pid = df.at[idx, 'ProductID']
                
                # A. 아직 안 쓴 쿠폰인 경우 (Status가 비어있음)
                if pd.isna(status) or status == "":
                    # 키 생성
                    text = f"{clean_pid}{SECRET_SALT}"
                    license_key = hashlib.md5(text.encode()).hexdigest()
                    
                    # 엑셀 업데이트 (사용됨 표시)
                    df.at[idx, 'Status'] = "USED"
                    df.at[idx, 'ProductID'] = clean_pid
                    df.at[idx, 'Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 구글 시트에 저장
                    conn.update(worksheet="Sheet1", data=df)
                    
                    st.success("✅ 정품 인증키가 발급되었습니다!")
                    st.code(license_key, language="text")
                    st.info("👆 위 키를 복사해서 프로그램에 입력하세요.")
                    st.balloons()

                # B. 이미 사용된 쿠폰인 경우
                else:
                    # 본인이 다시 조회한 경우 (AS 차원)
                    if str(saved_pid).strip().upper() == clean_pid:
                        text = f"{clean_pid}{SECRET_SALT}"
                        license_key = hashlib.md5(text.encode()).hexdigest()
                        st.info("🔄 이미 등록하신 쿠폰입니다. 키를 다시 보여드립니다.")
                        st.code(license_key, language="text")
                    else:
                        st.error("❌ 이미 사용된 쿠폰입니다.")
            else:
                st.error("❌ 존재하지 않는 쿠폰 번호입니다.")
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")