import 'package:dartz/dartz.dart';
import '../../domain/entities/recipe_summary.dart';
import '../../domain/entities/category.dart';
import '../../domain/repositories/home_repository.dart';
import '../datasources/home_api_service.dart';
import '../../../../core/errors/failures.dart';
import '../../../../core/errors/exceptions.dart';

class HomeRepositoryImpl implements HomeRepository {
  final HomeApiService apiService;

  HomeRepositoryImpl({required this.apiService});

  @override
  Future<Either<Failure, List<RecipeSummary>>> getFeaturedRecipes({
    int limit = 10,
  }) async {
    try {
      final response = await apiService.getFeaturedRecipes(limit: limit);
      return Right(response.items);
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<RecipeSummary>>> getRecentRecipes({
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final response = await apiService.getRecipes(
        page: page,
        pageSize: pageSize,
        sortBy: 'created_at',
        sortOrder: 'desc',
      );
      return Right(response.items);
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<RecipeSummary>>> getPopularRecipes({
    int limit = 10,
  }) async {
    try {
      final response = await apiService.getRecipes(
        pageSize: limit,
        sortBy: 'average_rating',
        sortOrder: 'desc',
      );
      return Right(response.items);
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Category>>> getCategories() async {
    try {
      final categories = await apiService.getCategories();
      return Right(categories);
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<RecipeSummary>>> getRecipesByCategory({
    required String categoryId,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final response = await apiService.getRecipesByCategory(
        categoryId: categoryId,
        page: page,
        pageSize: pageSize,
      );
      return Right(response.items);
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }
}
