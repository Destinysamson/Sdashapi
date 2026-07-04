// SdashAPI — Flutter / Dart Example
// ====================================
// Add to pubspec.yaml: http: ^1.0.0

import 'dart:convert';
import 'package:http/http.dart' as http;

const _baseUrl = 'https://sdashapi.com/api/v1';
const _token   = 'sdash_your_token_here'; // Replace with your AccessToken

Map<String, String> get _headers => {'AccessToken': _token};

// ----------------------------------------------------------
// Models
// ----------------------------------------------------------

class Question {
  final int id;
  final String question;
  final String? section;
  final Map<String, String> option;
  final String answer;
  final String? solution;
  final String? image;
  final String examtype;
  final String examyear;

  const Question({
    required this.id,
    required this.question,
    this.section,
    required this.option,
    required this.answer,
    this.solution,
    this.image,
    required this.examtype,
    required this.examyear,
  });

  factory Question.fromJson(Map<String, dynamic> json) => Question(
        id:       json['id'] as int,
        question: json['question'] as String,
        section:  json['section'] as String?,
        option:   Map<String, String>.from(json['option'] as Map),
        answer:   json['answer'] as String,
        solution: json['solution'] as String?,
        image:    json['image'] as String?,
        examtype: json['examtype'] as String,
        examyear: json['examyear'] as String,
      );
}

// ----------------------------------------------------------
// API Service
// ----------------------------------------------------------

class SdashApiService {
  /// Fetch one or more questions.
  /// [limit] = 1 returns a single Question object.
  /// [limit] > 1 returns a List<Question>.
  static Future<dynamic> fetchQuestions({
    String? subject,
    String? type,
    int? year,
    int? id,
    int limit = 1,
  }) async {
    final params = <String, String>{'limit': limit.toString()};
    if (subject != null) params['subject'] = subject;
    if (type != null)    params['type']    = type;
    if (year != null)    params['year']    = year.toString();
    if (id != null)      params['id']      = id.toString();

    final uri = Uri.https('sdashapi.com', '/api/v1/q', params);
    final res  = await http.get(uri, headers: _headers);
    final body = jsonDecode(res.body) as Map<String, dynamic>;

    if (res.statusCode != 200) {
      throw Exception('SdashAPI error: ${body['message']}');
    }

    if (limit == 1) {
      return Question.fromJson(body['data'] as Map<String, dynamic>);
    }
    return (body['data'] as List)
        .map((q) => Question.fromJson(q as Map<String, dynamic>))
        .toList();
  }

  /// List all subjects.
  static Future<List<Map<String, dynamic>>> fetchSubjects() async {
    final res  = await http.get(Uri.parse('$_baseUrl/subjects'), headers: _headers);
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    return List<Map<String, dynamic>>.from(body['data'] as List);
  }

  /// List all exam types.
  static Future<List<Map<String, dynamic>>> fetchExams() async {
    final res  = await http.get(Uri.parse('$_baseUrl/exams'), headers: _headers);
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    return List<Map<String, dynamic>>.from(body['data'] as List);
  }

  /// List all available years.
  static Future<List<int>> fetchYears() async {
    final res  = await http.get(Uri.parse('$_baseUrl/years'), headers: _headers);
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    return List<int>.from(body['data'] as List);
  }

  /// Report a question issue.
  static Future<String> reportQuestion({
    required int questionId,
    String reportType = 'wrong_answer',
    String message = '',
  }) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/report'),
      headers: {..._headers, 'Content-Type': 'application/json'},
      body: jsonEncode({
        'question_id': questionId,
        'report_type': reportType,
        'message': message,
      }),
    );
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    return body['message'] as String;
  }
}

// ----------------------------------------------------------
// Usage example
// ----------------------------------------------------------

void main() async {
  // Single random question
  final q = await SdashApiService.fetchQuestions() as Question;
  print('Q: ${q.question}');
  q.option.forEach((key, val) {
    final mark = key == q.answer ? '✅' : '  ';
    print('$mark ${key.toUpperCase()}) $val');
  });

  // 5 UTME Biology questions
  final questions = await SdashApiService.fetchQuestions(
    subject: 'biology',
    type:    'utme',
    year:    2021,
    limit:   5,
  ) as List<Question>;

  for (final q in questions) {
    print('\n${q.question} [${q.examtype} ${q.examyear}]');
  }

  // List subjects
  final subjects = await SdashApiService.fetchSubjects();
  print('\nSubjects: ${subjects.map((s) => s['name']).join(', ')}');
}
