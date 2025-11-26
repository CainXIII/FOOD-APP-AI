import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/smart_suggestions_provider.dart';

class SmartSuggestionsWidget extends ConsumerWidget {
  final Function(String) onSuggestionSelected;

  const SmartSuggestionsWidget({
    super.key,
    required this.onSuggestionSelected,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final suggestionsState = ref.watch(smartSuggestionsProvider);

    if (suggestionsState.suggestions.isEmpty) {
      return const SizedBox.shrink();
    }

    return Container(
      margin: const EdgeInsets.only(top: 8),
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Text(
              'Gợi ý thông minh',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: suggestionsState.suggestions.map((suggestion) {
              return ActionChip(
                label: Text(suggestion.text),
                onPressed: () => onSuggestionSelected(suggestion.text),
                backgroundColor: Theme.of(context).colorScheme.secondaryContainer,
                labelStyle: TextStyle(
                  color: Theme.of(context).colorScheme.onSecondaryContainer,
                ),
                side: BorderSide.none,
                avatar: _getCategoryIcon(suggestion.category),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget? _getCategoryIcon(String category) {
    IconData? icon;
    switch (category) {
      case 'recipes':
        icon = Icons.restaurant;
        break;
      case 'ingredients':
        icon = Icons.kitchen;
        break;
      case 'time':
        icon = Icons.access_time;
        break;
      case 'difficulty':
        icon = Icons.school;
        break;
      case 'cuisine':
        icon = Icons.flag;
        break;
      case 'health':
        icon = Icons.favorite;
        break;
      case 'dessert':
        icon = Icons.cake;
        break;
      case 'storage':
        icon = Icons.inventory;
        break;
      default:
        icon = Icons.lightbulb;
    }

    return Icon(icon, size: 16);
  }
}