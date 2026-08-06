import 'package:flutter/material.dart';
import '../../../app/dependency_injection.dart';
import '../../../core/conversation/conversation_manager.dart';
import '../../../core/ai/memory/memory_engine.dart';
import '../../../core/ai/memory/memory.dart';
import '../../../core/services/chat_service.dart';
import 'widgets/chat_drawer.dart';
import 'widgets/message_bubble.dart';
import 'widgets/input_bar.dart';
import 'widgets/welcome_view.dart';
class ChatPage extends StatefulWidget { const ChatPage({super.key}); @override State<ChatPage> createState() => _ChatPageState(); }
class _ChatPageState extends State<ChatPage> {
  final _m = getIt<ConversationManager>();
  final _mem = getIt<MemoryEngine>();
  final _chat = getIt<ChatService>();
  final _ctrl = TextEditingController();
  List<Memory> _msgs = [];
  @override
  void initState() { super.initState(); _m.currentConversationId.addListener(_onConversationChanged); _mem.lastUpdatedConversationId.addListener(_onMemoryChanged); _m.version.addListener(_onConversationListChanged); _load(); }
  @override
  void dispose() { _m.currentConversationId.removeListener(_onConversationChanged); _mem.lastUpdatedConversationId.removeListener(_onMemoryChanged); _m.version.removeListener(_onConversationListChanged); _ctrl.dispose(); super.dispose(); }
  void _onConversationChanged() => _load();
  void _onConversationListChanged() { if (mounted) setState(() {}); }
  void _onMemoryChanged() {
    final updatedId = _mem.lastUpdatedConversationId.value;
    final currentId = _m.currentConversationId.value;
    if (updatedId!= null && updatedId == currentId) { _load(); }
  }
  Future<void> _load() async { final id = _m.currentConversationId.value; if (id == null) { if (mounted) setState(() => _msgs = []); return; } final ms = await _mem.getByConversation(id); if (mounted) setState(() => _msgs = ms); }
  Future<void> _send() async {
    final t = _ctrl.text.trim(); if (t.isEmpty) return; _ctrl.clear();
    try { final currentId = _m.currentConversationId.value; if (currentId == null) { await _chat.sendFirstMessage(t); } else { await _chat.sendMessage(currentId, t); } } catch (e) { if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('فشل: $e'))); }
  }
  @override
  Widget build(BuildContext c) => Scaffold(appBar: AppBar(title: const Text('AI Core OS'), actions: [IconButton(icon: const Icon(Icons.add), onPressed: () => _m.newChat())]), drawer: const ChatDrawer(), body: Column(children: [Expanded(child: _msgs.isEmpty? const WelcomeView() : ListView.builder(padding: const EdgeInsets.symmetric(vertical: 8), itemCount: _msgs.length, itemBuilder: (c, i) => MessageBubble(text: _msgs[i].content, isUser: true))), InputBar(controller: _ctrl, onSend: _send)]));
}
