# 🍳 Food App - Chat Test Interface

Web interface tạm thời để test tính năng chat sử dụng Streamlit.

## 🚀 Cài đặt

```bash
# Di chuyển vào thư mục
cd web-app-test

# Cài đặt dependencies
pip install -r requirements.txt
```

## ▶️ Chạy ứng dụng

### 1. Chạy Backend API
```bash
# Ở thư mục gốc (food-app-backend)
python run.py
```

Backend sẽ chạy tại: `http://localhost:8000`

### 2. Chạy Web Test Interface
```bash
# Ở thư mục web-app-test
streamlit run app.py
```

Web interface sẽ mở tại: `http://localhost:8501`

## ✨ Tính năng

### Chat Interface
- ✅ Giao diện chat thân thiện với streamlit
- ✅ Hiển thị lịch sử chat real-time
- ✅ Timestamp cho mỗi tin nhắn
- ✅ Loading spinner khi đang xử lý

### Chat Modes
1. **Full Chat** (with RAG + Tools)
   - Sử dụng RAG để tìm kiếm context
   - Có thể gọi tools (generate_menu, search_recipes, etc.)
   - Lưu lịch sử chat vào database

2. **Simple Chat** (without RAG)
   - Chỉ chat đơn giản với GPT
   - Không sử dụng RAG hoặc tools
   - Phản hồi nhanh hơn

### Quản lý lịch sử
- 📥 **Tải lịch sử**: Tải chat history từ database
- 🗑️ **Xóa lịch sử**: Xóa toàn bộ lịch sử chat
- 👤 **User ID**: Tùy chỉnh user ID để test

### Thông tin debug
- ℹ️ Context được sử dụng từ RAG
- ℹ️ Tools được gọi trong quá trình xử lý
- ℹ️ Intent được detect từ message
- 🔌 Trạng thái kết nối API

## 🎯 Cách sử dụng

### Test Chat cơ bản
1. Nhập tin nhắn vào ô chat
2. Nhấn Enter hoặc click Send
3. Xem phản hồi từ assistant

### Test với RAG
1. Bỏ check "Dùng Simple Chat"
2. Hỏi câu hỏi về món ăn: "Cách làm phở bò?"
3. Xem context được sử dụng trong expander

### Test với Tools
1. Yêu cầu tạo menu: "Tạo thực đơn cho mùa đông"
2. Xem tools được gọi trong expander
3. Kiểm tra kết quả trả về

### Test lịch sử
1. Chat một vài tin nhắn
2. Click "Tải lịch sử" để load từ database
3. Click "Xóa lịch sử" để reset

## 📝 API Endpoints được test

- `POST /api/chat` - Full chat with RAG + tools
- `POST /api/chat/simple` - Simple chat without RAG
- `GET /api/chat/history` - Load chat history
- `DELETE /api/chat/history` - Clear chat history
- `GET /` - API health check

## 🎨 Giao diện

### Main Chat Area
- Chat messages với styling riêng cho user/assistant
- Input box ở dưới cùng
- Auto-scroll khi có tin nhắn mới

### Sidebar
- **Cấu hình**: User ID, chat mode
- **Lịch sử**: Tải/xóa lịch sử
- **API Status**: Kiểm tra backend đang chạy

### Footer
- Hiển thị user ID hiện tại
- Số lượng messages trong session
- Session ID (nếu có)

## 🐛 Troubleshooting

### "Không kết nối được API"
- Kiểm tra backend đang chạy: `python run.py`
- Kiểm tra port 8000 có bị chiếm không
- Kiểm tra firewall settings

### "Request timeout"
- API mất quá nhiều thời gian (>30s)
- Kiểm tra database connection
- Kiểm tra Qdrant service đang chạy

### "Lỗi API: 500"
- Kiểm tra logs của backend
- Xem chi tiết lỗi trong error message
- Kiểm tra config trong `.env`

## 🔧 Customization

### Thay đổi API URL
```python
# Trong app.py
API_BASE_URL = "http://your-server:8000"
```

### Thay đổi timeout
```python
# Trong app.py, dòng requests.post
timeout=30  # Đổi thành giá trị khác (seconds)
```

### Thay đổi giao diện
- Chỉnh CSS trong phần `st.markdown()` 
- Thay đổi layout trong `st.set_page_config()`
- Custom colors và styling

## 📦 Dependencies

- **streamlit**: Web framework cho Python
- **requests**: HTTP client để gọi API

## 🎯 Next Steps

Sau khi test xong, có thể:
- [ ] Thêm test cho voice endpoints
- [ ] Thêm test cho menu generation
- [ ] Thêm upload file để test image analysis
- [ ] Thêm visualization cho RAG results
- [ ] Export chat history ra file

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Backend logs: Terminal chạy `python run.py`
2. Streamlit logs: Terminal chạy `streamlit run app.py`
3. Browser console: F12 → Console tab
4. API documentation: http://localhost:8000/docs
