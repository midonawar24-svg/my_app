import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/app/app.dart';
import 'package:my_app/app/dependency_injection.dart';

void main() {
  setUpAll(() async {
    await getIt.reset();
    await setupDependencies();
  });

  testWidgets('AI Core OS loads', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();
    expect(find.text('AI Core OS'), findsOneWidget);
  });
}
