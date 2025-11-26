// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'recipe_ingredient_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RecipeIngredientModel _$RecipeIngredientModelFromJson(
        Map<String, dynamic> json) =>
    RecipeIngredientModel(
      id: json['id'] as String,
      name: json['name'] as String,
      nameEn: json['name_en'] as String?,
      amount: (json['amount'] as num).toDouble(),
      unit: json['unit'] as String,
      preparation: json['preparation'] as String?,
      isOptional: json['is_optional'] as bool? ?? false,
    );

Map<String, dynamic> _$RecipeIngredientModelToJson(
        RecipeIngredientModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'name_en': instance.nameEn,
      'amount': instance.amount,
      'unit': instance.unit,
      'preparation': instance.preparation,
      'is_optional': instance.isOptional,
    };
