import 'dart:io';

class InternetCheck {
  static Future<String> run() async {
    try {
      final result = await InternetAddress.lookup('example.com')
          .timeout(const Duration(seconds: 8));

      if (result.isNotEmpty && result.first.rawAddress.isNotEmpty) {
        return 'INTERNET: CONNECTED';
      }

      return 'INTERNET: NOT CONNECTED';
    } catch (e) {
      return 'INTERNET: NOT CONNECTED — $e';
    }
  }
}
