import 'package:equatable/equatable.dart';

/// User entity - domain layer
class User extends Equatable {
  final String id;
  final String email;
  final String username;
  final String? fullName;
  final String? avatarUrl;
  final DateTime createdAt;
  final DateTime? updatedAt;

  const User({
    required this.id,
    required this.email,
    required this.username,
    this.fullName,
    this.avatarUrl,
    required this.createdAt,
    this.updatedAt,
  });

  @override
  List<Object?> get props => [
        id,
        email,
        username,
        fullName,
        avatarUrl,
        createdAt,
        updatedAt,
      ];
}
