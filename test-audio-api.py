#!/usr/bin/env python3
import requests
import json
import base64
import time
import os
from datetime import datetime

# Base URL
BASE_URL = "https://thinkai.lat"


def log_result(test_name, success, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"[{timestamp}] {status} - {test_name}")
    if details:
        print(f"  └─ {details}")
    print()


def test_text_to_speech():
    """Test the text-to-speech endpoint"""
    print("=" * 60)
    print("🎤 Testing Text-to-Speech API")
    print("=" * 60)

    test_texts = [
        "Hello, this is a test of the audio system.",
        "The quick brown fox jumps over the lazy dog.",
        "Testing ElevenLabs integration with Think AI.",
    ]

    results = []

    for i, text in enumerate(test_texts, 1):
        try:
            print(f"\nTest {i}: Synthesizing '{text[:30]}...'")

            response = requests.post(
                f"{BASE_URL}/api/audio/synthesize",
                json={"text": text},
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                # Save audio file as evidence
                filename = f"audio-test-evidence/tts-test-{i}.mp3"
                os.makedirs("audio-test-evidence", exist_ok=True)
                with open(filename, "wb") as f:
                    f.write(response.content)

                file_size = len(response.content)
                log_result(
                    f"TTS Test {i}",
                    True,
                    f"Generated {file_size} bytes, saved to {filename}",
                )
                results.append(True)
            else:
                log_result(
                    f"TTS Test {i}",
                    False,
                    f"Status: {response.status_code}, Error: {response.text}",
                )
                results.append(False)

        except Exception as e:
            log_result(f"TTS Test {i}", False, f"Exception: {str(e)}")
            results.append(False)

    return all(results)


def test_speech_to_text():
    """Test the speech-to-text endpoint"""
    print("=" * 60)
    print("🎙️ Testing Speech-to-Text API")
    print("=" * 60)

    # Create a simple WAV file with silence (for testing)
    # This is a minimal WAV header + silent audio data
    wav_header = b"RIFF$\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00"
    silent_audio = wav_header + b"\x00" * 2048  # 2KB of silence

    try:
        print("\nTesting with mock audio data...")

        response = requests.post(
            f"{BASE_URL}/api/audio/transcribe",
            data=silent_audio,
            headers={"Content-Type": "audio/wav"},
        )

        if response.status_code == 200:
            result = response.json()
            log_result("STT Test", True, f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            log_result(
                "STT Test",
                False,
                f"Status: {response.status_code}, Error: {response.text}",
            )
            return False

    except Exception as e:
        log_result("STT Test", False, f"Exception: {str(e)}")
        return False


def test_audio_caching():
    """Test that audio caching works correctly"""
    print("=" * 60)
    print("💾 Testing Audio Caching")
    print("=" * 60)

    test_text = "This message should be cached for faster retrieval"

    try:
        # First request - should generate new audio
        print("\nFirst request (should generate new audio)...")
        start_time = time.time()
        response1 = requests.post(
            f"{BASE_URL}/api/audio/synthesize",
            json={"text": test_text},
            headers={"Content-Type": "application/json"},
        )
        time1 = time.time() - start_time

        if response1.status_code != 200:
            log_result(
                "Cache Test - First Request",
                False,
                f"Failed with status {response1.status_code}",
            )
            return False

        audio_data1 = response1.content
        print(f"  └─ Generated in {time1:.2f}s, size: {len(audio_data1)} bytes")

        # Second request - should use cache
        print("\nSecond request (should use cache)...")
        start_time = time.time()
        response2 = requests.post(
            f"{BASE_URL}/api/audio/synthesize",
            json={"text": test_text},
            headers={"Content-Type": "application/json"},
        )
        time2 = time.time() - start_time

        if response2.status_code != 200:
            log_result(
                "Cache Test - Second Request",
                False,
                f"Failed with status {response2.status_code}",
            )
            return False

        audio_data2 = response2.content
        print(f"  └─ Retrieved in {time2:.2f}s, size: {len(audio_data2)} bytes")

        # Verify cache is working
        cache_working = (
            len(audio_data1) == len(audio_data2)
            and time2 < time1 * 0.5  # Same size  # Second request should be much faster
        )

        log_result(
            "Audio Caching", cache_working, f"Cache speedup: {time1/time2:.1f}x faster"
        )

        return cache_working

    except Exception as e:
        log_result("Audio Caching", False, f"Exception: {str(e)}")
        return False


def check_cache_directory():
    """Check if cache directory exists and has files"""
    print("=" * 60)
    print("📁 Checking Audio Cache Directory")
    print("=" * 60)

    cache_dir = "/home/administrator/think_ai/audio_cache"

    if os.path.exists(cache_dir):
        files = os.listdir(cache_dir)
        mp3_files = [f for f in files if f.endswith(".mp3")]

        print(f"Cache directory: {cache_dir}")
        print(f"Total files: {len(files)}")
        print(f"MP3 files: {len(mp3_files)}")

        if mp3_files:
            print("\nCached audio files:")
            for f in mp3_files[:5]:  # Show first 5
                file_path = os.path.join(cache_dir, f)
                size = os.path.getsize(file_path)
                print(f"  - {f} ({size:,} bytes)")

            if len(mp3_files) > 5:
                print(f"  ... and {len(mp3_files) - 5} more files")

        log_result(
            "Cache Directory", True, f"Found {len(mp3_files)} cached audio files"
        )
        return True
    else:
        log_result("Cache Directory", False, "Directory does not exist")
        return False


def main():
    """Run all audio tests"""
    print("\n" + "=" * 60)
    print("🎵 THINK AI AUDIO FEATURE TEST SUITE")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")

    # Run tests
    results = {
        "Text-to-Speech": test_text_to_speech(),
        "Speech-to-Text": test_speech_to_text(),
        "Audio Caching": test_audio_caching(),
        "Cache Directory": check_cache_directory(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 60 + "\n")

    # Save summary
    summary_file = "audio-test-evidence/test-summary.json"
    os.makedirs("audio-test-evidence", exist_ok=True)
    with open(summary_file, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "base_url": BASE_URL,
                "results": results,
                "total_tests": total,
                "passed_tests": passed,
                "success_rate": passed / total,
            },
            f,
            indent=2,
        )

    print(f"📄 Test summary saved to: {summary_file}")


if __name__ == "__main__":
    main()
