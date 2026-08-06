import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import 'conversation.dart';
import 'conversation_store.dart';
import '../services/logger.dart';

class ConversationManager {
  final ConversationStore _store;
  final Logger _log;
  final Uuid _uuid = const Uuid();
  final List<Conversation> _cache = [];
  final ValueNotifier<List<Conversation>> conversationsNotifier = ValueNotifier([]);
  final ValueNotifier<String?> currentConversationId = ValueNotifier(null);
  final ValueNotifier<int> version = ValueNotifier(0);

  ConversationManager({required ConversationStore store, required Logger logger})
      : _store = store,
        _log = logger;

  Future<void> initialize() async {
    await _cleanupEmpty();
    await _refresh();
  }

  Future<void> _refresh() async {
    try {
      final all = await _store.getAll();
      _cache..clear()..addAll(all);
      _notify();
    } catch (e) {
      _log.error('ConversationManager _refresh failed', e);
      rethrow;
    }
  }

  Future<void> _cleanupEmpty() async {
    await _store.transaction(() async {
      final all = await _store.getAll();
      final now = DateTime.now();
      for (final c in all) {
        if (c.messageCount == 0 && c.title == 'محادثة جديدة' && now.difference(c.createdAt).inHours > 24) {
          await _store.delete(c.id);
        }
      }
    });
  }

  void _bumpVersion() => version.value++;
  void _notify() {
    final sorted = List<Conversation>.from(_cache);
    sorted.sort((a, b) {
      if (a.pinned!= b.pinned) return a.pinned? -1 : 1;
      return b.lastMessageAt.compareTo(a.lastMessageAt);
    });
    conversationsNotifier.value = List.unmodifiable(sorted);
    _bumpVersion();
  }

  /// Manager هو Orchestrator فقط - الـ Store يملك الـ synchronization.
  Future<void> _writeAndRefresh(Future<void> Function() mutation) async {
    await mutation();
    try {
      await _refresh();
    } catch (e) {
      _log.error('writeAndRefresh refresh failed', e);
      rethrow;
    }
  }

  Future<void> _updateConversation(String id, Conversation Function(Conversation) updater) {
    return _writeAndRefresh(() async {
      final updated = await _store.update(id, updater);
      _log.info('Conversation ${updated.id} updated');
    });
  }

  void newChat() => currentConversationId.value = null;
  Future<void> select(String id) async => currentConversationId.value = id;

  Future<Conversation> createNew({String? firstMessage}) async {
    late Conversation created;
    await _writeAndRefresh(() async {
      final id = _uuid.v4();
      final title = firstMessage!= null && firstMessage.isNotEmpty
     ? (firstMessage.length <= 30? firstMessage : '${firstMessage.substring(0, 30)}...')
          : 'محادثة جديدة';
      created = Conversation(id: id, title: title, messageCount: 0);
      await _store.save(created);
      _log.info('Conversation created: ${created.id}');
    });
    currentConversationId.value = created.id;
    return created;
  }

  Future<void> rename(String id, String t) => _updateConversation(id, (c) => c.copyWith(title: t));
  Future<void> touchConversation(String id) => _updateConversation(id, (c) => c.copyWith(messageCount: c.messageCount + 1, lastMessageAt: DateTime.now()));
  Future<void> togglePin(String id) => _updateConversation(id, (c) => c.copyWith(pinned:!c.pinned));

  Future<void> delete(String id) async {
    await _writeAndRefresh(() async {
      await _store.delete(id);
      _log.info('Conversation deleted: $id');
    });
    if (currentConversationId.value == id) currentConversationId.value = null;
  }
}
