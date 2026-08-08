class ApiConfig {
  static const String _defaultBaseUrl = 'http://127.0.0.1:8000';

  static const String _runtimeBaseUrl =
      String.fromEnvironment('API_BASE_URL');

  String get baseUrl {
    final value = _runtimeBaseUrl.trim();

    if (value.isNotEmpty) {
      return value.replaceFirst(RegExp(r'/$'), '');
    }

    return _defaultBaseUrl;
  }

  Duration get connectTimeout => const Duration(seconds: 15);

  Duration get receiveTimeout => const Duration(seconds: 30);
}
