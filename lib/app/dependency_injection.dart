import 'package:get_it/get_it.dart';
import '../core/kernel/ai_core_kernel.dart';
import '../core/kernel/ai_runtime.dart';
import '../core/conversation/conversation_store.dart';
import '../core/conversation/in_memory_conversation_store.dart';
import '../core/conversation/conversation_manager.dart';
import '../core/storage/memory_store.dart';
import '../core/storage/in_memory_store.dart';
import '../core/ai/memory/memory_repository.dart';
import '../core/ai/memory/repositories/in_memory_memory_repository.dart';
import '../core/ai/memory/memory_engine.dart';
import '../core/services/logger.dart';
import '../core/services/config.dart';
final getIt = GetIt.instance;
Future<void> setupDependencies() async { getIt.registerSingleton<Logger>(Logger()); getIt.registerSingleton<AppConfig>(AppConfig()); getIt.registerSingleton<MemoryStore>(InMemoryStore()); getIt.registerSingleton<ConversationStore>(InMemoryConversationStore()); getIt.registerSingleton<MemoryRepository>(InMemoryMemoryRepository(getIt<MemoryStore>())); getIt.registerSingleton<MemoryEngine>(MemoryEngine(repository: getIt<MemoryRepository>())); getIt.registerSingleton<ConversationManager>(ConversationManager(store: getIt<ConversationStore>())); getIt.registerSingleton<AiRuntime>(AiRuntime()); getIt.registerSingleton<AiCoreKernel>(AiCoreKernel(memoryEngine: getIt<MemoryEngine>(), conversationManager: getIt<ConversationManager>(), runtime: getIt<AiRuntime>(), logger: getIt<Logger>())); }
