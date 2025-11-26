import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/chat_session.dart';
import '../../../../core/providers/providers.dart';
import '../../data/datasources/chat_remote_datasource.dart';

class ChatHistoryState {
  final List<ChatSession> sessions;
  final List<ChatSession> filteredSessions;
  final bool isLoading;
  final String? error;
  final String searchQuery;

  const ChatHistoryState({
    this.sessions = const [],
    this.filteredSessions = const [],
    this.isLoading = false,
    this.error,
    this.searchQuery = '',
  });

  ChatHistoryState copyWith({
    List<ChatSession>? sessions,
    List<ChatSession>? filteredSessions,
    bool? isLoading,
    String? error,
    String? searchQuery,
  }) {
    return ChatHistoryState(
      sessions: sessions ?? this.sessions,
      filteredSessions: filteredSessions ?? this.filteredSessions,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      searchQuery: searchQuery ?? this.searchQuery,
    );
  }
}

class ChatHistoryNotifier extends StateNotifier<ChatHistoryState> {
  final ChatRemoteDataSource _dataSource;

  ChatHistoryNotifier(this._dataSource) : super(const ChatHistoryState());

  Future<void> loadChatHistory() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      // TODO: Implement API call to get chat sessions
      // For now, using mock data
      final mockSessions = [
        ChatSession(
          id: '1',
          title: 'Công thức gà nướng',
          createdAt: DateTime.now().subtract(const Duration(days: 1)),
          lastMessageAt: DateTime.now().subtract(const Duration(hours: 2)),
          messageCount: 12,
          lastMessagePreview: 'Bạn có thể cho tôi công thức gà nướng mật ong không?',
        ),
        ChatSession(
          id: '2',
          title: 'Món ăn chay',
          createdAt: DateTime.now().subtract(const Duration(days: 3)),
          lastMessageAt: DateTime.now().subtract(const Duration(days: 1)),
          messageCount: 8,
          lastMessagePreview: 'Tôi cần ý tưởng món chay cho bữa tối gia đình',
        ),
        ChatSession(
          id: '3',
          title: 'Cách nấu phở',
          createdAt: DateTime.now().subtract(const Duration(days: 5)),
          lastMessageAt: DateTime.now().subtract(const Duration(days: 3)),
          messageCount: 15,
          lastMessagePreview: 'Hướng dẫn nấu phở bò từ A đến Z',
        ),
      ];

      state = state.copyWith(
        sessions: mockSessions,
        filteredSessions: mockSessions,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Không thể tải lịch sử trò chuyện',
      );
    }
  }

  void searchChats(String query) {
    final searchQuery = query.toLowerCase().trim();
    final filtered = searchQuery.isEmpty
        ? state.sessions
        : state.sessions.where((session) {
            return session.title.toLowerCase().contains(searchQuery) ||
                   (session.lastMessagePreview?.toLowerCase().contains(searchQuery) ?? false);
          }).toList();

    state = state.copyWith(
      searchQuery: query,
      filteredSessions: filtered,
    );
  }

  Future<void> createNewChat() async {
    // TODO: Implement create new chat
    // This would typically navigate to chat screen with a new session
  }

  Future<void> openChat(String chatId) async {
    // TODO: Implement open specific chat
    // This would load the chat session and navigate to chat screen
  }

  Future<void> renameChat(String chatId, String newTitle) async {
    try {
      // TODO: Implement API call to rename chat

      final updatedSessions = state.sessions.map((session) {
        if (session.id == chatId) {
          return session.copyWith(title: newTitle);
        }
        return session;
      }).toList();

      final updatedFiltered = state.filteredSessions.map((session) {
        if (session.id == chatId) {
          return session.copyWith(title: newTitle);
        }
        return session;
      }).toList();

      state = state.copyWith(
        sessions: updatedSessions,
        filteredSessions: updatedFiltered,
      );
    } catch (e) {
      state = state.copyWith(error: 'Không thể đổi tên cuộc trò chuyện');
    }
  }

  Future<void> deleteChat(String chatId) async {
    try {
      // TODO: Implement API call to delete chat

      final updatedSessions = state.sessions.where((session) => session.id != chatId).toList();
      final updatedFiltered = state.filteredSessions.where((session) => session.id != chatId).toList();

      state = state.copyWith(
        sessions: updatedSessions,
        filteredSessions: updatedFiltered,
      );
    } catch (e) {
      state = state.copyWith(error: 'Không thể xóa cuộc trò chuyện');
    }
  }
}

// Providers
final chatHistoryDataSourceProvider = Provider<ChatRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return ChatRemoteDataSource(dioClient);
});

final chatHistoryProvider = StateNotifierProvider<ChatHistoryNotifier, ChatHistoryState>((ref) {
  final dataSource = ref.watch(chatHistoryDataSourceProvider);
  return ChatHistoryNotifier(dataSource);
});