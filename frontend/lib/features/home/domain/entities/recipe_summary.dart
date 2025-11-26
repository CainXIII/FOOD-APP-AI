import 'package:equatable/equatable.dart';

class RecipeSummary extends Equatable {
  final String id;
  final String titleVi;
  final String? titleEn;
  final String slug;
  final String descriptionVi;
  final String? thumbnailUrl;
  final String categoryId;
  final String categoryNameVi;
  final String authorId;
  final String authorName;
  final String? authorAvatar;
  final int prepTimeMinutes;
  final int cookTimeMinutes;
  final int totalTimeMinutes;
  final int servings;
  final String difficulty;
  final bool isVegetarian;
  final bool isVegan;
  final double avgRating;
  final int totalRatings;
  final int totalFavorites;
  final bool isFeatured;
  final DateTime createdAt;
  final DateTime updatedAt;

  const RecipeSummary({
    required this.id,
    required this.titleVi,
    this.titleEn,
    required this.slug,
    required this.descriptionVi,
    this.thumbnailUrl,
    required this.categoryId,
    required this.categoryNameVi,
    required this.authorId,
    required this.authorName,
    this.authorAvatar,
    required this.prepTimeMinutes,
    required this.cookTimeMinutes,
    required this.totalTimeMinutes,
    required this.servings,
    required this.difficulty,
    required this.isVegetarian,
    required this.isVegan,
    required this.avgRating,
    required this.totalRatings,
    required this.totalFavorites,
    required this.isFeatured,
    required this.createdAt,
    required this.updatedAt,
  });

  String get displayTitle => titleVi;
  
  String get timeDisplay => '$totalTimeMinutes phút';
  
  String get difficultyDisplay {
    switch (difficulty) {
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
        id,
        titleVi,
        titleEn,
        slug,
        descriptionVi,
        thumbnailUrl,
        categoryId,
        categoryNameVi,
        authorId,
        authorName,
        authorAvatar,
        prepTimeMinutes,
        cookTimeMinutes,
        totalTimeMinutes,
        servings,
        difficulty,
        isVegetarian,
        isVegan,
        avgRating,
        totalRatings,
        totalFavorites,
        isFeatured,
        createdAt,
        updatedAt,
      ];
}
