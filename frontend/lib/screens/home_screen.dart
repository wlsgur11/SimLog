import 'package:flutter/material.dart';
import 'emotion_record_screen.dart';

class HomeScreen extends StatefulWidget {
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
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with TickerProviderStateMixin {
  late AnimationController _fadeController;
  late AnimationController _slideController;
  late AnimationController _bounceController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;
  late Animation<double> _bounceAnimation;

  @override
  void initState() {
    super.initState();
    _fadeController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _slideController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _bounceController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    
    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _fadeController,
      curve: Curves.easeInOut,
    ));
    
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _slideController,
      curve: Curves.easeOutCubic,
    ));

    _bounceAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _bounceController,
      curve: Curves.elasticOut,
    ));
    
    _fadeController.forward();
    _slideController.forward();
    _bounceController.forward();
  }

  @override
  void dispose() {
    _fadeController.dispose();
    _slideController.dispose();
    _bounceController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    
    // 화면 크기에 따라 아이콘 크기와 패딩 조정 (글씨 크기 증가)
    final iconSize = screenWidth > 600 ? 52.0 : 44.0;
    final cardPadding = screenWidth > 600 ? 18.0 : 14.0;
    final titleFontSize = screenWidth > 600 ? 20.0 : 18.0; // 16.0 -> 20.0, 14.0 -> 18.0
    final subtitleFontSize = screenWidth > 600 ? 16.0 : 14.0; // 12.0 -> 16.0, 10.0 -> 14.0
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('SimLog 홈'),
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.black87,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFFE8F5E8),
              Color(0xFFF0F8FF),
              Color(0xFFF5F0FF),
              Colors.white,
            ],
            stops: [0.0, 0.3, 0.7, 1.0],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: EdgeInsets.all(screenWidth > 600 ? 32.0 : 24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // 환영 메시지 (애니메이션 적용)
                FadeTransition(
                  opacity: _fadeAnimation,
                  child: SlideTransition(
                    position: _slideAnimation,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.blue.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: const Icon(
                                Icons.psychology,
                                color: Colors.blue,
                                size: 24,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    widget.nickname != null
                                        ? '환영합니다, ${widget.nickname}님!'
                                        : (widget.email != null ? '환영합니다, ${widget.email}!' : 'SimLog에 오신 것을 환영합니다!'),
                                    style: TextStyle(
                                      fontSize: screenWidth > 600 ? 32.0 : 28.0, // 28.0 -> 32.0, 24.0 -> 28.0
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black87,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    '오늘 하루는 어떠셨나요?',
                                    style: TextStyle(
                                      fontSize: screenWidth > 600 ? 22.0 : 20.0, // 18.0 -> 22.0, 16.0 -> 20.0
                                      color: Colors.grey[600],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 32),
                // 빠른 액션 카드들
                Expanded(
                  child: ScaleTransition(
                    scale: _bounceAnimation,
                    child: GridView.count(
                      crossAxisCount: screenWidth > 600 ? 2 : 2,
                      crossAxisSpacing: screenWidth > 600 ? 20.0 : 16.0,
                      mainAxisSpacing: screenWidth > 600 ? 20.0 : 16.0,
                      childAspectRatio: screenWidth > 600 ? 1.2 : 1.0,
                      children: [
                        _buildActionCard(
                          context,
                          Icons.edit_note,
                          '일기 작성',
                          '오늘의 감정을 기록해보세요',
                          const Color(0xFF4CAF50),
                          iconSize,
                          cardPadding,
                          titleFontSize,
                          subtitleFontSize,
                          () {
                            Future.delayed(Duration.zero, () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => EmotionRecordScreen(accessToken: widget.accessToken),
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
                          const Color(0xFF2196F3),
                          iconSize,
                          cardPadding,
                          titleFontSize,
                          subtitleFontSize,
                          () => widget.onNavTap?.call(0),
                        ),
                        _buildActionCard(
                          context,
                          Icons.eco,
                          '마음 정원',
                          '감정에 따라 자라는 정원을 보세요',
                          const Color(0xFFFF9800),
                          iconSize,
                          cardPadding,
                          titleFontSize,
                          subtitleFontSize,
                          () => widget.onNavTap?.call(1),
                        ),
                        _buildActionCard(
                          context,
                          Icons.person,
                          '내 정보',
                          '내 정보와 설정을 확인해보세요',
                          const Color(0xFF9C27B0),
                          iconSize,
                          cardPadding,
                          titleFontSize,
                          subtitleFontSize,
                          () => widget.onNavTap?.call(2),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
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
      elevation: 8,
      shadowColor: color.withOpacity(0.3),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(20),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Colors.white,
                color.withOpacity(0.05),
                color.withOpacity(0.1),
              ],
            ),
            border: Border.all(
              color: color.withOpacity(0.1),
              width: 1,
            ),
          ),
          child: Padding(
            padding: EdgeInsets.all(cardPadding),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: EdgeInsets.all(cardPadding * 0.8),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: [
                        color.withOpacity(0.1),
                        color.withOpacity(0.2),
                      ],
                    ),
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: color.withOpacity(0.2),
                        blurRadius: 8,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Icon(
                    icon,
                    size: iconSize,
                    color: color,
                  ),
                ),
                SizedBox(height: cardPadding * 1.2),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: titleFontSize,
                    fontWeight: FontWeight.bold,
                    color: Colors.black87,
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                SizedBox(height: cardPadding * 0.6),
                Text(
                  subtitle,
                  style: TextStyle(
                    fontSize: subtitleFontSize,
                    color: Colors.grey[600],
                    height: 1.3,
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
} 