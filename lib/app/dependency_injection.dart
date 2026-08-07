import 'package:get_it/get_it.dart';
import '../core/kernel/ai_core_kernel.dart';
import '../core/kernel/ai_runtime.dart';
import '../core/conversation/conversation_store.dart';
import '../core/conversation/hive_conversation_store.dart';
import '../core/conversation/conversation_manager.dart';
import '../core/storage/memory_store.dart';
import '../core/storage/hive_memory_store.dart';
import '../core/ai/memory/memory_repository.dart';
import '../core/ai/memory/repositories/in_memory_memory_repository.dart';
import '../core/ai/memory/memory_engine.dart';
import '../core/services/logger.dart';
import '../core/services/config.dart';
import '../core/services/chat_service.dart';
import '../core/network/api_config.dart';
import '../core/network/api_client.dart';
import '../core/services/chat_api_service.dart';

final getIt = GetIt.instance;

Future<void> setupDependencies() async {
  if (!getIt.isRegistered<Logger>()) getIt.registerSingleton<Logger>(Logger());
  if (!getIt.isRegistered<AppConfig>()) getIt.registerSingleton<AppConfig>(AppConfig());
  if (!getIt.isRegistered<MemoryStore>()) getIt.registerSingleton<MemoryStore>(HiveMemoryStore());
  if (!getIt.isRegistered<ConversationStore>()) getIt.registerSingleton<ConversationStore>(HiveConversationStore());
  if (!getIt.isRegistered<MemoryRepository>()) getIt.registerSingleton<MemoryRepository>(InMemoryMemoryRepository(getIt<MemoryStore>()));
  if (!getIt.isRegistered<MemoryEngine>()) getIt.registerSingleton<MemoryEngine>(MemoryEngine(repository: getIt<MemoryRepository>()));
  if (!getIt.isRegistered<ConversationManager>()) getIt.registerSingleton<ConversationManager>(ConversationManager(store: getIt<ConversationStore>(), logger: getIt<Logger>()));
  if (!getIt.isRegistered<ApiConfig>()) getIt.registerSingleton<ApiConfig>(ApiConfig());
  if (!getIt.isRegistered<ApiClient>()) getIt.registerSingleton<ApiClient>(ApiClient(config: getIt<ApiConfig>()));
  if (!getIt.isRegistered<ChatApiService>()) getIt.registerSingleton<ChatApiService>(ChatApiService(getIt<ApiClient>()));
  if (!getIt.isRegistered<ChatService>()) getIt.registerSingleton<ChatService>(ChatService(convManager: getIt<ConversationManager>(), memoryEngine: getIt<MemoryEngine>(), apiService: getIt<ChatApiService>()));
  if (!getIt.isRegistered<AiRuntime>()) getIt.registerSingleton<AiRuntime>(AiRuntime());
  if (!getIt.isRegistered<AiCoreKernel>()) getIt.registerSingleton<AiCoreKernel>(AiCoreKernel(memoryEngine: getIt<MemoryEngine>(), conversationManager: getIt<ConversationManager>(), runtime: getIt<AiRuntime>(), logger: getIt<Logger>()));
}
