import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import 'memory.dart';
import 'memory_repository.dart';

class MemoryEngine {
  final MemoryRepository _repo;
  final Uuid _uuid = const Uuid();
  final ValueNotifier<MemoryStats> statsNotifier = ValueNotifier(MemoryStats.empty());
  final ValueNotifier<int> _ver = ValueNotifier(0);
  final ValueNotifier<String?> lastUpdatedConversationId = ValueNotifier(null);
  ValueNotifier<int> get version => _ver;

  MemoryEngine({required MemoryRepository repository}) : _repo = repository;

  Future<void> initialize() async { await _refresh(); }

  Future<void> _refresh() async {
    statsNotifier.value = MemoryStats(total: await _repo.count(), lastUpdate: DateTime.now());
    _ver.value++;
  }

  Future<Memory> remember({required String content, required String conversationId, Map<String, dynamic> metadata = const {}}) async {
    final id = _uuid.v4();
    final m = Memory(id: id, content: content, conversationId: conversationId, metadata: metadata);
    final r = await _repo.save(m);
    debugPrint("SAVED: $conversationId -> $id");
    // FIX: force notify even if same conversationId
    lastUpdatedConversationId.value = null;
    lastUpdatedConversationId.value = conversationId;
    await _refresh();
    return r;
  }

  Future<void> deleteMemory(String id) async { await _repo.delete(id); await _refresh(); }
  Future<void> deleteConversation(String cid) async { await _repo.deleteConversation(cid); await _refresh(); }
  Future<List<Memory>> getByConversation(String cid) => _repo.getByConversation(cid);
  Future<List<Memory>> searchInConversation(String cid, String q) => _repo.searchInConversation(cid, q);
  Future<List<Memory>> getAll() => _repo.getAll();
  Future<List<Memory>> search(String q) => _repo.search(q);
}
