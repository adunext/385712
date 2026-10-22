# /// script
# requires-python = ">=3.11"
# dependencies = ["opencv-python-headless==4.12.0.88"]
# ///
"""Coarse local framing only: one image or five video samples, no face tracking."""
from pathlib import Path
from statistics import median
import json
import subprocess


def approximate_face(file, mode, duration=0):
    fallback = {'cx': .5, 'cy': .5, 'h': .4}
    report = {'method': 'opencv-haar-largest-face', 'sampleCount': 0,
              'detectedSamples': 0, 'status': 'undetected', 'reviewRequired': True}
    try:
        import cv2
        import numpy as np
        cascade = cv2.CascadeClassifier(str(Path(cv2.data.haarcascades) / 'haarcascade_frontalface_default.xml'))
        if cascade.empty():
            raise ValueError('Local face detector unavailable')
        times = [0] if mode == 'image' else [max(0, duration - .1) * p for p in [.05, .25, .5, .75, .95]]
        rows = []
        for time in times:
            command = ['ffmpeg', '-v', 'error']
            if mode == 'video':
                command += ['-ss', str(round(time, 3))]
            command += ['-i', str(file), '-vf', 'scale=1280:1280:force_original_aspect_ratio=decrease',
                        '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', 'pipe:1']
            result = subprocess.run(command, capture_output=True, timeout=30, check=True)
            pixels = cv2.imdecode(np.frombuffer(result.stdout, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            report['sampleCount'] += 1
            if pixels is None:
                continue
            height, width = pixels.shape
            faces = cascade.detectMultiScale(pixels, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
            if not len(faces):
                continue
            x, y, w, h = max(faces, key=lambda b: int(b[2]) * int(b[3]))
            rows.append({'time': round(time, 3), 'cx': float((x + w / 2) / width),
                         'cy': float((y + h / 2) / height), 'w': float(w / width), 'h': float(h / height)})
        report.update(detectedSamples=len(rows), samples=rows)
        if rows:
            face = {key: round(median(row[key] for row in rows), 6) for key in ['cx', 'cy', 'w', 'h']}
            report['status'] = 'approximate'
            return face, report
        report['reason'] = 'No frontal face found; use centered cover without extra zoom. A manual face hint can override it.'
    except (ImportError, OSError, ValueError, AttributeError, subprocess.SubprocessError):
        report['reason'] = 'Local detector unavailable; use centered cover without extra zoom. A manual face hint can override it.'
    return fallback, report


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--video-duration', type=float, default=0)
    args = parser.parse_args()
    face, report = approximate_face(args.file, 'video' if args.video_duration else 'image', args.video_duration)
    print(json.dumps({'face': face, 'framing': report}, ensure_ascii=False, indent=2))
