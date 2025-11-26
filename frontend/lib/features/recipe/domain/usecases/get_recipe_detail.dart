import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/recipe.dart';
import '../repositories/recipe_repository.dart';

/// Get recipe detail usecase
class GetRecipeDetail {
  final RecipeRepository repository;

  GetRecipeDetail(this.repository);

  Future<Either<Failure, Recipe>> call(String id) {
    return repository.getRecipeDetail(id);
  }
}
