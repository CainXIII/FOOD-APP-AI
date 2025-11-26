import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/user.dart';

/// Auth repository interface - domain layer
abstract class AuthRepository {
  /// Register new user
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String username,
    String? fullName,
  });

  /// Login with email and password
  Future<Either<Failure, User>> login({
    required String email,
    required String password,
  });

  /// Logout current user
  Future<Either<Failure, void>> logout();

  /// Get current user info
  Future<Either<Failure, User>> getCurrentUser();

  /// Refresh access token
  Future<Either<Failure, void>> refreshToken();

  /// Check if user is logged in
  Future<bool> isLoggedIn();

  /// Get stored access token
  Future<String?> getAccessToken();

  /// Get stored refresh token
  Future<String?> getRefreshToken();
}
