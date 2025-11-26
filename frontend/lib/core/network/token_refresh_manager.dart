import 'dart:async';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/app_constants.dart';
import '../constants/api_endpoints.dart';

/// Manages token refresh with queue to prevent multiple simultaneous refresh calls
class TokenRefreshManager {
  final SharedPreferences prefs;
  final Dio dio;
  
  Completer<String>? _refreshCompleter;
  bool _isRefreshing = false;

  TokenRefreshManager({
    required this.prefs,
    required this.dio,
  });

  /// Refresh access token with queue management
  /// Multiple calls will wait for the same refresh operation
  Future<String?> refreshToken() async {
    // If already refreshing, wait for the existing operation
    if (_isRefreshing && _refreshCompleter != null) {
      return _refreshCompleter!.future;
    }

    // Start new refresh operation
    _isRefreshing = true;
    _refreshCompleter = Completer<String>();

    try {
      final refreshToken = prefs.getString(AppConstants.refreshTokenKey);

      if (refreshToken == null || refreshToken.isEmpty) {
        throw Exception('No refresh token available');
      }

      // Create a new Dio instance without interceptors to avoid circular calls
      final refreshDio = Dio(
        BaseOptions(
          baseUrl: ApiEndpoints.baseUrl,
          connectTimeout: AppConstants.connectionTimeout,
          receiveTimeout: AppConstants.receiveTimeout,
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        ),
      );

      final response = await refreshDio.post(
        ApiEndpoints.refreshToken,
        data: {'refresh_token': refreshToken},
        options: Options(
          headers: {
            'Authorization': 'Bearer $refreshToken',
          },
        ),
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final newAccessToken = data['access_token'] as String?;
        final newRefreshToken = data['refresh_token'] as String?;

        if (newAccessToken != null) {
          // Save new tokens
          await prefs.setString(
            AppConstants.accessTokenKey,
            newAccessToken,
          );
          
          if (newRefreshToken != null) {
            await prefs.setString(
              AppConstants.refreshTokenKey,
              newRefreshToken,
            );
          }

          // Complete all waiting requests with new token
          _refreshCompleter?.complete(newAccessToken);
          return newAccessToken;
        }
      }

      throw Exception('Token refresh failed');
    } catch (e) {
      // Clear tokens on refresh failure
      await _clearTokens();
      
      // Complete with error
      _refreshCompleter?.completeError(e);
      rethrow;
    } finally {
      _isRefreshing = false;
      _refreshCompleter = null;
    }
  }

  /// Clear all authentication tokens
  Future<void> _clearTokens() async {
    await prefs.remove(AppConstants.accessTokenKey);
    await prefs.remove(AppConstants.refreshTokenKey);
    await prefs.remove(AppConstants.userDataKey);
  }

  /// Check if currently refreshing
  bool get isRefreshing => _isRefreshing;
}
