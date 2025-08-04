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
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    
    // 화면 크기에 따라 아이콘 크기와 패딩 조정
    final iconSize = screenWidth > 600 ? 48.0 : 40.0;
    final cardPadding = screenWidth > 600 ? 16.0 : 12.0;
    final titleFontSize = screenWidth > 600 ? 16.0 : 14.0;
    final subtitleFontSize = screenWidth > 600 ? 12.0 : 10.0;
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('SimLog 홈'),
        centerTitle: true,
      ),
      body: Padding(
        padding: EdgeInsets.all(screenWidth > 600 ? 32.0 : 24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 환영 메시지
            Text(
              nickname != null
                  ? '환영합니다, $nickname님!'
                  : (email != null ? '환영합니다, $email!' : 'SimLog에 오신 것을 환영합니다!'),
              style: TextStyle(
                fontSize: screenWidth > 600 ? 28.0 : 24.0, 
                fontWeight: FontWeight.bold
              ),
            ),
            const SizedBox(height: 8),
            Text(
              '오늘 하루는 어떠셨나요?',
              style: TextStyle(
                fontSize: screenWidth > 600 ? 18.0 : 16.0, 
                color: Colors.grey
              ),
            ),
            const SizedBox(height: 32),
            // 빠른 액션 카드들
            Expanded(
              child: GridView.count(
                crossAxisCount: screenWidth > 600 ? 2 : 2,
                crossAxisSpacing: screenWidth > 600 ? 20.0 : 16.0,
                mainAxisSpacing: screenWidth > 600 ? 20.0 : 16.0,
                childAspectRatio: screenWidth > 600 ? 1.2 : 1.0, // 화면이 클 때 비율 조정
                children: [
                  _buildActionCard(
                    context,
                    Icons.edit,
                    '일기 작성',
                    '오늘의 감정을 기록해보세요',
                    Colors.blue,
                    iconSize,
                    cardPadding,
                    titleFontSize,
                    subtitleFontSize,
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
                    iconSize,
                    cardPadding,
                    titleFontSize,
                    subtitleFontSize,
                    () => onNavTap?.call(0),
                  ),
                  _buildActionCard(
                    context,
                    Icons.eco,
                    '마음 정원',
                    '감정에 따라 자라는 정원을 보세요',
                    Colors.orange,
                    iconSize,
                    cardPadding,
                    titleFontSize,
                    subtitleFontSize,
                    () => onNavTap?.call(1),
                  ),
                  _buildActionCard(
                    context,
                    Icons.person,
                    '내 정보',
                    '내 정보와 설정을 확인해보세요',
                    Colors.purple,
                    iconSize,
                    cardPadding,
                    titleFontSize,
                    subtitleFontSize,
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
    double iconSize,
    double cardPadding,
    double titleFontSize,
    double subtitleFontSize,
    VoidCallback onTap,
  ) {
    return Card(
      elevation: 4,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: EdgeInsets.all(cardPadding),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: iconSize,
                color: color,
              ),
              SizedBox(height: cardPadding * 0.7),
              Text(
                title,
                style: TextStyle(
                  fontSize: titleFontSize,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              SizedBox(height: cardPadding * 0.3),
              Text(
                subtitle,
                style: TextStyle(
                  fontSize: subtitleFontSize,
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