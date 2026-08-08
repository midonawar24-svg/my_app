class ChatRequest {
  final String message;
  final String? conversationId;
  final bool shouldRemember;
  final double confidence;
  final String memoryType;
  final Map<String, dynamic>? context;

  ChatRequest({
    required this.message,
    this.conversationId,
    this.shouldRemember = false,
    this.confidence = 0.0,
    this.memoryType = 'knowledge',
    this.context,
  });

  Map<String, dynamic> toJson() {
    return {
      'message': message,
      if (conversationId != null) 'conversation_id': conversationId,
      if (conversationId != null) 'conversationId': conversationId,
      'should_remember': shouldRemember,
      'confidence': confidence,
      'memory_type': memoryType,
      if (context != null) 'context': context,
    };
  }
}
