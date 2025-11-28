import '../config/environment.dart';

/// API endpoints configuration
class ApiEndpoints {
  static String get baseUrl => EnvironmentConfig.apiBaseUrl;
  
  // Auth
  static const String register = '/auth/register';
  static const String login = '/auth/login';
  static const String refreshToken = '/auth/refresh';
  static const String me = '/auth/me';
  
  // Recipes
  static const String recipes = '/recipes';
  static String recipeDetail(String id) => '/recipes/$id';
  static String recipeImage(String id) => '/recipes/$id/image';
  
  // Categories
  static const String categories = '/categories';
  static String categoryDetail(String id) => '/categories/$id';
  
  // Ingredients
  static const String ingredients = '/ingredients';
  static String ingredientDetail(String id) => '/ingredients/$id';
  
  // Chat
  static const String chats = '/chat';
  static String chatDetail(String id) => '/chat/$id';
  static String chatMessages(String id) => '/chat/$id/messages';
  static String chatStream(String id) => '/chat/$id/stream';
  
  // Social (Favorites, Ratings, Comments)
  static const String favorites = '/social/favorites';
  static String removeFavorite(String recipeId) => '/social/favorites/$recipeId';
  static const String ratings = '/social/ratings';
  static String recipeRatings(String recipeId) => '/social/recipes/$recipeId/ratings';
  static const String comments = '/social/comments';
  static String recipeComments(String recipeId) => '/social/recipes/$recipeId/comments';
  
  // Uploads
  static const String uploadAvatar = '/uploads/users/avatar';
  static const String uploadAudio = '/uploads/chat/audio';
  static String uploadRecipeImage(String id) => '/uploads/recipes/$id/image';
}
