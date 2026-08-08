class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic data;

  const ApiException(
    this.message, {
    this.statusCode,
    this.data,
  });

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class NetworkException extends ApiException {
  const NetworkException(super.message);
}

class ServerException extends ApiException {
  const ServerException(
    super.message, {
    super.statusCode,
    super.data,
  });
}

class RequestTimeoutException extends ApiException {
  const RequestTimeoutException() : super('Request timed out');
}
