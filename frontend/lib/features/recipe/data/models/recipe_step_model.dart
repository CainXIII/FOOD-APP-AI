import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/recipe_step.dart';

part 'recipe_step_model.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake)
class RecipeStepModel extends RecipeStep {
  const RecipeStepModel({
    required super.stepNumber,
    required super.instruction,
    super.instructionEn,
    super.duration,
    super.imageUrl,
    super.tips,
  });

  factory RecipeStepModel.fromJson(Map<String, dynamic> json) =>
      _$RecipeStepModelFromJson(json);

  Map<String, dynamic> toJson() => _$RecipeStepModelToJson(this);

  RecipeStep toEntity() {
    return RecipeStep(
      stepNumber: stepNumber,
      instruction: instruction,
      instructionEn: instructionEn,
      duration: duration,
      imageUrl: imageUrl,
      tips: tips,
    );
  }
}
