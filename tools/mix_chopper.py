#!/usr/bin/env python3
"""
Automated Mix Chopper
Processes audio files based on customer timestamp requirements
"""

from pydub import AudioSegment
import os
from typing import List, Tuple

def time_to_ms(time_str: str) -> int:
    """Convert time string (MM:SS or M:SS) to milliseconds"""
    if ':' in time_str:
        parts = time_str.split(':')
        minutes = int(parts[0])
        seconds = int(parts[1])
        return (minutes * 60 + seconds) * 1000
    else:
        # Just seconds
        return int(time_str) * 1000

def create_mix_from_segments(audio: AudioSegment, keep_segments: List[Tuple[str, str]], name: str) -> AudioSegment:
    """Create a new mix by keeping only the specified segments"""
    result = AudioSegment.empty()
    
    print(f"\nCreating {name}:")
    for i, (start_str, end_str) in enumerate(keep_segments):
        start_ms = time_to_ms(start_str)
        end_ms = time_to_ms(end_str)
        
        # Extract segment
        segment = audio[start_ms:end_ms]
        result += segment
        
        segment_duration = (end_ms - start_ms) / 1000
        print(f"  Segment {i+1}: {start_str}-{end_str} ({segment_duration:.1f}s)")
    
    total_duration = len(result) / 1000
    print(f"  Total duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
    
    return result

def main():
    # Get input file path
    input_file = input("Enter the path to your original mix file: ").strip()
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        return
    
    print(f"Loading audio file: {input_file}")
    audio = AudioSegment.from_file(input_file)
    original_duration = len(audio) / 1000
    print(f"Original duration: {original_duration:.1f} seconds ({original_duration/60:.1f} minutes)")
    
    # 7-minute mix segments (keep these parts)
    seven_min_segments = [
        ("0:00", "1:01"),
        ("1:15", "3:11"),
        ("3:25", "4:58"),
        ("5:03", "5:18"),
        ("5:26", "5:43"),
        ("5:48", "5:53"),
        ("6:00", "6:14"),
        ("6:20", "6:29"),
        ("6:38", "7:21"),
        ("7:36", "7:53")
    ]
    
    # 3-minute mix segments (keep these parts)
    three_min_segments = [
        ("0:00", "0:07"),
        ("0:15", "0:41"),
        ("0:50", "0:56"),
        ("1:15", "1:25"),
        ("1:47", "2:13"),
        ("2:22", "2:28"),
        ("2:50", "3:12"),
        ("3:53", "4:00"),
        ("4:08", "4:15"),
        ("4:23", "4:37"),
        ("4:45", "4:54"),
        ("5:34", "5:43"),
        ("5:47", "5:55"),
        ("6:01", "6:13"),
        ("6:20", "6:30"),
        ("6:38", "6:47"),
        ("6:51", "6:56"),
        ("7:01", "7:12"),
        ("7:36", "7:39"),
        ("7:46", "7:53")
    ]
    
    # Create the mixes
    seven_min_mix = create_mix_from_segments(audio, seven_min_segments, "7-minute mix")
    three_min_mix = create_mix_from_segments(audio, three_min_segments, "3-minute mix")
    
    # For 2.5-minute mix, take the best parts from 3-minute mix
    # Keep choreographed beginning (first 2 minutes) + select best remaining parts
    two_half_segments = [
        ("0:00", "0:07"),
        ("0:15", "0:41"),
        ("0:50", "0:56"),
        ("1:15", "1:25"),
        ("1:47", "2:13"),  # End of choreographed section
        ("2:22", "2:28"),
        ("4:23", "4:37"),  # Good energy section
        ("5:34", "5:43"),
        ("6:38", "6:47"),
        ("7:36", "7:39")   # Strong ending
    ]
    
    two_half_mix = create_mix_from_segments(audio, two_half_segments, "2.5-minute mix")
    
    # Export the files
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.dirname(input_file) or "."
    
    seven_min_path = os.path.join(output_dir, f"{base_name}_7min.wav")
    three_min_path = os.path.join(output_dir, f"{base_name}_3min.wav")
    two_half_path = os.path.join(output_dir, f"{base_name}_2.5min.wav")
    
    print(f"\nExporting files...")
    seven_min_mix.export(seven_min_path, format="wav")
    print(f"✓ 7-minute mix: {seven_min_path}")
    
    three_min_mix.export(three_min_path, format="wav")
    print(f"✓ 3-minute mix: {three_min_path}")
    
    two_half_mix.export(two_half_path, format="wav")
    print(f"✓ 2.5-minute mix: {two_half_path}")
    
    print(f"\n🎉 All mixes created successfully!")
    print(f"Final durations:")
    print(f"  7-minute mix: {len(seven_min_mix)/1000/60:.1f} minutes")
    print(f"  3-minute mix: {len(three_min_mix)/1000/60:.1f} minutes")
    print(f"  2.5-minute mix: {len(two_half_mix)/1000/60:.1f} minutes")

if __name__ == "__main__":
    main()
