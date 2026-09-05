class HazardData {
  final String name;
  final int probability;
  final String detail;
  final IconDataKey icon;

  const HazardData(this.name, this.probability, this.detail, this.icon);
}

enum IconDataKey { lightning, storm, wind, rain, hail, cloudburst }

const currentTemp = 31;
const feelsLike = 38;
const humidity = 84;
const wind = 18;
const gust = 34;
const riskScore = 87;
const confidence = 91;
const stormEta = 42;

const riskSeries = [46, 58, 74, 88, 92, 84, 68, 49, 34, 24, 18, 14, 12];

const hazards = [
  HazardData('Lightning', 94, '1,240 strikes detected in the last 20 min', IconDataKey.lightning),
  HazardData('Thunderstorm', 91, 'Cloud tops at 14.2 km, still deepening', IconDataKey.storm),
  HazardData('Strong wind', 78, 'Gust front modelled at 70–85 km/h', IconDataKey.wind),
  HazardData('Heavy rain', 72, '45–60 mm expected in the first hour', IconDataKey.rain),
  HazardData('Hail', 41, 'Small hail possible, 1–2 cm in the core', IconDataKey.hail),
  HazardData('Cloudburst', 28, 'Localised burst risk over eastern drainage', IconDataKey.cloudburst),
];

String iconFor(IconDataKey key) {
  switch (key) {
    case IconDataKey.lightning:
      return '⚡';
    case IconDataKey.storm:
      return '⛈';
    case IconDataKey.wind:
      return '≋';
    case IconDataKey.rain:
      return '☂';
    case IconDataKey.hail:
      return '•';
    case IconDataKey.cloudburst:
      return '☁';
  }
}
