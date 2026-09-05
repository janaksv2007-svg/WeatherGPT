import 'package:flutter/material.dart';
enum WeatherCondition {
  clear,
  cloudy,
  rain,
  thunderstorm,
  severeStorm,
  fog,
}
WeatherCondition currentWeatherCondition =
    WeatherCondition.clear;

class WeatherTheme {
  final Color background;
  final Color backgroundSecondary;
  final Color accent;
  final Color iconColor;
  final Color cardColor;

  const WeatherTheme({
    required this.background,
    required this.backgroundSecondary,
    required this.accent,
    required this.iconColor,
    required this.cardColor,
  });

  static WeatherTheme forCondition(WeatherCondition condition) {
    switch (condition) {
      case WeatherCondition.clear:
  return const WeatherTheme(
    background: Color(0xFF071A2D),
    backgroundSecondary: Color(0xFF10283D),
    accent: Color(0xFFD9E2EC),
    iconColor: Color(0xFFF1F5F9),
    cardColor: Color(0xFF0D2238),
  );

      case WeatherCondition.cloudy:
        return const WeatherTheme(
          background: Color(0xFF101923),
          backgroundSecondary: Color(0xFF182532),
          accent: Color(0xFF94A3B8),
          iconColor: Color(0xFFCBD5E1),
          cardColor: Color(0xFF16212D),
        );

      case WeatherCondition.rain:
        return const WeatherTheme(
          background: Color(0xFF071522),
          backgroundSecondary: Color(0xFF0B2032),
          accent: Color(0xFF38BDF8),
          iconColor: Color(0xFF60A5FA),
          cardColor: Color(0xFF0D1F30),
        );

      case WeatherCondition.thunderstorm:
        return const WeatherTheme(
          background: Color(0xFF090D1A),
          backgroundSecondary: Color(0xFF15152B),
          accent: Color(0xFF22D3EE),
          iconColor: Color(0xFFA855F7),
          cardColor: Color(0xFF11162A),
        );

      case WeatherCondition.severeStorm:
        return const WeatherTheme(
          background: Color(0xFF130A0A),
          backgroundSecondary: Color(0xFF25100D),
          accent: Color(0xFFF97316),
          iconColor: Color(0xFFEF4444),
          cardColor: Color(0xFF211313),
        );

      case WeatherCondition.fog:
        return const WeatherTheme(
          background: Color(0xFF11151A),
          backgroundSecondary: Color(0xFF1C2228),
          accent: Color(0xFFA8B5C2),
          iconColor: Color(0xFFD1D5DB),
          cardColor: Color(0xFF192027),
        );
    }
  }
}