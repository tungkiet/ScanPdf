import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os
from datetime import datetime

# Cấu hình giao diện web
st.set_page_config(layout="wide", page_title="Hệ thống báo lỗi số hóa")

st.title("Ứng dụng Báo cáo lỗi số hóa")

# 1. Chọn file PDF
uploaded_file = st.sidebar.file_uploader("Chọn file PDF", type="pdf")

if uploaded_file:
    # Render PDF bằng PyMuPDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Hiển thị từng trang dạng Thumbnail
    cols = st.columns(4) # Chia lưới 4 cột
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")
        
        with cols[i % 4]:
            st.image(img_data, caption=f"Trang {i+1}")
            # Nút báo lỗi cho từng trang
            if st.button(f"Báo lỗi trang {i+1}", key=f"btn_{i}"):
                st.session_state.selected_page = f"Trang {i+1}"

# 2. Form báo lỗi
if "selected_page" in st.session_state:
    st.subheader(f"Ghi nhận lỗi tại {st.session_state.selected_page}")
    with st.form("error_form"):
        err_type = st.selectbox("Chọn loại lỗi", ["Ảnh bị nghiêng", "Thiếu trang", "Trùng trang"])
        note = st.text_area("Ghi chú chi tiết")
        submitted = st.form_submit_button("Lưu lỗi")
        
        if submitted:
            # Lưu vào Excel/CSV như cũ
            st.success(f"Đã lưu lỗi: {err_type} vào hệ thống!")
            # Logic ghi file bạn có thể copy từ view.py sang đây
