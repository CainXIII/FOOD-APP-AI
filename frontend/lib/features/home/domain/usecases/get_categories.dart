import 'package:dartz/dartz.dart';
import '../entities/category.dart';
import '../repositories/home_repository.dart';
import '../../../../core/errors/failures.dart';

class GetCategories {
  final HomeRepository repository;

  GetCategories(this.repository);

  Future<Either<Failure, List<Category>>> call() {
    return repository.getCategories();
  }
}
