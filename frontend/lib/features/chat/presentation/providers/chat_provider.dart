import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/chat_message.dart';
import '../../../../core/providers/providers.dart';
import '../../data/datasources/chat_remote_datasource.dart';

// Data source provider
final chatDataSourceProvider = Provider<ChatRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return ChatRemoteDataSource(dioClient);
});

// Chat state
class ChatState {
  final List<ChatMessage> messages;
  final bool isLoading;
  final String? error;
  final bool isTyping;
  final bool isOnline;

  const ChatState({
    this.messages = const [],
    this.isLoading = false,
    this.error,
    this.isTyping = false,
    this.isOnline = true,
  });

  ChatState copyWith({
    List<ChatMessage>? messages,
    bool? isLoading,
    String? error,
    bool? isTyping,
    bool? isOnline,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      isTyping: isTyping ?? this.isTyping,
      isOnline: isOnline ?? this.isOnline,
    );
  }
}

// Chat notifier
class ChatNotifier extends StateNotifier<ChatState> {
  final ChatRemoteDataSource _dataSource;
  String? _currentChatId;

  ChatNotifier(this._dataSource) : super(const ChatState());

  Future<void> sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    // Add user message with sending status
    final userMessage = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: MessageContent.text(text.trim()),
      isUser: true,
      timestamp: DateTime.now(),
      status: MessageStatus.sending,
    );

    state = state.copyWith(
      messages: [...state.messages, userMessage],
      isLoading: true,
      isTyping: true,
      error: null,
    );

    try {
      // Create chat session if not exists
      if (_currentChatId == null) {
        final chatData = await _dataSource.createChat();
        _currentChatId = chatData['id'];
      }

      // Update user message to sent status
      final sentMessage = userMessage.copyWith(status: MessageStatus.sent);
      final updatedMessages = state.messages.map((msg) {
        return msg.id == userMessage.id ? sentMessage : msg;
      }).toList();

      state = state.copyWith(messages: updatedMessages);

      // Send message to API and get AI response
      final response = await _dataSource.sendMessage(
        chatId: _currentChatId!,
        content: text.trim(),
      );

      // Add AI message from response
      final aiMessage = ChatMessage(
        id: response['id'].toString(),
        content: MessageContent.text(response['content'] as String),
        isUser: false,
        timestamp: DateTime.parse(response['created_at'] as String),
        status: MessageStatus.delivered,
      );

      state = state.copyWith(
        messages: [...state.messages, aiMessage],
        isLoading: false,
        isTyping: false,
      );
    } catch (e) {
      // Check if it's a budget exceeded error
      final errorMessage = e.toString().toLowerCase();
      final isBudgetExceeded = errorMessage.contains('budget') || 
                              errorMessage.contains('exceeded') || 
                              errorMessage.contains('quota');

      // Mark user message as failed
      final failedMessage = userMessage.copyWith(
        status: MessageStatus.failed,
        error: e.toString(),
      );
      final updatedMessages = state.messages.map((msg) {
        return msg.id == userMessage.id ? failedMessage : msg;
      }).toList();

      // Add a fallback AI message for budget exceeded errors
      final messagesToAdd = [...updatedMessages];
      if (isBudgetExceeded) {
        final fallbackMessage = ChatMessage(
          id: 'fallback_${DateTime.now().millisecondsSinceEpoch}',
          content: MessageContent.text(
            'Xin chào! Tôi là trợ lý nấu ăn AI. Hiện tại dịch vụ AI đang tạm thời không khả dụng do hạn mức sử dụng. '
            'Tôi có thể giúp bạn với một số mẹo nấu ăn cơ bản:\n\n'
            '🍳 Món ăn đơn giản:\n'
            '• Phở bò: Nấu nước dùng từ xương bò, thêm bún tươi và thịt bò tái chín\n'
            '• Cơm tấm: Nướng thịt heo và ướp gia vị đậm đà\n'
            '• Canh chua: Dùng cá và rau củ tạo vị chua thanh\n\n'
            '💡 Mẹo vặt:\n'
            '• Luôn nêm nếm thức ăn trong quá trình nấu\n'
            '• Dùng lửa nhỏ để thức ăn chín đều\n'
            '• Bảo quản thực phẩm đúng cách để giữ độ tươi ngon\n\n'
            'Vui lòng thử lại sau hoặc liên hệ hỗ trợ để được giúp đỡ thêm!'
          ),
          isUser: false,
          timestamp: DateTime.now(),
          status: MessageStatus.delivered,
        );
        messagesToAdd.add(fallbackMessage);
      }

      state = state.copyWith(
        messages: messagesToAdd,
        isLoading: false,
        isTyping: false,
        error: isBudgetExceeded 
          ? 'Dịch vụ AI tạm thời không khả dụng do hạn mức sử dụng. Đã hiển thị phản hồi dự phòng.'
          : 'Có lỗi xảy ra. Vui lòng thử lại.',
      );
    }
  }

  Future<void> retryMessage(String messageId) async {
    final message = state.messages.firstWhere((msg) => msg.id == messageId);
    if (message.status != MessageStatus.failed || !message.isUser) return;

    await sendMessage(message.text);
  }

  void clearChat() {
    _currentChatId = null;
    state = const ChatState();
  }

  void updateOnlineStatus(bool isOnline) {
    state = state.copyWith(isOnline: isOnline);
  }

  void clearError() {
    state = state.copyWith(error: null);
  }

  Future<void> loadChatHistory() async {
    if (_currentChatId == null) return;

    try {
      final chatData = await _dataSource.getChatDetails(_currentChatId!);
      final messages = (chatData['messages'] as List?)?.map((msg) {
        return ChatMessage(
          id: msg['id'].toString(),
          content: MessageContent.text(msg['content'] as String),
          isUser: msg['role'] == 'user',
          timestamp: DateTime.parse(msg['created_at'] as String),
        );
      }).toList() ?? [];

      state = state.copyWith(messages: messages);
    } catch (e) {
      // Handle error silently or show notification
    }
  }
}

// Providers
final chatNotifierProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  final dataSource = ref.watch(chatDataSourceProvider);
  return ChatNotifier(dataSource);
});

final chatMessagesProvider = Provider<List<ChatMessage>>((ref) {
  return ref.watch(chatNotifierProvider).messages;
});

final chatLoadingProvider = Provider<bool>((ref) {
  return ref.watch(chatNotifierProvider).isLoading;
});

final chatTypingProvider = Provider<bool>((ref) {
  return ref.watch(chatNotifierProvider).isTyping;
});

final chatErrorProvider = Provider<String?>((ref) {
  return ref.watch(chatNotifierProvider).error;
});

final chatOnlineProvider = Provider<bool>((ref) {
  return ref.watch(chatNotifierProvider).isOnline;
});
