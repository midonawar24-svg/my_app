class ChatRequest {
  final String message;
  final String conversationId;

  const ChatRequest({
    required this.message,
    required this.conversationId,
  });

  Map<String, dynamic> toJson() => {
        'message': message,
        'conversation_id': conversationId,
      };
}
