import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

/// Register usecase
class RegisterUseCase {
  final AuthRepository repository;

  RegisterUseCase(this.repository);

  Future<Either<Failure, User>> call({
    required String email,
    required String password,
    required String username,
    String? fullName,
  }) async {
    return await repository.register(
      email: email,
      password: password,
      username: username,
      fullName: fullName,
    );
  }
}
