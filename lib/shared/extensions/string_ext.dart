extension StringExt on String {
  String get truncated => length <= 30? this : '${substring(0, 30)}...';
}
