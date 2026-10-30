# -*- coding: utf-8 -*-
"""Facebook-only uploader for the daily workflow.

Finds the freshly generated video in output/, builds the caption and
publishes it to the Facebook Page. Nothing else is uploaded anywhere.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from upload_facebook import upload_to_facebook


def get_latest_video():
    fv = Path("output/final_video.mp4")
    if fv.exists():
        meta = {"story": "", "topic": ""}
        tp = Path("output/topic.txt")
        if tp.exists():
            meta["topic"] = tp.read_text(encoding="utf-8").strip()
        st = Path("output/story.txt")
        if st.exists():
            meta["story"] = st.read_text(encoding="utf-8").strip()
        return {"video_path": str(fv), "topic": meta.get("topic") or "Ancient History",
                "metadata": meta}

    out_dir = Path("output")
    if out_dir.exists():
        candidates = [p for p in out_dir.glob("*/final_video.mp4") if p.is_file()]
        if candidates:
            latest = max(candidates, key=lambda p: p.stat().st_mtime)
            meta = {"story": "", "topic": ""}
            tp = latest.parent / "topic.txt"
            if tp.exists():
                meta["topic"] = tp.read_text(encoding="utf-8").strip()
            st = latest.parent / "story.txt"
            if st.exists():
                meta["story"] = st.read_text(encoding="utf-8").strip()
            return {"video_path": str(latest),
                    "topic": meta.get("topic") or "Ancient History",
                    "metadata": meta}
    return None


def generate_caption(topic, metadata=None):
    from lang_config import LANG
    topic_str = topic or "Ancient History"
    story = (metadata.get("story", "") if metadata else "").strip()
    lines = [f"\U0001F4DC {topic_str}", ""]
    if story:
        lines += [story, ""]
    lines += [LANG.get("hashtags", "#history")]
    return "\n".join(lines)


def main():
    vdata = get_latest_video()
    if not vdata:
        print("No video file found in output/ directory.")
        sys.exit(1)
    caption = generate_caption(vdata["topic"], vdata.get("metadata"))
    thumb = Path("output/thumbnail.jpg")
    thumb_path = str(thumb) if thumb.exists() else None
    result = upload_to_facebook(
        video_path=vdata["video_path"],
        description=caption,
        title=vdata["topic"][:100],
        thumbnail_path=thumb_path,
    )
    if not result:
        print("Facebook upload did not succeed.")
        sys.exit(1)
    print(f"Facebook upload OK: {result.get('id')}")


if __name__ == "__main__":
    main()
