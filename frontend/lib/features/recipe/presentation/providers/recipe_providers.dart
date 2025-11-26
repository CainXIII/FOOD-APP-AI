import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/providers/providers.dart';
import '../../domain/usecases/get_recipe_detail.dart';
import '../../domain/usecases/toggle_favorite.dart';
import '../../domain/usecases/rate_recipe.dart';
import '../datasources/recipe_api_service.dart';
import '../repositories/recipe_repository_impl.dart';

// API Service
final recipeApiServiceProvider = Provider<RecipeApiService>((ref) {
  final dio = ref.watch(dioClientProvider).dio;
  return RecipeApiService(dio);
});

// Repository
final recipeRepositoryProvider = Provider((ref) {
  final apiService = ref.watch(recipeApiServiceProvider);
  return RecipeRepositoryImpl(apiService);
});

// Usecases
final getRecipeDetailProvider = Provider((ref) {
  final repository = ref.watch(recipeRepositoryProvider);
  return GetRecipeDetail(repository);
});

final toggleFavoriteProvider = Provider((ref) {
  final repository = ref.watch(recipeRepositoryProvider);
  return ToggleFavorite(repository);
});

final rateRecipeProvider = Provider((ref) {
  final repository = ref.watch(recipeRepositoryProvider);
  return RateRecipe(repository);
});

// Recipe Detail State
final recipeDetailProvider = FutureProvider.family((ref, String id) async {
  final usecase = ref.watch(getRecipeDetailProvider);
  final result = await usecase(id);
  return result.fold(
    (failure) => throw Exception(failure.message),
    (recipe) => recipe,
  );
});
