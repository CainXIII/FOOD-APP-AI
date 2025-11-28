import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/chat_message.dart';

class SmartSuggestion {
  final String text;
  final String category;
  final double confidence;

  const SmartSuggestion({
    required this.text,
    required this.category,
    required this.confidence,
  });
}

class SmartSuggestionsState {
  final List<SmartSuggestion> suggestions;
  final bool isLoading;

  const SmartSuggestionsState({
    this.suggestions = const [],
    this.isLoading = false,
  });

  SmartSuggestionsState copyWith({
    List<SmartSuggestion>? suggestions,
    bool? isLoading,
  }) {
    return SmartSuggestionsState(
      suggestions: suggestions ?? this.suggestions,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}

class SmartSuggestionsNotifier extends StateNotifier<SmartSuggestionsState> {
  SmartSuggestionsNotifier() : super(const SmartSuggestionsState());

  void analyzeConversation(List<ChatMessage> messages) {
    state = state.copyWith(isLoading: true);

    final suggestions = <SmartSuggestion>[];

    if (messages.isEmpty) {
      // Default suggestions for new conversations
      suggestions.addAll([
        SmartSuggestion(
          text: 'Hãy giới thiệu về bạn',
          category: 'general',
          confidence: 0.9,
        ),
        SmartSuggestion(
          text: 'Công thức nấu ăn nào phổ biến nhất?',
          category: 'recipes',
          confidence: 0.8,
        ),
        SmartSuggestion(
          text: 'Món ăn Việt Nam',
          category: 'cuisine',
          confidence: 0.7,
        ),
      ]);
    } else {
      // Analyze conversation history
      final userMessages = messages.where((msg) => msg.isUser).toList();
      final aiMessages = messages.where((msg) => !msg.isUser).toList();

      // Extract keywords and topics from conversation
      final topics = _extractTopics(userMessages, aiMessages);

      // Generate context-aware suggestions
      suggestions.addAll(_generateSuggestions(topics, userMessages.length));
    }

    // Sort by confidence
    suggestions.sort((a, b) => b.confidence.compareTo(a.confidence));

    state = state.copyWith(
      suggestions: suggestions.take(5).toList(), // Limit to top 5
      isLoading: false,
    );
  }

  List<String> _extractTopics(List<ChatMessage> userMessages, List<ChatMessage> aiMessages) {
    final topics = <String>[];

    // Keywords that indicate different topics
    final topicKeywords = {
      'chicken': ['gà', 'chicken', 'ga'],
      'beef': ['bò', 'beef', 'bo'],
      'pork': ['heo', 'pork', 'thịt heo'],
      'fish': ['cá', 'fish', 'ca'],
      'vegetarian': ['chay', 'vegetarian', 'rau'],
      'soup': ['canh', 'soup', 'pho', 'phở'],
      'rice': ['com', 'rice', 'cơm'],
      'noodles': ['mi', 'noodles', 'bún', 'bun'],
      'stir_fry': ['xào', 'stir fry', 'xao'],
      'grill': ['nướng', 'grill', 'nuong'],
      'vietnamese': ['việt nam', 'vietnamese', 'viet nam'],
      'asian': ['châu á', 'asian', 'chau a'],
      'italian': ['italia', 'italian', 'ý'],
      'quick': ['nhanh', 'quick', 'fast'],
      'easy': ['dễ', 'easy', 'simple'],
    };

    final allText = [...userMessages, ...aiMessages]
        .map((msg) => msg.content.text ?? '')
        .join(' ')
        .toLowerCase();

    for (final entry in topicKeywords.entries) {
      for (final keyword in entry.value) {
        if (allText.contains(keyword)) {
          topics.add(entry.key);
          break;
        }
      }
    }

    return topics;
  }

  List<SmartSuggestion> _generateSuggestions(List<String> topics, int messageCount) {
    final suggestions = <SmartSuggestion>[];

    // Base suggestions based on conversation length
    if (messageCount < 3) {
      suggestions.add(SmartSuggestion(
        text: 'Bạn có thể nấu món gì với nguyên liệu tôi có?',
        category: 'ingredients',
        confidence: 0.8,
      ));
    }

    // Topic-specific suggestions
    // TODO: Replace with API-driven suggestions from /search/suggestions endpoint
    for (final topic in topics) {
      switch (topic) {
        case 'chicken':
          suggestions.addAll([
            SmartSuggestion(
              text: 'Món gà khác',
              category: 'recipes',
              confidence: 0.9,
            ),
            SmartSuggestion(
              text: 'Cách ướp gà',
              category: 'tips',
              confidence: 0.8,
            ),
          ]);
          break;

        case 'vietnamese':
          suggestions.addAll([
            SmartSuggestion(
              text: 'Món Việt khác',
              category: 'recipes',
              confidence: 0.9,
            ),
            SmartSuggestion(
              text: 'Gia vị Việt Nam',
              category: 'ingredients',
              confidence: 0.8,
            ),
          ]);
          break;

        case 'vegetarian':
          suggestions.addAll([
            SmartSuggestion(
              text: 'Món chay khác',
              category: 'recipes',
              confidence: 0.9,
            ),
            SmartSuggestion(
              text: 'Thay thế protein',
              category: 'tips',
              confidence: 0.8,
            ),
          ]);
          break;

        case 'quick':
          suggestions.addAll([
            SmartSuggestion(
              text: 'Món nhanh 30 phút',
              category: 'time',
              confidence: 0.9,
            ),
            SmartSuggestion(
              text: 'Mẹo nấu nhanh',
              category: 'tips',
              confidence: 0.8,
            ),
          ]);
          break;
      }
    }

    // General follow-up suggestions
    if (messageCount > 5) {
      suggestions.addAll([
        SmartSuggestion(
          text: 'Món tráng miệng',
          category: 'dessert',
          confidence: 0.6,
        ),
        SmartSuggestion(
          text: 'Cách bảo quản thực phẩm',
          category: 'storage',
          confidence: 0.5,
        ),
        SmartSuggestion(
          text: 'Món ăn healthy',
          category: 'health',
          confidence: 0.5,
        ),
      ]);
    }

    return suggestions;
  }

  void clearSuggestions() {
    state = const SmartSuggestionsState();
  }
}

final smartSuggestionsProvider = StateNotifierProvider<SmartSuggestionsNotifier, SmartSuggestionsState>((ref) {
  return SmartSuggestionsNotifier();
});