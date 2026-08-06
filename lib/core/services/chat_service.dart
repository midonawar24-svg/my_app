import 'package:flutter/foundation.dart';
import '../conversation/conversation.dart';
import '../conversation/conversation_manager.dart';
import '../ai/memory/memory_engine.dart';
import '../ai/memory/memory.dart';

class ChatService {
  final ConversationManager _conv;
  final MemoryEngine _mem;

  ChatService({required ConversationManager convManager, required MemoryEngine memoryEngine})
      : _conv = convManager,
        _mem = memoryEngine;

  Future<Conversation> sendFirstMessage(String text) async {
    Conversation? created;
    Memory? savedMemory;
    try {
      debugPrint("SEND FIRST START: $text");
      created = await _conv.createNew(firstMessage: text);
      savedMemory = await _mem.remember(content: text, conversationId: created.id);
      debugPrint("SAVED: ${savedMemory.id}");
      await _conv.touchConversation(created.id);
      debugPrint("TOUCH DONE: ${created.id}");
      return created;
    } catch (e) {
      debugPrint("SEND FIRST FAIL: $e");
      if (savedMemory != null) { try { await _mem.deleteMemory(savedMemory.id); } catch(_){} }
      if (created != null) { try { await _conv.delete(created.id); } catch(_){} }
      rethrow;
    }
  }

  Future<void> sendMessage(String conversationId, String text) async {
    debugPrint("SEND START: $text -> $conversationId");
    Memory? saved;
    try {
      saved = await _mem.remember(content: text, conversationId: conversationId);
      debugPrint("REMEMBER DONE: ${saved.id}");
      await _conv.touchConversation(conversationId);
      debugPrint("TOUCH DONE: $conversationId");
    } catch (e) {
      debugPrint("SEND FAIL: $e");
      if (saved != null) { try { await _mem.deleteMemory(saved.id); } catch(_){} }
      rethrow;
    }
  }

  Future<void> deleteConversation(String id) async {
    await _mem.deleteConversation(id);
    await _conv.delete(id);
  }
}
