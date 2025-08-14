#!/usr/bin/env python3
"""
Enhanced Mix Segment Exporter for NFL Halftime Show
Exports individual segments for precise editing in Ableton Live
"""

import os
from pydub import AudioSegment

def time_to_seconds(time_str):
    """Convert MM:SS format to seconds"""
    parts = time_str.split(':')
    return int(parts[0]) * 60 + int(parts[1])

def export_individual_segments():
    """Export each segment as individual files for Ableton editing"""
    
    # Get input file
    input_file = input("Enter the path to your original mix file: ").strip()
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        return
    
    print(f"Loading audio file: {input_file}")
    audio = AudioSegment.from_file(input_file)
    
    # Base filename for exports
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.dirname(input_file)
    
    # Create segments directory
    segments_dir = os.path.join(output_dir, f"{base_name}_Segments")
    os.makedirs(segments_dir, exist_ok=True)
    
    # Define all segments with their intended use
    segments = [
        # 7-minute mix segments
        ("7min_01", "0:00", "1:01", "Strong opening"),
        ("7min_02", "1:15", "3:11", "Main groove section"),
        ("7min_03", "3:25", "4:58", "Build-up section"),
        ("7min_04", "5:03", "5:18", "Transition"),
        ("7min_05", "5:26", "5:43", "Bridge"),
        ("7min_06", "5:48", "5:53", "Quick hit"),
        ("7min_07", "6:00", "6:14", "Energy boost"),
        ("7min_08", "6:20", "6:29", "Accent"),
        ("7min_09", "6:38", "7:21", "Climax section"),
        ("7min_10", "7:36", "7:53", "Strong ending"),
        
        # 3-minute mix additional segments
        ("3min_01", "0:00", "0:07", "Quick intro"),
        ("3min_02", "0:15", "0:41", "Opening hook"),
        ("3min_03", "0:50", "0:56", "Transition"),
        ("3min_04", "1:15", "1:25", "Beat drop"),
        ("3min_05", "1:47", "2:13", "Main section"),
        ("3min_06", "2:22", "2:28", "Quick break"),
        ("3min_07", "2:50", "3:12", "Build section"),
        ("3min_08", "3:53", "4:00", "Accent hit"),
        ("3min_09", "4:08", "4:15", "Rhythm change"),
        ("3min_10", "4:23", "4:37", "Core groove"),
        ("3min_11", "4:45", "4:54", "Transition"),
        ("3min_12", "5:34", "5:43", "Energy peak"),
        ("3min_13", "5:47", "5:55", "Bridge"),
        ("3min_14", "6:01", "6:13", "Build-up"),
        ("3min_15", "6:20", "6:30", "Drop section"),
        ("3min_16", "6:38", "6:47", "Climax start"),
        ("3min_17", "6:51", "6:56", "Peak moment"),
        ("3min_18", "7:01", "7:12", "Final build"),
        ("3min_19", "7:36", "7:39", "Quick hit"),
        ("3min_20", "7:46", "7:53", "Final ending"),
    ]
    
    print(f"\nExporting {len(segments)} individual segments to: {segments_dir}")
    print("=" * 60)
    
    # Export each segment
    for segment_name, start_time, end_time, description in segments:
        start_ms = time_to_seconds(start_time) * 1000
        end_ms = time_to_seconds(end_time) * 1000
        
        # Extract segment
        segment = audio[start_ms:end_ms]
        duration = len(segment) / 1000.0
        
        # Create filename
        filename = f"{segment_name}_{start_time.replace(':', '-')}_to_{end_time.replace(':', '-')}.wav"
        filepath = os.path.join(segments_dir, filename)
        
        # Export segment
        segment.export(filepath, format="wav")
        
        print(f"✓ {segment_name}: {start_time}-{end_time} ({duration:.1f}s) - {description}")
    
    print("=" * 60)
    print(f"🎉 All segments exported successfully!")
    print(f"📁 Location: {segments_dir}")
    print("\n📋 ABLETON WORKFLOW:")
    print("1. Create new Ableton Live project")
    print("2. Import all segment files into Session View")
    print("3. Arrange segments in desired order")
    print("4. Fine-tune timing and beat-matching")
    print("5. Add crossfades between segments")
    print("6. Export final mixes at exact NFL requirements")
    print("\n⚠️  NFL TIMING REQUIREMENTS:")
    print("- 7-minute mix: Must be EXACTLY 7:00")
    print("- 3-minute mix: Must be EXACTLY 3:00") 
    print("- 2.5-minute mix: Must be EXACTLY 2:30")
    print("\n💡 TIP: Use Ableton's Warp feature to stretch/compress segments to hit exact timings!")

if __name__ == "__main__":
    export_individual_segments()
