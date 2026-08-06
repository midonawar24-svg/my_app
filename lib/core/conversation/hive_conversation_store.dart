import 'package:hive/hive.dart';
import 'conversation_store.dart';
import 'conversation.dart';

class HiveConversationStore implements ConversationStore {
  static const String _boxName = 'conversations';
  static Future<void> init() async {
    if (!Hive.isBoxOpen(_boxName)) await Hive.openBox(_boxName);
  }
  Box get _box => Hive.box(_boxName);

  Map<String, dynamic> _toMap(Conversation c) => {
    'id': c.id,
    'title': c.title,
    'messageCount': c.messageCount,
    'createdAt': c.createdAt.toIso8601String(),
    'lastMessageAt': c.lastMessageAt.toIso8601String(),
    'pinned': c.pinned,
  };

  Conversation _fromMap(Map<dynamic, dynamic> raw) {
    final m = Map<String, dynamic>.from(raw);
    return Conversation(
      id: m['id'] as String,
      title: m['title'] as String,
      messageCount: m['messageCount'] as int? ?? 0,
      createdAt: DateTime.parse(m['createdAt'] as String),
      lastMessageAt: DateTime.parse(m['lastMessageAt'] as String),
      pinned: m['pinned'] as bool? ?? false,
    );
  }

  @override Future<List<Conversation>> getAll() async => _box.values.map((e) => _fromMap(e as Map)).toList();
  @override Future<Conversation?> getById(String id) async {
    final raw = _box.get(id);
    return raw == null ? null : _fromMap(raw as Map);
  }
  @override Future<void> save(Conversation c) async => await _box.put(c.id, _toMap(c));
  @override Future<void> delete(String id) async => await _box.delete(id);
  @override Future<void> clear() async => await _box.clear();
  @override Future<Conversation> update(String id, Conversation Function(Conversation) updater) async {
    final cur = await getById(id);
    if (cur == null) throw StateError('Conversation $id not found');
    final upd = updater(cur);
    await save(upd);
    return upd;
  }
  @override Future<T> transaction<T>(Future<T> Function() action) async => await action();
}
