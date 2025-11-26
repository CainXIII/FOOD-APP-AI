import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../models/recipe_model.dart';

part 'recipe_api_service.g.dart';

@RestApi()
abstract class RecipeApiService {
  factory RecipeApiService(Dio dio, {String baseUrl}) = _RecipeApiService;

  @GET(ApiEndpoints.recipes + '/{id}')
  Future<RecipeModel> getRecipeDetail(@Path('id') String id);

  @POST(ApiEndpoints.recipes + '/{id}/favorite')
  Future<Map<String, dynamic>> toggleFavorite(@Path('id') String id);

  @POST(ApiEndpoints.recipes + '/{id}/rating')
  Future<void> rateRecipe(
    @Path('id') String id,
    @Body() Map<String, dynamic> body,
  );

  @GET(ApiEndpoints.recipes + '/{id}/rating')
  Future<Map<String, dynamic>?> getUserRating(@Path('id') String id);
}
