import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_file(
        file_path, export_format, mode,
        min_segment_duration, max_segment_duration,
        min_silence_amp, min_silence_len, keep_silence
    ):
    audio_file = AudioSegment.from_file(file_path,)
    print("Splitting")
    segments = split_on_silence(audio_file,
                                min_silence_len=min_silence_len,
                                silence_thresh=min_silence_amp,
                                keep_silence=keep_silence)
    
    base_file_name = os.path.basename(file_path)
    
    export_folder = f"{mode}/{base_file_name}"
    os.makedirs(export_folder, exist_ok=True)
    
    seg_idx = 0
    # Iterate over the segments and truncate or save them based on the duration
    for i, segment in enumerate(segments):
        segment_duration = len(segment)
        print("Segment", i)

        # Check if the segment duration is less than the minimum duration
        while mode == "large" and segment_duration < min_segment_duration: # Merge only if mode is large, else no merge
            # If the segment is too short, merge it with the next segment if possible
            if i + 1 >= len(segments):
                break

            next_segment = segments[i + 1]
            # Check if the merged segment duration is within the maximum duration
            if len(segment) + len(next_segment) > max_segment_duration:
                break
            merged_segment = segment + next_segment

            print("Big Chunkus")
            segment = merged_segment
            segment_duration = len(segment)
            segments.pop(i + 1)  # Remove the next segment from the list

        # Check if the segment duration exceeds the maximum duration
        loop_idx = 0
        while segment_duration > max_segment_duration:
            # Truncate the segment to the maximum duration
            store = segment[:max_segment_duration]
            print("Export Truncus", seg_idx)
            store.export(f"{export_folder}/{base_file_name}_{seg_idx}-trunc.{export_format}", format=export_format)
            loop_idx += 1
            seg_idx += 1
            cur_seg_off = max_segment_duration * loop_idx
            if cur_seg_off < len(segment):
                segment = segment[cur_seg_off:cur_seg_off+max_segment_duration]
            segment_duration = len(segment)

        # Export the segment to a file
        print("Export Chunkus", seg_idx)
        segment.export(f"{export_folder}/{base_file_name}_{seg_idx}.{export_format}", format=export_format)
        seg_idx += 1
