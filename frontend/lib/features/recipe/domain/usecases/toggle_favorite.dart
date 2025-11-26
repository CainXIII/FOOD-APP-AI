import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../repositories/recipe_repository.dart';

/// Toggle favorite usecase
class ToggleFavorite {
  final RecipeRepository repository;

  ToggleFavorite(this.repository);

  Future<Either<Failure, bool>> call(String recipeId) {
    return repository.toggleFavorite(recipeId);
  }
}
