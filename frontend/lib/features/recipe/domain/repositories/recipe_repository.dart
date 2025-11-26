import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/recipe.dart';

/// Recipe repository interface
abstract class RecipeRepository {
  /// Get recipe detail by ID
  Future<Either<Failure, Recipe>> getRecipeDetail(String id);
  
  /// Toggle favorite status
  Future<Either<Failure, bool>> toggleFavorite(String id);
  
  /// Rate recipe
  Future<Either<Failure, void>> rateRecipe(String id, int rating);
  
  /// Get user's rating for recipe
  Future<Either<Failure, int?>> getUserRating(String id);
}
