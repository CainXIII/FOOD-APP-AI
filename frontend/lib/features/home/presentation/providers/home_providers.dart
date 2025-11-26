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
      List<RecipeSummaryModel> items;
      
      switch (_recipeType) {
        case 'featured':
          items = await _dataSource.getFeaturedRecipes(page: page, pageSize: 10);
          break;
        case 'popular':
          items = await _dataSource.getPopularRecipes(page: page, pageSize: 10);
          break;
        case 'recent':
          items = await _dataSource.getRecentRecipes(page: page, pageSize: 10);
          break;
        default:
          items = [];
      }

      // Assuming API returns items directly without pagination metadata
      // If API has pagination metadata, update accordingly
      state = state.updateWithData(
        newItems: items,
        page: page,
        totalPages: items.length >= 10 ? page + 1 : page, // Simple logic
        totalItems: state.totalItems + items.length,
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

// BACKUP: Mock data helpers (for fallback/testing)
List<dynamic> _getMockRecipes() {
  return [
    {
      'id': '1',
      'title': 'Phở Bò Hà Nội',
      'description': 'Món phở truyền thống của Hà Nội với nước dùng thanh ngọt',
      'imageUrl': 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=400',
      'cookingTime': 120,
      'difficulty': 'medium',
      'rating': 4.8,
      'totalReviews': 245,
      'author': 'Chef Minh',
      'isFavorited': false,
    },
    {
      'id': '2',
      'title': 'Bún Chả Hà Nội',
      'description': 'Thịt nướng thơm phức ăn kèm bún tươi và nước mắm chua ngọt',
      'imageUrl': 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400',
      'cookingTime': 45,
      'difficulty': 'easy',
      'rating': 4.9,
      'totalReviews': 312,
      'author': 'Chef Lan',
      'isFavorited': false,
    },
    {
      'id': '3',
      'title': 'Cơm Tấm Sườn Bì',
      'description': 'Cơm tấm sài gòn với sườn nướng và bì giòn',
      'imageUrl': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400',
      'cookingTime': 60,
      'difficulty': 'medium',
      'rating': 4.7,
      'totalReviews': 189,
      'author': 'Chef Hùng',
      'isFavorited': false,
    },
    {
      'id': '4',
      'title': 'Bánh Mì Thịt Nướng',
      'description': 'Bánh mì giòn với thịt nướng, pate và rau sống',
      'imageUrl': 'https://images.unsplash.com/photo-1588137378633-dea1336ce1e2?w=400',
      'cookingTime': 30,
      'difficulty': 'easy',
      'rating': 4.6,
      'totalReviews': 156,
      'author': 'Chef Thanh',
      'isFavorited': true,
    },
    {
      'id': '5',
      'title': 'Bún Bò Huế',
      'description': 'Món bún cay đặc trưng xứ Huế với nước dùng đậm đà',
      'imageUrl': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=400',
      'cookingTime': 150,
      'difficulty': 'hard',
      'rating': 4.9,
      'totalReviews': 278,
      'author': 'Chef Hương',
      'isFavorited': false,
    },
    {
      'id': '6',
      'title': 'Gỏi Cuốn Tôm Thịt',
      'description': 'Món cuốn tươi mát với tôm, thịt và rau sống',
      'imageUrl': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400',
      'cookingTime': 25,
      'difficulty': 'easy',
      'rating': 4.5,
      'totalReviews': 134,
      'author': 'Chef Tâm',
      'isFavorited': false,
    },
    {
      'id': '7',
      'title': 'Canh Chua Cá',
      'description': 'Canh chua thanh mát với cá tươi và rau củ',
      'imageUrl': 'https://images.unsplash.com/photo-1590301157890-4810ed352733?w=400',
      'cookingTime': 40,
      'difficulty': 'medium',
      'rating': 4.4,
      'totalReviews': 98,
      'author': 'Chef Linh',
      'isFavorited': false,
    },
    {
      'id': '8',
      'title': 'Thịt Kho Tàu',
      'description': 'Thịt ba chỉ kho đậm đà với trứng và nước dừa',
      'imageUrl': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=400',
      'cookingTime': 90,
      'difficulty': 'medium',
      'rating': 4.7,
      'totalReviews': 167,
      'author': 'Chef Nam',
      'isFavorited': true,
    },
  ];
}

List<dynamic> _getMockCategories() {
  return [
    {'id': '1', 'name': 'Món Chính', 'icon': '🍲', 'count': 156},
    {'id': '2', 'name': 'Món Ăn Sáng', 'icon': '🥐', 'count': 89},
    {'id': '3', 'name': 'Món Ăn Vặt', 'icon': '🍢', 'count': 124},
    {'id': '4', 'name': 'Món Tráng Miệng', 'icon': '🍰', 'count': 78},
    {'id': '5', 'name': 'Món Chay', 'icon': '🥗', 'count': 67},
    {'id': '6', 'name': 'Món Nướng', 'icon': '🍖', 'count': 92},
  ];
}
