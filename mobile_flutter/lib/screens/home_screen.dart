import 'package:flutter/material.dart';

import '../widgets.dart';
import '../widgets/live_status_bar.dart';
import '../data/mock_data.dart';
import '../weather_theme.dart';

import 'chat_screen.dart';
import 'nowcast_screen.dart';
import 'risk_map_screen.dart';
import 'safety_screen.dart';
import 'settings_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  IconData _weatherIcon(WeatherCondition condition) {
    switch (condition) {
      case WeatherCondition.clear:
        return Icons.wb_sunny_outlined;
      case WeatherCondition.cloudy:
        return Icons.cloud_outlined;
      case WeatherCondition.rain:
        return Icons.water_drop_outlined;
      case WeatherCondition.thunderstorm:
        return Icons.thunderstorm_outlined;
      case WeatherCondition.severeStorm:
        return Icons.warning_amber_rounded;
      case WeatherCondition.fog:
        return Icons.foggy;
    }
  }

  @override
  Widget build(BuildContext context) {
    final weatherTheme =
        WeatherTheme.forCondition(currentWeatherCondition);

    final accent = weatherTheme.accent;
    final iconColor = weatherTheme.iconColor;

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
      children: [
        // ------------------------------------------------------------
        // HEADER
        // ------------------------------------------------------------
        TopHeader(
          title: 'WeatherGPT',
          subtitle: 'Chennai',
          onSettings: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const SettingsScreen(),
              ),
            );
          },
        ),

        const SizedBox(height: 12),

        // ------------------------------------------------------------
        // LIVE MONITORING
        // ------------------------------------------------------------
        const LiveStatusBar(
          updatedText: 'Updated just now',
        ),

        const SizedBox(height: 18),

        // ------------------------------------------------------------
        // CURRENT WEATHER
        // ------------------------------------------------------------
        AppCard(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.location_on_outlined,
                    size: 15,
                    color: accent,
                  ),
                  const SizedBox(width: 5),
                  const Text(
                    'CHENNAI',
                    style: TextStyle(
                      fontSize: 11,
                      letterSpacing: 1.3,
                      fontWeight: FontWeight.w700,
                      color: textLo,
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 10),

              Row(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  const Text(
                    '31°',
                    style: TextStyle(
                      fontSize: 58,
                      fontWeight: FontWeight.w800,
                      color: textHi,
                      height: .95,
                    ),
                  ),

                  const SizedBox(width: 10),

                  const Padding(
                    padding: EdgeInsets.only(bottom: 5),
                    child: Text(
                      'Thunderstorm\ndeveloping',
                      style: TextStyle(
                        fontSize: 13,
                        color: textMid,
                        height: 1.35,
                      ),
                    ),
                  ),

                  const Spacer(),

                  Icon(
                    _weatherIcon(currentWeatherCondition),
                    size: 48,
                    color: iconColor,
                  ),
                ],
              ),

              const SizedBox(height: 12),

              const Text(
                'Feels like 38°  ·  Humidity 84%  ·  Wind 18 km/h',
                style: TextStyle(
                  fontSize: 11.5,
                  color: textLo,
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 14),

        // ------------------------------------------------------------
        // STORM APPROACHING
        // ------------------------------------------------------------
        GestureDetector(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const NowcastScreen(),
              ),
            );
          },
          child: AppCard(
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(9),
                  decoration: BoxDecoration(
                    color: accent.withOpacity(.10),
                    borderRadius: BorderRadius.circular(13),
                  ),
                  child: Icon(
                    Icons.warning_amber_rounded,
                    color: accent,
                  ),
                ),

                const SizedBox(width: 12),

                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Storm approaching · 42 min',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w800,
                          color: textHi,
                        ),
                      ),

                      SizedBox(height: 4),

                      Text(
                        'Cell C-14 · moving NW → SE at 27 km/h',
                        style: TextStyle(
                          fontSize: 12.5,
                          color: textMid,
                        ),
                      ),
                    ],
                  ),
                ),

                const Icon(
                  Icons.chevron_right,
                  color: textLo,
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // ------------------------------------------------------------
        // RISK SCORE
        // ------------------------------------------------------------
        GestureDetector(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const RiskMapScreen(),
              ),
            );
          },
          child: AppCard(
            child: Row(
              children: [
                const RiskGauge(
                  score: riskScore,
                ),

                const SizedBox(width: 18),

                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Local Risk Score',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w800,
                          color: textHi,
                        ),
                      ),

                      const SizedBox(height: 7),

                      const Text(
                        'High risk. Strong lightning, heavy rain and damaging gusts are expected.',
                        style: TextStyle(
                          fontSize: 12.5,
                          color: textMid,
                          height: 1.4,
                        ),
                      ),

                      const SizedBox(height: 10),

                      Row(
                        children: [
                          Icon(
                            Icons.auto_awesome,
                            size: 14,
                            color: accent,
                          ),

                          const SizedBox(width: 5),

                          Text(
                            'AI confidence 91%',
                            style: TextStyle(
                              fontSize: 11.5,
                              color: accent,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // ------------------------------------------------------------
        // AI INSIGHT
        // ------------------------------------------------------------
        AppCard(
          color: weatherTheme.backgroundSecondary,
          child: Row(
            children: [
              Icon(
                Icons.auto_awesome,
                color: accent,
                size: 22,
              ),

              const SizedBox(width: 12),

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'AI INSIGHT',
                      style: TextStyle(
                        fontSize: 12,
                        color: accent,
                        fontWeight: FontWeight.w800,
                        letterSpacing: .7,
                      ),
                    ),

                    const SizedBox(height: 5),

                    const Text(
                      'Get indoors within the next 30 minutes.',
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: textHi,
                      ),
                    ),

                    const SizedBox(height: 4),

                    const Text(
                      'The storm is organising rapidly and tracking directly towards your area.',
                      style: TextStyle(
                        fontSize: 12.5,
                        color: textMid,
                        height: 1.35,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 20),

        // ------------------------------------------------------------
        // EXPECTED HAZARDS
        // ------------------------------------------------------------
        const SectionHeader(
          title: 'Expected hazards',
          meta: 'Next 6 hours',
        ),

        ...hazards.map(
          (h) => Padding(
            padding: const EdgeInsets.only(bottom: 9),
            child: HazardTile(
              hazard: h,
            ),
          ),
        ),

        const SizedBox(height: 8),

        // ------------------------------------------------------------
        // QUICK ACTIONS
        // ------------------------------------------------------------
        const SectionHeader(
          title: 'Quick actions',
        ),

        Row(
          children: [
            Expanded(
              child: _Action(
                icon: Icons.shield_outlined,
                label: 'Stay safe',
                color: accent,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const SafetyScreen(),
                    ),
                  );
                },
              ),
            ),

            const SizedBox(width: 9),

            Expanded(
              child: _Action(
                icon: Icons.map_outlined,
                label: 'Storm map',
                color: accent,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const RiskMapScreen(),
                    ),
                  );
                },
              ),
            ),

            const SizedBox(width: 9),

            Expanded(
              child: _Action(
                icon: Icons.auto_awesome,
                label: 'Ask AI',
                color: accent,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const ChatScreen(),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ],
    );
  }
}

// ============================================================================
// QUICK ACTION BUTTON
// ============================================================================

class _Action extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _Action({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AppCard(
        padding: const EdgeInsets.symmetric(
          vertical: 15,
          horizontal: 8,
        ),
        child: Column(
          children: [
            Icon(
              icon,
              color: color,
              size: 21,
            ),

            const SizedBox(height: 7),

            Text(
              label,
              style: const TextStyle(
                fontSize: 11.5,
                fontWeight: FontWeight.w700,
                color: textMid,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}