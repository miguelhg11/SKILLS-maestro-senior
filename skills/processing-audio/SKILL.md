---
name: processing-audio
description: Implement audio intelligence including Speech-to-Text (ASR), Text-to-Speech (TTS), and audio analysis. Covers integration with Whisper, ElevenLabs, Deepgram, and handling real-time audio streams. Use when building voice interfaces, transcription services, or accessibility features.
---

# Processing Audio

## Purpose

This skill provides patterns for incorporating audio intelligence into applications. It covers the transformation of voice to text (transcription), text to voice (synthesis), and the manipulation of audio data for AI workflows.

## When to Use

**Use this skill when:**
- Building voice-controlled applications.
- Transcribing meetings, podcasts, or uploaded files.
- Generating realistic voiceovers for content.
- Implementing accessibility features for visually impaired users.
- Analyzing sentiment or emotional tone in audio.

## Quick Start

### Transcription with OpenAI Whisper (Python)

Whisper is the current state-of-the-art for general-purpose transcription.

```python
from openai import OpenAI

client = OpenAI()

def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript

# Usage
# text = transcribe_audio("recording.mp3")
# print(text)
```

## Core Concepts

### 1. Speech-to-Text (STT / ASR)
Converting audio to text.
- **Batch Processing**: Uploading a whole file and waiting for the result (e.g., OpenAI Whisper API). Best for accuracy.
- **Streaming (Real-time)**: Sending audio chunks and receiving partial transcripts (e.g., Deepgram, google-cloud-speech). Best for responsiveness.
- **Diarization**: Distinguishing *who* is speaking ("Speaker A", "Speaker B").

### 2. Text-to-Speech (TTS)
Converting text to audio.
- **Neural TTS**: Uses deep learning to generate human-like speech (ElevenLabs, OpenAI Audio).
- **Latency**: Critical for conversational agents. Streaming audio response is preferred over generating the full file.

### 3. Audio Formats & Codecs
- **WAV**: Uncompressed, large. Good for processing.
- **MP3/AAC**: Compressed, consumer standard.
- **Sample Rate**: 16kHz is standard for voice ML; 44.1kHz+ for music.
- **Chunks/Frames**: Processing audio in small windows (e.g., 20ms) for real-time analysis.

## Advanced Patterns

### Real-time Voice Agent (Streaming)
Latency is key. A typical pipeline:
1.  **VAD (Voice Activity Detection)**: Detect when user starts/stops speaking (e.g., Silero VAD).
2.  **STT Stream**: Send detected audio to STT provider.
3.  **LLM**: Send transcript to LLM.
4.  **TTS Stream**: Send LLM response to TTS provider.
5.  **Playback**: Stream received audio bytes to client immediately.

### Deepgram Streaming Example (Python)
```python
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
import asyncio

async def stream_transcription():
    deepgram = DeepgramClient("YOUR_KEY")
    
    connection = deepgram.listen.live.v("1")
    
    def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if sentence:
            print(f"Transcript: {sentence}")

    connection.on(LiveTranscriptionEvents.Transcript, on_message)
    
    options = LiveOptions(model="nova-2", language="en-US")
    await connection.start(options)
    
    # ... send audio bytes to connection.send(data) ...
```

## Decision Framework

### STT Provider Selection
| Provider | Pros | Cons | Best For |
|:---|:---|:---|:---|
| **OpenAI Whisper** | High accuracy, multi-language | Slower (API), no streaming | General purpose, async |
| **Deepgram** | Extremely fast, streaming support | Cost at scale | Real-time agents |
| **AssemblyAI** | Great features (summarization, lemur) | Latency moderate | Analytics, podcasts |
| **Local Whisper** | Free, private | High VRAM usage | Privacy-sensitive, zero-cost |

### TTS Provider Selection
| Provider | Pros | Cons | Best For |
|:---|:---|:---|:---|
| **ElevenLabs** | Best emotional range, voice cloning | Expensive | Creative content, personalized agents |
| **OpenAI TTS** | Good quality, cheaper | Fewer voices, less control | General assistants |
| **Azure/Google** | Reliable, fast, many languages | More "robotic" feel | Enterprise, telephony |

## Integration with Other Skills
- **`building-browser-agents`**: Give your browser agent a "voice" to read page content or listen to commands.
- **`managing-media`**: Handle the storage and playback of the generated/recorded audio files.
- **`ai-data-engineering`**: Process audio logs for RAG (retrieval-augmented generation).
