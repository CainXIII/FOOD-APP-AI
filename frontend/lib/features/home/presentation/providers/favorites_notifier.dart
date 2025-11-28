import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/datasources/favorites_remote_datasource.dart';
import '../../../../core/providers/providers.dart';

// State to manage favorite recipes
class FavoritesState {
  final Set<String> favoriteIds;
  final bool isLoading;
  final String? error;

  const FavoritesState({
    this.favoriteIds = const {},
    this.isLoading = false,
    this.error,
  });

  FavoritesState copyWith({
    Set<String>? favoriteIds,
    bool? isLoading,
    String? error,
  }) {
    return FavoritesState(
      favoriteIds: favoriteIds ?? this.favoriteIds,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }

  bool isFavorite(String recipeId) {
    return favoriteIds.contains(recipeId);
  }
}

// Provider for FavoritesRemoteDataSource
final favoritesDataSourceProvider = Provider<FavoritesRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return FavoritesRemoteDataSource(dioClient);
});

// Notifier to manage favorites with backend sync
class FavoritesNotifier extends StateNotifier<FavoritesState> {
  final FavoritesRemoteDataSource _dataSource;

  FavoritesNotifier(this._dataSource) : super(const FavoritesState()) {
    // Load favorites on initialization
    loadFavorites();
  }

  /// Load favorites from backend
  Future<void> loadFavorites() async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final favorites = await _dataSource.getFavorites();
      state = state.copyWith(
        favoriteIds: Set<String>.from(favorites),
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  /// Toggle favorite status (add/remove)
  Future<void> toggleFavorite(String recipeId) async {
    final wasFavorite = state.isFavorite(recipeId);
    
    // Optimistic update
    final currentFavorites = Set<String>.from(state.favoriteIds);
    if (wasFavorite) {
      currentFavorites.remove(recipeId);
    } else {
      currentFavorites.add(recipeId);
    }
    state = state.copyWith(favoriteIds: currentFavorites, error: null);

    try {
      // Call backend API
      if (wasFavorite) {
        await _dataSource.removeFavorite(recipeId);
      } else {
        await _dataSource.addFavorite(recipeId);
      }
    } catch (e) {
      // Revert on error
      final revertedFavorites = Set<String>.from(state.favoriteIds);
      if (wasFavorite) {
        revertedFavorites.add(recipeId);
      } else {
        revertedFavorites.remove(recipeId);
      }
      state = state.copyWith(
        favoriteIds: revertedFavorites,
        error: 'Failed to update favorite: $e',
      );
    }
  }

  /// Add recipe to favorites
  Future<void> addFavorite(String recipeId) async {
    if (state.isFavorite(recipeId)) return;
    await toggleFavorite(recipeId);
  }

  /// Remove recipe from favorites
  Future<void> removeFavorite(String recipeId) async {
    if (!state.isFavorite(recipeId)) return;
    await toggleFavorite(recipeId);
  }

  bool isFavorite(String recipeId) {
    return state.isFavorite(recipeId);
  }
}

// Provider
final favoritesProvider = StateNotifierProvider<FavoritesNotifier, FavoritesState>((ref) {
  final dataSource = ref.watch(favoritesDataSourceProvider);
  return FavoritesNotifier(dataSource);
});
