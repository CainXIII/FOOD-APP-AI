import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';
import '../models/recipe_summary_model.dart';

class RecipeRemoteDataSource {
  final DioClient _dioClient;

  RecipeRemoteDataSource(this._dioClient);

  /// Get featured recipes (sorted by rating, featured flag, or views)
  Future<List<RecipeSummaryModel>> getFeaturedRecipes({
    int page = 1,
    int pageSize = 10,
  }) async {
    final response = await getFeaturedRecipesResponse(page: page, pageSize: pageSize);
    return response.items;
  }

  /// Get featured recipes response with pagination metadata
  Future<RecipeListResponse> getFeaturedRecipesResponse({
    int page = 1,
    int pageSize = 10,
  }) async {
    final response = await _dioClient.dio.get(
      '/recipes',
      queryParameters: {
        'page': page,
        'page_size': pageSize,
        'is_featured': true,  // Filter by featured flag
        'sort_by': 'average_rating',
        'sort_order': 'desc',
      },
    );

    // Manual status check
    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return RecipeListResponse.fromJson(response.data);
  }

  /// Get popular recipes (high ratings)
  Future<List<RecipeSummaryModel>> getPopularRecipes({
    int page = 1,
    int pageSize = 10,
  }) async {
    final response = await getPopularRecipesResponse(page: page, pageSize: pageSize);
    return response.items;
  }

  /// Get popular recipes response with pagination metadata
  Future<RecipeListResponse> getPopularRecipesResponse({
    int page = 1,
    int pageSize = 10,
  }) async {
    final response = await _dioClient.dio.get(
      '/recipes',
      queryParameters: {
        'page': page,
        'page_size': pageSize,
        'sort_by': 'views_count',  // Sort by popularity (views)
        'sort_order': 'desc',
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return RecipeListResponse.fromJson(response.data);
  }

  /// Get recent recipes (newly created)
  Future<List<RecipeSummaryModel>> getRecentRecipes({
    int page = 1,
    int pageSize = 10,
  }) async {
    final response = await getRecentRecipesResponse(page: page, pageSize: pageSize);
    return response.items;
  }

  /// Get recent recipes response with pagination metadata
  Future<RecipeListResponse> getRecentRecipesResponse({
    int page = 1,
    int pageSize = 10,
  }) async {
    final response = await _dioClient.dio.get(
      '/recipes',
      queryParameters: {
        'page': page,
        'page_size': pageSize,
        'sort_by': 'created_at',
        'sort_order': 'desc',
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return RecipeListResponse.fromJson(response.data);
  }

  /// Get recipes by category
  Future<List<dynamic>> getRecipesByCategory({
    required String categoryId,
    int page = 1,
    int pageSize = 20,
  }) async {
    final response = await _dioClient.dio.get(
      '/recipes',
      queryParameters: {
        'category_id': categoryId,
        'page': page,
        'page_size': pageSize,
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return (response.data['items'] as List?) ?? [];
  }

  /// Get recipe details by ID
  Future<Map<String, dynamic>> getRecipeDetails(String recipeId) async {
    final response = await _dioClient.dio.get('/recipes/$recipeId');

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return response.data as Map<String, dynamic>;
  }

  /// Search recipes
  Future<List<dynamic>> searchRecipes({
    required String query,
    int page = 1,
    int pageSize = 20,
    String? difficulty,
    bool? isVegetarian,
    bool? isVegan,
  }) async {
    final response = await _dioClient.dio.get(
      '/recipes',
      queryParameters: {
        'search': query,
        'page': page,
        'page_size': pageSize,
        if (difficulty != null) 'difficulty': difficulty,
        if (isVegetarian != null) 'is_vegetarian': isVegetarian,
        if (isVegan != null) 'is_vegan': isVegan,
      },
    );

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return (response.data['items'] as List?) ?? [];
  }
}
