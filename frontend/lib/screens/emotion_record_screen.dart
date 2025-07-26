import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'diary_loading_screen.dart';

class EmotionRecordScreen extends StatefulWidget {
  final String accessToken;
  const EmotionRecordScreen({Key? key, required this.accessToken}) : super(key: key);

  @override
  State<EmotionRecordScreen> createState() => _EmotionRecordScreenState();
}

class _EmotionRecordScreenState extends State<EmotionRecordScreen> {
  double sleepScore = 5;
  double stressScore = 5;
  final TextEditingController diaryController = TextEditingController();
  bool isRecording = false;
  bool isLoading = false;

  // TODO: 음성 입력 기능 구현 (speech_to_text 등)
  void onVoiceInput() async {
    setState(() { isRecording = true; });
    await Future.delayed(const Duration(seconds: 2));
    diaryController.text += ' (음성 입력 예시)';
    setState(() { isRecording = false; });
  }

  Future<void> onSubmit() async {
    if (diaryController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('일기 내용을 입력해주세요.')),
      );
      return;
    }
    setState(() { isLoading = true; });
    try {
      final record = await ApiService.createRecord(
        accessToken: widget.accessToken,
        content: diaryController.text.trim(),
        sleepScore: sleepScore.round(),
        stressScore: stressScore.round(),
      );
      // 저장 성공 시 로딩 화면 → 결과 화면으로 데이터 전달
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => DiaryLoadingScreen(record: record),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString().replaceAll('Exception: ', ''))),
      );
    } finally {
      setState(() { isLoading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('감정 기록 입력')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '오늘 하루를 알려주세요!',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Text('수면 정도: ${sleepScore.round()}'),
            Slider(
              value: sleepScore,
              min: 1,
              max: 10,
              divisions: 9,
              label: sleepScore.round().toString(),
              onChanged: (v) => setState(() => sleepScore = v),
            ),
            const SizedBox(height: 8),
            Text('스트레스 정도: ${stressScore.round()}'),
            Slider(
              value: stressScore,
              min: 1,
              max: 10,
              divisions: 9,
              label: stressScore.round().toString(),
              onChanged: (v) => setState(() => stressScore = v),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: diaryController,
              maxLines: 5,
              decoration: InputDecoration(
                labelText: '오늘의 일기를 입력하세요',
                border: OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(isRecording ? Icons.mic : Icons.mic_none),
                  onPressed: isRecording ? null : onVoiceInput,
                ),
              ),
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: isLoading ? null : onSubmit,
                child: isLoading
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    : const Text('일기 저장하기'),
              ),
            ),
          ],
        ),
      ),
    );
  }
} 