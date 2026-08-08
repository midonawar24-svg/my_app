import '../../services/chat_api_service.dart';
import '../../network/models/chat_request.dart';
import 'ai_provider.dart';

class ApiAiProvider implements AiProvider {
  final ChatApiService _api;

  ApiAiProvider(this._api);

  @override
  Future<String> generateReply({
    required String message,
    required String conversationId,
    bool shouldRemember = false,
    double confidence = 0.0,
    String memoryType = 'knowledge',
    Map<String, dynamic>? context,
  }) async {
    final response = await _api.sendMessage(
      ChatRequest(
        message: message,
        conversationId: conversationId,
        shouldRemember: shouldRemember,
        confidence: confidence,
        memoryType: memoryType,
        context: context,
      ),
    );

    return response.reply;
  }
}
