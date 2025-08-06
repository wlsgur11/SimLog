import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SimLog',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        fontFamily: 'MaruBuri', // 기본 폰트로 MaruBuri 설정
        textTheme: const TextTheme(
          displayLarge: TextStyle(fontFamily: 'MaruBuri'),
          displayMedium: TextStyle(fontFamily: 'MaruBuri'),
          displaySmall: TextStyle(fontFamily: 'MaruBuri'),
          headlineLarge: TextStyle(fontFamily: 'MaruBuri'),
          headlineMedium: TextStyle(fontFamily: 'MaruBuri'),
          headlineSmall: TextStyle(fontFamily: 'MaruBuri'),
          titleLarge: TextStyle(fontFamily: 'MaruBuri'),
          titleMedium: TextStyle(fontFamily: 'MaruBuri'),
          titleSmall: TextStyle(fontFamily: 'MaruBuri'),
          bodyLarge: TextStyle(fontFamily: 'MaruBuri'),
          bodyMedium: TextStyle(fontFamily: 'MaruBuri'),
          bodySmall: TextStyle(fontFamily: 'MaruBuri'),
          labelLarge: TextStyle(fontFamily: 'MaruBuri'),
          labelMedium: TextStyle(fontFamily: 'MaruBuri'),
          labelSmall: TextStyle(fontFamily: 'MaruBuri'),
        ),
      ),
      home: const SplashScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
