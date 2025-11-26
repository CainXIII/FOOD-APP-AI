# 🍳 Cooking Assistant - Flutter App

Ứng dụng di động trợ lý nấu ăn AI với giao diện đẹp mắt và trải nghiệm người dùng tuyệt vời.

## ✨ Tính năng

- 🎤 **Voice Chat** - Trò chuyện bằng giọng nói với AI
- 🔍 **Smart Search** - Tìm kiếm công thức thông minh
- 📱 **Cross-platform** - Chạy trên iOS, Android và Web
- 🌙 **Dark Mode** - Hỗ trợ chế độ tối
- 💾 **Offline Support** - Lưu công thức offline
- 🔔 **Notifications** - Nhắc nhở nấu ăn

## 🚀 Bắt đầu nhanh

### Yêu cầu hệ thống
- Flutter 3.16+
- Dart 3.2+
- Android Studio / Xcode (cho development)

### Cài đặt

```bash
# Clone repository
git clone <repository-url>
cd ai-cooking-assistant/frontend

# Cài đặt dependencies
flutter pub get

# Kiểm tra thiết bị
flutter devices
```

### Chạy ứng dụng

```bash
# Chạy trên Android emulator
flutter run

# Chạy trên iOS simulator (macOS)
flutter run --device-id <ios-simulator-id>

# Chạy trên web
flutter run -d chrome
```

## 🏗️ Kiến trúc

```
lib/
├── core/           # Core utilities và config
├── features/       # Features theo domain
│   ├── auth/       # Authentication
│   ├── chat/       # AI Chat
│   ├── home/       # Home screen
│   └── profile/    # User profile
├── shared/         # Shared components
│   ├── models/     # Data models
│   ├── providers/  # State management
│   └── widgets/    # Reusable widgets
└── utils/          # Utilities
```

## 📱 Screenshots

*Screenshots sẽ được thêm vào sau*

## 🧪 Testing

```bash
# Chạy unit tests
flutter test

# Chạy widget tests
flutter test --coverage

# Chạy integration tests
flutter test integration_test/
```

## 🚀 Build Production

```bash
# Build APK
flutter build apk --release

# Build iOS
flutter build ios --release

# Build web
flutter build web --release
```

## 📦 Dependencies chính

- **Riverpod** - State management
- **Cached Network Image** - Image caching
- **HTTP** - API client
- **Shared Preferences** - Local storage
- **Flutter TTS** - Text-to-speech
- **Speech to Text** - Voice input

## 🔧 Environment Setup

Tạo file `.env` trong thư mục root:

```env
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30000
ENABLE_VOICE_CHAT=true
```

## 🤝 Đóng góp

1. Fork project
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

MIT License - Xem file `LICENSE` để biết thêm chi tiết.
