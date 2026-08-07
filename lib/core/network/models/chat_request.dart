class ChatRequest {
  final String message;
  final String? conversationId;
  ChatRequest({required this.message, this.conversationId});
  
  Map<String, dynamic> toJson() {
    return {
      'message': message,
      if (conversationId != null) 'conversation_id': conversationId, // الأساس لـ FastAPI
      if (conversationId != null) 'conversationId': conversationId, // توافق مع backends أخرى
    };
  }
}
