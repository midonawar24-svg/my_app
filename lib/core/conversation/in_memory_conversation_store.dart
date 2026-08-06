import 'dart:async';
import 'conversation.dart';
import 'conversation_store.dart';
import 'conversation_exceptions.dart';
import '../ai/memory/utils/async_lock.dart';

class InMemoryConversationStore implements ConversationStore {
  final Map<String, Conversation> _map = {};
  final AsyncLock _lock = AsyncLock();
  static const _txKey = #inTransaction;

  Future<T> _withLock<T>(Future<T> Function() action) {
    if (Zone.current[_txKey] == true) {
      return action();
    }
    return _lock.synchronized(action);
  }

  @override
  Future<T> transaction<T>(Future<T> Function() action) {
    return _lock.synchronized(() {
      return runZoned(() async {
        return await action();
      }, zoneValues: {_txKey: true});
    });
  }

  @override
  Future<List<Conversation>> getAll() => _withLock(() async => _map.values.toList());

  @override
  Future<Conversation?> getById(String id) => _withLock(() async => _map[id]);

  @override
  Future<void> save(Conversation c) => _withLock(() async { _map[c.id] = c; });

  @override
  Future<Conversation> update(String id, Conversation Function(Conversation current) updater) {
    return _withLock(() async {
      final existing = _map[id];
      if (existing == null) throw ConversationNotFoundException(id);
      final updated = updater(existing);
      _map[id] = updated;
      return updated;
    });
  }

  @override
  Future<void> delete(String id) => _withLock(() async { _map.remove(id); });

  @override
  Future<void> clear() => _withLock(() async { _map.clear(); });
}
