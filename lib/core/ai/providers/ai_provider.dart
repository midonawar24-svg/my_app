abstract class AiProvider {
  Future<String> generateReply({
    required String message,
    required String conversationId,
  });
}
