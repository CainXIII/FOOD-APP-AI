import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/chat_message.dart';
import '../providers/chat_provider.dart';
import 'recipe_card_widget.dart';
import 'quick_replies_widget.dart';

class MessageBubble extends ConsumerStatefulWidget {
  final ChatMessage message;

  const MessageBubble({
    super.key,
    required this.message,
  });

  @override
  ConsumerState<MessageBubble> createState() => _MessageBubbleState();
}

class _MessageBubbleState extends ConsumerState<MessageBubble> {
  bool _showActions = false;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isUser = widget.message.isUser;

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Stack(
        children: [
          Row(
            mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // AI avatar (left side)
              if (!isUser) ...[
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        theme.colorScheme.primary,
                        theme.colorScheme.secondary,
                      ],
                    ),
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.smart_toy, color: Colors.white, size: 18),
                ),
                const SizedBox(width: 8),
              ],

              // Message bubble
              Flexible(
                child: GestureDetector(
                  onLongPress: () => setState(() => _showActions = !_showActions),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: widget.message.status == MessageStatus.failed
                          ? theme.colorScheme.errorContainer
                          : isUser
                              ? theme.colorScheme.primary
                              : theme.colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.only(
                        topLeft: Radius.circular(isUser ? 20 : 4),
                        topRight: Radius.circular(isUser ? 4 : 20),
                        bottomLeft: const Radius.circular(20),
                        bottomRight: const Radius.circular(20),
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.05),
                          blurRadius: 5,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Message content based on type
                        _buildMessageContent(context),

                        const SizedBox(height: 4),
                        Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              _formatTimestamp(widget.message.timestamp),
                              style: theme.textTheme.bodySmall?.copyWith(
                                color: widget.message.status == MessageStatus.failed
                                    ? theme.colorScheme.onErrorContainer.withOpacity(0.7)
                                    : isUser ? Colors.white70 : Colors.grey[600],
                                fontSize: 11,
                              ),
                            ),
                            if (isUser && widget.message.status != MessageStatus.sending) ...[
                              const SizedBox(width: 4),
                              Icon(
                                _getStatusIcon(widget.message.status),
                                size: 12,
                                color: widget.message.status == MessageStatus.failed
                                    ? theme.colorScheme.error
                                    : isUser ? Colors.white70 : Colors.grey[600],
                              ),
                            ],
                          ],
                        ),
                        if (widget.message.error != null) ...[
                          const SizedBox(height: 4),
                          Text(
                            widget.message.error!,
                            style: theme.textTheme.bodySmall?.copyWith(
                              color: theme.colorScheme.error,
                              fontSize: 11,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),

              // User avatar (right side)
              if (isUser) ...[
                const SizedBox(width: 8),
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primaryContainer,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.person,
                    color: theme.colorScheme.onPrimaryContainer,
                    size: 18,
                  ),
                ),
              ],
            ],
          ),
          _buildActionButtons(),
        ],
      ),
    );
  }

  Widget _buildActionButtons() {
    if (!_showActions) return const SizedBox.shrink();

    return Positioned(
      right: widget.message.isUser ? 50 : 0,
      left: widget.message.isUser ? 0 : 50,
      bottom: 0,
      child: Container(
        margin: const EdgeInsets.only(top: 8),
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surface,
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 8,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.copy, size: 18),
              onPressed: _copyMessage,
              tooltip: 'Sao chép',
            ),
            if (widget.message.status == MessageStatus.failed) ...[
              IconButton(
                icon: const Icon(Icons.refresh, size: 18),
                onPressed: _retryMessage,
                tooltip: 'Thử lại',
              ),
            ],
            IconButton(
              icon: const Icon(Icons.delete, size: 18),
              onPressed: _deleteMessage,
              tooltip: 'Xóa',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMessageContent(BuildContext context) {
    final theme = Theme.of(context);
    final content = widget.message.content;
    final textColor = widget.message.status == MessageStatus.failed
        ? theme.colorScheme.onErrorContainer
        : widget.message.isUser ? Colors.white : Colors.black87;

    switch (content.type) {
      case MessageType.text:
        return Text(
          content.text ?? '',
          style: theme.textTheme.bodyMedium?.copyWith(
            color: textColor,
            height: 1.4,
          ),
        );

      case MessageType.recipe:
        if (content.recipe != null) {
          return RecipeCardWidget(
            recipe: content.recipe!,
            onTap: () {
              // TODO: Navigate to recipe detail
            },
          );
        }
        return const SizedBox.shrink();

      case MessageType.image:
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (content.imageUrl != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: CachedNetworkImage(
                  imageUrl: content.imageUrl!,
                  height: 200,
                  width: 250,
                  fit: BoxFit.cover,
                  placeholder: (context, url) => Container(
                    height: 200,
                    width: 250,
                    color: theme.colorScheme.surfaceContainerHighest,
                    child: const Center(child: CircularProgressIndicator()),
                  ),
                  errorWidget: (context, url, error) => Container(
                    height: 200,
                    width: 250,
                    color: theme.colorScheme.surfaceContainerHighest,
                    child: Icon(
                      Icons.image_not_supported,
                      color: theme.colorScheme.onSurfaceVariant,
                    ),
                  ),
                ),
              ),
            if (content.text != null && content.text!.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                content.text!,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: textColor,
                  height: 1.4,
                ),
              ),
            ],
          ],
        );

      case MessageType.audio:
        return Row(
          children: [
            IconButton(
              icon: const Icon(Icons.play_arrow),
              onPressed: () {
                // TODO: Play audio
              },
              color: textColor,
            ),
            Expanded(
              child: Text(
                content.text ?? 'Audio message',
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: textColor,
                  height: 1.4,
                ),
              ),
            ),
          ],
        );

      case MessageType.quickReplies:
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (content.text != null && content.text!.isNotEmpty)
              Text(
                content.text!,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: textColor,
                  height: 1.4,
                ),
              ),
            if (content.quickReplies != null)
              QuickRepliesWidget(
                replies: content.quickReplies!,
                onReplySelected: (value) {
                  // TODO: Handle quick reply selection
                },
              ),
          ],
        );
    }
  }

  IconData _getStatusIcon(MessageStatus status) {
    switch (status) {
      case MessageStatus.sending:
        return Icons.access_time;
      case MessageStatus.sent:
        return Icons.check;
      case MessageStatus.delivered:
        return Icons.done_all;
      case MessageStatus.read:
        return Icons.done_all;
      case MessageStatus.failed:
        return Icons.error;
    }
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inMinutes < 1) {
      return 'Vừa xong';
    } else if (difference.inHours < 1) {
      return '${difference.inMinutes} phút trước';
    } else if (difference.inDays < 1) {
      return DateFormat('HH:mm').format(timestamp);
    } else {
      return DateFormat('dd/MM HH:mm').format(timestamp);
    }
  }

  void _copyMessage() {
    Clipboard.setData(ClipboardData(text: widget.message.text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Đã sao chép tin nhắn')),
    );
    setState(() => _showActions = false);
  }

  void _retryMessage() {
    ref.read(chatNotifierProvider.notifier).retryMessage(widget.message.id);
    setState(() => _showActions = false);
  }

  void _deleteMessage() {
    // TODO: Implement delete functionality
    setState(() => _showActions = false);
  }
}
