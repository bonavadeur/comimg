import subprocess
import pathlib
import os
import re
import sys

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

for file in pathlib.Path(".").glob("*.MOV"):
    input_file = str(file)
    output_file = file.stem + ".mp4"

    print(f"\n🔄 Compressing {input_file}")

    duration, width, height = get_video_info(input_file)

    # Chọn cấu hình bitrate
    if width >= 3840 or height >= 2160: # 4K
        min_bitrate, max_bitrate, target_bitrate = "20M", "60M", "40M"
    elif width >= 1920 or height >= 1080: # FHD
        min_bitrate, max_bitrate, target_bitrate = "5M", "15M", "8M"

    # Pass 1
    ffmpeg_cmd_pass1 = [
        "ffmpeg", "-y", "-i", input_file,
        "-c:v", "libx264",
        "-b:v", target_bitrate,
        "-minrate", min_bitrate,
        "-maxrate", max_bitrate,
        "-bufsize", "80M",
        "-preset", "slow",
        "-pass", "1", "-an", "-f", "mp4", "NUL"
    ]
    subprocess.run(ffmpeg_cmd_pass1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Pass 2
    ffmpeg_cmd_pass2 = [
        "ffmpeg", "-y", "-i", input_file,
        "-c:v", "libx264",
        "-b:v", target_bitrate,
        "-minrate", min_bitrate,
        "-maxrate", max_bitrate,
        "-bufsize", "80M",
        "-preset", "slow",
        "-pass", "2",
        "-c:a", "aac", "-b:a", "192k",
        output_file
    ]
    run_ffmpeg_with_progress(ffmpeg_cmd_pass2, duration)

    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        os.remove(input_file)

    for log_file in ["ffmpeg2pass-0.log", "ffmpeg2pass-0.log.mbtree"]:
        if os.path.exists(log_file):
            os.remove(log_file)

print("\n🎉 DONE!!!")
