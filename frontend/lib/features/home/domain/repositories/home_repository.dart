import 'package:dartz/dartz.dart';
import '../entities/recipe_summary.dart';
import '../entities/category.dart';
import '../../../../core/errors/failures.dart';

abstract class HomeRepository {
  Future<Either<Failure, List<RecipeSummary>>> getFeaturedRecipes({int limit = 10});
  
  Future<Either<Failure, List<RecipeSummary>>> getRecentRecipes({
    int page = 1,
    int pageSize = 20,
  });
  
  Future<Either<Failure, List<RecipeSummary>>> getPopularRecipes({int limit = 10});
  
  Future<Either<Failure, List<Category>>> getCategories();
  
  Future<Either<Failure, List<RecipeSummary>>> getRecipesByCategory({
    required String categoryId,
    int page = 1,
    int pageSize = 20,
  });
}
