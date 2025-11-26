import 'package:equatable/equatable.dart';

class Category extends Equatable {
  final String id;
  final String nameVi;
  final String? nameEn;
  final String slug;
  final String? descriptionVi;
  final String? descriptionEn;
  final String? iconUrl;
  final int displayOrder;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Category({
    required this.id,
    required this.nameVi,
    this.nameEn,
    required this.slug,
    this.descriptionVi,
    this.descriptionEn,
    this.iconUrl,
    required this.displayOrder,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
  });

  String get displayName => nameVi;

  @override
  List<Object?> get props => [
        id,
        nameVi,
        nameEn,
        slug,
        descriptionVi,
        descriptionEn,
        iconUrl,
        displayOrder,
        isActive,
        createdAt,
        updatedAt,
      ];
}
