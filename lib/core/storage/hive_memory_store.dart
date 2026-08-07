import 'package:hive/hive.dart';
import '../ai/memory/memory.dart';
import 'memory_store.dart';

class HiveMemoryStore implements MemoryStore {
  static const String _boxName = 'memories';
  static Future<void> init() async {
    if (!Hive.isBoxOpen(_boxName)) await Hive.openBox(_boxName);
  }
  Box get _box => Hive.box(_boxName);

  Map<String, dynamic> _toMap(Memory m) => {
    'id': m.id,
    'content': m.content,
    'conversationId': m.conversationId,
    'metadata': m.metadata,
    'createdAt': m.createdAt.toIso8601String(),
    'lastAccess': m.lastAccess.toIso8601String(),
    'accessCount': m.accessCount,
  };

  Memory _fromMap(Map<dynamic, dynamic> raw) {
    final m = Map<String, dynamic>.from(raw);
    return Memory(
      id: m['id'] as String,
      content: m['content'] as String,
      conversationId: m['conversationId'] as String,
      metadata: Map<String, dynamic>.from(m['metadata'] as Map? ?? {}),
      createdAt: DateTime.parse(m['createdAt'] as String),
      lastAccess: DateTime.parse(m['lastAccess'] as String),
      accessCount: m['accessCount'] as int? ?? 0,
    );
  }

  @override Future<Memory> save(Memory m) async { await _box.put(m.id, _toMap(m)); return m; }
  @override Future<Memory?> getById(String id) async {
    final raw = _box.get(id);
    return raw == null ? null : _fromMap(raw as Map);
  }
  @override Future<List<Memory>> getAll() async => _box.values.map((e) => _fromMap(e as Map)).toList();
  @override Future<List<Memory>> search(String q) async {
    final all = await getAll();
    final lower = q.toLowerCase();
    return all.where((e) => e.content.toLowerCase().contains(lower)).toList();
  }
  @override
  Future<List<Memory>> getByConversation(String cid) async {
    final all = await getAll();
    final list = all.where((e) => e.conversationId == cid).toList();
    list.sort((a, b) => a.createdAt.compareTo(b.createdAt));
    return list;
  }
  @override Future<void> delete(String id) async => await _box.delete(id);
  @override Future<void> deleteConversation(String cid) async {
    final all = _box.toMap();
    for (final entry in all.entries) {
      final map = Map<String, dynamic>.from(entry.value as Map);
      if (map['conversationId'] == cid) await _box.delete(entry.key);
    }
  }
  @override Future<void> clear() async => await _box.clear();
  @override Future<int> count() async => _box.length;
}
