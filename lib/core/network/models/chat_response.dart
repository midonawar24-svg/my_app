class ChatResponse {
  final String reply;
  final String conversationId;
  final String? provider;
  final Map<String, dynamic>? extra;

  const ChatResponse({
    required this.reply,
    required this.conversationId,
    this.provider,
    this.extra,
  });

  factory ChatResponse.fromJson(Map<String, dynamic> json) {
    final extra = Map<String, dynamic>.from(json)
      ..removeWhere(
        (k, _) => {
          'reply',
          'response',
          'conversation_id',
          'conversationId',
          'provider',
        }.contains(k),
      );

    return ChatResponse(
      reply: json['reply'] as String? ?? json['response'] as String? ?? '',
      conversationId:
          json['conversation_id'] as String? ??
          json['conversationId'] as String? ??
          '',
      provider: json['provider'] as String?,
      extra: extra.isEmpty ? null : extra,
    );
  }
}
