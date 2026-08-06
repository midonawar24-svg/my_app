import 'package:flutter/foundation.dart';

@immutable
class Conversation {
  final String id;
  final String title;
  final int messageCount;
  final DateTime createdAt;
  final DateTime lastMessageAt;
  final bool pinned;

  Conversation({
    required this.id,
    required this.title,
    this.messageCount = 0,
    DateTime? createdAt,
    DateTime? lastMessageAt,
    this.pinned = false,
  })  : createdAt = createdAt ?? DateTime.now(),
        lastMessageAt = lastMessageAt ?? DateTime.now();

  Conversation copyWith({
    String? title,
    int? messageCount,
    DateTime? lastMessageAt,
    bool? pinned,
  }) {
    return Conversation(
      id: id,
      title: title ?? this.title,
      messageCount: messageCount ?? this.messageCount,
      createdAt: createdAt,
      lastMessageAt: lastMessageAt ?? this.lastMessageAt,
      pinned: pinned ?? this.pinned,
    );
  }
}
