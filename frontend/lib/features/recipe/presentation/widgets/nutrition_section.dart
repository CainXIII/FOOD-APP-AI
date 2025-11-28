import 'package:flutter/material.dart';
import '../../domain/entities/nutrition_fact.dart';

class NutritionSection extends StatelessWidget {
  final NutritionFact? nutrition;
  final int servings;

  const NutritionSection({
    super.key,
    required this.nutrition,
    required this.servings,
  });

  @override
  Widget build(BuildContext context) {
    if (nutrition == null) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(32.0),
          child: Text('Chưa có thông tin dinh dưỡng'),
        ),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Per Serving Note
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.blue[50],
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                const Icon(Icons.info_outline, color: Colors.blue),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Giá trị dinh dưỡng cho 1 khẩu phần (tổng $servings phần)',
                    style: const TextStyle(
                      color: Colors.blue,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Macronutrients
          _SectionTitle(title: 'Chất dinh dưỡng chính'),
          const SizedBox(height: 12),
          _NutrientCard(
            icon: Icons.local_fire_department,
            color: Colors.orange,
            label: 'Calories',
            value: '${nutrition!.caloriesPerServing?.toStringAsFixed(0) ?? "N/A"}',
            unit: 'kcal',
          ),
          _NutrientCard(
            icon: Icons.rice_bowl,
            color: Colors.brown,
            label: 'Carbohydrates',
            value: '${nutrition!.totalCarbohydrates?.toStringAsFixed(1) ?? "N/A"}',
            unit: 'g',
          ),
          _NutrientCard(
            icon: Icons.egg,
            color: Colors.red,
            label: 'Protein',
            value: '${nutrition!.protein?.toStringAsFixed(1) ?? "N/A"}',
            unit: 'g',
          ),
          _NutrientCard(
            icon: Icons.water_drop,
            color: Colors.yellow[700]!,
            label: 'Tổng chất béo',
            value: '${nutrition!.totalFat?.toStringAsFixed(1) ?? "N/A"}',
            unit: 'g',
          ),

          const SizedBox(height: 24),

          // Fats Breakdown
          if (nutrition!.saturatedFat != null ||
              nutrition!.transFat != null ||
              nutrition!.polyunsaturatedFat != null ||
              nutrition!.monounsaturatedFat != null) ...[
            _SectionTitle(title: 'Chất béo chi tiết'),
            const SizedBox(height: 12),
            if (nutrition!.saturatedFat != null)
              _NutrientRow(
                label: 'Chất béo bão hòa',
                value: '${nutrition!.saturatedFat!.toStringAsFixed(1)} g',
              ),
            if (nutrition!.transFat != null)
              _NutrientRow(
                label: 'Chất béo chuyển hóa',
                value: '${nutrition!.transFat!.toStringAsFixed(1)} g',
              ),
            if (nutrition!.polyunsaturatedFat != null)
              _NutrientRow(
                label: 'Chất béo không bão hòa đa',
                value: '${nutrition!.polyunsaturatedFat!.toStringAsFixed(1)} g',
              ),
            if (nutrition!.monounsaturatedFat != null)
              _NutrientRow(
                label: 'Chất béo không bão hòa đơn',
                value: '${nutrition!.monounsaturatedFat!.toStringAsFixed(1)} g',
              ),
            const SizedBox(height: 24),
          ],

          // Other Nutrients
          _SectionTitle(title: 'Các chất khác'),
          const SizedBox(height: 12),
          if (nutrition!.cholesterol != null)
            _NutrientRow(
              label: 'Cholesterol',
              value: '${nutrition!.cholesterol!.toStringAsFixed(0)} mg',
            ),
          if (nutrition!.sodium != null)
            _NutrientRow(
              label: 'Natri',
              value: '${nutrition!.sodium!.toStringAsFixed(0)} mg',
            ),
          if (nutrition!.dietaryFiber != null)
            _NutrientRow(
              label: 'Chất xơ',
              value: '${nutrition!.dietaryFiber!.toStringAsFixed(1)} g',
            ),
          if (nutrition!.sugars != null)
            _NutrientRow(
              label: 'Đường',
              value: '${nutrition!.sugars!.toStringAsFixed(1)} g',
            ),

          const SizedBox(height: 24),

          // Vitamins & Minerals
          if (nutrition!.vitaminA != null ||
              nutrition!.vitaminC != null ||
              nutrition!.calcium != null ||
              nutrition!.iron != null) ...[
            _SectionTitle(title: 'Vitamin & Khoáng chất'),
            const SizedBox(height: 12),
            if (nutrition!.vitaminA != null)
              _NutrientRow(
                label: 'Vitamin A',
                value: '${nutrition!.vitaminA!.toStringAsFixed(0)} IU',
              ),
            if (nutrition!.vitaminC != null)
              _NutrientRow(
                label: 'Vitamin C',
                value: '${nutrition!.vitaminC!.toStringAsFixed(1)} mg',
              ),
            if (nutrition!.calcium != null)
              _NutrientRow(
                label: 'Canxi',
                value: '${nutrition!.calcium!.toStringAsFixed(0)} mg',
              ),
            if (nutrition!.iron != null)
              _NutrientRow(
                label: 'Sắt',
                value: '${nutrition!.iron!.toStringAsFixed(1)} mg',
              ),
          ],
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;

  const _SectionTitle({required this.title});

  @override
  Widget build(BuildContext context) {
    return Text(
      title,
      style: const TextStyle(
        fontSize: 18,
        fontWeight: FontWeight.bold,
      ),
    );
  }
}

class _NutrientCard extends StatelessWidget {
  final IconData icon;
  final Color color;
  final String label;
  final String value;
  final String unit;

  const _NutrientCard({
    required this.icon,
    required this.color,
    required this.label,
    required this.value,
    required this.unit,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: color, size: 24),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                label,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
            Text(
              value,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(width: 4),
            Text(
              unit,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _NutrientRow extends StatelessWidget {
  final String label;
  final String value;

  const _NutrientRow({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(fontSize: 15),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
