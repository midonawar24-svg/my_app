import 'dart:async';
class AsyncLock { Future<void> _last = Future.value(); Future<T> synchronized<T>(Future<T> Function() fn) { final completer = Completer<T>(); _last = _last.then((_) async { try { final result = await fn(); completer.complete(result); } catch (e, st) { completer.completeError(e, st); } }); return completer.future; } }
