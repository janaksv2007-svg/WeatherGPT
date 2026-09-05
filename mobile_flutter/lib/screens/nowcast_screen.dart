
import 'package:flutter/material.dart';

import '../widgets.dart';
import '../data/mock_data.dart';
import '../weather_theme.dart';

class NowcastScreen extends StatelessWidget {
  const NowcastScreen({super.key});

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
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios_new_rounded,
            color: textHi,
            size: 20,
          ),
          onPressed: () => Navigator.pop(context),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text(
              'Next 6 hours',
              style: TextStyle(
                color: textHi,
                fontSize: 19,
                fontWeight: FontWeight.w800,
                decoration: TextDecoration.none,
              ),
            ),
            Text(
              'Updated every 5 minutes',
              style: TextStyle(
                color: textLo,
                fontSize: 11,
                fontWeight: FontWeight.w500,
                decoration: TextDecoration.none,
              ),
            ),
          ],
        ),
      ),

      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 4, 16, 28),
        children: [
          // WORST TIME
          AppCard(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'WORST TIME TO BE OUTSIDE',
                  style: TextStyle(
                    fontSize: 10,
                    letterSpacing: 1.2,
                    color: textLo,
                    fontWeight: FontWeight.w700,
                    decoration: TextDecoration.none,
                  ),
                ),

                const SizedBox(height: 8),

                Row(
                  children: [
                    const Text(
                      '7:28 PM',
                      style: TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.w900,
                        color: textHi,
                        decoration: TextDecoration.none,
                      ),
                    ),

                    const Spacer(),

                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: riskHigh.withOpacity(.12),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(
                          color: riskHigh.withOpacity(.30),
                        ),
                      ),
                      child: const Text(
                        'HIGH',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.w900,
                          color: riskHigh,
                          decoration: TextDecoration.none,
                        ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 5),

                const Text(
                  'Storm risk reaches 92/100 in about 1 hr 37 min.',
                  style: TextStyle(
                    fontSize: 12,
                    color: textMid,
                    height: 1.35,
                    decoration: TextDecoration.none,
                  ),
                ),

                const SizedBox(height: 16),

                const MiniLineChart(
                  values: riskSeries,
                ),

                const SizedBox(height: 8),

                const Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    _SmallLabel('Now'),
                    _SmallLabel('+1h'),
                    _SmallLabel('+2h'),
                    _SmallLabel('+3h'),
                    _SmallLabel('+4h'),
                    _SmallLabel('+6h'),
                  ],
                ),
              ],
            ),
          ),

          const SizedBox(height: 14),

          // STORM DIRECTION
          AppCard(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: accent.withOpacity(.10),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Icon(
                        Icons.navigation_outlined,
                        color: iconColor,
                        size: 22,
                      ),
                    ),

                    const SizedBox(width: 12),

                    const Expanded(
                      child: Text(
                        'Where the storm is going',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w800,
                          color: textHi,
                          decoration: TextDecoration.none,
                        ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 12),

                const Text(
                  'Cell C-14 is 34 km away and moving towards you at 27 km/h.',
                  style: TextStyle(
                    fontSize: 12.5,
                    color: textMid,
                    height: 1.4,
                    decoration: TextDecoration.none,
                  ),
                ),

                const SizedBox(height: 16),

                const Row(
                  children: [
                    _Stat(
                      label: 'Reaches you',
                      value: '6:40 PM',
                    ),
                    _Stat(
                      label: 'Clears',
                      value: '7:55 PM',
                    ),
                    _Stat(
                      label: 'Duration',
                      value: '~75 min',
                    ),
                  ],
                ),
              ],
            ),
          ),

          const SizedBox(height: 20),

          const SectionHeader(
            title: 'Hour by hour',
            meta: 'Risk score',
          ),

          const SizedBox(height: 8),

          // HOURLY RISK
          AppCard(
            padding: const EdgeInsets.all(18),
            child: Column(
              children: [
                for (int i = 0; i < 6; i++)
                  Padding(
                    padding: EdgeInsets.only(
                      bottom: i == 5 ? 0 : 14,
                    ),
                    child: Row(
                      children: [
                        SizedBox(
                          width: 42,
                          child: Text(
                            i == 0 ? 'Now' : '+${i}h',
                            style: const TextStyle(
                              fontSize: 11,
                              color: textLo,
                              decoration: TextDecoration.none,
                            ),
                          ),
                        ),

                        Expanded(
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(99),
                            child: LinearProgressIndicator(
                              value: riskSeries[i * 2] / 100,
                              minHeight: 7,
                              backgroundColor: night600,
                              valueColor:
                                  AlwaysStoppedAnimation<Color>(
                                riskColor(riskSeries[i * 2]),
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(width: 10),

                        SizedBox(
                          width: 28,
                          child: Text(
                            '${riskSeries[i * 2]}',
                            textAlign: TextAlign.right,
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w800,
                              color: riskColor(
                                riskSeries[i * 2],
                              ),
                              decoration: TextDecoration.none,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
              ],
            ),
          ),

          const SizedBox(height: 14),

          // AI CONFIDENCE
          AppCard(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(9),
                  decoration: BoxDecoration(
                    color: accent.withOpacity(.10),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    Icons.verified_outlined,
                    color: iconColor,
                    size: 21,
                  ),
                ),

                const SizedBox(width: 12),

                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '91% confidence',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w800,
                          color: textHi,
                          decoration: TextDecoration.none,
                        ),
                      ),

                      SizedBox(height: 4),

                      Text(
                        'Radar · satellite IR · lightning · rain gauges',
                        style: TextStyle(
                          fontSize: 11.5,
                          color: textMid,
                          decoration: TextDecoration.none,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // AI RECOMMENDATION
          AppCard(
            color: weatherTheme.backgroundSecondary,
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(
                  Icons.auto_awesome,
                  color: accent,
                  size: 21,
                ),

                const SizedBox(width: 12),

                const Expanded(
                  child: Text(
                    'AI recommendation: plan to be indoors before the storm reaches your area.',
                    style: TextStyle(
                      fontSize: 13,
                      color: textHi,
                      fontWeight: FontWeight.w700,
                      height: 1.35,
                      decoration: TextDecoration.none,
                    ),
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

class _SmallLabel extends StatelessWidget {
  final String text;

  const _SmallLabel(this.text);

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(
        fontSize: 9.5,
        color: textLo,
        decoration: TextDecoration.none,
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  final String label;
  final String value;

  const _Stat({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(
              fontSize: 9.5,
              color: textLo,
              decoration: TextDecoration.none,
            ),
          ),

          const SizedBox(height: 3),

          Text(
            value,
            style: const TextStyle(
              fontSize: 11.5,
              fontWeight: FontWeight.w800,
              color: textHi,
              decoration: TextDecoration.none,
            ),
          ),
        ],
      ),
    );
  }
}