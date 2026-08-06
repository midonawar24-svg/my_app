class ConversationException implements Exception {
  final String message;
  const ConversationException(this.message);
  @override
  String toString() => 'ConversationException: $message';
}

class ConversationNotFoundException extends ConversationException {
  const ConversationNotFoundException(String id) : super('Conversation $id not found');
}

/// Reserved for future persistence failures (e.g. Drift/SQLite).
class ConversationCreationException extends ConversationException {
  const ConversationCreationException([String? detail]) : super(detail?? 'Failed to create conversation');
}
