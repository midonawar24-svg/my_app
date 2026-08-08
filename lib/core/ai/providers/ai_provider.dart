abstract class AiProvider {
  Future<String> generateReply({
    required String message,
    required String conversationId,
    bool shouldRemember = false,
    double confidence = 0.0,
    String memoryType = 'knowledge',
    Map<String, dynamic>? context,
  });
}
