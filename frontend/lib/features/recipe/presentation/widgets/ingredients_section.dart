import 'package:flutter/material.dart';
import '../../domain/entities/recipe_ingredient.dart';

class IngredientsSection extends StatefulWidget {
  final List<RecipeIngredient> ingredients;
  final int servings;

  const IngredientsSection({
    super.key,
    required this.ingredients,
    required this.servings,
  });

  @override
  State<IngredientsSection> createState() => _IngredientsSectionState();
}

class _IngredientsSectionState extends State<IngredientsSection> {
  late int _currentServings;
  final Set<int> _checkedIngredients = {};

  @override
  void initState() {
    super.initState();
    _currentServings = widget.servings;
  }

  double _getScaledQuantity(double originalQuantity) {
    return originalQuantity * _currentServings / widget.servings;
  }

  @override
  Widget build(BuildContext context) {
    if (widget.ingredients.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(32.0),
          child: Text('Chưa có thông tin nguyên liệu'),
        ),
      );
    }

    return Column(
      children: [
        // Servings Adjuster
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.grey[100],
            border: Border(
              bottom: BorderSide(color: Colors.grey[300]!),
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Khẩu phần:',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(width: 16),
              IconButton(
                onPressed: _currentServings > 1
                    ? () {
                        setState(() {
                          _currentServings--;
                        });
                      }
                    : null,
                icon: const Icon(Icons.remove_circle_outline),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  '$_currentServings',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              IconButton(
                onPressed: () {
                  setState(() {
                    _currentServings++;
                  });
                },
                icon: const Icon(Icons.add_circle_outline),
              ),
            ],
          ),
        ),

        // Ingredients List
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: widget.ingredients.length,
            itemBuilder: (context, index) {
              final ingredient = widget.ingredients[index];
              final isChecked = _checkedIngredients.contains(index);
              final scaledQuantity = _getScaledQuantity(ingredient.quantity);

              return CheckboxListTile(
                value: isChecked,
                onChanged: (value) {
                  setState(() {
                    if (value == true) {
                      _checkedIngredients.add(index);
                    } else {
                      _checkedIngredients.remove(index);
                    }
                  });
                },
                title: Text(
                  ingredient.nameVi,
                  style: TextStyle(
                    decoration: isChecked
                        ? TextDecoration.lineThrough
                        : TextDecoration.none,
                    color: isChecked ? Colors.grey : Colors.black,
                  ),
                ),
                subtitle: Text(
                  '${scaledQuantity.toStringAsFixed(1)} ${ingredient.unit}',
                  style: TextStyle(
                    color: isChecked ? Colors.grey : Colors.grey[600],
                  ),
                ),
                secondary: ingredient.isOptional
                    ? Chip(
                        label: const Text(
                          'Tùy chọn',
                          style: TextStyle(fontSize: 10),
                        ),
                        backgroundColor: Colors.orange[100],
                        labelPadding: const EdgeInsets.symmetric(horizontal: 4),
                      )
                    : null,
              );
            },
          ),
        ),
      ],
    );
  }
}
