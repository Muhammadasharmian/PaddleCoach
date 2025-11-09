#!/usr/bin/env python3
"""
Test script to verify Eleven Labs API functionality.
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    print("\n[1] Importing elevenlabs...")
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play
    print("✓ Imports successful")
    
    print("\n[2] Creating client...")
    api_key = "sk_6d09c01893945be9d97377004f6b6ef2f620892861ff0cd7"
    client = ElevenLabs(api_key=api_key)
    print(f"✓ Client created: {type(client)}")
    
    print("\n[3] Testing API call with text to speech...")
    test_text = "Hello, this is a test of the Eleven Labs text to speech API."
    print(f"Test text: {test_text}")
    
    # Using the correct API method as per documentation
    audio_generator = client.text_to_speech.convert(
        text=test_text,
        voice_id="bPMKpgEe88vKSwusXTMU",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    print(f"✓ API call successful, generator: {type(audio_generator)}")
    
    print("\n[4] Saving audio to file...")
    from pathlib import Path
    output_path = Path("test_output.mp3")
    
    chunk_count = 0
    total_bytes = 0
    with open(output_path, 'wb') as f:
        for chunk in audio_generator:
            if chunk:
                chunk_count += 1
                total_bytes += len(chunk)
                f.write(chunk)
                print(f"  Chunk {chunk_count}: {len(chunk)} bytes")
    
    print(f"✓ Audio saved to {output_path}")
    print(f"  Total chunks: {chunk_count}")
    print(f"  Total size: {total_bytes} bytes ({total_bytes/1024:.2f} KB)")
    print(f"  File exists: {output_path.exists()}")
    print(f"  File size: {output_path.stat().st_size} bytes")
    
    print("\n✅ ALL TESTS PASSED!")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
