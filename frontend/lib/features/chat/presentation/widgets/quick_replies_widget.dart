import 'package:flutter/material.dart';
import '../models/chat_message.dart';

class QuickRepliesWidget extends StatelessWidget {
  final List<QuickReply> replies;
  final Function(String) onReplySelected;

  const QuickRepliesWidget({
    super.key,
    required this.replies,
    required this.onReplySelected,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      margin: const EdgeInsets.only(top: 8),
      child: Wrap(
        spacing: 8,
        runSpacing: 8,
        children: replies.map((reply) {
          return ActionChip(
            label: Text(reply.text),
            onPressed: () => onReplySelected(reply.value),
            backgroundColor: theme.colorScheme.primaryContainer,
            labelStyle: TextStyle(
              color: theme.colorScheme.onPrimaryContainer,
            ),
            side: BorderSide.none,
          );
        }).toList(),
      ),
    );
  }
}