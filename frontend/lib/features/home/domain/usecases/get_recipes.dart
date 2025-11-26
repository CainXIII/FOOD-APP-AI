import 'package:dartz/dartz.dart';
import '../entities/recipe_summary.dart';
import '../repositories/home_repository.dart';
import '../../../../core/errors/failures.dart';

class GetFeaturedRecipes {
  final HomeRepository repository;

  GetFeaturedRecipes(this.repository);

  Future<Either<Failure, List<RecipeSummary>>> call({int limit = 10}) {
    return repository.getFeaturedRecipes(limit: limit);
  }
}

class GetRecentRecipes {
  final HomeRepository repository;

  GetRecentRecipes(this.repository);

  Future<Either<Failure, List<RecipeSummary>>> call({
    int page = 1,
    int pageSize = 20,
  }) {
    return repository.getRecentRecipes(page: page, pageSize: pageSize);
  }
}

class GetPopularRecipes {
  final HomeRepository repository;

  GetPopularRecipes(this.repository);

  Future<Either<Failure, List<RecipeSummary>>> call({int limit = 10}) {
    return repository.getPopularRecipes(limit: limit);
  }
}
