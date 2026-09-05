import 'package:flutter/material.dart';
import 'data/mock_data.dart';
import 'screens/home_screen.dart';
import 'screens/nowcast_screen.dart';
import 'screens/risk_map_screen.dart';
import 'screens/safety_screen.dart';
import 'screens/insights_screen.dart';
import 'screens/settings_screen.dart';
import 'weather_theme.dart';

void main() {
  runApp(const WeatherGPTApp());
}

class WeatherGPTApp extends StatelessWidget {
  const WeatherGPTApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WeatherGPT',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Colors.transparent,
        colorScheme: ColorScheme.dark(
          primary: WeatherTheme.forCondition(
            currentWeatherCondition,
          ).accent,
          secondary: WeatherTheme.forCondition(
            currentWeatherCondition,
          ).accent,
          surface: const Color(0xFF0C1220),
        ),
        fontFamily: 'Arial',
        useMaterial3: true,
      ),
      home: const WeatherShell(),
    );
  }
}
class WeatherShell extends StatefulWidget {
  const WeatherShell({super.key});

  @override
  State<WeatherShell> createState() => _WeatherShellState();
}

class _WeatherShellState extends State<WeatherShell> {
  int selectedIndex = 0;

  final pages = const [
    HomeScreen(),
    NowcastScreen(),
    RiskMapScreen(),
    SafetyScreen(),
    InsightsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                WeatherTheme.forCondition(
                  currentWeatherCondition,
                ).backgroundSecondary,
                WeatherTheme.forCondition(
                  currentWeatherCondition,
                ).background,
              ],
              stops: const [0.0, 0.35],
            ),
          ),
          child: IndexedStack(
            index: selectedIndex,
            children: pages,
          ),
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (index) {
          setState(() => selectedIndex = index);
        },
        backgroundColor: const Color(0xF20A0F19),
        indicatorColor: WeatherTheme.forCondition(
          currentWeatherCondition,
        ).accent.withOpacity(0.18),
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: Icon(
              Icons.home,
              color: WeatherTheme.forCondition(
                currentWeatherCondition,
              ).iconColor,
            ),
            label: 'Now',
          ),
          NavigationDestination(
            icon: const Icon(Icons.thunderstorm_outlined),
            selectedIcon: Icon(
              Icons.thunderstorm,
              color: WeatherTheme.forCondition(
                currentWeatherCondition,
              ).iconColor,
            ),
            label: 'Nowcast',
          ),
          NavigationDestination(
            icon: const Icon(Icons.map_outlined),
            selectedIcon: Icon(
              Icons.map,
              color: WeatherTheme.forCondition(
                currentWeatherCondition,
              ).iconColor,
            ),
            label: 'Map',
          ),
          NavigationDestination(
            icon: const Icon(Icons.shield_outlined),
            selectedIcon: Icon(
              Icons.shield,
              color: WeatherTheme.forCondition(
                currentWeatherCondition,
              ).iconColor,
            ),
            label: 'Safety',
          ),
          NavigationDestination(
            icon: const Icon(Icons.insights_outlined),
            selectedIcon: Icon(
              Icons.insights,
              color: WeatherTheme.forCondition(
                currentWeatherCondition,
              ).iconColor,
            ),
            label: 'Insights',
          ),
        ],
      ),
    );
  }
}
