import 'package:flutter/material.dart';
import '../../../app/dependency_injection.dart';
import '../../../core/conversation/conversation_manager.dart';
import '../../../core/kernel/ai_core_kernel.dart';
import '../../../core/ai/memory/memory_engine.dart';
import '../../../core/ai/memory/memory.dart';
import 'widgets/chat_drawer.dart';
import 'widgets/message_bubble.dart';
import 'widgets/input_bar.dart';
import 'widgets/welcome_view.dart';
class ChatPage extends StatefulWidget { const ChatPage({super.key}); @override State<ChatPage> createState() => _ChatPageState(); }
class _ChatPageState extends State<ChatPage> { final _manager = getIt<ConversationManager>(); final _memory = getIt<MemoryEngine>(); final _kernel = getIt<AiCoreKernel>(); final _controller = TextEditingController(); List<Memory> _messages = []; @override void initState() { super.initState(); _manager.currentConversationId.addListener(_load); _manager.version.addListener(_load); _memory.version.addListener(_load); _load(); } Future<void> _load() async { final id = _manager.currentConversationId.value; if (id == null) { if (mounted) setState(() => _messages = []); return; } final msgs = await _memory.getByConversation(id); if (mounted) setState(() => _messages = msgs); } Future<void> _send() async { final text = _controller.text.trim(); if (text.isEmpty) return; _controller.clear(); await _kernel.process(text); await _load(); } @override Widget build(BuildContext context) { return Scaffold(appBar: AppBar(title: const Text('AI Core OS'), actions: [IconButton(icon: const Icon(Icons.add), onPressed: () => _manager.createNew())]), drawer: const ChatDrawer(), body: Column(children: [Expanded(child: _messages.isEmpty ? const WelcomeView() : ListView.builder(padding: const EdgeInsets.symmetric(vertical: 8), itemCount: _messages.length, itemBuilder: (context, i) { final msg = _messages[i]; return MessageBubble(text: msg.content, isUser: true); })), InputBar(controller: _controller, onSend: _send)])); } }
