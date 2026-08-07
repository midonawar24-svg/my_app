import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'api_config.dart';
import 'api_exception.dart';

class ApiClient {
  final http.Client _client;
  final ApiConfig _config;
  final String baseUrl;

  ApiClient({
    http.Client? client,
    ApiConfig? config,
    String? baseUrl,
  })  : _client = client ?? http.Client(),
        _config = config ?? ApiConfig(),
        baseUrl = baseUrl ?? (config ?? ApiConfig()).baseUrl;

  Future<T> post<T>(
    String path, {
    Object? data,
    required T Function(dynamic json) parser,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    try {
      final response = await _client
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: data != null ? jsonEncode(data) : null,
          )
          .timeout(_config.receiveTimeout);
      return _handleResponse(response, parser);
    } on SocketException {
      throw const NetworkException('No internet connection');
    } on TimeoutException {
      throw const RequestTimeoutException();
    }
  }

  Future<T> get<T>(
    String path, {
    required T Function(dynamic json) parser,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    try {
      final response = await _client
          .get(uri, headers: {'Content-Type': 'application/json'})
          .timeout(_config.receiveTimeout);
      return _handleResponse(response, parser);
    } on SocketException {
      throw const NetworkException('No internet connection');
    } on TimeoutException {
      throw const RequestTimeoutException();
    }
  }

  Future<T> delete<T>(
    String path, {
    Object? data,
    required T Function(dynamic json) parser,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    try {
      final response = await _client
          .delete(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: data != null ? jsonEncode(data) : null,
          )
          .timeout(_config.receiveTimeout);
      return _handleResponse(response, parser);
    } on SocketException {
      throw const NetworkException('No internet connection');
    } on TimeoutException {
      throw const RequestTimeoutException();
    }
  }

  T _handleResponse<T>(
    http.Response response,
    T Function(dynamic) parser,
  ) {
    final status = response.statusCode;
    dynamic body;

    try {
      body = response.body.isNotEmpty ? jsonDecode(response.body) : null;
    } catch (_) {
      body = response.body;
    }

    if (status >= 200 && status < 300) {
      return parser(body);
    }

    throw ServerException(
      body is Map
          ? (body['detail'] ?? body['message'] ?? 'Server error').toString()
          : 'Server error: $status',
      statusCode: status,
      data: body,
    );
  }

  void close() => _client.close();

  void dispose() => close();
}
