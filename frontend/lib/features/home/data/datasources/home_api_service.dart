import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';
import '../models/recipe_summary_model.dart';
import '../models/category_model.dart';

part 'home_api_service.g.dart';

@RestApi()
abstract class HomeApiService {
  factory HomeApiService(Dio dio, {String baseUrl}) = _HomeApiService;

  @GET('/recipes')
  Future<RecipeListResponse> getRecipes({
    @Query('page') int page = 1,
    @Query('page_size') int pageSize = 20,
    @Query('sort_by') String? sortBy,
    @Query('sort_order') String? sortOrder,
  });

  @GET('/recipes')
  Future<RecipeListResponse> getFeaturedRecipes({
    @Query('is_featured') bool isFeatured = true,
    @Query('page_size') int limit = 10,
  });

  @GET('/recipes')
  Future<RecipeListResponse> getRecipesByCategory({
    @Query('category_id') required String categoryId,
    @Query('page') int page = 1,
    @Query('page_size') int pageSize = 20,
  });

  @GET('/categories')
  Future<List<CategoryModel>> getCategories({
    @Query('is_active') bool? isActive = true,
  });
}
