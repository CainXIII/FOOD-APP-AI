import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/recipe_ingredient.dart';

part 'recipe_ingredient_model.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake)
class RecipeIngredientModel extends RecipeIngredient {
  const RecipeIngredientModel({
    required super.id,
    required super.name,
    super.nameEn,
    required super.amount,
    required super.unit,
    super.preparation,
    super.isOptional,
  });

  factory RecipeIngredientModel.fromJson(Map<String, dynamic> json) =>
      _$RecipeIngredientModelFromJson(json);

  Map<String, dynamic> toJson() => _$RecipeIngredientModelToJson(this);

  RecipeIngredient toEntity() {
    return RecipeIngredient(
      id: id,
      name: name,
      nameEn: nameEn,
      amount: amount,
      unit: unit,
      preparation: preparation,
      isOptional: isOptional,
    );
  }
}
