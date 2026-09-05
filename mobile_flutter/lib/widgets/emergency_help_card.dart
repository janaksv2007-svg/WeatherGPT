import 'package:flutter/material.dart';

class EmergencyHelpCard extends StatelessWidget {
  const EmergencyHelpCard({super.key});

  void _showEmergencyInfo(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: const Color(0xFF111827),
          title: const Row(
            children: [
              Icon(
                Icons.emergency_rounded,
                color: Color(0xFFEF4444),
              ),
              SizedBox(width: 10),
              Text(
                'Emergency Help',
                style: TextStyle(
                  color: Color(0xFFF1F5F9),
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
          content: const Text(
            'If you are in immediate danger or need emergency assistance, call 112.\n\n'
            '112 is the unified emergency number in India for police, fire, medical and other emergency assistance.',
            style: TextStyle(
              color: Color(0xFFCBD5E1),
              height: 1.5,
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text(
                'Close',
                style: TextStyle(
                  color: Color(0xFF2DD4BF),
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1A1114),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(
          color: const Color(0xFF4A2026),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(9),
                decoration: BoxDecoration(
                  color: const Color(0xFFEF4444).withOpacity(.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.emergency_rounded,
                  color: Color(0xFFEF4444),
                  size: 22,
                ),
              ),

              const SizedBox(width: 12),

              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Need immediate help?',
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: Color(0xFFF1F5F9),
                      ),
                    ),

                    SizedBox(height: 3),

                    Text(
                      'Emergency assistance is available 24/7.',
                      style: TextStyle(
                        fontSize: 11.5,
                        color: Color(0xFF9FB0C9),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),

          const SizedBox(height: 14),

          GestureDetector(
            onTap: () => _showEmergencyInfo(context),
            child: Container(
              padding: const EdgeInsets.symmetric(
                horizontal: 14,
                vertical: 13,
              ),
              decoration: BoxDecoration(
                color: const Color(0xFFEF4444).withOpacity(.10),
                borderRadius: BorderRadius.circular(13),
                border: Border.all(
                  color: const Color(0xFFEF4444).withOpacity(.35),
                ),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.phone_in_talk_rounded,
                    color: Color(0xFFEF4444),
                    size: 21,
                  ),

                  const SizedBox(width: 10),

                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Emergency Services',
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w700,
                            color: Color(0xFFF1F5F9),
                          ),
                        ),

                        SizedBox(height: 2),

                        Text(
                          '112 · Police · Fire · Medical',
                          style: TextStyle(
                            fontSize: 11,
                            color: Color(0xFF9FB0C9),
                          ),
                        ),
                      ],
                    ),
                  ),

                  const Text(
                    '112',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w900,
                      color: Color(0xFFEF4444),
                    ),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 9),

          GestureDetector(
            onTap: () => _showEmergencyInfo(context),
            child: const Row(
              children: [
                Icon(
                  Icons.info_outline,
                  size: 14,
                  color: Color(0xFF76859E),
                ),

                SizedBox(width: 6),

                Expanded(
                  child: Text(
                    'Tap for emergency information',
                    style: TextStyle(
                      fontSize: 10.5,
                      color: Color(0xFF76859E),
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