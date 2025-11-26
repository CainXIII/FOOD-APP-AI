import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/recipe.dart';
import 'recipe_ingredient_model.dart';
import 'recipe_step_model.dart';
import 'nutrition_model.dart';

part 'recipe_model.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake, explicitToJson: true)
class RecipeModel extends Recipe {
  const RecipeModel({
    required super.id,
    required super.titleVi,
    super.titleEn,
    required super.slug,
    required super.descriptionVi,
    super.descriptionEn,
    super.thumbnail,
    super.videoUrl,
    super.categoryId,
    super.categoryName,
    required super.authorId,
    required super.authorName,
    super.authorAvatar,
    required super.prepTime,
    required super.cookTime,
    required super.servings,
    required super.difficulty,
    super.isVegetarian,
    super.isVegan,
    super.isGlutenFree,
    super.isDairyFree,
    super.averageRating,
    super.totalRatings,
    super.totalFavorites,
    super.isFavorited,
    super.userRating,
    super.ingredients,
    super.steps,
    super.nutrition,
    super.tags,
    required super.createdAt,
    super.updatedAt,
  });

  factory RecipeModel.fromJson(Map<String, dynamic> json) =>
      _$RecipeModelFromJson(json);

  Map<String, dynamic> toJson() => _$RecipeModelToJson(this);

  Recipe toEntity() {
    return Recipe(
      id: id,
      titleVi: titleVi,
      titleEn: titleEn,
      slug: slug,
      descriptionVi: descriptionVi,
      descriptionEn: descriptionEn,
      thumbnail: thumbnail,
      videoUrl: videoUrl,
      categoryId: categoryId,
      categoryName: categoryName,
      authorId: authorId,
      authorName: authorName,
      authorAvatar: authorAvatar,
      prepTime: prepTime,
      cookTime: cookTime,
      servings: servings,
      difficulty: difficulty,
      isVegetarian: isVegetarian,
      isVegan: isVegan,
      isGlutenFree: isGlutenFree,
      isDairyFree: isDairyFree,
      averageRating: averageRating,
      totalRatings: totalRatings,
      totalFavorites: totalFavorites,
      isFavorited: isFavorited,
      userRating: userRating,
      ingredients: ingredients,
      steps: steps,
      nutrition: nutrition,
      tags: tags,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }
}
