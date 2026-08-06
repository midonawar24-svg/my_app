import 'package:flutter/widgets.dart';
import 'app.dart';
import 'dependency_injection.dart';
import '../core/kernel/ai_core_kernel.dart';
import 'package:flutter/material.dart';
Future<void> bootstrap() async { WidgetsFlutterBinding.ensureInitialized(); await setupDependencies(); final kernel = getIt<AiCoreKernel>(); await kernel.initialize(); runApp(const MyApp()); }
