import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';

class ChatRemoteDataSource {
  final DioClient _dioClient;

  ChatRemoteDataSource(this._dioClient);

  /// Create a new chat session
  Future<Map<String, dynamic>> createChat({String? title}) async {
    final response = await _dioClient.dio.post(
      '/chat',
      data: {
        'title': title ?? 'New Conversation',
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return response.data as Map<String, dynamic>;
  }

  /// Get all chat sessions
  Future<List<dynamic>> getChats({
    int page = 1,
    int pageSize = 20,
  }) async {
    final response = await _dioClient.dio.get(
      '/chat',
      queryParameters: {
        'page': page,
        'page_size': pageSize,
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return (response.data as List?) ?? [];
  }

  /// Get chat details with messages
  Future<Map<String, dynamic>> getChatDetails(String chatId) async {
    final response = await _dioClient.dio.get('/chat/$chatId');

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return response.data as Map<String, dynamic>;
  }

  /// Send message to chat
  Future<Map<String, dynamic>> sendMessage({
    required String chatId,
    required String content,
  }) async {
    final response = await _dioClient.dio.post(
      '/chat/$chatId/messages',
      data: {
        'content': content,
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return response.data as Map<String, dynamic>;
  }

  /// Delete chat
  Future<void> deleteChat(String chatId) async {
    final response = await _dioClient.dio.delete('/chat/$chatId');

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }
  }
}
