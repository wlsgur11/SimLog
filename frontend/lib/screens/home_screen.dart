import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';
import '../services/api_service.dart';
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
  
  bool _alertChecked = false;
  bool _isDeveloper = false; // 개발자 여부 추가

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

    // 사용자 정보 가져오기 (개발자 여부 확인)
    _loadUserInfo();

    // 알림 체크 (첫 진입 시 1회)
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      await _maybeShowKindAlert();
    });
  }

  Future<void> _loadUserInfo() async {
    try {
      final userInfo = await ApiService.getMyInfo(widget.accessToken);
      print("🔍 사용자 정보 로드: $userInfo"); // 디버깅 로그 추가
      if (mounted) {
        setState(() {
          _isDeveloper = userInfo['is_developer'] ?? false;
        });
        print("🔍 개발자 여부: $_isDeveloper"); // 디버깅 로그 추가
      }
    } catch (e) {
      print("❌ 사용자 정보 로드 실패: $e"); // 디버깅 로그 추가
      // 사용자 정보 로드 실패 시 기본값 사용
      if (mounted) {
        setState(() {
          _isDeveloper = false;
        });
      }
    }
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
                        // 개발자 테스트용 알림 버튼
                        if (_isDeveloper) // 개발자 여부에 따라 표시
                          _buildActionCard(
                            context,
                            Icons.bug_report,
                            '테스트 알림',
                            '7일 우울 알림 모달 테스트',
                            const Color(0xFFFF5722),
                            iconSize,
                            cardPadding,
                            titleFontSize,
                            subtitleFontSize,
                            _forceShowAlertForTesting,
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

  Future<void> _maybeShowKindAlert() async {
    if (_alertChecked) return;
    _alertChecked = true;
    try {
      final result = await ApiService.checkAlert(accessToken: widget.accessToken);
      if (result['should_alert'] == true) {
        if (!mounted) return;
        _showKindAlertModal(
          message: (result['message'] as String?) ?? '요즘 마음이 오래도록 힘들었어요.',
          formUrl: (result['form_url'] as String?) ?? 'https://forms.gle/RM8vijEWkqgPo1de9',
        );
      }
    } catch (_) {
      // 무시: 알림 실패해도 앱 흐름엔 영향 없음
    }
  }

  Future<void> _forceShowAlertForTesting() async {
    try {
      final result = await ApiService.forceShowAlertForTesting(accessToken: widget.accessToken);
      if (result['should_alert'] == true) {
        if (!mounted) return;
        _showKindAlertModal(
          message: (result['message'] as String?) ?? '개발자 테스트용 알림입니다.',
          formUrl: (result['form_url'] as String?) ?? 'https://forms.gle/RM8vijEWkqgPo1de9',
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('테스트 알림 표시 실패: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _showKindAlertModal({required String message, required String formUrl}) {
    showDialog(
      context: context,
      barrierDismissible: true,
      builder: (ctx) {
        bool consent = false;
        bool loading = false;
        return StatefulBuilder(builder: (context, setState) {
          return AlertDialog(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            title: const Text('괜찮아요, 함께 해볼까요?'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  message,
                  style: const TextStyle(height: 1.4),
                ),
                const SizedBox(height: 12),
                const Text(
                  '혹시 원하시면 최근 7일 요약을 간단히 공유할 수 있어요. 상담 선생님께 직접 링크를 보여드리면 됩니다. (7일 후 자동 만료, 전체 본문은 포함되지 않아요)',
                  style: TextStyle(fontSize: 13, color: Colors.black54, height: 1.4),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Checkbox(
                      value: consent,
                      onChanged: (v) => setState(() => consent = v ?? false),
                    ),
                    const Expanded(
                      child: Text(
                        '최근 7일 요약 공유에 동의합니다',
                        style: TextStyle(fontSize: 14),
                      ),
                    )
                  ],
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: loading
                    ? null
                    : () async {
                        // 동의 없이 바로 폼 열기
                        try {
                          final uri = Uri.parse(formUrl);
                          if (await canLaunchUrl(uri)) {
                            final launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
                            if (!launched) {
                              await launchUrl(uri, mode: LaunchMode.inAppWebView);
                            }
                          } else {
                            // 링크를 열 수 없는 경우 클립보드에 복사
                            await Clipboard.setData(ClipboardData(text: formUrl));
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('링크가 클립보드에 복사되었습니다. 브라우저에서 직접 열어주세요.'),
                                  duration: Duration(seconds: 5),
                                ),
                              );
                            }
                          }
                        } catch (e) {
                          if (mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('링크를 열 수 없습니다: ${e.toString()}'),
                                backgroundColor: Colors.red,
                                duration: const Duration(seconds: 3),
                              ),
                            );
                          }
                        }
                        // 7일 억제
                        try { await ApiService.ackAlert(accessToken: widget.accessToken); } catch (_) {}
                        if (mounted) Navigator.of(context).pop();
                      },
                child: const Text('동의 없이 바로가기'),
              ),
              FilledButton(
                onPressed: (!consent || loading)
                    ? null
                    : () async {
                        setState(() => loading = true);
                        try {
                          // 동의하고 요약 공유
                          await ApiService.setConsent(accessToken: widget.accessToken, consented: true);
                          final created = await ApiService.createWeeklyShare(accessToken: widget.accessToken);
                          final sharePath = created['share_path'] as String;
                          final shareUrl = '${ApiService.baseUrl}$sharePath';
                          
                          // 요약 링크 생성 결과 화면 표시
                          if (mounted) {
                            _showShareResult(shareUrl);
                          }
                          
                          // 7일 억제
                          try { await ApiService.ackAlert(accessToken: widget.accessToken); } catch (_) {}
                          
                        } catch (e) {
                          setState(() => loading = false);
                          if (mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text('요약 공유 실패: $e')),
                            );
                          }
                        }
                      },
                child: loading ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator()) : const Text('동의하고 바로가기'),
              ),
            ],
          );
        });
      },
    );
  }

  Future<void> _refreshUserInfo() async {
    print("🔄 사용자 정보 강제 새로고침 시작");
    await _loadUserInfo();
  }

  void _showShareResult(String shareUrl) {
    showDialog(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          title: const Text('공유 링크가 준비됐어요'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('상담 선생님께 직접 보여주거나 전달해 주세요. (7일 후 자동 만료)'),
              const SizedBox(height: 10),
              SelectableText(shareUrl, style: const TextStyle(fontSize: 14, color: Colors.blue)),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () async {
                await Clipboard.setData(ClipboardData(text: shareUrl));
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('복사되었습니다')));
                }
              },
              child: const Text('복사'),
            ),
            TextButton(
              onPressed: () async {
                try {
                  final uri = Uri.parse(shareUrl);
                  if (await canLaunchUrl(uri)) {
                    await launchUrl(uri, mode: LaunchMode.externalApplication);
                  } else {
                    await Clipboard.setData(ClipboardData(text: shareUrl));
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('링크가 클립보드에 복사되었습니다')),
                      );
                    }
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('링크 열기 실패: $e')),
                    );
                  }
                }
              },
              child: const Text('열기'),
            ),
            FilledButton(
              onPressed: () async {
                // 모달 닫기
                Navigator.of(ctx).pop();
                // 마음체크 폼으로 이동
                try {
                  final uri = Uri.parse('https://forms.gle/RM8vijEWkqgPo1de9');
                  if (await canLaunchUrl(uri)) {
                    final launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
                    if (!launched) {
                      await launchUrl(uri, mode: LaunchMode.inAppWebView);
                    }
                  } else {
                    await Clipboard.setData(ClipboardData(text: 'https://forms.gle/RM8vijEWkqgPo1de9'));
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('링크가 클립보드에 복사되었습니다. 브라우저에서 직접 열어주세요.'),
                          duration: Duration(seconds: 5),
                        ),
                      );
                    }
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('링크를 열 수 없습니다: ${e.toString()}'),
                        backgroundColor: Colors.red,
                        duration: const Duration(seconds: 3),
                      ),
                    );
                  }
                }
              },
              child: const Text('마음체크 하기'),
            ),
          ],
        );
      },
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