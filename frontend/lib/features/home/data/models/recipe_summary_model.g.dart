// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'recipe_summary_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RecipeSummaryModel _$RecipeSummaryModelFromJson(Map<String, dynamic> json) =>
    RecipeSummaryModel(
      id: json['id'] as String,
      titleVi: json['title_vi'] as String,
      titleEn: json['title_en'] as String?,
      slug: json['slug'] as String,
      descriptionVi: json['description_vi'] as String,
      thumbnailUrl: json['thumbnail_url'] as String?,
      categoryId: json['category_id'] as String,
      categoryNameVi: json['category_name_vi'] as String,
      authorId: json['author_id'] as String,
      authorName: json['author_name'] as String,
      authorAvatar: json['author_avatar'] as String?,
      prepTimeMinutes: (json['prep_time_minutes'] as num).toInt(),
      cookTimeMinutes: (json['cook_time_minutes'] as num).toInt(),
      totalTimeMinutes: (json['total_time_minutes'] as num).toInt(),
      servings: (json['servings'] as num).toInt(),
      difficulty: json['difficulty'] as String,
      isVegetarian: json['is_vegetarian'] as bool,
      isVegan: json['is_vegan'] as bool,
      avgRating: (json['avg_rating'] as num).toDouble(),
      totalRatings: (json['total_ratings'] as num).toInt(),
      totalFavorites: (json['total_favorites'] as num).toInt(),
      isFeatured: json['is_featured'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$RecipeSummaryModelToJson(RecipeSummaryModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title_vi': instance.titleVi,
      'title_en': instance.titleEn,
      'slug': instance.slug,
      'description_vi': instance.descriptionVi,
      'thumbnail_url': instance.thumbnailUrl,
      'category_id': instance.categoryId,
      'category_name_vi': instance.categoryNameVi,
      'author_id': instance.authorId,
      'author_name': instance.authorName,
      'author_avatar': instance.authorAvatar,
      'prep_time_minutes': instance.prepTimeMinutes,
      'cook_time_minutes': instance.cookTimeMinutes,
      'total_time_minutes': instance.totalTimeMinutes,
      'servings': instance.servings,
      'difficulty': instance.difficulty,
      'is_vegetarian': instance.isVegetarian,
      'is_vegan': instance.isVegan,
      'avg_rating': instance.avgRating,
      'total_ratings': instance.totalRatings,
      'total_favorites': instance.totalFavorites,
      'is_featured': instance.isFeatured,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

RecipeListResponse _$RecipeListResponseFromJson(Map<String, dynamic> json) =>
    RecipeListResponse(
      items: (json['items'] as List<dynamic>)
          .map((e) => RecipeSummaryModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      total: (json['total'] as num).toInt(),
      page: (json['page'] as num).toInt(),
      pageSize: (json['page_size'] as num).toInt(),
      totalPages: (json['total_pages'] as num).toInt(),
    );

Map<String, dynamic> _$RecipeListResponseToJson(RecipeListResponse instance) =>
    <String, dynamic>{
      'items': instance.items,
      'total': instance.total,
      'page': instance.page,
      'page_size': instance.pageSize,
      'total_pages': instance.totalPages,
    };
