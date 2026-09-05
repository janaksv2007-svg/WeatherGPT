import 'package:flutter/material.dart';
import 'data/mock_data.dart';

const night800 = Color(0xFF0C1220);
const night700 = Color(0xFF121A2B);
const night600 = Color(0xFF18223A);
const line = Color(0xFF1E2940);
const teal = Color(0xFF2DD4BF);
const textHi = Color(0xFFF1F5F9);
const textMid = Color(0xFF9FB0C9);
const textLo = Color(0xFF76859E);
const riskLow = Color(0xFF34D399);
const riskMod = Color(0xFFF59E0B);
const riskHigh = Color(0xFFEF4444);
const aiPurple = Color(0xFFA855F7);

Color riskColor(int score) {
  if (score >= 67) return riskHigh;
  if (score >= 34) return riskMod;
  return riskLow;
}

class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry padding;
  final Color? color;

  const AppCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(16),
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: color ?? night800,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: line),
        boxShadow: const [
          BoxShadow(
            color: Color(0x66000000),
            blurRadius: 24,
            offset: Offset(0, 10),
          ),
        ],
      ),
      child: child,
    );
  }
}

class SectionHeader extends StatelessWidget {
  final String title;
  final String? meta;

  const SectionHeader({
    super.key,
    required this.title,
    this.meta,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Expanded(
            child: Text(
              title,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w700,
                color: textHi,
              ),
            ),
          ),
          if (meta != null)
            Text(
              meta!,
              style: const TextStyle(
                fontSize: 11,
                color: textLo,
              ),
            ),
        ],
      ),
    );
  }
}

class TopHeader extends StatelessWidget {
  final String title;
  final String subtitle;
  final VoidCallback? onSettings;

  const TopHeader({
    super.key,
    required this.title,
    required this.subtitle,
    this.onSettings,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w800,
                  color: textHi,
                ),
              ),
              const SizedBox(height: 3),
              Text(
                subtitle,
                style: const TextStyle(
                  fontSize: 12.5,
                  color: textLo,
                ),
              ),
            ],
          ),
        ),
        if (onSettings != null)
          IconButton(
            onPressed: onSettings,
            icon: const Icon(
              Icons.settings_outlined,
              size: 21,
              color: textMid,
            ),
          ),
      ],
    );
  }
}

class RiskGauge extends StatelessWidget {
  final int score;

  const RiskGauge({
    super.key,
    required this.score,
  });

  @override
  Widget build(BuildContext context) {
    final color = riskColor(score);

    return SizedBox(
      width: 142,
      height: 142,
      child: Stack(
        alignment: Alignment.center,
        children: [
          SizedBox(
            width: 142,
            height: 142,
            child: CircularProgressIndicator(
              value: score / 100,
              strokeWidth: 11,
              backgroundColor: night600,
              valueColor: AlwaysStoppedAnimation(color),
            ),
          ),
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                '$score',
                style: TextStyle(
                  fontSize: 38,
                  fontWeight: FontWeight.w900,
                  color: color,
                ),
              ),
              const Text(
                '/100',
                style: TextStyle(
                  fontSize: 12,
                  color: textLo,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                score >= 67
                    ? 'HIGH RISK'
                    : score >= 34
                        ? 'MODERATE'
                        : 'LOW',
                style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.w800,
                  color: color,
                  letterSpacing: 1,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class MiniLineChart extends StatelessWidget {
  final List<int> values;

  const MiniLineChart({
    super.key,
    required this.values,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 100,
      width: double.infinity,
      child: CustomPaint(
        painter: LineChartPainter(values),
      ),
    );
  }
}

class LineChartPainter extends CustomPainter {
  final List<int> values;

  LineChartPainter(this.values);

  @override
  void paint(Canvas canvas, Size size) {
    final grid = Paint()
      ..color = line
      ..strokeWidth = 1;

    for (int i = 1; i < 4; i++) {
      final y = size.height * i / 4;
      canvas.drawLine(
        Offset(0, y),
        Offset(size.width, y),
        grid,
      );
    }

    final path = Path();
    final fill = Path();

    for (int i = 0; i < values.length; i++) {
      final x = i * size.width / (values.length - 1);
      final y =
          size.height -
          (values[i] / 100) * (size.height - 8) -
          4;

      if (i == 0) {
        path.moveTo(x, y);
        fill.moveTo(x, size.height);
        fill.lineTo(x, y);
      } else {
        path.lineTo(x, y);
        fill.lineTo(x, y);
      }
    }

    fill.lineTo(size.width, size.height);
    fill.close();

    canvas.drawPath(
      fill,
      Paint()..color = riskHigh.withOpacity(.10),
    );

    canvas.drawPath(
      path,
      Paint()
        ..color = teal
        ..strokeWidth = 3
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round,
    );

    final peakIndex = values.indexOf(
      values.reduce(
        (a, b) => a > b ? a : b,
      ),
    );

    final px =
        peakIndex * size.width / (values.length - 1);

    final py =
        size.height -
        (values[peakIndex] / 100) *
            (size.height - 8) -
        4;

    canvas.drawCircle(
      Offset(px, py),
      4,
      Paint()..color = riskHigh,
    );
  }

  @override
  bool shouldRepaint(
    covariant LineChartPainter oldDelegate,
  ) {
    return oldDelegate.values != values;
  }
}

class HazardTile extends StatelessWidget {
  final HazardData hazard;

  const HazardTile({
    super.key,
    required this.hazard,
  });

  @override
  Widget build(BuildContext context) {
    final color = riskColor(hazard.probability);

    return AppCard(
      padding: const EdgeInsets.all(13),
      child: Row(
        children: [
          Container(
            width: 38,
            height: 38,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: color.withOpacity(.10),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: color.withOpacity(.25),
              ),
            ),
            child: Text(
              iconFor(hazard.icon),
              style: TextStyle(
                fontSize: 18,
                color: color,
              ),
            ),
          ),
          const SizedBox(width: 11),
          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                Text(
                  hazard.name,
                  style: const TextStyle(
                    fontWeight: FontWeight.w700,
                    color: textHi,
                  ),
                ),
                const SizedBox(height: 3),
                Text(
                  hazard.detail,
                  style: const TextStyle(
                    fontSize: 11.5,
                    color: textLo,
                  ),
                ),
              ],
            ),
          ),
          Text(
            '${hazard.probability}%',
            style: TextStyle(
              fontWeight: FontWeight.w800,
              color: color,
            ),
          ),
        ],
      ),
    );
  }
}