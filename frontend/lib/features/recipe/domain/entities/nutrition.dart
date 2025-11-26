import 'package:equatable/equatable.dart';

/// Nutrition facts entity
class Nutrition extends Equatable {
  final double calories;
  final double protein;
  final double carbs;
  final double fat;
  final double fiber;
  final double sugar;
  final double sodium;

  const Nutrition({
    required this.calories,
    required this.protein,
    required this.carbs,
    required this.fat,
    this.fiber = 0,
    this.sugar = 0,
    this.sodium = 0,
  });

  @override
  List<Object?> get props => [calories, protein, carbs, fat, fiber, sugar, sodium];
}
