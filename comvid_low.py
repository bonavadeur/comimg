import subprocess
import pathlib
import os
import re
import sys
from itertools import chain


def get_video_info(file):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration = float(result.stdout.strip())

    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0:s=x",
        file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    width, height = map(int, result.stdout.strip().split("x"))

    return duration, width, height

def run_ffmpeg_with_progress(cmd, duration):
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)

    last_percent = -1
    for line in process.stderr:
        match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
        if match:
            h, m, s = match.groups()
            seconds = int(h) * 3600 + int(m) * 60 + float(s)
            percent = int((seconds / duration) * 100)
            if percent != last_percent:
                sys.stdout.write(f"\rCompressing... {percent}%")
                sys.stdout.flush()
                last_percent = percent

    process.wait()
    print("\r✅ Done!!!")


def get_video_codec(file):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_name",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()


def compress(file):
    input_file = str(file)
    output_file = file.stem + "_compressed.mp4"

    print(f"\n🔄 Compressing {input_file}")

    duration, width, height = get_video_info(input_file)
    codec = get_video_codec(input_file)

    if width >= 3840 or height >= 2160: # 4K
        min_bitrate, max_bitrate, target_bitrate = "15M", "25M", "20M"
        crf_value = "24"
    elif width >= 1920 or height >= 1080: # FHD
        min_bitrate, max_bitrate, target_bitrate = "2M", "6M", "3M"
        crf_value = "27"

    print(f"Detected codec: {codec}")
    if codec == "hevc":
        vcodec = "libx265"
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-c:v", "libx265",
            # "-pix_fmt", "yuv420p10le",
            # "-color_primaries", "bt2020",
            # "-color_trc", "arib-std-b67",
            "-colorspace", "bt2020nc",
            "-tag:v", "hvc1",
            "-movflags", "+faststart",
            "-preset", "slow",
            "-crf", crf_value,
            "-c:a", "aac", "-b:a", "128k",
            "-map_metadata", "0",
            output_file
        ]
        run_ffmpeg_with_progress(ffmpeg_cmd, duration)

    else:
        vcodec = "libx264"

        # Pass 1
        ffmpeg_cmd_pass1 = [
            "ffmpeg", "-y", "-i", input_file,
            "-c:v", vcodec,
            "-b:v", target_bitrate,
            "-minrate", min_bitrate,
            "-maxrate", max_bitrate,
            "-bufsize", "80M",
            "-preset", "slow",
            "-pass", "1", "-an", "-f", "mp4", "NUL",
            "-map_metadata", "0",
        ]
        subprocess.run(ffmpeg_cmd_pass1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Pass 2
        ffmpeg_cmd_pass2 = [
            "ffmpeg", "-y", "-i", input_file,
            "-c:v", vcodec,
            "-b:v", target_bitrate,
            "-minrate", min_bitrate,
            "-maxrate", max_bitrate,
            "-bufsize", "80M",
            "-preset", "slow",
            "-pass", "2",
            "-c:a", "aac", "-b:a", "192k",
            "-map_metadata", "0",
            output_file
        ]
        run_ffmpeg_with_progress(ffmpeg_cmd_pass2, duration)

    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        os.remove(input_file)

    for log_file in ["ffmpeg2pass-0.log", "ffmpeg2pass-0.log.mbtree"]:
        if os.path.exists(log_file):
            os.remove(log_file)



for file in pathlib.Path(".").glob("*.MOV"):
    if "_compressed" not in file.name:
        compress(file)
for file in pathlib.Path(".").glob("*.MP4"):
    if "_compressed" not in file.name:
        compress(file)
        

print("\n🎉 DONE!!!")
