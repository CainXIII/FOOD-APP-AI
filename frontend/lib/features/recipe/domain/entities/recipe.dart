import 'package:equatable/equatable.dart';
import 'recipe_ingredient.dart';
import 'recipe_step.dart';
import 'nutrition.dart';

/// Recipe entity - full detail
class Recipe extends Equatable {
  final String id;
  final String titleVi;
  final String? titleEn;
  final String slug;
  final String descriptionVi;
  final String? descriptionEn;
  final String? thumbnail;
  final String? videoUrl;
  
  // Category and author
  final String? categoryId;
  final String? categoryName;
  final String authorId;
  final String authorName;
  final String? authorAvatar;
  
  // Time and difficulty
  final int prepTime;
  final int cookTime;
  final int servings;
  final String difficulty;
  
  // Dietary flags
  final bool isVegetarian;
  final bool isVegan;
  final bool isGlutenFree;
  final bool isDairyFree;
  
  // Ratings and favorites
  final double? averageRating;
  final int totalRatings;
  final int totalFavorites;
  final bool isFavorited;
  final int? userRating;
  
  // Recipe content
  final List<RecipeIngredient> ingredients;
  final List<RecipeStep> steps;
  final Nutrition? nutrition;
  final List<String> tags;
  
  // Metadata
  final DateTime createdAt;
  final DateTime? updatedAt;

  const Recipe({
    required this.id,
    required this.titleVi,
    this.titleEn,
    required this.slug,
    required this.descriptionVi,
    this.descriptionEn,
    this.thumbnail,
    this.videoUrl,
    this.categoryId,
    this.categoryName,
    required this.authorId,
    required this.authorName,
    this.authorAvatar,
    required this.prepTime,
    required this.cookTime,
    required this.servings,
    required this.difficulty,
    this.isVegetarian = false,
    this.isVegan = false,
    this.isGlutenFree = false,
    this.isDairyFree = false,
    this.averageRating,
    this.totalRatings = 0,
    this.totalFavorites = 0,
    this.isFavorited = false,
    this.userRating,
    this.ingredients = const [],
    this.steps = const [],
    this.nutrition,
    this.tags = const [],
    required this.createdAt,
    this.updatedAt,
  });

  String get displayTitle => titleEn ?? titleVi;
  String get displayDescription => descriptionEn ?? descriptionVi;
  int get totalTime => prepTime + cookTime;
  
  String get timeDisplay {
    if (totalTime < 60) return '$totalTime phút';
    final hours = totalTime ~/ 60;
    final mins = totalTime % 60;
    if (mins == 0) return '$hours giờ';
    return '$hours giờ $mins phút';
  }
  
  String get difficultyDisplay {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'Dễ';
      case 'medium':
        return 'Trung bình';
      case 'hard':
        return 'Khó';
      default:
        return difficulty;
    }
  }

  @override
  List<Object?> get props => [
        id, titleVi, titleEn, slug, descriptionVi, descriptionEn,
        thumbnail, videoUrl, categoryId, categoryName, authorId,
        authorName, authorAvatar, prepTime, cookTime, servings,
        difficulty, isVegetarian, isVegan, isGlutenFree, isDairyFree,
        averageRating, totalRatings, totalFavorites, isFavorited,
        userRating, ingredients, steps, nutrition, tags,
        createdAt, updatedAt,
      ];
}
