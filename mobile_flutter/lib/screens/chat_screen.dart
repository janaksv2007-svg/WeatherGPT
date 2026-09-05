import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  bool _isLoading = false;

  final List<Map<String, dynamic>> _messages = [
    {
      'role': 'ai',
      'text':
          'Hi! I’m WeatherGPT 👋\nAsk me about storms, rain forecasts, risk scores, travel weather, or What-If scenarios.'
    },
  ];

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _isLoading) return;

    setState(() {
      _messages.add({
        'role': 'user',
        'text': text,
      });
      _controller.clear();
      _isLoading = true;
    });
    _scrollToBottom();

    try {
      // Call backend POST /chat
      final result = await ApiService.sendChatMessage(message: text);

      String responseText = result['response'] ?? '';
      final weather = result['weather'];
      final risk = result['risk'];
      final simulation = result['simulation'];

      if (responseText.isEmpty) {
        responseText = _getLocalFallback(text);
      }

      setState(() {
        _messages.add({
          'role': 'ai',
          'text': responseText,
          'weather': weather,
          'risk': risk,
          'simulation': simulation,
        });
      });
    } catch (e) {
      setState(() {
        _messages.add({
          'role': 'ai',
          'text': _getLocalFallback(text),
        });
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
      _scrollToBottom();
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  String _getLocalFallback(String text) {
    final question = text.toLowerCase();
    if (question.contains('rain') || question.contains('umbrella')) {
      return '🌧️ Rain is possible in Chennai. Carrying an umbrella is recommended for changing weather conditions.';
    } else if (question.contains('storm') || question.contains('risk')) {
      return '⛈️ Storm Risk Score: 87/100 — HIGH.\nHeavy rain, lightning and gusty winds reported nearby.';
    } else if (question.contains('lightning')) {
      return '⚡ Lightning Risk is HIGH. Please remain indoors and stay away from open areas until conditions improve.';
    } else {
      return '🌤️ WeatherGPT is ready. Ask about forecasts, risk levels, or What-If scenarios!';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF050B14),
      appBar: AppBar(
        backgroundColor: const Color(0xFF050B14),
        foregroundColor: Colors.white,
        elevation: 0,
        title: const Row(
          children: [
            CircleAvatar(
              radius: 18,
              backgroundColor: Color(0xFF6C4DFF),
              child: Icon(
                Icons.auto_awesome,
                color: Colors.white,
                size: 19,
              ),
            ),
            SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'WeatherGPT',
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  'AI Weather & Risk Assistant',
                  style: TextStyle(
                    fontSize: 11,
                    color: Color(0xFF8D99AE),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(18),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message['role'] == 'user';
                final weather = message['weather'];
                final risk = message['risk'];
                final sim = message['simulation'];

                return Align(
                  alignment:
                      isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 14),
                    padding: const EdgeInsets.all(15),
                    constraints: const BoxConstraints(maxWidth: 340),
                    decoration: BoxDecoration(
                      color: isUser
                          ? const Color(0xFF123B45)
                          : const Color(0xFF111927),
                      borderRadius: BorderRadius.circular(18),
                      border: Border.all(
                        color: isUser
                            ? const Color(0xFF1F5463)
                            : const Color(0xFF1C2A3A),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          message['text'] ?? '',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 14,
                            height: 1.45,
                          ),
                        ),
                        if (weather != null && weather is Map) ...[
                          const SizedBox(height: 10),
                          Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: const Color(0xFF0A121E),
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                  color: Colors.blueAccent.withOpacity(0.3)),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.wb_sunny_outlined,
                                    color: Colors.amber, size: 20),
                                const SizedBox(width: 8),
                                Text(
                                  '${weather['location'] ?? 'Chennai'}: ${weather['temperature'] ?? 29}°C | ${weather['condition'] ?? 'Clear'}',
                                  style: const TextStyle(
                                      color: Colors.white70, fontSize: 12),
                                ),
                              ],
                            ),
                          ),
                        ],
                        if (risk != null && risk is Map) ...[
                          const SizedBox(height: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10, vertical: 6),
                            decoration: BoxDecoration(
                              color: risk['risk_level'] == 'HIGH'
                                  ? Colors.redAccent.withOpacity(0.2)
                                  : Colors.orangeAccent.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: risk['risk_level'] == 'HIGH'
                                    ? Colors.redAccent
                                    : Colors.orangeAccent,
                              ),
                            ),
                            child: Text(
                              '⚠️ Risk Score: ${risk['risk_score']}/100 — ${risk['risk_level']}',
                              style: TextStyle(
                                color: risk['risk_level'] == 'HIGH'
                                    ? Colors.redAccent
                                    : Colors.orangeAccent,
                                fontWeight: FontWeight.bold,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 8),
              child: SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(
                    strokeWidth: 2, color: Color(0xFF6C4DFF)),
              ),
            ),
          // Quick Question Chips
          SizedBox(
            height: 44,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 14),
              children: [
                _quickQuestion('🌧 Will it rain in Chennai?'),
                _quickQuestion('⚡ What is current storm risk?'),
                _quickQuestion('What if rainfall reaches 100mm?'),
                _quickQuestion('🛡 Safety precautions?'),
              ],
            ),
          ),
          const SizedBox(height: 10),
          // Input row
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(14, 0, 14, 14),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      style: const TextStyle(color: Colors.white),
                      onSubmitted: (_) => _sendMessage(),
                      decoration: InputDecoration(
                        hintText: 'Ask WeatherGPT AI...',
                        hintStyle: const TextStyle(color: Color(0xFF667085)),
                        filled: true,
                        fillColor: const Color(0xFF111927),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(18),
                          borderSide:
                              const BorderSide(color: Color(0xFF1C2A3A)),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFF6C4DFF),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: IconButton(
                      onPressed: _sendMessage,
                      icon: const Icon(Icons.arrow_upward, color: Colors.white),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _quickQuestion(String text) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ActionChip(
        label: Text(text),
        backgroundColor: const Color(0xFF111927),
        side: const BorderSide(color: Color(0xFF263548)),
        labelStyle: const TextStyle(color: Colors.white, fontSize: 12),
        onPressed: () {
          _controller.text = text;
          _sendMessage();
        },
      ),
    );
  }
}