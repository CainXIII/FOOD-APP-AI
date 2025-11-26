import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/recipe_summary.dart';

part 'recipe_summary_model.g.dart';

@JsonSerializable()
class RecipeSummaryModel extends RecipeSummary {
  const RecipeSummaryModel({
    required super.id,
    @JsonKey(name: 'title_vi') required super.titleVi,
    @JsonKey(name: 'title_en') super.titleEn,
    required super.slug,
    @JsonKey(name: 'description_vi') required super.descriptionVi,
    @JsonKey(name: 'thumbnail_url') super.thumbnailUrl,
    @JsonKey(name: 'category_id') required super.categoryId,
    @JsonKey(name: 'category_name_vi') required super.categoryNameVi,
    @JsonKey(name: 'author_id') required super.authorId,
    @JsonKey(name: 'author_name') required super.authorName,
    @JsonKey(name: 'author_avatar') super.authorAvatar,
    @JsonKey(name: 'prep_time_minutes') required super.prepTimeMinutes,
    @JsonKey(name: 'cook_time_minutes') required super.cookTimeMinutes,
    @JsonKey(name: 'total_time_minutes') required super.totalTimeMinutes,
    required super.servings,
    required super.difficulty,
    required super.isVegetarian,
    required super.isVegan,
    @JsonKey(name: 'avg_rating') required super.avgRating,
    @JsonKey(name: 'total_ratings') required super.totalRatings,
    @JsonKey(name: 'total_favorites') required super.totalFavorites,
    @JsonKey(name: 'is_featured') required super.isFeatured,
    @JsonKey(name: 'created_at') required super.createdAt,
    @JsonKey(name: 'updated_at') required super.updatedAt,
  });

  factory RecipeSummaryModel.fromJson(Map<String, dynamic> json) =>
      _$RecipeSummaryModelFromJson(json);

  Map<String, dynamic> toJson() => _$RecipeSummaryModelToJson(this);
}

@JsonSerializable()
class RecipeListResponse {
  final List<RecipeSummaryModel> items;
  final int total;
  final int page;
  @JsonKey(name: 'page_size')
  final int pageSize;
  @JsonKey(name: 'total_pages')
  final int totalPages;

  const RecipeListResponse({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
    required this.totalPages,
  });

  factory RecipeListResponse.fromJson(Map<String, dynamic> json) =>
      _$RecipeListResponseFromJson(json);

  Map<String, dynamic> toJson() => _$RecipeListResponseToJson(this);
}
