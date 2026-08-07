class ChatResponse {
  final String reply;
  final String? conversationId;
  ChatResponse({required this.reply, this.conversationId});
  
  factory ChatResponse.fromJson(Map<String, dynamic> json) {
    final dynamic raw = json['reply'] ?? json['message'] ?? json['response'] ?? json['text'] ?? json['data'] ?? '';
    String text;
    if (raw is String) {
      text = raw;
    } else if (raw is Map && raw['content'] != null) {
      text = raw['content'].toString();
    } else {
      text = raw.toString();
    }
    return ChatResponse(
      reply: text,
      conversationId: json['conversation_id'] as String? ?? json['conversationId'] as String? ?? json['id'] as String?,
    );
  }
}
