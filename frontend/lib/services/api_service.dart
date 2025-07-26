import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // TODO: 실제 서버 주소로 변경
  static const String baseUrl = 'http://localhost:8000';

  static Future<Map<String, dynamic>> signup({
    required String email,
    required String password,
    required String nickname,
    String? socialType,
    String? socialId,
  }) async {
    final url = Uri.parse('$baseUrl/auth/signup');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
        'nickname': nickname,
        'social_type': socialType,
        'social_id': socialId,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['detail'] ?? '회원가입 실패');
    }
  }

  static Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final url = Uri.parse('$baseUrl/auth/login');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['detail'] ?? '로그인 실패');
    }
  }

  static Future<Map<String, dynamic>> getMyInfo(String accessToken) async {
    final url = Uri.parse('$baseUrl/users/me');
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('사용자 정보 조회 실패');
    }
  }

  static Future<Map<String, dynamic>> createRecord({
    required String accessToken,
    required String content,
    required int sleepScore,
    required int stressScore,
    bool shareWithCounselor = false,
  }) async {
    final url = Uri.parse('$baseUrl/records/');
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $accessToken',
      },
      body: jsonEncode({
        'content': content,
        'sleep_score': sleepScore,
        'stress_score': stressScore,
        'share_with_counselor': shareWithCounselor,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['detail'] ?? '감정 기록 저장 실패');
    }
  }

  static Future<List<Map<String, dynamic>>> getRecords({
    required String accessToken,
    int skip = 0,
    int limit = 100,
  }) async {
    final url = Uri.parse('$baseUrl/records/?skip=$skip&limit=$limit');
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.cast<Map<String, dynamic>>();
    } else {
      throw Exception('감정 기록 조회 실패');
    }
  }

  static Future<List<Map<String, dynamic>>> getRecordsByPeriod({
    required String accessToken,
    required int days,
  }) async {
    final url = Uri.parse('$baseUrl/records/period/$days');
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.cast<Map<String, dynamic>>();
    } else {
      final errorBody = jsonDecode(response.body);
      throw Exception(errorBody['detail'] ?? '기간별 감정 기록 조회 실패');
    }
  }

  static Future<Map<String, dynamic>> getEmotionStatistics({
    required String accessToken,
    required int days,
  }) async {
    final url = Uri.parse('$baseUrl/records/statistics/$days');
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final errorBody = jsonDecode(response.body);
      throw Exception(errorBody['detail'] ?? '감정 통계 조회 실패');
    }
  }

  static Future<Map<String, dynamic>> getTodayRecord({
    required String accessToken,
  }) async {
    final url = Uri.parse('$baseUrl/records/today/record');
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('오늘 기록 조회 실패');
    }
  }

  static Future<Map<String, dynamic>> getTodayStatus({
    required String accessToken,
  }) async {
    final url = Uri.parse('$baseUrl/records/today/status');
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('오늘 상태 조회 실패');
    }
  }

  static Future<Map<String, dynamic>> updateProfile({
    required String accessToken,
    String? nickname,
    String? password,
  }) async {
    final url = Uri.parse('$baseUrl/users/me');
    final response = await http.put(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $accessToken',
      },
      body: jsonEncode({
        if (nickname != null) 'nickname': nickname,
        if (password != null) 'password': password,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final errorBody = jsonDecode(response.body);
      throw Exception(errorBody['detail'] ?? '프로필 수정 실패');
    }
  }
} 