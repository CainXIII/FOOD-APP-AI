import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';
import '../../../home/data/models/recipe_summary_model.dart';

/// Remote data source for search operations
class SearchRemoteDataSource {
  final DioClient _dioClient;

  SearchRemoteDataSource(this._dioClient);

  /// Semantic search for recipes
  Future<List<RecipeSummaryModel>> semanticSearch({
    required String query,
    int page = 1,
    int pageSize = 20,
    int? limit,
  }) async {
    try {
      final response = await _dioClient.dio.get(
        '/search/semantic',
        queryParameters: {
          'query': query,
          'page': page,
          'page_size': pageSize,
          if (limit != null) 'limit': limit,
        },
      );

      final List<dynamic> results = response.data['recipes'] ?? [];
      return results
          .map((json) => RecipeSummaryModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      throw Exception('Failed to search recipes: $e');
    }
  }

  /// Search by ingredients
  Future<List<RecipeSummaryModel>> searchByIngredients({
    required List<String> ingredients,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final response = await _dioClient.dio.post(
        '/search/ingredients',
        data: {
          'ingredients': ingredients,
          'page': page,
          'page_size': pageSize,
        },
      );

      final List<dynamic> results = response.data['recipes'] ?? [];
      return results
          .map((json) => RecipeSummaryModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      throw Exception('Failed to search by ingredients: $e');
    }
  }

  /// Get recipe recommendations
  Future<List<RecipeSummaryModel>> getRecommendations({
    String? recipeId,
    int limit = 10,
  }) async {
    try {
      final response = await _dioClient.dio.get(
        '/search/recommendations',
        queryParameters: {
          if (recipeId != null) 'recipe_id': recipeId,
          'limit': limit,
        },
      );

      final List<dynamic> results = response.data['recipes'] ?? [];
      return results
          .map((json) => RecipeSummaryModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      throw Exception('Failed to get recommendations: $e');
    }
  }
}
