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
  Future<void> initialize() async {
    await _cleanupEmpty();
    await _refresh();
  }
  Future<void> _refresh() async {
    final all = await _store.getAll();
    _cache..clear()..addAll(all);
    _notify();
  }
  Future<void> _cleanupEmpty() async {
    final all = await _store.getAll();
    final now = DateTime.now();
    for (final c in all) {
      if (c.messageCount == 0 && c.title == 'محادثة جديدة' && now.difference(c.createdAt).inHours > 24) {
        await _store.delete(c.id);
      }
    }
  }
  void _notify() {
    final sorted = List<Conversation>.from(_cache);
    sorted.sort((a, b) {
      if (a.pinned!= b.pinned) return a.pinned? -1 : 1;
      return b.lastMessageAt.compareTo(a.lastMessageAt);
    });
    conversationsNotifier.value = List.unmodifiable(sorted);
    version.value++;
  }
  void newChat() => currentConversationId.value = null;
  Future<Conversation> createNew({String? firstMessage}) async {
    final id = _uuid.v4();
    final title = firstMessage!= null && firstMessage.isNotEmpty
       ? (firstMessage.length <= 30? firstMessage : '${firstMessage.substring(0, 30)}...')
        : 'محادثة جديدة';
    final conv = Conversation(id: id, title: title, messageCount: 0);
    await _store.save(conv);
    await _refresh();
    currentConversationId.value = id;
    return conv;
  }
  Future<void> select(String id) async { currentConversationId.value = id; }
  Future<void> rename(String id, String t) async {
    final idx = _cache.indexWhere((c) => c.id == id);
    if (idx!= -1) {
      final updated = _cache[idx].copyWith(title: t);
      await _store.save(updated);
      await _refresh();
    }
  }
  Future<void> touchConversation(String id) async {
    final idx = _cache.indexWhere((c) => c.id == id);
    if (idx!= -1) {
      final updated = _cache[idx].copyWith(lastMessageAt: DateTime.now(), messageCount: _cache[idx].messageCount + 1);
      await _store.save(updated);
      await _refresh();
    }
  }
  Future<void> togglePin(String id) async {
    final idx = _cache.indexWhere((c) => c.id == id);
    if (idx!= -1) {
      final updated = _cache[idx].copyWith(pinned:!_cache[idx].pinned);
      await _store.save(updated);
      await _refresh();
    }
  }
  Future<void> delete(String id) async {
    await _store.delete(id);
    await _refresh();
    if (currentConversationId.value == id) currentConversationId.value = null;
  }
}
