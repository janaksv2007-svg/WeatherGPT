import 'package:flutter/material.dart';

import '../widgets.dart';
import '../data/mock_data.dart';
import '../widgets/emergency_help_card.dart';
import '../weather_theme.dart';

class SafetyScreen extends StatelessWidget {
  const SafetyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final weatherTheme =
        WeatherTheme.forCondition(currentWeatherCondition);

    final accent = weatherTheme.accent;
    final iconColor = weatherTheme.iconColor;

    return Scaffold(
      backgroundColor: weatherTheme.background,
      appBar: AppBar(
        backgroundColor: weatherTheme.background,
        elevation: 0,
        title: const Text(
          'Stay safe now',
          style: TextStyle(
            color: textHi,
            fontWeight: FontWeight.w700,
          ),
        ),
        iconTheme: IconThemeData(
          color: iconColor,
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
        children: [
          // CURRENT ALERT
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: weatherTheme.backgroundSecondary,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                color: riskHigh.withOpacity(0.35),
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.20),
                  blurRadius: 20,
                  offset: const Offset(0, 8),
                ),
              ],
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: riskHigh.withOpacity(0.14),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: const Icon(
                    Icons.warning_amber_rounded,
                    color: riskHigh,
                    size: 27,
                  ),
                ),
                const SizedBox(width: 14),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'SEVERE WEATHER ALERT',
                        style: TextStyle(
                          color: riskHigh,
                          fontSize: 12,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 1.1,
                        ),
                      ),
                      SizedBox(height: 6),
                      Text(
                        'Thunderstorm approaching',
                        style: TextStyle(
                          color: textHi,
                          fontSize: 19,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      SizedBox(height: 5),
                      Text(
                        'Strong lightning and heavy rain are possible in your area.',
                        style: TextStyle(
                          color: textMid,
                          fontSize: 13,
                          height: 1.45,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 18),

          // EMERGENCY HELP
          const EmergencyHelpCard(),

          const SizedBox(height: 24),

          // STAY SAFE
          const SectionHeader(
            title: 'Stay safe now',
          ),

          const SizedBox(height: 12),

          _SafetyAction(
            icon: Icons.home_rounded,
            title: 'Move indoors',
            description:
                'Stay inside a sturdy building and avoid exposed outdoor areas.',
            accent: accent,
            iconColor: iconColor,
            priority: 'NOW',
          ),

          const SizedBox(height: 12),

          _SafetyAction(
            icon: Icons.flash_on_rounded,
            title: 'Avoid open spaces',
            description:
                'Do not stay in fields, rooftops, beaches, or other exposed locations.',
            accent: accent,
            iconColor: iconColor,
            priority: 'IMPORTANT',
          ),

          const SizedBox(height: 12),

          _SafetyAction(
            icon: Icons.power_rounded,
            title: 'Protect electronics',
            description:
                'Unplug sensitive devices if conditions become severe and it is safe to do so.',
            accent: accent,
            iconColor: iconColor,
            priority: 'IMPORTANT',
          ),

          const SizedBox(height: 12),

          _SafetyAction(
            icon: Icons.directions_car_rounded,
            title: 'Avoid unnecessary travel',
            description:
                'Heavy rain can reduce visibility and create dangerous road conditions.',
            accent: accent,
            iconColor: iconColor,
            priority: 'CAUTION',
          ),

          const SizedBox(height: 24),

          // AI SAFETY EXPLANATION
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: weatherTheme.backgroundSecondary,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                color: accent.withOpacity(0.22),
              ),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 42,
                  height: 42,
                  decoration: BoxDecoration(
                    color: accent.withOpacity(0.13),
                    borderRadius: BorderRadius.circular(13),
                  ),
                  child: Icon(
                    Icons.auto_awesome_rounded,
                    color: iconColor,
                    size: 23,
                  ),
                ),
                const SizedBox(width: 13),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'WeatherGPT recommendation',
                        style: TextStyle(
                          color: textHi,
                          fontSize: 15,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      SizedBox(height: 7),
                      Text(
                        'The safest option is to remain indoors until the storm passes. '
                        'WeatherGPT will continue monitoring the storm and update the risk automatically.',
                        style: TextStyle(
                          color: textMid,
                          fontSize: 13,
                          height: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // QUICK CHECKLIST
          const SectionHeader(
            title: 'Quick checklist',
          ),

          const SizedBox(height: 12),

          AppCard(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                _ChecklistItem(
                  icon: Icons.battery_charging_full_rounded,
                  text: 'Keep your phone charged',
                  accent: accent,
                  iconColor: iconColor,
                ),

                const Divider(
                  color: line,
                  height: 22,
                ),

                _ChecklistItem(
                  icon: Icons.water_drop_rounded,
                  text: 'Keep drinking water available',
                  accent: accent,
                  iconColor: iconColor,
                ),

                const Divider(
                  color: line,
                  height: 22,
                ),

                _ChecklistItem(
                  icon: Icons.flashlight_on_rounded,
                  text: 'Keep a flashlight nearby',
                  accent: accent,
                  iconColor: iconColor,
                ),

                const Divider(
                  color: line,
                  height: 22,
                ),

                _ChecklistItem(
                  icon: Icons.notifications_active_rounded,
                  text: 'Keep WeatherGPT alerts enabled',
                  accent: accent,
                  iconColor: iconColor,
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // STORM STATUS
          Container(
            padding: const EdgeInsets.all(17),
            decoration: BoxDecoration(
              color: weatherTheme.backgroundSecondary,
              borderRadius: BorderRadius.circular(18),
              border: Border.all(
                color: line,
              ),
            ),
            child: Row(
              children: [
                Container(
                  width: 10,
                  height: 10,
                  decoration: const BoxDecoration(
                    color: riskHigh,
                    shape: BoxShape.circle,
                  ),
                ),

                const SizedBox(width: 11),

                const Expanded(
                  child: Text(
                    'Monitoring continuously · Risk updates automatically',
                    style: TextStyle(
                      color: textMid,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),

                Icon(
                  Icons.refresh_rounded,
                  color: iconColor,
                  size: 19,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================================
// SAFETY ACTION CARD
// ============================================================================

class _SafetyAction extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final Color accent;
  final Color iconColor;
  final String priority;

  const _SafetyAction({
    required this.icon,
    required this.title,
    required this.description,
    required this.accent,
    required this.iconColor,
    required this.priority,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: night800,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(
          color: line,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 46,
            height: 46,
            decoration: BoxDecoration(
              color: accent.withOpacity(0.12),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(
              icon,
              color: iconColor,
              size: 24,
            ),
          ),

          const SizedBox(width: 13),

          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        title,
                        style: const TextStyle(
                          color: textHi,
                          fontSize: 15,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),

                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: accent.withOpacity(0.10),
                        borderRadius: BorderRadius.circular(7),
                      ),
                      child: Text(
                        priority,
                        style: TextStyle(
                          color: iconColor,
                          fontSize: 9,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 0.7,
                        ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 6),

                Text(
                  description,
                  style: const TextStyle(
                    color: textMid,
                    fontSize: 12.5,
                    height: 1.45,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================================
// CHECKLIST ITEM
// ============================================================================

class _ChecklistItem extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color accent;
  final Color iconColor;

  const _ChecklistItem({
    required this.icon,
    required this.text,
    required this.accent,
    required this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: accent.withOpacity(0.10),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(
            icon,
            color: iconColor,
            size: 19,
          ),
        ),

        const SizedBox(width: 12),

        Expanded(
          child: Text(
            text,
            style: const TextStyle(
              color: textHi,
              fontSize: 13,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),

        const Icon(
          Icons.check_circle_rounded,
          color: riskLow,
          size: 19,
        ),
      ],
    );
  }
}