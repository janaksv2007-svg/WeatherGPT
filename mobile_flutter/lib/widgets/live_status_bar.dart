import 'package:flutter/material.dart';

class LiveStatusBar extends StatelessWidget {
  final String updatedText;

  const LiveStatusBar({
    super.key,
    this.updatedText = 'Updated just now',
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 14,
        vertical: 11,
      ),
      decoration: BoxDecoration(
        color: const Color(0xFF0C1820),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: const Color(0xFF1D3A3A),
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 9,
            height: 9,
            decoration: const BoxDecoration(
              color: Color(0xFF34D399),
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 10),
          const Expanded(
            child: Text(
              'LIVE MONITORING',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.8,
                color: Color(0xFFF1F5F9),
              ),
            ),
          ),
          Text(
            updatedText,
            style: const TextStyle(
              fontSize: 11,
              color: Color(0xFF9FB0C9),
            ),
          ),
        ],
      ),
    );
  }
}