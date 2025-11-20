"""
Food App - Chat Test Interface
Streamlit web app for testing chat functionality
"""

import streamlit as st
import requests
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{API_BASE_URL}/api/chat"
CHAT_SIMPLE_ENDPOINT = f"{API_BASE_URL}/api/chat/simple"
CHAT_HISTORY_ENDPOINT = f"{API_BASE_URL}/api/chat/history"

# Page config
st.set_page_config(
    page_title="Food App - Chat Test",
    page_icon="🍳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "test_user_001"
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Cấu hình")
    
    # User ID
    st.session_state.user_id = st.text_input(
        "User ID",
        value=st.session_state.user_id,
        help="ID người dùng để lưu lịch sử chat"
    )
    
    # API Endpoint selection
    use_simple = st.checkbox(
        "Dùng Simple Chat (không RAG)",
        value=False,
        help="Simple chat không sử dụng RAG và tools"
    )
    
    st.divider()
    
    # Chat history controls
    st.subheader("📜 Lịch sử chat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Tải lịch sử", use_container_width=True):
            try:
                response = requests.get(
                    CHAT_HISTORY_ENDPOINT,
                    params={"user_id": st.session_state.user_id, "limit": 50}
                )
                if response.status_code == 200:
                    history = response.json()
                    if history:
                        st.session_state.messages = []
                        for msg in history:
                            st.session_state.messages.append({
                                "role": "user",
                                "content": msg["user_message"],
                                "timestamp": msg["timestamp"]
                            })
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": msg["assistant_message"],
                                "timestamp": msg["timestamp"]
                            })
                        st.success(f"✅ Đã tải {len(history)} tin nhắn")
                        st.rerun()
                    else:
                        st.info("Chưa có lịch sử chat")
                else:
                    st.error(f"Lỗi: {response.status_code}")
            except Exception as e:
                st.error(f"Không thể tải lịch sử: {e}")
    
    with col2:
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            try:
                response = requests.delete(
                    CHAT_HISTORY_ENDPOINT,
                    params={"user_id": st.session_state.user_id}
                )
                if response.status_code == 200:
                    st.session_state.messages = []
                    st.success("✅ Đã xóa lịch sử")
                    st.rerun()
                else:
                    st.error(f"Lỗi: {response.status_code}")
            except Exception as e:
                st.error(f"Không thể xóa lịch sử: {e}")
    
    st.divider()
    
    # API Status
    st.subheader("🔌 Trạng thái API")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API đang chạy")
            api_info = response.json()
            st.caption(f"Version: {api_info.get('version', 'N/A')}")
        else:
            st.error("❌ API không phản hồi")
    except:
        st.error("❌ Không kết nối được API")
        st.caption("Hãy chạy: python run.py")

# Main chat interface
st.title("🍳 Food App - Chat Assistant")
st.caption("Test interface cho tính năng chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"🕐 {message['timestamp']}")

# Chat input
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                # Choose endpoint
                if use_simple:
                    response = requests.post(
                        CHAT_SIMPLE_ENDPOINT,
                        json={"message": prompt},
                        timeout=30
                    )
                else:
                    response = requests.post(
                        CHAT_ENDPOINT,
                        json={
                            "message": prompt,
                            "user_id": st.session_state.user_id,
                            "session_id": st.session_state.session_id
                        },
                        timeout=30
                    )
                
                if response.status_code == 200:
                    data = response.json()

                    # Fallback answer resolution (first non-empty key)
                    assistant_message = None
                    for _k in ("response", "answer", "message", "content"):
                        _v = data.get(_k)
                        if isinstance(_v, str) and _v.strip():
                            assistant_message = _v.strip()
                            break
                    if not assistant_message:
                        assistant_message = "⚠️ Không có nội dung phản hồi từ API."

                    # Extract metadata
                    sources = data.get("sources") or data.get("context_used")
                    tools_used = data.get("tools_used")
                    intent = data.get("intent")
                    latency_ms = data.get("latency_ms") or data.get("latency")

                    # Update session_id if available
                    if "session_id" in data and not use_simple:
                        st.session_state.session_id = data["session_id"]

                    # Display main answer
                    st.markdown(assistant_message)

                    # Metadata / diagnostics
                    if not use_simple:
                        with st.expander("ℹ️ Thông tin thêm"):
                            if intent:
                                st.write(f"**Intent:** {intent}")
                            if latency_ms is not None:
                                st.write(f"**Latency:** {latency_ms} ms")
                            if tools_used:
                                st.write("**Tools sử dụng:**")
                                st.json(tools_used)
                            if sources:
                                st.write("**Nguồn / Context:**")
                                st.json(sources)
                            debug_keys = ["pipeline_steps", "model", "tokens", "cost"]
                            extra = {k: data[k] for k in debug_keys if k in data}
                            if extra:
                                st.write("**Thông tin bổ sung:**")
                                st.json(extra)

                    # Add to messages with meta summary
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "meta": {
                            "intent": intent,
                            "latency_ms": latency_ms,
                            "tools_used_count": len(tools_used) if tools_used else 0,
                            "sources_count": (len(sources) if isinstance(sources, (list, dict)) else 0)
                        }
                    })
                    
                else:
                    error_msg = f"❌ Lỗi API: {response.status_code}"
                    try:
                        error_detail = response.json()
                        error_msg += f"\n\n```json\n{json.dumps(error_detail, indent=2, ensure_ascii=False)}\n```"
                    except:
                        error_msg += f"\n\n{response.text}"
                    
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    
            except requests.exceptions.Timeout:
                error_msg = "⏱️ Request timeout - API mất quá nhiều thời gian để phản hồi"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
            except Exception as e:
                error_msg = f"❌ Lỗi: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"👤 User: {st.session_state.user_id}")
with col2:
    st.caption(f"💬 Messages: {len(st.session_state.messages)}")
with col3:
    if st.session_state.session_id:
        st.caption(f"🔑 Session: {st.session_state.session_id[:8]}...")
    else:
        st.caption("🔑 Session: None")
