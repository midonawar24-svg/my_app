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
  }) async {
    final response = await _api.sendMessage(
      ChatRequest(
        message: message,
        conversationId: conversationId,
      ),
    );

    return response.reply;
  }
}
