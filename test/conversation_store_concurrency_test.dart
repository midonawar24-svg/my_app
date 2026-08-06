import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/core/conversation/conversation.dart';
import 'package:my_app/core/conversation/in_memory_conversation_store.dart';
import 'package:my_app/core/conversation/conversation_manager.dart';
import 'package:my_app/core/services/logger.dart';

void main() {
  late InMemoryConversationStore store;
  late ConversationManager manager;

  setUp(() {
    store = InMemoryConversationStore();
    manager = ConversationManager(store: store, logger: Logger());
  });

  test('No Lost Update - rename + pin parallel', () async {
    final conv = await manager.createNew(firstMessage: 'test');
    await Future.wait([
      manager.rename(conv.id, 'Title A'),
      manager.togglePin(conv.id),
    ]);
    final result = await store.getById(conv.id);
    expect(result, isNotNull);
    expect(result!.title, 'Title A');
    expect(result.pinned, true);
  });

  test('No Deadlock inside transaction() getAll + delete', () async {
    await manager.createNew(firstMessage: 'c1');
    await manager.createNew(firstMessage: 'c2');
    await expectLater(
      store.transaction(() async {
        final all = await store.getAll();
        for (final c in all) {
          await store.delete(c.id);
        }
      }),
      completes,
    );
    expect(await store.getAll(), isEmpty);
  });

  test('Transaction context does not leak to parallel operations', () async {
    final conv = await manager.createNew(firstMessage: 'base');
    final completer = Completer<void>();
    
    final txFuture = store.transaction(() async {
      completer.complete();
      await Future.delayed(Duration(milliseconds: 100));
      await store.update(conv.id, (c) => c.copyWith(title: 'inside_tx'));
    });

    await completer.future;
    final parallelRead = await store.getById(conv.id);
    expect(parallelRead, isNotNull);
    
    await txFuture;
    final after = await store.getById(conv.id);
    expect(after!.title, 'inside_tx');
  });

  test('100 parallel updates - no race', () async {
    final conv = await manager.createNew(firstMessage: 'counter');
    await Future.wait(List.generate(100, (_) => manager.touchConversation(conv.id)));
    final result = await store.getById(conv.id);
    expect(result!.messageCount, 100);
  });

  test('Zone preserves transaction context across await', () async {
    await store.transaction(() async {
      await Future.delayed(Duration(milliseconds: 10));
      final all = await store.getAll();
      expect(all, isNotNull);
    });
  });
}
