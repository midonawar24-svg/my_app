import 'dart:async';

class AsyncLock {
  Future<void> _lock = Future.value();

  Future<T> synchronized<T>(Future<T> Function() action) {
    final prev = _lock;
    final completer = Completer<void>();
    _lock = completer.future;
    return prev.then((_) => action()).whenComplete(() => completer.complete());
  }
}
