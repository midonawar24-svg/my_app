class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );
  static const String apiPrefix = '/api/v1';

  // Reserved for future clients (e.g. Dio) - http package uses single timeout
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 30);

  static String get fullBaseUrl => '$baseUrl$apiPrefix';
}
