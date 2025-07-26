import 'package:flutter/material.dart';
import 'home_screen.dart';
import 'analysis_screen.dart';
import 'garden_screen.dart';
import 'profile_screen.dart';
import 'emotion_record_screen.dart';

class MainNavigationScreen extends StatefulWidget {
  final String? nickname;
  final String? email;
  final String accessToken;
  final int initialIndex;
  
  const MainNavigationScreen({
    Key? key, 
    this.nickname, 
    this.email, 
    required this.accessToken,
    this.initialIndex = 0,
  }) : super(key: key);

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  late int _selectedIndex;
  late final List<Widget> _screens;
  
  // GlobalKey를 사용하여 화면에 접근
  final GlobalKey<AnalysisScreenState> _analysisKey = GlobalKey<AnalysisScreenState>();
  final GlobalKey<GardenScreenState> _gardenKey = GlobalKey<GardenScreenState>();

  @override
  void initState() {
    super.initState();
    _selectedIndex = widget.initialIndex;
    _screens = [
      AnalysisScreen(key: _analysisKey, accessToken: widget.accessToken),
      GardenScreen(key: _gardenKey, accessToken: widget.accessToken),
      ProfileScreen(
        nickname: widget.nickname,
        email: widget.email,
        accessToken: widget.accessToken,
      ),
    ];
  }

  void _onItemTapped(int index) {
    if (_selectedIndex != index && mounted) {
      setState(() {
        _selectedIndex = index;
      });
    }
  }

  void _onHomeTapped() {
    if (mounted) {
      setState(() {
        _selectedIndex = -1;
      });
    }
  }

  void _onFloatingActionButtonPressed() {
    Future.delayed(Duration.zero, () {
      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => EmotionRecordScreen(accessToken: widget.accessToken),
          ),
        ).then((_) {
          // 일기 작성 후 돌아오면 캐시 갱신
          _refreshCache();
        });
      }
    });
  }

  void _refreshCache() {
    // AnalysisScreen과 GardenScreen의 캐시를 갱신
    _analysisKey.currentState?.refreshCache();
    _gardenKey.currentState?.refreshCache();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _selectedIndex == -1
          ? HomeScreen(
              nickname: widget.nickname,
              email: widget.email,
              accessToken: widget.accessToken,
              onNavTap: (index) {
                setState(() {
                  _selectedIndex = index;
                });
              },
            )
          : _screens[_selectedIndex],
      floatingActionButton: _selectedIndex == -1
          ? null
          : FloatingActionButton(
              onPressed: _onFloatingActionButtonPressed,
              backgroundColor: Colors.deepPurple,
              foregroundColor: Colors.white,
              child: const Icon(Icons.add, size: 28),
            ),
      floatingActionButtonLocation: _selectedIndex == -1
          ? null
          : FloatingActionButtonLocation.centerDocked,
      bottomNavigationBar: _selectedIndex == -1
          ? null
          : SafeArea(
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 4,
                      offset: const Offset(0, -2),
                    ),
                  ],
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Expanded(
                        child: _buildNavButton(
                          icon: Icons.home,
                          label: '홈',
                          isSelected: false,
                          onTap: _onHomeTapped,
                        ),
                      ),
                      Expanded(
                        child: _buildNavButton(
                          icon: Icons.analytics,
                          label: '분석',
                          isSelected: _selectedIndex == 0,
                          onTap: () => _onItemTapped(0),
                        ),
                      ),
                      const SizedBox(width: 40),
                      Expanded(
                        child: _buildNavButton(
                          icon: Icons.eco,
                          label: '정원',
                          isSelected: _selectedIndex == 1,
                          onTap: () => _onItemTapped(1),
                        ),
                      ),
                      Expanded(
                        child: _buildNavButton(
                          icon: Icons.person,
                          label: '내정보',
                          isSelected: _selectedIndex == 2,
                          onTap: () => _onItemTapped(2),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
    );
  }

  Widget _buildNavButton({
    required IconData icon,
    required String label,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected ? Colors.deepPurple : Colors.grey,
              size: 22,
            ),
            const SizedBox(height: 2),
            Flexible(
              child: Text(
                label,
                style: TextStyle(
                  color: isSelected ? Colors.deepPurple : Colors.grey,
                  fontSize: 11,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
                overflow: TextOverflow.ellipsis,
                maxLines: 1,
              ),
            ),
          ],
        ),
      ),
    );
  }
} 