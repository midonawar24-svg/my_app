import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import 'conversation.dart';
import 'conversation_store.dart';
class ConversationManager {
  final ConversationStore _store;
  final Uuid _uuid = const Uuid();
  final List<Conversation> _cache = [];
  final ValueNotifier<List<Conversation>> conversationsNotifier = ValueNotifier([]);
  final ValueNotifier<String?> currentConversationId = ValueNotifier(null);
  final ValueNotifier<int> version = ValueNotifier(0);
  ConversationManager({required ConversationStore store}) : _store = store;
  Future<void> initialize() async { await _refresh(); }
  Future<void> _refresh() async { final all = await _store.getAll(); _cache..clear()..addAll(all); _notify(); }
  void _notify() { final sorted = List<Conversation>.from(_cache); sorted.sort((a, b) { if (a.pinned!= b.pinned) return a.pinned? -1 : 1; return b.lastMessageAt.compareTo(a.lastMessageAt); }); conversationsNotifier.value = sorted; version.value++; }
  Future<Conversation> createNew({String? firstMessage}) async { final id = _uuid.v4(); final title = firstMessage!= null && firstMessage.isNotEmpty? (firstMessage.length <= 30? firstMessage : '${firstMessage.substring(0, 30)}...') : 'محادثة جديدة'; final conv = Conversation(id: id, title: title); await _store.save(conv); _cache.add(conv); currentConversationId.value = id; _notify(); return conv; }
  Future<void> select(String id) async { currentConversationId.value = id; }
  Future<void> rename(String id, String newTitle) async { final idx = _cache.indexWhere((c) => c.id == id); if (idx!= -1) { final updated = _cache[idx].copyWith(title: newTitle); _cache[idx] = updated; await _store.save(updated); _notify(); } }
  Future<void> touchConversation(String id) async { final idx = _cache.indexWhere((c) => c.id == id); if (idx!= -1) { final c = _cache[idx]; final updated = c.copyWith(lastMessageAt: DateTime.now(), messageCount: c.messageCount + 1); _cache[idx] = updated; await _store.save(updated); _notify(); } }
  Future<void> togglePin(String id) async { final idx = _cache.indexWhere((c) => c.id == id); if (idx!= -1) { final c = _cache[idx]; final updated = c.copyWith(pinned:!c.pinned); _cache[idx] = updated; await _store.save(updated); _notify(); } }
  Future<void> delete(String id) async { await _store.delete(id); _cache.removeWhere((c) => c.id == id); if (currentConversationId.value == id) currentConversationId.value = null; _notify(); }
  Future<void> clearAll() async { await _store.clear(); _cache.clear(); currentConversationId.value = null; _notify(); }
}
