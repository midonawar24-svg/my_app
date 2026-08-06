import 'package:flutter/foundation.dart';
class Logger {
  void info(String msg) { if (kDebugMode) print('[INFO] $msg'); }
  void error(String msg, [Object? e]) { if (kDebugMode) print('[ERROR] $msg - $e'); }
}
