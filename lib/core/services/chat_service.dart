import 'package:flutter/foundation.dart';

import '../conversation/conversation.dart';
import '../conversation/conversation_manager.dart';
import '../ai/memory/memory_engine.dart';
import '../ai/memory/memory.dart';
import '../ai/providers/ai_provider.dart';

class ChatService {
  final ConversationManager _conv;
  final MemoryEngine _mem;
  final AiProvider? _provider;

  ChatService({
    required ConversationManager convManager,
    required MemoryEngine memoryEngine,
    AiProvider? provider,
  })  : _conv = convManager,
        _mem = memoryEngine,
        _provider = provider;

  String _fakeReply(String text) {
    final value = text.trim();

    if (value.isEmpty) {
      return 'Fake AI: رسالة فارغة!';
    }

    return "Fake AI: استقبلت '$value'";
  }

  Future<String> _generateReply(
    String text,
    String conversationId,
  ) async {
    if (_provider != null) {
      try {
        final reply = await _provider.generateReply(
          message: text,
          conversationId: conversationId,
        );

        if (reply.trim().isNotEmpty) {
          debugPrint("AI PROVIDER ASSISTANT: $reply");
          return reply;
        }
      } catch (e) {
        debugPrint("AI PROVIDER FAIL -> LOCAL FAKE FALLBACK: $e");
      }
    }

    final fallback = _fakeReply(text);
    debugPrint("LOCAL FAKE ASSISTANT: $fallback");
    return fallback;
  }

  Future<Conversation> sendFirstMessage(String text) async {
    Conversation? created;
    Memory? savedMemory;

    try {
      debugPrint("SEND FIRST START: $text");

      created = await _conv.createNew(firstMessage: text);

      savedMemory = await _mem.remember(
        content: text,
        conversationId: created.id,
        metadata: const {'role': 'user'},
      );

      debugPrint("USER SAVED: ${savedMemory.id}");

      final reply = await _generateReply(text, created.id);

      await _mem.remember(
        content: reply,
        conversationId: created.id,
        metadata: const {'role': 'assistant'},
      );

      debugPrint("ASSISTANT SAVED: $reply");

      await _conv.touchConversation(created.id);

      debugPrint("TOUCH DONE: ${created.id}");

      return created;
    } catch (e) {
      debugPrint("SEND FIRST FAIL: $e");

      if (savedMemory != null) {
        try {
          await _mem.deleteMemory(savedMemory.id);
        } catch (_) {}
      }

      if (created != null) {
        try {
          await _conv.delete(created.id);
        } catch (_) {}
      }

      rethrow;
    }
  }

  Future<void> sendMessage(
    String conversationId,
    String text,
  ) async {
    debugPrint("SEND START: $text -> $conversationId");

    Memory? saved;

    try {
      saved = await _mem.remember(
        content: text,
        conversationId: conversationId,
        metadata: const {'role': 'user'},
      );

      debugPrint("USER SAVED: ${saved.id}");

      final reply = await _generateReply(text, conversationId);

      await _mem.remember(
        content: reply,
        conversationId: conversationId,
        metadata: const {'role': 'assistant'},
      );

      debugPrint("ASSISTANT SAVED: $reply");

      await _conv.touchConversation(conversationId);

      debugPrint("TOUCH DONE: $conversationId");
    } catch (e) {
      debugPrint("SEND FAIL: $e");

      if (saved != null) {
        try {
          await _mem.deleteMemory(saved.id);
        } catch (_) {}
      }

      rethrow;
    }
  }

  Future<void> deleteConversation(String id) async {
    await _mem.deleteConversation(id);
    await _conv.delete(id);
  }
}
