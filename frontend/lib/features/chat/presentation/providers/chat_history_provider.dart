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
      // Call backend API to get chat sessions
      final chatsData = await _dataSource.getChats();
      
      final sessions = chatsData.map((chatJson) {
        return ChatSession.fromJson(chatJson as Map<String, dynamic>);
      }).toList();

      state = state.copyWith(
        sessions: sessions,
        filteredSessions: sessions,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Không thể tải lịch sử trò chuyện: $e',
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
    try {
      final chatData = await _dataSource.createChat();
      
      // Add new chat to the list
      final newSession = ChatSession.fromJson(chatData);
      final updatedSessions = [newSession, ...state.sessions];
      
      state = state.copyWith(
        sessions: updatedSessions,
        filteredSessions: state.searchQuery.isEmpty 
            ? updatedSessions 
            : state.filteredSessions,
      );
      
      return;
    } catch (e) {
      state = state.copyWith(error: 'Không thể tạo cuộc trò chuyện mới: $e');
    }
  }

  Future<void> openChat(String chatId) async {
    try {
      // Load chat details if needed
      await _dataSource.getChatDetails(chatId);
      // Navigation will be handled by the UI
    } catch (e) {
      state = state.copyWith(error: 'Không thể mở cuộc trò chuyện: $e');
    }
  }

  Future<void> renameChat(String chatId, String newTitle) async {
    try {
      // Call API to rename chat
      await _dataSource.updateChat(chatId: chatId, title: newTitle);

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
      state = state.copyWith(error: 'Không thể đổi tên cuộc trò chuyện: $e');
    }
  }

  Future<void> deleteChat(String chatId) async {
    try {
      // Call API to delete chat
      await _dataSource.deleteChat(chatId);

      final updatedSessions = state.sessions.where((session) => session.id != chatId).toList();
      final updatedFiltered = state.filteredSessions.where((session) => session.id != chatId).toList();

      state = state.copyWith(
        sessions: updatedSessions,
        filteredSessions: updatedFiltered,
      );
    } catch (e) {
      state = state.copyWith(error: 'Không thể xóa cuộc trò chuyện: $e');
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