import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:record/record.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'dart:async';
import 'dart:js_interop';
import 'dart:html' as html;

class VoiceService {
  static const String baseUrl = 'http://localhost:8000';
  final AudioRecorder _audioRecorder = AudioRecorder();
  bool _isRecording = false;
  
  // 웹용 음성 녹음 변수들
  html.MediaRecorder? _mediaRecorder;
  html.MediaStream? _mediaStream;
  List<html.Blob> _recordedChunks = [];

  /// 마이크 권한 요청
  Future<bool> requestMicrophonePermission() async {
    final status = await Permission.microphone.request();
    return status.isGranted;
  }

  /// 음성 녹음 시작
  Future<bool> startRecording() async {
    if (_isRecording) return false;

    try {
      if (kIsWeb) {
        // 웹에서는 MediaRecorder API 사용
        return await _startWebRecording();
      } else {
        // 모바일에서는 record 패키지 사용
        final hasPermission = await requestMicrophonePermission();
        if (!hasPermission) {
          throw Exception('마이크 권한이 필요합니다.');
        }

        final tempDir = Directory.systemTemp;
        final tempFile = File('${tempDir.path}/audio_${DateTime.now().millisecondsSinceEpoch}.wav');
        
        await _audioRecorder.start(
          const RecordConfig(
            encoder: AudioEncoder.wav,
            bitRate: 128000,
            sampleRate: 16000,
          ),
          path: tempFile.path,
        );
        _isRecording = true;
        return true;
      }
    } catch (e) {
      throw Exception('녹음을 시작할 수 없습니다: $e');
    }
  }

  /// 웹에서 MediaRecorder를 사용한 녹음 시작
  Future<bool> _startWebRecording() async {
    try {
      // 마이크 스트림 요청
      _mediaStream = await html.window.navigator.mediaDevices!.getUserMedia({
        'audio': {
          'sampleRate': 16000,
          'channelCount': 1,
        }
      });

      _recordedChunks.clear();
      
      // MediaRecorder 생성
      _mediaRecorder = html.MediaRecorder(_mediaStream!, {
        'mimeType': 'audio/webm;codecs=opus'
      });

      // 데이터 수집 이벤트
      _mediaRecorder!.addEventListener('dataavailable', (event) {
        final blobEvent = event as html.BlobEvent;
        if (blobEvent.data != null && blobEvent.data!.size > 0) {
          _recordedChunks.add(blobEvent.data!);
        }
      });

      // 녹음 시작
      _mediaRecorder!.start();
      _isRecording = true;
      return true;
    } catch (e) {
      throw Exception('웹 녹음 시작 실패: $e');
    }
  }

  /// 음성 녹음 중지
  Future<String?> stopRecording() async {
    if (!_isRecording) return null;

    try {
      if (kIsWeb) {
        return await _stopWebRecording();
      } else {
        final path = await _audioRecorder.stop();
        _isRecording = false;
        return path;
      }
    } catch (e) {
      _isRecording = false;
      throw Exception('녹음을 중지할 수 없습니다: $e');
    }
  }

  /// 웹에서 MediaRecorder 녹음 중지
  Future<String?> _stopWebRecording() async {
    try {
      if (_mediaRecorder == null) return null;

      final completer = Completer<String?>();
      
      _mediaRecorder!.addEventListener('stop', (event) {
        // 녹음된 데이터를 Blob으로 결합
        final blob = html.Blob(_recordedChunks, 'audio/webm');
        
        // Blob URL 생성 (임시 파일 경로 역할)
        final url = html.Url.createObjectUrl(blob);
        completer.complete(url);
      });

      _mediaRecorder!.stop();
      _mediaStream?.getTracks().forEach((track) => track.stop());
      _isRecording = false;

      return await completer.future;
    } catch (e) {
      _isRecording = false;
      throw Exception('웹 녹음 중지 실패: $e');
    }
  }

  /// 녹음 중인지 확인
  bool get isRecording => _isRecording;

  /// 음성 파일을 텍스트로 변환
  Future<Map<String, dynamic>> speechToText({
    required String accessToken,
    required String audioFilePath,
  }) async {
    try {
      if (kIsWeb) {
        return await _speechToTextWeb(accessToken: accessToken, blobUrl: audioFilePath);
      } else {
        return await _speechToTextMobile(accessToken: accessToken, audioFilePath: audioFilePath);
      }
    } catch (e) {
      return {
        'success': false,
        'error': '음성인식 처리 중 오류가 발생했습니다: $e',
      };
    }
  }

  /// 모바일에서 파일 기반 음성인식
  Future<Map<String, dynamic>> _speechToTextMobile({
    required String accessToken,
    required String audioFilePath,
  }) async {
    final file = File(audioFilePath);
    if (!await file.exists()) {
      throw Exception('오디오 파일을 찾을 수 없습니다.');
    }

    final bytes = await file.readAsBytes();
    
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/voice/stt'),
    );

    request.headers['Authorization'] = 'Bearer $accessToken';
    request.files.add(
      http.MultipartFile.fromBytes(
        'audio_file',
        bytes,
        filename: 'audio.wav',
      ),
    );

    final response = await request.send();
    final responseBody = await response.stream.bytesToString();
    final result = json.decode(responseBody);

    if (response.statusCode == 200) {
      return {
        'success': true,
        'text': result['text'] ?? '',
        'confidence': result['confidence'] ?? 0.0,
      };
    } else {
      return {
        'success': false,
        'error': result['detail'] ?? '음성인식에 실패했습니다.',
      };
    }
  }

  /// 웹에서 Blob 기반 음성인식
  Future<Map<String, dynamic>> _speechToTextWeb({
    required String accessToken,
    required String blobUrl,
  }) async {
    // Blob URL에서 실제 Blob 데이터 가져오기
    final response = await html.HttpRequest.request(
      blobUrl,
      responseType: 'blob',
    );
    
    final blob = response.response as html.Blob;
    
    // Blob을 Uint8List로 변환
    final reader = html.FileReader();
    final completer = Completer<Uint8List>();
    
    reader.onLoadEnd.listen((event) {
      final result = reader.result as List<int>;
      completer.complete(Uint8List.fromList(result));
    });
    
    reader.readAsArrayBuffer(blob);
    final bytes = await completer.future;
    
    // HTTP 요청 생성
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/voice/stt'),
    );

    request.headers['Authorization'] = 'Bearer $accessToken';
    request.files.add(
      http.MultipartFile.fromBytes(
        'audio_file',
        bytes,
        filename: 'audio.webm',
        contentType: MediaType('audio', 'webm'),
      ),
    );

    final httpResponse = await request.send();
    final responseBody = await httpResponse.stream.bytesToString();
    final result = json.decode(responseBody);

    if (httpResponse.statusCode == 200) {
      return {
        'success': true,
        'text': result['text'] ?? '',
        'confidence': result['confidence'] ?? 0.0,
      };
    } else {
      return {
        'success': false,
        'error': result['detail'] ?? '음성인식에 실패했습니다.',
      };
    }
  }



  /// 리소스 해제
  void dispose() {
    _audioRecorder.dispose();
  }
} 