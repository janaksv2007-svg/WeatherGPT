import 'package:flutter/material.dart';
import '../widgets.dart';
import '../weather_theme.dart';

class RiskMapScreen extends StatefulWidget {
  const RiskMapScreen({super.key});

  @override
  State<RiskMapScreen> createState() => _RiskMapScreenState();
}

class _RiskMapScreenState extends State<RiskMapScreen> {
  double hours = 0;
  String selected = 'C-14';

  @override
  Widget build(BuildContext context) {
    final weatherTheme =
        WeatherTheme.forCondition(currentWeatherCondition);

    final accent = weatherTheme.accent;
    final iconColor = weatherTheme.iconColor;

    return Scaffold(
      backgroundColor: weatherTheme.background,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 30),
          children: [
            TopHeader(
              title: 'Storm map',
              subtitle: '3 storms tracked within 60 km of you',
            ),

            const SizedBox(height: 18),

            // ============================================================
            // MAP
            // ============================================================
            AppCard(
              padding: EdgeInsets.zero,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: SizedBox(
                  height: 330,
                  child: CustomPaint(
                    painter: RadarMapPainter(
                      hours: hours,
                      selected: selected,
                      accent: accent,
                      iconColor: iconColor,
                      background: weatherTheme.backgroundSecondary,
                    ),
                    child: Stack(
                      children: [
                        Positioned(
                          top: 14,
                          left: 14,
                          child: _MapChip(
                            icon: Icons.layers_outlined,
                            text: 'Layers',
                            iconColor: iconColor,
                            accent: accent,
                          ),
                        ),

                        Positioned(
                          bottom: 14,
                          right: 14,
                          child: _MapChip(
                            icon: Icons.my_location,
                            text: 'You',
                            iconColor: iconColor,
                            accent: accent,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 12),

            // ============================================================
            // LEGEND
            // ============================================================
            Row(
              children: const [
                _Legend(
                  color: riskLow,
                  text: 'Weak',
                ),
                SizedBox(width: 14),
                _Legend(
                  color: riskMod,
                  text: 'Moderate',
                ),
                SizedBox(width: 14),
                _Legend(
                  color: riskHigh,
                  text: 'Severe',
                ),
                SizedBox(width: 14),
                _Legend(
                  color: teal,
                  text: 'You',
                ),
              ],
            ),

            const SizedBox(height: 18),

            // ============================================================
            // FORECAST TIME
            // ============================================================
            const SectionHeader(
              title: 'Forecast time',
              meta: 'Now → +6h',
            ),

            AppCard(
              color: weatherTheme.cardColor,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.schedule_outlined,
                        size: 18,
                        color: iconColor,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        hours == 0
                            ? 'Now'
                            : '+${hours.toStringAsFixed(1)} hours',
                        style: const TextStyle(
                          color: textHi,
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 6),

                  SliderTheme(
                    data: SliderTheme.of(context).copyWith(
                      activeTrackColor: accent,
                      thumbColor: iconColor,
                      inactiveTrackColor: line,
                      overlayColor: accent.withOpacity(0.12),
                    ),
                    child: Slider(
                      value: hours,
                      min: 0,
                      max: 6,
                      divisions: 12,
                      onChanged: (value) {
                        setState(() {
                          hours = value;
                        });
                      },
                    ),
                  ),

                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'NOW',
                        style: TextStyle(
                          color: textLo,
                          fontSize: 10,
                        ),
                      ),
                      Text(
                        '+6 HOURS',
                        style: TextStyle(
                          color: textLo,
                          fontSize: 10,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 22),

            // ============================================================
            // STORMS
            // ============================================================
            const SectionHeader(
              title: 'Storms nearby',
              meta: 'Tap to highlight',
            ),

            _StormCard(
              id: 'C-14',
              strength: 88,
              label: 'Severe',
              color: riskHigh,
              selected: selected == 'C-14',
              onTap: () {
                setState(() {
                  selected = 'C-14';
                });
              },
              accent: accent,
              iconColor: iconColor,
            ),

            const SizedBox(height: 10),

            _StormCard(
              id: 'C-19',
              strength: 61,
              label: 'Moderate',
              color: riskMod,
              selected: selected == 'C-19',
              onTap: () {
                setState(() {
                  selected = 'C-19';
                });
              },
              accent: accent,
              iconColor: iconColor,
            ),

            const SizedBox(height: 10),

            _StormCard(
              id: 'C-22',
              strength: 33,
              label: 'Weak',
              color: riskLow,
              selected: selected == 'C-22',
              onTap: () {
                setState(() {
                  selected = 'C-22';
                });
              },
              accent: accent,
              iconColor: iconColor,
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// STORM CARD
// ============================================================================

class _StormCard extends StatelessWidget {
  final String id;
  final int strength;
  final String label;
  final Color color;
  final bool selected;
  final VoidCallback onTap;
  final Color accent;
  final Color iconColor;

  const _StormCard({
    required this.id,
    required this.strength,
    required this.label,
    required this.color,
    required this.selected,
    required this.onTap,
    required this.accent,
    required this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AppCard(
        color: selected
            ? accent.withOpacity(0.10)
            : const Color(0xFF0C1220),
        child: Row(
          children: [
            Container(
              width: 42,
              height: 42,
              decoration: BoxDecoration(
                color: color.withOpacity(.10),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: color.withOpacity(.30),
                ),
              ),
              child: Icon(
                Icons.thunderstorm_outlined,
                color: color,
                size: 21,
              ),
            ),

            const SizedBox(width: 12),

            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Storm cell $id',
                    style: const TextStyle(
                      color: textHi,
                      fontSize: 14,
                      fontWeight: FontWeight.w800,
                    ),
                  ),

                  const SizedBox(height: 4),

                  Text(
                    '$label · $strength% intensity',
                    style: TextStyle(
                      color: color,
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),

            Icon(
              selected
                  ? Icons.radio_button_checked
                  : Icons.radio_button_unchecked,
              color: selected ? iconColor : textLo,
              size: 20,
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// RADAR MAP
// ============================================================================

class RadarMapPainter extends CustomPainter {
  final double hours;
  final String selected;
  final Color accent;
  final Color iconColor;
  final Color background;

  RadarMapPainter({
    required this.hours,
    required this.selected,
    required this.accent,
    required this.iconColor,
    required this.background,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final mapBackground = Paint()
      ..color = background;

    canvas.drawRect(
      Offset.zero & size,
      mapBackground,
    );

    // ============================================================
    // GRID
    // ============================================================

    final grid = Paint()
      ..color = const Color(0xFF1A2940)
      ..strokeWidth = 1;

    for (int i = 1; i < 10; i++) {
      final x = size.width * i / 10;
      final y = size.height * i / 10;

      canvas.drawLine(
        Offset(x, 0),
        Offset(x, size.height),
        grid,
      );

      canvas.drawLine(
        Offset(0, y),
        Offset(size.width, y),
        grid,
      );
    }

    final user = Offset(
      size.width * .50,
      size.height * .62,
    );

    // ============================================================
    // RADAR CIRCLES
    // ============================================================

    for (final radius in [42.0, 84.0, 126.0]) {
      canvas.drawCircle(
        user,
        radius,
        Paint()
          ..color = accent.withOpacity(.18)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1,
      );
    }

    // ============================================================
    // STORM CELLS
    // ============================================================

    void drawStorm(
      String id,
      double x,
      double y,
      double radius,
      Color color,
    ) {
      final point = Offset(x, y);

      canvas.drawCircle(
        point,
        radius * 1.55,
        Paint()..color = color.withOpacity(.05),
      );

      canvas.drawCircle(
        point,
        radius,
        Paint()..color = color.withOpacity(.14),
      );

      canvas.drawCircle(
        point,
        radius * .62,
        Paint()..color = color.withOpacity(.26),
      );

      canvas.drawCircle(
        point,
        radius * .30,
        Paint()..color = color.withOpacity(.80),
      );

      if (selected == id) {
        canvas.drawCircle(
          point,
          radius + 7,
          Paint()
            ..color = color
            ..style = PaintingStyle.stroke
            ..strokeWidth = 2,
        );
      }

      final textPainter = TextPainter(
        text: TextSpan(
          text: id,
          style: const TextStyle(
            color: textHi,
            fontSize: 11,
            fontWeight: FontWeight.w700,
          ),
        ),
        textDirection: TextDirection.ltr,
      )..layout();

      textPainter.paint(
        canvas,
        Offset(
          x - textPainter.width / 2,
          y - radius - 18,
        ),
      );
    }

    drawStorm(
      'C-14',
      size.width * (.30 + .16 * hours / 6),
      size.height * (.44 + .14 * hours / 6),
      43,
      riskHigh,
    );

    drawStorm(
      'C-19',
      size.width * (.16 + .13 * hours / 6),
      size.height * (.72 - .04 * hours / 6),
      28,
      riskMod,
    );

    drawStorm(
      'C-22',
      size.width * (.74 + .06 * hours / 6),
      size.height * (.26 + .07 * hours / 6),
      20,
      riskLow,
    );

    // ============================================================
    // YOU
    // ============================================================

    canvas.drawCircle(
      user,
      8,
      Paint()..color = iconColor,
    );

    canvas.drawCircle(
      user,
      23,
      Paint()..color = accent.withOpacity(.10),
    );

    final youText = TextPainter(
      text: const TextSpan(
        text: 'You',
        style: TextStyle(
          color: textMid,
          fontSize: 11,
          fontWeight: FontWeight.w700,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout();

    youText.paint(
      canvas,
      Offset(
        user.dx - youText.width / 2,
        user.dy + 28,
      ),
    );
  }

  @override
  bool shouldRepaint(
    covariant RadarMapPainter oldDelegate,
  ) {
    return oldDelegate.hours != hours ||
        oldDelegate.selected != selected ||
        oldDelegate.accent != accent ||
        oldDelegate.iconColor != iconColor ||
        oldDelegate.background != background;
  }
}

// ============================================================================
// LEGEND
// ============================================================================

class _Legend extends StatelessWidget {
  final Color color;
  final String text;

  const _Legend({
    required this.color,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 7,
          height: 7,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: color,
          ),
        ),

        const SizedBox(width: 5),

        Text(
          text,
          style: const TextStyle(
            color: textLo,
            fontSize: 10.5,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }
}

// ============================================================================
// MAP CHIP
// ============================================================================

class _MapChip extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color iconColor;
  final Color accent;

  const _MapChip({
    required this.icon,
    required this.text,
    required this.iconColor,
    required this.accent,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 10,
        vertical: 7,
      ),
      decoration: BoxDecoration(
        color: const Color(0xE6101828),
        borderRadius: BorderRadius.circular(99),
        border: Border.all(
          color: accent.withOpacity(.30),
        ),
      ),
      child: Row(
        children: [
          Icon(
            icon,
            size: 14,
            color: iconColor,
          ),

          const SizedBox(width: 5),

          Text(
            text,
            style: const TextStyle(
              color: textMid,
              fontSize: 10.5,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}