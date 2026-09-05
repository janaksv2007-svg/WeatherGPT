import 'package:flutter/material.dart';
import '../widgets.dart';
import '../weather_theme.dart';

class InsightsScreen extends StatefulWidget {
  const InsightsScreen({super.key});

  @override
  State<InsightsScreen> createState() => _InsightsScreenState();
}

class _InsightsScreenState extends State<InsightsScreen> {
  double start = 1;
  double duration = 60;
  String activity = 'Two-wheeler commute';

  final activities = {
    'Two-wheeler commute': 1.12,
    'Outdoor sport': 1.18,
    'Field / farm work': 1.22,
    'Construction site': 1.30,
  };

  int get simulatedRisk {
    final factor = activities[activity]!;
    final base = start < 2
        ? 92
        : start < 4
            ? 68
            : 34;

    return (base * factor).clamp(0, 100).round();
  }

  @override
  Widget build(BuildContext context) {
    final weatherTheme =
        WeatherTheme.forCondition(currentWeatherCondition);

    final accent = weatherTheme.accent;
    final iconColor = weatherTheme.iconColor;

    final risk = simulatedRisk;
    final riskColorValue = riskColor(risk);

    return Scaffold(
      backgroundColor: weatherTheme.background,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 30),
          children: [
            // ============================================================
            // HEADER
            // ============================================================

            const TopHeader(
              title: 'Insights',
              subtitle:
                  'Check if your plan is safe, then explore past weather',
            ),

            const SizedBox(height: 18),

            // ============================================================
            // WHAT-IF SIMULATOR
            // ============================================================

            const SectionHeader(
              title: 'Is my plan safe?',
              meta: 'What-if simulator',
            ),

            const SizedBox(height: 10),

            AppCard(
              color: weatherTheme.cardColor,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // --------------------------------------------------------
                  // ACTIVITY
                  // --------------------------------------------------------

                  const Text(
                    'Activity',
                    style: TextStyle(
                      fontSize: 12.5,
                      fontWeight: FontWeight.w700,
                      color: textMid,
                    ),
                  ),

                  const SizedBox(height: 9),

                  Wrap(
                    spacing: 7,
                    runSpacing: 7,
                    children: activities.keys.map(
                      (a) {
                        final isSelected = activity == a;

                        return ChoiceChip(
                          label: Text(
                            a,
                            style: TextStyle(
                              fontSize: 11,
                              color: isSelected
                                  ? iconColor
                                  : textMid,
                              fontWeight: isSelected
                                  ? FontWeight.w700
                                  : FontWeight.w500,
                            ),
                          ),
                          selected: isSelected,
                          selectedColor:
                              accent.withOpacity(.18),
                          backgroundColor: night700,
                          side: BorderSide(
                            color: isSelected
                                ? accent
                                : line,
                          ),
                          onSelected: (_) {
                            setState(() {
                              activity = a;
                            });
                          },
                        );
                      },
                    ).toList(),
                  ),

                  const SizedBox(height: 20),

                  // --------------------------------------------------------
                  // START TIME
                  // --------------------------------------------------------

                  Row(
                    children: [
                      const Text(
                        'Start time',
                        style: TextStyle(
                          fontSize: 12.5,
                          fontWeight: FontWeight.w700,
                          color: textMid,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        start == 0
                            ? 'Now'
                            : '+${start.toStringAsFixed(1)} hr',
                        style: TextStyle(
                          fontWeight: FontWeight.w800,
                          color: iconColor,
                        ),
                      ),
                    ],
                  ),

                  SliderTheme(
                    data: SliderTheme.of(context).copyWith(
                      activeTrackColor: accent,
                      inactiveTrackColor: night600,
                      thumbColor: iconColor,
                      overlayColor:
                          accent.withOpacity(.12),
                    ),
                    child: Slider(
                      value: start,
                      min: 0,
                      max: 5,
                      divisions: 10,
                      onChanged: (v) {
                        setState(() {
                          start = v;
                        });
                      },
                    ),
                  ),

                  // --------------------------------------------------------
                  // OUTSIDE DURATION
                  // --------------------------------------------------------

                  Row(
                    children: [
                      const Text(
                        'Outside duration',
                        style: TextStyle(
                          fontSize: 12.5,
                          fontWeight: FontWeight.w700,
                          color: textMid,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        '${duration.round()} min',
                        style: TextStyle(
                          fontWeight: FontWeight.w800,
                          color: iconColor,
                        ),
                      ),
                    ],
                  ),

                  SliderTheme(
                    data: SliderTheme.of(context).copyWith(
                      activeTrackColor: accent,
                      inactiveTrackColor: night600,
                      thumbColor: iconColor,
                      overlayColor:
                          accent.withOpacity(.12),
                    ),
                    child: Slider(
                      value: duration,
                      min: 15,
                      max: 180,
                      divisions: 11,
                      onChanged: (v) {
                        setState(() {
                          duration = v;
                        });
                      },
                    ),
                  ),

                  const SizedBox(height: 8),

                  // --------------------------------------------------------
                  // RISK RESULT
                  // --------------------------------------------------------

                  Container(
                    padding: const EdgeInsets.all(15),
                    decoration: BoxDecoration(
                      color: riskColorValue.withOpacity(.08),
                      borderRadius:
                          BorderRadius.circular(16),
                      border: Border.all(
                        color:
                            riskColorValue.withOpacity(.25),
                      ),
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment:
                                CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'RISK FOR THIS PLAN',
                                style: TextStyle(
                                  fontSize: 10.5,
                                  letterSpacing: 1.2,
                                  color: textLo,
                                  fontWeight:
                                      FontWeight.w800,
                                ),
                              ),

                              const SizedBox(height: 5),

                              Text(
                                risk >= 67
                                    ? 'Reschedule this plan'
                                    : risk >= 34
                                        ? 'Possible with precautions'
                                        : 'Safe to go ahead',
                                style: const TextStyle(
                                  fontSize: 17,
                                  fontWeight:
                                      FontWeight.w900,
                                  color: textHi,
                                ),
                              ),
                            ],
                          ),
                        ),

                        Text(
                          '$risk',
                          style: TextStyle(
                            fontSize: 36,
                            fontWeight: FontWeight.w900,
                            color: riskColorValue,
                          ),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 10),

                  Text(
                    risk >= 67
                        ? 'Risk peaks while the storm is strongest. '
                            'Shift the plan before the peak or after the cell clears.'
                        : risk >= 34
                            ? 'Keep it short and stay close to shelter. '
                                'Risk increases as the storm approaches.'
                            : 'Conditions stay benign across this window.',
                    style: const TextStyle(
                      fontSize: 12.5,
                      color: textMid,
                      height: 1.4,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 22),

            // ============================================================
            // AI EXPLANATION
            // ============================================================

            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: weatherTheme.backgroundSecondary,
                borderRadius: BorderRadius.circular(18),
                border: Border.all(
                  color: accent.withOpacity(.22),
                ),
              ),
              child: Row(
                crossAxisAlignment:
                    CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 42,
                    height: 42,
                    decoration: BoxDecoration(
                      color: accent.withOpacity(.12),
                      borderRadius:
                          BorderRadius.circular(12),
                    ),
                    child: Icon(
                      Icons.auto_awesome_rounded,
                      color: iconColor,
                      size: 22,
                    ),
                  ),

                  const SizedBox(width: 12),

                  Expanded(
                    child: Column(
                      crossAxisAlignment:
                          CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'WeatherGPT insight',
                          style: TextStyle(
                            color: textHi,
                            fontSize: 14,
                            fontWeight: FontWeight.w800,
                          ),
                        ),

                        const SizedBox(height: 5),

                        Text(
                          risk >= 67
                              ? 'Your selected activity overlaps with the highest-risk part of the storm window.'
                              : risk >= 34
                                  ? 'Your plan is possible, but conditions may deteriorate as the storm approaches.'
                                  : 'Your selected time currently falls outside the strongest storm period.',
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
            ),

            const SizedBox(height: 24),

            // ============================================================
            // PAST WEATHER
            // ============================================================

            const SectionHeader(
              title: 'Past weather',
              meta: 'Historical climate',
            ),

            const SizedBox(height: 10),

            AppCard(
              color: weatherTheme.cardColor,
              child: Column(
                crossAxisAlignment:
                    CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Extreme weather trend',
                    style: TextStyle(
                      fontWeight: FontWeight.w800,
                      color: textHi,
                    ),
                  ),

                  const SizedBox(height: 5),

                  const Text(
                    'A visual history module can be connected to your historical API later.',
                    style: TextStyle(
                      fontSize: 12,
                      color: textLo,
                    ),
                  ),

                  const SizedBox(height: 15),

                  MiniLineChart(
                    values: const [
                      24,
                      30,
                      27,
                      42,
                      38,
                      50,
                      47,
                      61,
                      56,
                      70,
                      66,
                      78,
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // ============================================================
            // CURRENT WEATHER CONTEXT
            // ============================================================

            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: weatherTheme.backgroundSecondary,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: line,
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.insights_rounded,
                    color: iconColor,
                    size: 20,
                  ),

                  const SizedBox(width: 10),

                  const Expanded(
                    child: Text(
                      'WeatherGPT continuously updates this assessment as storm conditions change.',
                      style: TextStyle(
                        color: textMid,
                        fontSize: 11.5,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}