import 'package:flutter_riverpod/flutter_riverpod.dart';

// State to manage favorite recipes
class FavoritesState {
  final Set<String> favoriteIds;

  const FavoritesState({
    this.favoriteIds = const {},
  });

  FavoritesState copyWith({
    Set<String>? favoriteIds,
  }) {
    return FavoritesState(
      favoriteIds: favoriteIds ?? this.favoriteIds,
    );
  }

  bool isFavorite(String recipeId) {
    return favoriteIds.contains(recipeId);
  }
}

// Notifier to manage favorites
class FavoritesNotifier extends StateNotifier<FavoritesState> {
  FavoritesNotifier() : super(const FavoritesState());

  void toggleFavorite(String recipeId) {
    final currentFavorites = Set<String>.from(state.favoriteIds);
    
    if (currentFavorites.contains(recipeId)) {
      currentFavorites.remove(recipeId);
      // TODO: Call API to remove from favorites
    } else {
      currentFavorites.add(recipeId);
      // TODO: Call API to add to favorites
    }
    
    state = state.copyWith(favoriteIds: currentFavorites);
  }

  bool isFavorite(String recipeId) {
    return state.isFavorite(recipeId);
  }
}

// Provider
final favoritesProvider = StateNotifierProvider<FavoritesNotifier, FavoritesState>((ref) {
  return FavoritesNotifier();
});
