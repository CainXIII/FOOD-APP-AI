import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../repositories/recipe_repository.dart';

/// Rate recipe usecase
class RateRecipe {
  final RecipeRepository repository;

  RateRecipe(this.repository);

  Future<Either<Failure, void>> call({
    required String recipeId,
    required int rating,
  }) {
    if (rating < 1 || rating > 5) {
      return Future.value(
        Left(ValidationFailure('Rating must be between 1 and 5')),
      );
    }
    return repository.rateRecipe(recipeId, rating);
  }
}
