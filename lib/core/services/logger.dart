class Logger {
  void info(String msg) => print('[INFO] $msg');
  void error(String msg, Object e) => print('[ERROR] $msg: $e');
}
