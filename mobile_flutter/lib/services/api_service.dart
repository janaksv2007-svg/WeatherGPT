import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Configurable base URL for backend connection
  static String baseUrl = 'http://127.0.0.1:8000';

  /// Send chat message to unified FastAPI backend POST /chat
  static Future<Map<String, dynamic>> sendChatMessage({
    required String message,
    String sessionId = 'flutter-session-001',
    String language = 'en',
  }) async {
    final url = Uri.parse('$baseUrl/chat');
    try {
      final response = await http
          .post(
            url,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'message': message,
              'session_id': sessionId,
              'language': language,
            }),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        return {
          'success': false,
          'response':
              'Server returned error status code: ${response.statusCode}',
        };
      }
    } catch (e) {
      return {
        'success': false,
        'response':
            'Could not connect to WeatherGPT backend server ($baseUrl). Showing fallback mode.',
        'error': e.toString(),
      };
    }
  }

  /// Get current live weather from GET /api/weather
  static Future<Map<String, dynamic>?> getWeather(
      {String location = 'chennai'}) async {
    final url = Uri.parse('$baseUrl/api/weather?location=$location');
    try {
      final response =
          await http.get(url).timeout(const Duration(seconds: 8));
      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }
    } catch (e) {
      print('[ApiService] getWeather error: $e');
    }
    return null;
  }

  /// Get disaster alerts from GET /api/alerts
  static Future<List<dynamic>> getAlerts() async {
    final url = Uri.parse('$baseUrl/api/alerts');
    try {
      final response =
          await http.get(url).timeout(const Duration(seconds: 8));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['alerts'] ?? [];
      }
    } catch (e) {
      print('[ApiService] getAlerts error: $e');
    }
    return [];
  }

  /// Get RainViewer radar frame metadata from GET /api/radar/rainviewer
  static Future<Map<String, dynamic>?> getRadarFrames() async {
    final url = Uri.parse('$baseUrl/api/radar/rainviewer');
    try {
      final response =
          await http.get(url).timeout(const Duration(seconds: 8));
      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }
    } catch (e) {
      print('[ApiService] getRadarFrames error: $e');
    }
    return null;
  }

  /// Run counterfactual scenario simulation POST /api/simulation
  static Future<Map<String, dynamic>?> runSimulation({
    double? targetRainfallMm,
    double? rainfallChangeMm,
    double? windSpeedChangePercent,
    double? additionalRainfallHours,
  }) async {
    final url = Uri.parse('$baseUrl/api/simulation');
    try {
      final response = await http
          .post(
            url,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'target_rainfall_mm': targetRainfallMm,
              'rainfall_change_mm': rainfallChangeMm,
              'wind_speed_change_percent': windSpeedChangePercent,
              'additional_rainfall_hours': additionalRainfallHours,
            }),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }
    } catch (e) {
      print('[ApiService] runSimulation error: $e');
    }
    return null;
  }
}
