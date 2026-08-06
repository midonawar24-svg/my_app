import 'package:flutter/material.dart';
import '../features/chat/presentation/chat_page.dart';
class AppRoutes { static const chat = '/'; static Route<dynamic> onGenerateRoute(RouteSettings settings) { return MaterialPageRoute(builder: (_) => const ChatPage()); } }
