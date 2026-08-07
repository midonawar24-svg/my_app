class ApiConfig {
  // FastAPI default is 8000
  // Emulator: 10.0.2.2:8000
  // Physical device: use PC IP e.g. http://192.168.1.10:8000
  // Override: flutter run --dart-define=API_BASE_URL=http://192.168.1.10:8000
  static const String _defaultBaseUrl = 'http://10.0.2.2:8000';
  String get baseUrl => const String.fromEnvironment('API_BASE_URL', defaultValue: _defaultBaseUrl);
  Duration get connectTimeout => const Duration(seconds: 15);
  Duration get receiveTimeout => const Duration(seconds: 30);
}
