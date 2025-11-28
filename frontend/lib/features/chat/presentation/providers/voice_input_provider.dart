import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

class VoiceInputState {
  final bool isRecording;
  final String? recordingPath;
  final Duration recordingDuration;
  final bool isProcessing;
  final String? error;

  const VoiceInputState({
    this.isRecording = false,
    this.recordingPath,
    this.recordingDuration = Duration.zero,
    this.isProcessing = false,
    this.error,
  });

  VoiceInputState copyWith({
    bool? isRecording,
    String? recordingPath,
    Duration? recordingDuration,
    bool? isProcessing,
    String? error,
  }) {
    return VoiceInputState(
      isRecording: isRecording ?? this.isRecording,
      recordingPath: recordingPath ?? this.recordingPath,
      recordingDuration: recordingDuration ?? this.recordingDuration,
      isProcessing: isProcessing ?? this.isProcessing,
      error: error ?? this.error,
    );
  }
}

class VoiceInputNotifier extends StateNotifier<VoiceInputState> {
  final AudioRecorder _audioRecorder = AudioRecorder();
  DateTime? _recordingStartTime;

  VoiceInputNotifier() : super(const VoiceInputState());

  Future<void> startRecording() async {
    try {
      // Check permissions
      final hasPermission = await _audioRecorder.hasPermission();
      if (!hasPermission) {
        state = state.copyWith(error: 'Không có quyền truy cập micro');
        return;
      }

      // Get temporary directory for recording
      final tempDir = await getTemporaryDirectory();
      final filePath = '${tempDir.path}/voice_input_${DateTime.now().millisecondsSinceEpoch}.wav';

      // Start recording
      await _audioRecorder.start(
        const RecordConfig(
          encoder: AudioEncoder.wav,
          sampleRate: 16000,
          numChannels: 1,
        ),
        path: filePath,
      );

      _recordingStartTime = DateTime.now();
      state = state.copyWith(
        isRecording: true,
        recordingPath: filePath,
        recordingDuration: Duration.zero,
        error: null,
      );

      // Start duration timer
      _startDurationTimer();
    } catch (e) {
      state = state.copyWith(
        error: 'Không thể bắt đầu ghi âm: $e',
        isRecording: false,
      );
    }
  }

  Future<String?> stopRecording() async {
    if (!state.isRecording) return null;

    try {
      final path = await _audioRecorder.stop();
      _recordingStartTime = null;

      state = state.copyWith(
        isRecording: false,
        isProcessing: true,
      );

      if (path != null) {
        // Convert speech to text
        final text = await _speechToText(path);
        state = state.copyWith(isProcessing: false);
        return text;
      }
    } catch (e) {
      state = state.copyWith(
        isRecording: false,
        isProcessing: false,
        error: 'Lỗi khi dừng ghi âm: $e',
      );
    }

    state = state.copyWith(isProcessing: false);
    return null;
  }

  void _startDurationTimer() {
    Future.doWhile(() async {
      if (!state.isRecording || _recordingStartTime == null) return false;

      await Future.delayed(const Duration(milliseconds: 100));
      final duration = DateTime.now().difference(_recordingStartTime!);
      state = state.copyWith(recordingDuration: duration);

      return true;
    });
  }

  Future<String?> _speechToText(String audioPath) async {
    try {
      // TODO: Implement actual speech-to-text service integration
      // This should call a real speech recognition API like:
      // - Google Cloud Speech-to-Text
      // - Azure Speech Services 
      // - Amazon Transcribe
      // - OpenAI Whisper API
      
      await Future.delayed(const Duration(seconds: 2)); // Simulate processing
      
      // For now, return a placeholder until speech service is integrated
      state = state.copyWith(error: 'Speech-to-text service not yet implemented');
      return null;
    } catch (e) {
      state = state.copyWith(error: 'Không thể chuyển đổi giọng nói thành văn bản');
      return null;
    }
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

final voiceInputProvider = StateNotifierProvider<VoiceInputNotifier, VoiceInputState>((ref) {
  return VoiceInputNotifier();
});