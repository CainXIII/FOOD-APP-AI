import 'package:equatable/equatable.dart';

/// Base Failure class for error handling
abstract class Failure extends Equatable {
  final String message;
  final int? statusCode;

  const Failure(this.message, {this.statusCode});

  @override
  List<Object?> get props => [message, statusCode];
}

/// Server-related failures (5xx)
class ServerFailure extends Failure {
  const ServerFailure(super.message, {super.statusCode});
}

/// Network connection failures
class NetworkFailure extends Failure {
  const NetworkFailure(super.message) : super(statusCode: 0);
}

/// Authentication failures (401, 403)
class AuthFailure extends Failure {
  const AuthFailure(super.message, {super.statusCode});
}

/// Validation failures (400, 422)
class ValidationFailure extends Failure {
  final Map<String, dynamic>? errors;

  const ValidationFailure(super.message, {super.statusCode, this.errors});

  @override
  List<Object?> get props => [message, statusCode, errors];
}

/// Not found failures (404)
class NotFoundFailure extends Failure {
  const NotFoundFailure(super.message) : super(statusCode: 404);
}

/// Cache failures
class CacheFailure extends Failure {
  const CacheFailure(super.message) : super(statusCode: 0);
}

/// Unexpected/Unknown failures
class UnexpectedFailure extends Failure {
  const UnexpectedFailure(super.message, {super.statusCode});
}
