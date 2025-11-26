import 'package:dio/dio.dart';
import '../errors/exceptions.dart';

/// Centralized error handler for network requests
class ErrorHandler {
  static AppException handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return TimeoutException(
          'Request timeout. Please check your connection and try again.',
        );

      case DioExceptionType.badResponse:
        return _handleResponseError(error);

      case DioExceptionType.cancel:
        return AppException('Request cancelled');

      case DioExceptionType.connectionError:
        return NetworkException(
          'No internet connection. Please check your network settings.',
        );

      case DioExceptionType.badCertificate:
        return AppException('Certificate verification failed');

      case DioExceptionType.unknown:
      default:
        if (error.message?.contains('SocketException') ?? false) {
          return NetworkException('No internet connection');
        }
        return AppException(
          error.message ?? 'An unexpected error occurred',
        );
    }
  }

  static AppException _handleResponseError(DioException error) {
    final statusCode = error.response?.statusCode;
    final data = error.response?.data;

    String message = 'An error occurred';
    Map<String, dynamic>? errors;

    // Try to extract message from response
    if (data is Map<String, dynamic>) {
      // Check for FastAPI validation errors (422)
      if (data['detail'] is List) {
        final details = data['detail'] as List;
        if (details.isNotEmpty) {
          final firstError = details[0];
          if (firstError is Map<String, dynamic>) {
            // Extract readable message from FastAPI validation error
            final loc = firstError['loc'] as List?;
            final msg = firstError['msg']?.toString();
            final fieldObj = loc != null && loc.length > 1 ? loc.last : null;
            final field = fieldObj?.toString();
            
            if (msg != null && msg.isNotEmpty) {
              // Clean up field name (remove 'body' prefix if exists)
              final cleanField = field != null && field != 'body' ? field : null;
              message = cleanField != null ? '$cleanField: $msg' : msg;
            } else {
              message = 'Validation error';
            }
          }
        }
      } else {
        message = data['message'] as String? ??
            data['error'] as String? ??
            data['detail'] as String? ??
            message;
      }
      errors = data['errors'] as Map<String, dynamic>?;
    } else if (data is String) {
      message = data;
    }

    switch (statusCode) {
      case 400:
        return ValidationException(
          message,
          statusCode: statusCode,
          errors: errors,
        );

      case 401:
        return AuthException(
          message.isEmpty ? 'Unauthorized. Please login again.' : message,
          statusCode: statusCode,
        );

      case 403:
        return AuthException(
          message.isEmpty ? 'Access forbidden' : message,
          statusCode: statusCode,
        );

      case 404:
        return NotFoundException(
          message.isEmpty ? 'Resource not found' : message,
        );

      case 422:
        return ValidationException(
          message,
          statusCode: statusCode,
          errors: errors,
        );

      case 500:
      case 502:
      case 503:
      case 504:
        return ServerException(
          message.isEmpty ? 'Server error. Please try again later.' : message,
          statusCode: statusCode,
        );

      default:
        return AppException(message, statusCode: statusCode);
    }
  }

  /// Convert exception to user-friendly message
  static String getErrorMessage(dynamic error) {
    if (error is AppException) {
      return error.message;
    } else if (error is DioException) {
      return handleDioError(error).message;
    } else {
      return 'An unexpected error occurred';
    }
  }
}
