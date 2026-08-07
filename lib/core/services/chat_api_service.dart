import '../network/api_client.dart';
import '../network/models/chat_request.dart';
import '../network/models/chat_response.dart';

class ChatApiService {
  final ApiClient _api;
  ChatApiService(this._api);
  Future<ChatResponse> sendMessage(ChatRequest request) {
    return _api.post('/chat', data: request.toJson(), parser: (json) => ChatResponse.fromJson(json as Map<String, dynamic>));
  }
  Future<bool> checkHealth() {
    return _api.get('/health', parser: (_) => true);
  }
}
