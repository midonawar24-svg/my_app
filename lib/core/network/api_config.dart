class ApiConfig {
  static const String _defaultHost = '127.0.0.1';
  static const int _defaultPort = 8001;

  static const String _runtimeBaseUrl =
      String.fromEnvironment('API_BASE_URL');

  String get baseUrl {
    final value = _runtimeBaseUrl.trim();

    if (value.isNotEmpty) {
      return value.replaceFirst(RegExp(r'/$'), '');
    }

    return Uri(
      scheme: 'http',
      host: _defaultHost,
      port: _defaultPort,
    ).toString();
  }

  Duration get connectTimeout => const Duration(seconds: 15);

  Duration get receiveTimeout => const Duration(seconds: 30);
}
