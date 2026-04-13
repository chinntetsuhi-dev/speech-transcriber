import os
import json
import subprocess
from pathlib import Path

import torchaudio
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline


SUPPORTED_EXTENSIONS = {".mp3", ".mp4", ".wav", ".m4a", ".flac", ".aac", ".mov"}


class SpeechPipeline:
    def __init__(self, hf_token: str, ffmpeg_bin: str):
        self.hf_token = hf_token
        self.ffmpeg_bin = ffmpeg_bin

        os.add_dll_directory(self.ffmpeg_bin)
        os.environ["TORIO_USE_FFMPEG_VERSION"] = "4"

    def is_supported_file(self, input_path: Path) -> bool:
        return input_path.suffix.lower() in SUPPORTED_EXTENSIONS

    def convert_to_wav(self, input_path: Path, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_path)
        ]

        subprocess.run(cmd, check=True)

    def transcribe_audio(self, wav_path: Path, hotwords=None, prompt=None):
        model = WhisperModel("small", device="cpu", compute_type="int8")

        segments, info = model.transcribe(
            str(wav_path),
            beam_size=5,
            hotwords=hotwords,
            initial_prompt=prompt
        )

        results = []
        for seg in segments:
            text = seg.text.strip()
            if text:
                results.append({
                    "start": seg.start,
                    "end": seg.end,
                    "text": text
                })

        return results, info

    def diarize(self, wav_path: Path):
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            token=self.hf_token
        )

        waveform, sr = torchaudio.load(str(wav_path))

        diarization_output = pipeline({
            "waveform": waveform,
            "sample_rate": sr
        })

        annotation = diarization_output.speaker_diarization

        speaker_segments = []
        for turn, _, speaker in annotation.itertracks(yield_label=True):
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })

        return speaker_segments

    def assign_speaker(self, transcripts, speakers):
        results = []

        for t in transcripts:
            mid = (t["start"] + t["end"]) / 2
            assigned = "UNKNOWN"

            for s in speakers:
                if s["start"] <= mid <= s["end"]:
                    assigned = s["speaker"]
                    break

            results.append({
                "start": t["start"],
                "end": t["end"],
                "speaker": assigned,
                "text": t["text"]
            })

        return results

    def build_prompt_from_keywords(self, keywords: list[str]):
        if not keywords:
            return None, None

        hotwords = ", ".join(keywords)
        prompt = "可能出现的词：" + "，".join(keywords)
        return hotwords, prompt

    def save_txt(self, results, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)

        lines = []
        for r in results:
            lines.append(f"[{r['start']:.2f}-{r['end']:.2f}] {r['speaker']}: {r['text']}")

        path.write_text("\n".join(lines), encoding="utf-8")

    def save_json(self, results, path: Path, language: str, keywords: list[str]):
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "language": language,
            "keywords": keywords,
            "segments": results
        }

        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def run(
        self,
        input_path: str,
        keywords: list[str] | None = None,
        temp_dir: str = "temp",
        output_dir: str = "output",
    ):
        input_file = Path(input_path)

        if not input_file.exists():
            raise FileNotFoundError(f"文件不存在: {input_file}")

        if not self.is_supported_file(input_file):
            raise ValueError(f"不支持的文件格式: {input_file.suffix}")

        keywords = keywords or []

        wav_path = Path(temp_dir) / f"{input_file.stem}.wav"
        txt_path = Path(output_dir) / f"{input_file.stem}.txt"
        json_path = Path(output_dir) / f"{input_file.stem}.json"

        self.convert_to_wav(input_file, wav_path)

        hotwords, prompt = self.build_prompt_from_keywords(keywords)
        transcripts, info = self.transcribe_audio(wav_path, hotwords, prompt)
        speakers = self.diarize(wav_path)
        final_results = self.assign_speaker(transcripts, speakers)

        language = getattr(info, "language", "unknown")

        self.save_txt(final_results, txt_path)
        self.save_json(final_results, json_path, language, keywords)

        # 默认清理临时 wav
        try:
            if wav_path.exists():
                wav_path.unlink()
        except Exception:
            pass

        return {
            "input_file": str(input_file),
            "wav_file": str(wav_path),
            "txt_file": str(txt_path),
            "json_file": str(json_path),
            "language": language,
            "keywords": keywords,
            "segments": final_results,
        }