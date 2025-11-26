import 'package:equatable/equatable.dart';

/// Recipe step entity
class RecipeStep extends Equatable {
  final int stepNumber;
  final String instruction;
  final String? instructionEn;
  final int? duration;
  final String? imageUrl;
  final List<String> tips;

  const RecipeStep({
    required this.stepNumber,
    required this.instruction,
    this.instructionEn,
    this.duration,
    this.imageUrl,
    this.tips = const [],
  });

  String get displayInstruction => instructionEn ?? instruction;
  
  String? get durationDisplay {
    if (duration == null) return null;
    if (duration! < 60) return '$duration phút';
    final hours = duration! ~/ 60;
    final mins = duration! % 60;
    if (mins == 0) return '$hours giờ';
    return '$hours giờ $mins phút';
  }

  @override
  List<Object?> get props => [stepNumber, instruction, instructionEn, duration, imageUrl, tips];
}
