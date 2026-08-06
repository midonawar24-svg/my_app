import 'package:flutter/widgets.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'app.dart';
import 'dependency_injection.dart';
import '../core/kernel/ai_core_kernel.dart';
import '../core/conversation/hive_conversation_store.dart';
import '../core/storage/hive_memory_store.dart';

Future<void> bootstrap() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  await HiveConversationStore.init();
  await HiveMemoryStore.init();
  await setupDependencies();
  final kernel = getIt<AiCoreKernel>();
  await kernel.initialize();
  runApp(const MyApp());
}
