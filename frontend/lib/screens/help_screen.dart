import 'package:flutter/material.dart';

class HelpScreen extends StatelessWidget {
  const HelpScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('도움말'), centerTitle: true),
      body: const Padding(
        padding: EdgeInsets.all(24.0),
        child: Text(
          '심로그 앱 사용법\n\n- 일기 작성: + 버튼을 눌러 감정 일기를 작성하세요.\n- 분석: 최근 감정 통계와 AI 분석 결과를 확인할 수 있습니다.\n- 마음 정원: 감정 기록이 꽃으로 표현됩니다.\n- 내 정보: 닉네임/비밀번호를 변경할 수 있습니다.\n\n더 궁금한 점이 있으면 문의해 주세요!',
          style: TextStyle(fontSize: 16),
        ),
      ),
    );
  }
} 