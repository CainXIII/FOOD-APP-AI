import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/app_constants.dart';
import 'token_refresh_manager.dart';

/// Interceptor for handling authentication tokens
class AuthInterceptor extends Interceptor {
  final SharedPreferences prefs;
  final Dio dio;
  late final TokenRefreshManager _tokenRefreshManager;

  AuthInterceptor({
    required this.prefs,
    required this.dio,
  }) {
    _tokenRefreshManager = TokenRefreshManager(prefs: prefs, dio: dio);
  }

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Get access token from storage
    final accessToken = prefs.getString(AppConstants.accessTokenKey);

    // Add token to headers if available
    if (accessToken != null && accessToken.isNotEmpty) {
      options.headers['Authorization'] = 'Bearer $accessToken';
    }

    handler.next(options);
  }

  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    // Handle 401 Unauthorized - try to refresh token
    if (err.response?.statusCode == 401) {
      try {
        // Use TokenRefreshManager to handle refresh (prevents race conditions)
        final newAccessToken = await _tokenRefreshManager.refreshToken();

        if (newAccessToken != null) {
          // Retry the original request with new token
          final opts = Options(
            method: err.requestOptions.method,
            headers: {
              ...err.requestOptions.headers,
              'Authorization': 'Bearer $newAccessToken',
            },
          );

          final cloneReq = await dio.request(
            err.requestOptions.path,
            options: opts,
            data: err.requestOptions.data,
            queryParameters: err.requestOptions.queryParameters,
          );

          return handler.resolve(cloneReq);
        }
      } catch (e) {
        // Refresh failed, proceed with error
        // TokenRefreshManager already cleared tokens
      }
    }

    handler.next(err);
  }
}
