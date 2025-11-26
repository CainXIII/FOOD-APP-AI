// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'recipe_step_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RecipeStepModel _$RecipeStepModelFromJson(Map<String, dynamic> json) =>
    RecipeStepModel(
      stepNumber: (json['step_number'] as num).toInt(),
      instruction: json['instruction'] as String,
      instructionEn: json['instruction_en'] as String?,
      duration: (json['duration'] as num?)?.toInt(),
      imageUrl: json['image_url'] as String?,
      tips:
          (json['tips'] as List<dynamic>?)?.map((e) => e as String).toList() ??
              const [],
    );

Map<String, dynamic> _$RecipeStepModelToJson(RecipeStepModel instance) =>
    <String, dynamic>{
      'step_number': instance.stepNumber,
      'instruction': instance.instruction,
      'instruction_en': instance.instructionEn,
      'duration': instance.duration,
      'image_url': instance.imageUrl,
      'tips': instance.tips,
    };
