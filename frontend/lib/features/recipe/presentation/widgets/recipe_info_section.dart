import 'package:flutter/material.dart';
import '../../domain/entities/recipe.dart';

class RecipeInfoSection extends StatelessWidget {
  final Recipe recipe;

  const RecipeInfoSection({
    super.key,
    required this.recipe,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Description
          Text(
            recipe.descriptionVi,
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          const SizedBox(height: 16),

          // Info Cards
          Row(
            children: [
              Expanded(
                child: _InfoCard(
                  icon: Icons.schedule,
                  label: 'Chuẩn bị',
                  value: '${recipe.prepTime} phút',
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _InfoCard(
                  icon: Icons.timer,
                  label: 'Nấu',
                  value: '${recipe.cookTime} phút',
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _InfoCard(
                  icon: Icons.people,
                  label: 'Khẩu phần',
                  value: '${recipe.servings}',
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Difficulty and Tags
          Row(
            children: [
              _DifficultyChip(difficulty: recipe.difficulty),
              const SizedBox(width: 8),
              if (recipe.isVegetarian ?? false)
                const Chip(
                  label: Text('Chay', style: TextStyle(fontSize: 12)),
                  backgroundColor: Colors.green,
                  labelStyle: TextStyle(color: Colors.white),
                ),
              if (recipe.isVegan ?? false) ...[
                const SizedBox(width: 8),
                const Chip(
                  label: Text('Thuần chay', style: TextStyle(fontSize: 12)),
                  backgroundColor: Colors.green,
                  labelStyle: TextStyle(color: Colors.white),
                ),
              ],
            ],
          ),
          const SizedBox(height: 16),

          // Rating
          if (recipe.averageRating != null && recipe.averageRating! > 0) ...[
            Row(
              children: [
                const Icon(Icons.star, color: Colors.amber, size: 24),
                const SizedBox(width: 8),
                Text(
                  recipe.averageRating!.toStringAsFixed(1),
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  '(${recipe.totalRatings ?? 0} đánh giá)',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontSize: 14,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
          ],

          // Author
          Row(
            children: [
              CircleAvatar(
                radius: 20,
                backgroundImage: recipe.authorAvatar != null
                    ? NetworkImage(recipe.authorAvatar!)
                    : null,
                child: recipe.authorAvatar == null
                    ? const Icon(Icons.person)
                    : null,
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Tác giả',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                  ),
                  Text(
                    recipe.authorName,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _InfoCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _InfoCard({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).primaryColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Icon(icon, color: Theme.of(context).primaryColor),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey[600],
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}

class _DifficultyChip extends StatelessWidget {
  final String difficulty;

  const _DifficultyChip({required this.difficulty});

  @override
  Widget build(BuildContext context) {
    Color getColor() {
      switch (difficulty.toLowerCase()) {
        case 'easy':
          return Colors.green;
        case 'medium':
          return Colors.orange;
        case 'hard':
          return Colors.red;
        default:
          return Colors.grey;
      }
    }

    String getLabel() {
      switch (difficulty.toLowerCase()) {
        case 'easy':
          return 'Dễ';
        case 'medium':
          return 'Trung bình';
        case 'hard':
          return 'Khó';
        default:
          return difficulty;
      }
    }

    return Chip(
      label: Text(
        getLabel(),
        style: const TextStyle(color: Colors.white, fontSize: 12),
      ),
      backgroundColor: getColor(),
    );
  }
}
