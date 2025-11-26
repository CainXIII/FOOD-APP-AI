import 'package:equatable/equatable.dart';

/// Recipe ingredient entity
class RecipeIngredient extends Equatable {
  final String id;
  final String name;
  final String? nameEn;
  final double amount;
  final String unit;
  final String? preparation;
  final bool isOptional;

  const RecipeIngredient({
    required this.id,
    required this.name,
    this.nameEn,
    required this.amount,
    required this.unit,
    this.preparation,
    this.isOptional = false,
  });

  String get displayName => nameEn ?? name;
  
  String get displayAmount {
    if (amount == amount.toInt()) {
      return amount.toInt().toString();
    }
    return amount.toStringAsFixed(1);
  }

  @override
  List<Object?> get props => [id, name, nameEn, amount, unit, preparation, isOptional];
}
