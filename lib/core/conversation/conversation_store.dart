import 'conversation.dart';

abstract class ConversationStore {
  Future<List<Conversation>> getAll();
  Future<Conversation?> getById(String id);
  Future<void> save(Conversation conversation);
  Future<void> delete(String id);
  Future<void> clear();
  Future<Conversation> update(String id, Conversation Function(Conversation current) updater);
  Future<T> transaction<T>(Future<T> Function() action);
}
