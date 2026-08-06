import pathlib, re
print("Starting patch...")

# 1. chat_service.dart
p1 = pathlib.Path("lib/core/services/chat_service.dart")
t = p1.read_text(encoding="utf-8")
if 'SEND START' not in t:
    # نضيف debug في أول sendMessage بدون ما نمسح باقي الكود
    t = t.replace('Future<void> sendMessage', 'Future<void> sendMessage_OLD_DISABLED')
    new_func = '''
Future<void> sendMessage(String conversationId, String text) async {
  debugPrint("SEND START: $text");
  await _mem.remember(content: text, conversationId: conversationId);
  debugPrint("REMEMBER DONE: $conversationId");
  try {
    await _conv.touchConversation(conversationId);
    debugPrint("TOUCH DONE: $conversationId");
  } catch (e) {
    debugPrint("TOUCH SKIP: $e");
  }
}
'''
    # نحطه فوق القديمة
    t = new_func + "\n\n" + t
    p1.write_text(t, encoding="utf-8")
    print("✓ chat_service.dart patched")
else:
    print("= chat_service.dart already patched")

# 2. memory_engine.dart
p2 = pathlib.Path("lib/core/ai/memory/memory_engine.dart")
t = p2.read_text(encoding="utf-8")
if 'SAVED:' not in t:
    t = t.replace('await _repo.save(m);', 'await _repo.save(m);\n  debugPrint("SAVED: $conversationId");')
    t = t.replace('final r = await _repo.save(m);', 'final r = await _repo.save(m);\n  debugPrint("SAVED: $conversationId");')
    # لو مكررش مرتين
    if t.count('SAVED:') > 1:
        # نشيل التكرار
        t = t.replace('  debugPrint("SAVED: $conversationId");\n  debugPrint("SAVED: $conversationId");', '  debugPrint("SAVED: $conversationId");')
    p2.write_text(t, encoding="utf-8")
    print("✓ memory_engine.dart patched")
else:
    print("= memory_engine.dart already patched")

# 3. chat_page.dart
p3 = pathlib.Path("lib/features/chat/presentation/chat_page.dart")
t = p3.read_text(encoding="utf-8")
if 'LOAD START' not in t:
    t = t.replace('final id = _m.currentConversationId.value;', 'final id = _m.currentConversationId.value;\n  debugPrint("LOAD START: conversation=$id");')
    t = t.replace('final ms = await _mem.getByConversation(id);', 'final ms = await _mem.getByConversation(id);\n  debugPrint("LOAD END: conversation=$id, messages=${ms.length}");')
    p3.write_text(t, encoding="utf-8")
    print("✓ chat_page.dart patched")
else:
    print("= chat_page.dart already patched")

print("Done - ready to test")
