import 'package:flutter/material.dart';
import 'emotion_record_screen.dart';

class HomeScreen extends StatelessWidget {
  final String? nickname;
  final String? email;
  final String accessToken;
  final Function(int)? onNavTap;
  
  const HomeScreen({
    Key? key, 
    this.nickname, 
    this.email, 
    required this.accessToken,
    this.onNavTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SimLog 홈'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 환영 메시지
            Text(
              nickname != null
                  ? '환영합니다, $nickname님!'
                  : (email != null ? '환영합니다, $email!' : 'SimLog에 오신 것을 환영합니다!'),
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              '오늘 하루는 어떠셨나요?',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 32),
            // 빠른 액션 카드들
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                children: [
                  _buildActionCard(
                    context,
                    Icons.edit,
                    '일기 작성',
                    '오늘의 감정을 기록해보세요',
                    Colors.blue,
                    () {
                      Future.delayed(Duration.zero, () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => EmotionRecordScreen(accessToken: accessToken),
                          ),
                        );
                      });
                    },
                  ),
                  _buildActionCard(
                    context,
                    Icons.analytics,
                    '감정 분석',
                    '나의 감정 변화를 확인해보세요',
                    Colors.green,
                    () => onNavTap?.call(0),
                  ),
                  _buildActionCard(
                    context,
                    Icons.eco,
                    '마음 정원',
                    '감정에 따라 자라는 정원을 보세요',
                    Colors.orange,
                    () => onNavTap?.call(1),
                  ),
                  _buildActionCard(
                    context,
                    Icons.person,
                    '내 정보',
                    '내 정보와 설정을 확인해보세요',
                    Colors.purple,
                    () => onNavTap?.call(2),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(
    BuildContext context,
    IconData icon,
    String title,
    String subtitle,
    Color color,
    VoidCallback onTap,
  ) {
    return Card(
      elevation: 4,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: 40,
                color: color,
              ),
              const SizedBox(height: 8),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 4),
              Text(
                subtitle,
                style: const TextStyle(
                  fontSize: 10,
                  color: Colors.grey,
                ),
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }
} 