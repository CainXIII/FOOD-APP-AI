import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';

/// Remote data source for favorites (social features)
class FavoritesRemoteDataSource {
  final DioClient _dioClient;

  FavoritesRemoteDataSource(this._dioClient);

  /// Get user's favorite recipes
  Future<List<String>> getFavorites() async {
    try {
      final response = await _dioClient.dio.get('/social/favorites');
      
      // Backend returns: { "favorites": [{ "id": "...", "recipe_id": "..." }] }
      final List<dynamic> favorites = response.data['favorites'] ?? [];
      return favorites
          .map((fav) => fav['recipe_id'] as String)
          .toList();
    } catch (e) {
      throw Exception('Failed to fetch favorites: $e');
    }
  }

  /// Add recipe to favorites
  Future<void> addFavorite(String recipeId) async {
    try {
      await _dioClient.dio.post(
        '/social/favorites',
        data: {'recipe_id': recipeId},
      );
    } catch (e) {
      throw Exception('Failed to add favorite: $e');
    }
  }

  /// Remove recipe from favorites
  Future<void> removeFavorite(String recipeId) async {
    try {
      // Backend endpoint: DELETE /social/favorites/:recipe_id
      await _dioClient.dio.delete('/social/favorites/$recipeId');
    } catch (e) {
      throw Exception('Failed to remove favorite: $e');
    }
  }

  /// Check if recipe is favorited
  Future<bool> isFavorite(String recipeId) async {
    try {
      final favorites = await getFavorites();
      return favorites.contains(recipeId);
    } catch (e) {
      return false;
    }
  }
}
