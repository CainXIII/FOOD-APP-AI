import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../home/data/models/recipe_summary_model.dart';
import '../../data/datasources/search_remote_datasource.dart';
import '../../../../core/providers/providers.dart';

/// Search state
class SearchState {
  final List<RecipeSummaryModel> results;
  final List<String> recentSearches;
  final bool isLoading;
  final String? error;
  final String query;

  const SearchState({
    this.results = const [],
    this.recentSearches = const [],
    this.isLoading = false,
    this.error,
    this.query = '',
  });

  SearchState copyWith({
    List<RecipeSummaryModel>? results,
    List<String>? recentSearches,
    bool? isLoading,
    String? error,
    String? query,
  }) {
    return SearchState(
      results: results ?? this.results,
      recentSearches: recentSearches ?? this.recentSearches,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      query: query ?? this.query,
    );
  }
}

/// Search notifier
class SearchNotifier extends StateNotifier<SearchState> {
  final SearchRemoteDataSource _dataSource;

  SearchNotifier(this._dataSource) : super(const SearchState()) {
    _loadRecentSearches();
  }

  /// Load recent searches from local storage
  void _loadRecentSearches() {
    // TODO: Load from SharedPreferences
    // For now, using empty list
  }

  /// Perform semantic search
  Future<void> search(String query) async {
    if (query.trim().isEmpty) {
      state = state.copyWith(results: [], query: '', error: null);
      return;
    }

    state = state.copyWith(isLoading: true, error: null, query: query);

    try {
      final results = await _dataSource.semanticSearch(query: query);
      
      // Add to recent searches
      final updatedRecent = [query, ...state.recentSearches.where((q) => q != query)].take(10).toList();
      
      state = state.copyWith(
        results: results,
        recentSearches: updatedRecent,
        isLoading: false,
      );

      // TODO: Save recent searches to SharedPreferences
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Không thể tìm kiếm: $e',
      );
    }
  }

  /// Search by ingredients
  Future<void> searchByIngredients(List<String> ingredients) async {
    if (ingredients.isEmpty) {
      state = state.copyWith(results: [], error: null);
      return;
    }

    state = state.copyWith(isLoading: true, error: null);

    try {
      final results = await _dataSource.searchByIngredients(
        ingredients: ingredients,
      );
      
      state = state.copyWith(
        results: results,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Không thể tìm kiếm theo nguyên liệu: $e',
      );
    }
  }

  /// Clear search results
  void clearSearch() {
    state = state.copyWith(
      results: [],
      query: '',
      error: null,
    );
  }

  /// Clear recent searches
  void clearRecentSearches() {
    state = state.copyWith(recentSearches: []);
    // TODO: Clear from SharedPreferences
  }
}

// Providers
final searchDataSourceProvider = Provider<SearchRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return SearchRemoteDataSource(dioClient);
});

final searchProvider = StateNotifierProvider<SearchNotifier, SearchState>((ref) {
  final dataSource = ref.watch(searchDataSourceProvider);
  return SearchNotifier(dataSource);
});
