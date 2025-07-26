import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'record_detail_screen.dart';

class GardenScreen extends StatefulWidget {
  final String accessToken;
  const GardenScreen({Key? key, required this.accessToken}) : super(key: key);

  @override
  GardenScreenState createState() => GardenScreenState();
}

class GardenScreenState extends State<GardenScreen> {
  bool isLoading = true;
  List<Map<String, dynamic>> records = [];
  String selectedPeriod = '30';
  bool _disposed = false;
  
  // 캐시를 위한 변수들
  final Map<String, List<Map<String, dynamic>>> _recordsCache = {};
  final Map<String, DateTime> _cacheTimestamps = {};
  static const Duration _cacheValidDuration = Duration(minutes: 5); // 5분간 캐시 유효

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }

  Future<void> _loadData() async {
    if (_disposed) return;
    
    // 캐시된 데이터가 있고 유효한지 확인
    if (_isCacheValid(selectedPeriod)) {
      setState(() {
        records = _recordsCache[selectedPeriod] ?? [];
        isLoading = false;
      });
      return;
    }
    
    setState(() {
      isLoading = true;
    });

    try {
      final recordsData = await ApiService.getRecordsByPeriod(
        accessToken: widget.accessToken,
        days: int.parse(selectedPeriod),
      );

      if (_disposed) return;
      
      // 캐시에 저장
      _recordsCache[selectedPeriod] = recordsData;
      _cacheTimestamps[selectedPeriod] = DateTime.now();
      
      setState(() {
        records = recordsData;
        isLoading = false;
      });
    } catch (e) {
      if (_disposed) return;
      
      setState(() {
        isLoading = false;
      });
      
      if (mounted && !_disposed) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('데이터 로드 실패: ${e.toString()}')),
        );
      }
    }
  }

  bool _isCacheValid(String period) {
    final timestamp = _cacheTimestamps[period];
    if (timestamp == null) return false;
    
    final now = DateTime.now();
    return now.difference(timestamp) < _cacheValidDuration;
  }

  void _clearCache() {
    _recordsCache.clear();
    _cacheTimestamps.clear();
  }

  // 외부에서 호출할 수 있는 캐시 갱신 메서드
  void refreshCache() {
    _clearCache();
    if (mounted && !_disposed) {
      _loadData();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('마음 정원'),
        centerTitle: true,
        actions: [
          PopupMenuButton<String>(
            onSelected: (value) {
              if (mounted && !_disposed) {
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (!_disposed) {
                    setState(() {
                      selectedPeriod = value;
                    });
                    _loadData();
                  }
                });
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(value: '7', child: Text('최근 7일')),
              const PopupMenuItem(value: '14', child: Text('최근 14일')),
              const PopupMenuItem(value: '30', child: Text('최근 30일')),
            ],
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('${selectedPeriod}일'),
                  const Icon(Icons.arrow_drop_down),
                ],
              ),
            ),
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadData,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildGardenOverview(),
                    const SizedBox(height: 24),
                    _buildEmotionFlowers(),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildGardenOverview() {
    if (records.isEmpty) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(32.0),
          child: Center(
            child: Column(
              children: [
                Icon(Icons.eco, size: 64, color: Colors.grey),
                SizedBox(height: 16),
                Text(
                  '아직 정원에 꽃이 없습니다',
                  style: TextStyle(fontSize: 16, color: Colors.grey),
                ),
                SizedBox(height: 8),
                Text(
                  '감정을 기록하면 정원에 꽃이 피어납니다',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
              ],
            ),
          ),
        ),
      );
    }

    // 감정별 통계 계산
    Map<String, int> emotionCount = {};
    for (var record in records) {
      final emotion = record['emotion_analysis']?['primary_emotion'] ?? '알 수 없음';
      emotionCount[emotion] = (emotionCount[emotion] ?? 0) + 1;
    }

    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '정원 현황',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Text(
              '총 ${records.length}개의 꽃이 피어있습니다',
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: emotionCount.entries.map((entry) {
                return Chip(
                  label: Text('${entry.key} ${entry.value}개'),
                  backgroundColor: _getEmotionColor(entry.key).withOpacity(0.2),
                  labelStyle: TextStyle(
                    color: _getEmotionColor(entry.key),
                    fontWeight: FontWeight.bold,
                  ),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmotionFlowers() {
    if (records.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '감정 꽃들',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 16),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 0.8,
          ),
          itemCount: records.length,
          itemBuilder: (context, index) {
            final record = records[index];
            final emotion = record['emotion_analysis'] ?? {};
            final colorInfo = emotion['color'] ?? {};
            final colorName = colorInfo['name'] ?? '알 수 없음';
            final colorHex = colorInfo['hex'] ?? '#CCCCCC';
            final primaryEmotion = emotion['primary_emotion'] ?? '';
            final createdAt = DateTime.parse(record['created_at']);

            Color parseColor(String hex) {
              hex = hex.replaceAll('#', '');
              if (hex.length == 6) hex = 'FF$hex';
              return Color(int.parse(hex, radix: 16));
            }

            return Card(
              elevation: 2,
              child: InkWell(
                onTap: () {
                  _showFlowerDetail(record);
                },
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          color: parseColor(colorHex),
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          _getEmotionIcon(primaryEmotion),
                          color: Colors.white,
                          size: 20,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        primaryEmotion,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      Text(
                        '${createdAt.month}/${createdAt.day}',
                        style: const TextStyle(
                          fontSize: 10,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  void _showFlowerDetail(Map<String, dynamic> record) {
    Future.delayed(Duration.zero, () {
      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => RecordDetailScreen(record: record),
          ),
        );
      }
    });
  }

  Color _getEmotionColor(String emotion) {
    switch (emotion) {
      case '기쁨':
        return Colors.yellow;
      case '신뢰':
        return Colors.green;
      case '두려움':
        return Colors.cyan;
      case '놀람':
        return Colors.blue;
      case '슬픔':
        return Colors.indigo;
      case '혐오':
        return Colors.purple;
      case '분노':
        return Colors.red;
      case '기대':
        return Colors.orange;
      default:
        return Colors.grey;
    }
  }

  IconData _getEmotionIcon(String emotion) {
    switch (emotion) {
      case '기쁨':
        return Icons.sentiment_very_satisfied;
      case '신뢰':
        return Icons.favorite;
      case '두려움':
        return Icons.sentiment_very_dissatisfied;
      case '놀람':
        return Icons.sentiment_satisfied_alt;
      case '슬픔':
        return Icons.sentiment_dissatisfied;
      case '혐오':
        return Icons.sentiment_very_dissatisfied;
      case '분노':
        return Icons.sentiment_dissatisfied;
      case '기대':
        return Icons.sentiment_satisfied;
      default:
        return Icons.eco;
    }
  }
} 