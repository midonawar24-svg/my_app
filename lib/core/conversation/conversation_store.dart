import 'conversation.dart';
abstract class ConversationStore { Future<Conversation> save(Conversation c); Future<Conversation?> getById(String id); Future<List<Conversation>> getAll(); Future<void> delete(String id); Future<void> clear(); Future<int> count(); }
