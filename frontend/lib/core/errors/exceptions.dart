/// Base exception class
class AppException implements Exception {
  final String message;
  final int? statusCode;

  AppException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

/// Server exception (5xx)
class ServerException extends AppException {
  ServerException(super.message, {super.statusCode});
}

/// Network exception (no connection)
class NetworkException extends AppException {
  NetworkException(super.message) : super(statusCode: 0);
}

/// Authentication exception (401, 403)
class AuthException extends AppException {
  AuthException(super.message, {super.statusCode});
}

/// Validation exception (400, 422)
class ValidationException extends AppException {
  final Map<String, dynamic>? errors;

  ValidationException(super.message, {super.statusCode, this.errors});
}

/// Not found exception (404)
class NotFoundException extends AppException {
  NotFoundException(super.message) : super(statusCode: 404);
}

/// Cache exception
class CacheException extends AppException {
  CacheException(super.message) : super(statusCode: 0);
}

/// Timeout exception
class TimeoutException extends AppException {
  TimeoutException(super.message) : super(statusCode: 408);
}
