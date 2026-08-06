import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/app/app.dart';
import 'package:my_app/app/dependency_injection.dart';
import 'package:my_app/core/kernel/ai_core_kernel.dart';
void main() { testWidgets('AI Core OS loads', (WidgetTester tester) async { await setupDependencies(); final kernel = getIt<AiCoreKernel>(); await kernel.initialize(); await tester.pumpWidget(const MyApp()); await tester.pump(); expect(find.text('AI Core OS'), findsOneWidget); }); }
