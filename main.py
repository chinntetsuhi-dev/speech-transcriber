from pathlib import Path
import os
from backend.pipeline import SpeechPipeline


HF_TOKEN = os.getenv("HF_TOKEN")
FFMPEG_BIN = r"D:\ffmpeg\ffmpeg-8.1-full_build-shared\bin"


def list_supported_files():
    input_dir = Path("input")
    if not input_dir.exists():
        return []

    files = []
    for f in input_dir.iterdir():
        if f.is_file():
            files.append(f)

    return sorted(files, key=lambda x: x.name.lower())


def select_input_file():
    files = list_supported_files()

    if not files:
        print("input 文件夹中没有文件")
        return None

    print("可用文件：")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f.name}")

    user_input = input("\n请输入序号或文件名: ").strip()

    if user_input.isdigit():
        idx = int(user_input)
        if 1 <= idx <= len(files):
            return files[idx - 1]
        print("序号错误")
        return None

    p = Path("input") / user_input
    if not p.exists():
        print("文件不存在")
        return None

    return p


def ask_keywords():
    use = input("是否输入关键词？(y/n): ").strip().lower()

    if use != "y":
        return []

    raw = input("输入关键词（逗号分隔）: ").strip()
    return [k.strip() for k in raw.split(",") if k.strip()]


def main():
    input_file = select_input_file()
    if not input_file:
        return

    keywords = ask_keywords()

    pipeline = SpeechPipeline(
        hf_token=HF_TOKEN,
        ffmpeg_bin=FFMPEG_BIN,
    )

    result = pipeline.run(
        input_path=str(input_file),
        keywords=keywords,
        temp_dir="temp",
        output_dir="output",
    )

    print("\n===== 结果 =====")
    print("检测语言:", result["language"])
    print("TXT 输出:", result["txt_file"])
    print("JSON 输出:", result["json_file"])

    for r in result["segments"]:
        print(f"[{r['start']:.2f}-{r['end']:.2f}] {r['speaker']}: {r['text']}")


if __name__ == "__main__":
    main()