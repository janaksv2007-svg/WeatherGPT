import 'package:flutter/material.dart';
import '../widgets.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool alerts = true;
  double threshold = 60;
  String language = 'English';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF060910),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text('Settings', style: TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
        children: [
          const SectionHeader(title: 'Language', meta: 'AI and alerts'),
          AppCard(child: Column(children: [
            for (final l in ['English', 'தமிழ்', 'हिन्दी'])
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.language_outlined, color: teal),
                title: Text(l, style: const TextStyle(color: textHi, fontWeight: FontWeight.w700)),
                trailing: language == l ? const Icon(Icons.check, color: teal) : null,
                onTap: () => setState(() => language = l),
              ),
          ])),
          const SizedBox(height: 18),
          const SectionHeader(title: 'Alerts', meta: 'Your warning preferences'),
          AppCard(child: Column(children: [
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('Push warnings', style: TextStyle(color: textHi, fontWeight: FontWeight.w700)),
              subtitle: const Text('Storm arrival, lightning and flooding', style: TextStyle(color: textLo)),
              value: alerts,
              activeColor: teal,
              onChanged: (v) => setState(() => alerts = v),
            ),
            const Divider(color: line),
            Row(children: [
              const Text('Warn me above risk score', style: TextStyle(color: textMid, fontWeight: FontWeight.w700)),
              const Spacer(),
              Text('${threshold.round()}', style: const TextStyle(color: teal, fontWeight: FontWeight.w900)),
            ]),
            Slider(value: threshold, min: 20, max: 90, divisions: 14, activeColor: teal, inactiveColor: night600, onChanged: (v) => setState(() => threshold = v)),
          ])),
          const SizedBox(height: 18),
          const AppCard(child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Icon(Icons.info_outline, color: textMid),
            SizedBox(width: 12),
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('About WeatherGPT', style: TextStyle(fontWeight: FontWeight.w800, color: textHi)),
              SizedBox(height: 5),
              Text('Short-range storm forecasting for the next 6 hours. Radar, satellite, lightning sensors and local rain gauges are combined into one risk score with plain-language advice.', style: TextStyle(fontSize: 12.5, color: textMid, height: 1.4)),
              SizedBox(height: 7),
              Text('MVP UI · grid 1 km · refresh 5 min', style: TextStyle(fontSize: 10.5, color: textLo)),
            ])),
          ])),
        ],
      ),
    );
  }
}
