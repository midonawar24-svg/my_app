import 'package:flutter/material.dart';
import '../features/chat/presentation/chat_page.dart';
import '../shared/theme/app_theme.dart';
class MyApp extends StatelessWidget { const MyApp({super.key}); @override Widget build(BuildContext context) { return MaterialApp(title: 'AI Core OS', debugShowCheckedModeBanner: false, theme: AppTheme.light, darkTheme: AppTheme.dark, themeMode: ThemeMode.system, home: const ChatPage()); } }
