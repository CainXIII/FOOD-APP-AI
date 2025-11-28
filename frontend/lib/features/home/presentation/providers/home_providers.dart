import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/providers/providers.dart';
import '../../../../core/utils/pagination_state.dart';
import '../../data/datasources/recipe_remote_datasource.dart';
import '../../data/datasources/category_remote_datasource.dart';
import '../../data/models/recipe_summary_model.dart';

// Data source providers
final recipeDataSourceProvider = Provider<RecipeRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return RecipeRemoteDataSource(dioClient);
});

final categoryDataSourceProvider = Provider<CategoryRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return CategoryRemoteDataSource(dioClient);
});

// Real API Providers
final featuredRecipesProvider = FutureProvider((ref) async {
  final dataSource = ref.watch(recipeDataSourceProvider);
  return await dataSource.getFeaturedRecipes(pageSize: 5);
});

final recentRecipesProvider = FutureProvider((ref) async {
  final dataSource = ref.watch(recipeDataSourceProvider);
  return await dataSource.getRecentRecipes(pageSize: 10);
});

final popularRecipesProvider = FutureProvider((ref) async {
  final dataSource = ref.watch(recipeDataSourceProvider);
  return await dataSource.getPopularRecipes(pageSize: 8);
});

final categoriesProvider = FutureProvider((ref) async {
  final dataSource = ref.watch(categoryDataSourceProvider);
  return await dataSource.getCategories();
});

// Paginated Recipe Notifier
class PaginatedRecipesNotifier extends StateNotifier<PaginationState<RecipeSummaryModel>> {
  final RecipeRemoteDataSource _dataSource;
  final String _recipeType; // 'featured', 'popular', 'recent'

  PaginatedRecipesNotifier(this._dataSource, this._recipeType)
      : super(const PaginationState());

  Future<void> loadFirstPage() async {
    state = state.setLoading();
    await _loadPage(1, append: false);
  }

  Future<void> loadNextPage() async {
    if (state.isLoadingMore || !state.hasMore) return;
    
    state = state.setLoadingMore();
    await _loadPage(state.currentPage + 1, append: true);
  }

  Future<void> refresh() async {
    state = state.reset();
    await loadFirstPage();
  }

  Future<void> _loadPage(int page, {required bool append}) async {
    try {
      RecipeListResponse response;
      
      switch (_recipeType) {
        case 'featured':
          response = await _dataSource.getFeaturedRecipesResponse(page: page, pageSize: 10);
          break;
        case 'popular':
          response = await _dataSource.getPopularRecipesResponse(page: page, pageSize: 10);
          break;
        case 'recent':
          response = await _dataSource.getRecentRecipesResponse(page: page, pageSize: 10);
          break;
        default:
          response = const RecipeListResponse(
            items: [],
            total: 0,
            page: 1,
            pageSize: 10,
            totalPages: 0,
          );
      }

      state = state.updateWithData(
        newItems: response.items,
        page: response.page,
        totalPages: response.totalPages,
        totalItems: response.total,
        append: append,
      );
    } catch (e) {
      state = state.setError(e.toString());
    }
  }
}

// Paginated providers
final paginatedFeaturedRecipesProvider =
    StateNotifierProvider<PaginatedRecipesNotifier, PaginationState<RecipeSummaryModel>>((ref) {
  final dataSource = ref.watch(recipeDataSourceProvider);
  final notifier = PaginatedRecipesNotifier(dataSource, 'featured');
  notifier.loadFirstPage();
  return notifier;
});

final paginatedPopularRecipesProvider =
    StateNotifierProvider<PaginatedRecipesNotifier, PaginationState<RecipeSummaryModel>>((ref) {
  final dataSource = ref.watch(recipeDataSourceProvider);
  final notifier = PaginatedRecipesNotifier(dataSource, 'popular');
  notifier.loadFirstPage();
  return notifier;
});

final paginatedRecentRecipesProvider =
    StateNotifierProvider<PaginatedRecipesNotifier, PaginationState<RecipeSummaryModel>>((ref) {
  final dataSource = ref.watch(recipeDataSourceProvider);
  final notifier = PaginatedRecipesNotifier(dataSource, 'recent');
  notifier.loadFirstPage();
  return notifier;
});
