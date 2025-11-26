import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/nutrition.dart';

part 'nutrition_model.g.dart';

@JsonSerializable()
class NutritionModel extends Nutrition {
  const NutritionModel({
    required super.calories,
    required super.protein,
    required super.carbs,
    required super.fat,
    super.fiber,
    super.sugar,
    super.sodium,
  });

  factory NutritionModel.fromJson(Map<String, dynamic> json) =>
      _$NutritionModelFromJson(json);

  Map<String, dynamic> toJson() => _$NutritionModelToJson(this);

  Nutrition toEntity() {
    return Nutrition(
      calories: calories,
      protein: protein,
      carbs: carbs,
      fat: fat,
      fiber: fiber,
      sugar: sugar,
      sodium: sodium,
    );
  }
}
