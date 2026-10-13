import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# #1. Tạo frame (DataFrame) với đúng dữ liệu của bạn
data = {
    'Họ tên': [
        'Phạm Văn An', 'Nguyễn Văn Bình', 'Trần Yến Chi', 'Đặng Đăng Dũng', 
        'Nguyễn Hà', 'Phan Ngọc Lan', 'Huỳnh Văn Minh', 'Trương Bảo Nam', 
        'Trần Bảo Phúc', 'Đinh Trang Thảo'
    ],
    'Chuyên cần': [8.0, 9.0, 7.5, 6.0, 10.0, 8.5, 9.0, 7.0, 8.0, 9.5],
    'Giữa kỳ': [7.0, 8.5, 6.5, 5.5, 9.0, 6.0, 8.5, 6.5, 7.5, 9.0],
    'Cuối kỳ': [8.0, 8.0, 7.0, 5.0, 9.5, 5.5, 8.0, 7.0, 7.0, 9.5]
}
df = pd.DataFrame(data)

# Hiển thị bảng dữ liệu gốc
st.subheader("--- BẢNG DỮ LIỆU GỐC ---")
st.dataframe(df, use_container_width=True)

# #2. Tính điểm tổng kết và xếp loại theo code của bạn
df['Tong_ket'] = (
    0.2 * df['Chuyên cần'] + 0.3 * df['Giữa kỳ'] + 0.5 * df['Cuối kỳ']
)
df['Tong_ket'] = df['Tong_ket'].round(2) # Làm tròn 2 chữ số thập phân

# Hàm xếp loại sinh viên
def xep_loai_sv(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai_sv)

# Hiển thị bảng sau khi tính điểm tổng kết và xếp loại
st.subheader("--- BẢNG SAU KHI TÍNH TỔNG KẾT VÀ XẾP LOẠI ---")
st.dataframe(df, use_container_width=True)

# #3. Thống kê theo code của bạn
st.subheader("--- KẾT QUẢ THỐNG KÊ ---")
diem_tb_lop = df['Tong_ket'].mean()
max_diem = df['Tong_ket'].max()
min_diem = df['Tong_ket'].min()

sv_max = df[df['Tong_ket'] == max_diem]['Họ tên'].tolist()
sv_min = df[df['Tong_ket'] == min_diem]['Họ tên'].tolist()
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

# Hiển thị các chỉ số thống kê lên giao diện Streamlit
st.write(f"-> Điểm tổng kết trung bình của lớp: **{diem_tb_lop:.2f}**")
st.write(f"-> Sinh viên có điểm cao nhất ({max_diem}): **{', '.join(sv_max)}**")
st.write(f"-> Sinh viên có điểm thấp nhất ({min_diem}): **{', '.join(sv_min)}**")
st.write(f"-> Số sinh viên đạt (điểm tổng kết >= 5.0): **{so_sv_dat} / {len(df)} sinh viên**")

st.markdown("---")

# #4. Danh sách xổ xuống (Selectbox) tra cứu sinh viên
st.subheader("🔍 Tra cứu chi tiết sinh viên")
selected_sv = st.selectbox("Chọn tên sinh viên:", df['Họ tên'])
sv_info = df[df['Họ tên'] == selected_sv].iloc[0]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Chuyên cần", sv_info['Chuyên cần'])
c2.metric("Giữa kỳ", sv_info['Giữa kỳ'])
c3.metric("Cuối kỳ", sv_info['Cuối kỳ'])
c4.metric("Tổng kết", sv_info['Tong_ket'])
c5.metric("Xếp loại", sv_info['Xep_loai'])

st.markdown("---")

# #5. Trực quan hóa bằng biểu đồ cột ngang giống hệt bài của bạn
st.subheader("📈 Biểu đồ thể hiện điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df['Họ tên'], df['Tong_ket'], color='skyblue')

ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Họ tên sinh viên')
ax.set_title('Biểu đồ thể hiện điểm tổng kết của 10 sinh viên')
ax.set_xlim(0, 10)
ax.invert_yaxis()  # Đảo ngược trục Y để tên sinh viên đầu tiên hiển thị ở trên cùng

st.pyplot(fig)

# Hiển thị họ tên và MSSV ở cuối trang với kích thước chữ nhỏ
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Ứng dụng được tạo bởi: <b>Phạm Gia Thy</b> - MSSV: <b>54</b></p>", unsafe_allow_html=True)
