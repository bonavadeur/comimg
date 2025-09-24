import os
import subprocess

def merge_videos():
    videos = [f for f in os.listdir('.') if f.lower().endswith(('.mp4', '.mov'))]
    videos.sort()

    if not videos:
        print("❌ not found videos")
        return

    base_name, _ = os.path.splitext(videos[0])
    output = f"{base_name}_merged.mp4"

    if os.path.exists("file_list.txt"):
        os.remove("file_list.txt")

    with open("file_list.txt", "w", encoding="utf-8") as f:
        for v in videos:
            abs_path = os.path.abspath(v)
            f.write(f"file '{abs_path}'\n")

    print("📄 Danh sách video sẽ được nối:")
    for v in videos:
        print(" -", v)

    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "file_list.txt",
        "-c", "copy",
        output
    ]
    subprocess.run(cmd)

    if os.path.exists("file_list.txt"):
        os.remove("file_list.txt")

    print("✅ Succeeded")

if __name__ == "__main__":
    merge_videos()
