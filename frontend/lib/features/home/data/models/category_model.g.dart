// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'category_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CategoryModel _$CategoryModelFromJson(Map<String, dynamic> json) =>
    CategoryModel(
      id: json['id'] as String,
      nameVi: json['nameVi'] as String,
      nameEn: json['nameEn'] as String?,
      slug: json['slug'] as String,
      descriptionVi: json['descriptionVi'] as String?,
      descriptionEn: json['descriptionEn'] as String?,
      iconUrl: json['iconUrl'] as String?,
      displayOrder: (json['displayOrder'] as num).toInt(),
      isActive: json['isActive'] as bool,
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );

Map<String, dynamic> _$CategoryModelToJson(CategoryModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'nameVi': instance.nameVi,
      'nameEn': instance.nameEn,
      'slug': instance.slug,
      'descriptionVi': instance.descriptionVi,
      'descriptionEn': instance.descriptionEn,
      'iconUrl': instance.iconUrl,
      'displayOrder': instance.displayOrder,
      'isActive': instance.isActive,
      'createdAt': instance.createdAt.toIso8601String(),
      'updatedAt': instance.updatedAt.toIso8601String(),
    };
