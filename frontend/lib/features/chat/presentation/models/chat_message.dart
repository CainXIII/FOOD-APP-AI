enum MessageStatus {
  sending,
  sent,
  delivered,
  read,
  failed,
}

enum MessageType {
  text,
  recipe,
  image,
  audio,
  quickReplies,
}

class RecipeCard {
  final String id;
  final String title;
  final String description;
  final String? imageUrl;
  final int prepTimeMinutes;
  final int cookTimeMinutes;
  final int servings;
  final String difficulty;
  final double rating;

  const RecipeCard({
    required this.id,
    required this.title,
    required this.description,
    this.imageUrl,
    required this.prepTimeMinutes,
    required this.cookTimeMinutes,
    required this.servings,
    required this.difficulty,
    required this.rating,
  });

  factory RecipeCard.fromJson(Map<String, dynamic> json) {
    return RecipeCard(
      id: json['id'],
      title: json['title_vi'] ?? json['title_en'] ?? '',
      description: json['description_vi'] ?? json['description_en'] ?? '',
      imageUrl: json['thumbnail_url'],
      prepTimeMinutes: json['prep_time_minutes'] ?? 0,
      cookTimeMinutes: json['cook_time_minutes'] ?? 0,
      servings: json['servings'] ?? 1,
      difficulty: json['difficulty'] ?? 'medium',
      rating: (json['avg_rating'] ?? 0.0).toDouble(),
    );
  }
}

class QuickReply {
  final String text;
  final String value;

  const QuickReply({
    required this.text,
    required this.value,
  });
}

class MessageContent {
  final MessageType type;
  final String? text;
  final RecipeCard? recipe;
  final String? imageUrl;
  final String? audioUrl;
  final List<QuickReply>? quickReplies;

  const MessageContent({
    required this.type,
    this.text,
    this.recipe,
    this.imageUrl,
    this.audioUrl,
    this.quickReplies,
  });

  factory MessageContent.text(String text) {
    return MessageContent(type: MessageType.text, text: text);
  }

  factory MessageContent.recipe(RecipeCard recipe) {
    return MessageContent(type: MessageType.recipe, recipe: recipe);
  }

  factory MessageContent.image(String imageUrl, {String? text}) {
    return MessageContent(type: MessageType.image, imageUrl: imageUrl, text: text);
  }

  factory MessageContent.audio(String audioUrl, {String? text}) {
    return MessageContent(type: MessageType.audio, audioUrl: audioUrl, text: text);
  }

  factory MessageContent.quickReplies(List<QuickReply> replies, {String? text}) {
    return MessageContent(type: MessageType.quickReplies, quickReplies: replies, text: text);
  }
}

class ChatMessage {
  final String id;
  final MessageContent content;
  final bool isUser;
  final DateTime timestamp;
  final MessageStatus status;
  final String? error;

  const ChatMessage({
    required this.id,
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.status = MessageStatus.sent,
    this.error,
  });

  ChatMessage copyWith({
    String? id,
    MessageContent? content,
    bool? isUser,
    DateTime? timestamp,
    MessageStatus? status,
    String? error,
  }) {
    return ChatMessage(
      id: id ?? this.id,
      content: content ?? this.content,
      isUser: isUser ?? this.isUser,
      timestamp: timestamp ?? this.timestamp,
      status: status ?? this.status,
      error: error ?? this.error,
    );
  }

  // Backward compatibility
  String get text => content.text ?? '';
}
