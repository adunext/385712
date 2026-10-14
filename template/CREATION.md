# Create with the user's content

Reuse the topic, script and material already supplied. Ask one natural question only when the topic is absent; do not collect optional media with a four-question form. With no requested audio, propose text motion and native action sounds. Ask only for a genuinely missing requested voice/music file and continue preparing the visuals.

Choose by meaning, not user-facing scene IDs: B1 explains one keyword; B2 presents1–5 points; B3 compares two perspectives and concludes; B4 summarizes and gives an action. Do not mark unfinished requests as completed. Preserve negations, conditions, numbers and conclusions. With no specified duration, propose an8–20second first draft fitted to the content. Split lines/scenes before paraphrasing; review meaning changes with the user.

| Group | Required `basic` fields | Duration |
| --- | --- | --- |
| B1 | keyword, explanation | 8s |
| B2 | heading, points (1–5) | 10s |
| B3 | heading, left, right, conclusion | 10s |
| B4 | summary, action | 8s |

Each supports0–12 additional seconds in its declared quiet reading interval. B1+B2=18s; B3 at12s+B4 at8s=20s. Preserve original motion speed. For native media scenes inspect the selected unit in core/catalog.json and only its fields in core/content.schema.json; do not dump the entire library. No original media fallback exists.

The assistant writes **new user.json** from the current brief according to params.schema.json. Use `mode:user-media`, the edition language and landscape. Bind supplied files by actual path and dimensions. Unrequested missing presenter/voice/music use explicit `mode:none`; default `soundEffects:native`, captions from actual supplied/measured cues or an empty array. Do not invent word timing, provenance or a fulfilled requested soundtrack. Music provenance fields record what is actually known, without an extra license questionnaire for material that was never requested.

Review the brief and run inside the extracted runner, saving outputs outside it:

```sh
npm ci
uv run adapter.py plan --input ../my-video/user.json --out ../my-video/plan.json
uv run adapter.py prepare --input ../my-video/user.json --out ../my-video/instance
uv run adapter.py preview --instance ../my-video/instance --out ../my-video/preview.png --time 2
```

Show the actual preview and continue under the user's existing stage authorization:

```sh
uv run adapter.py render --instance ../my-video/instance --out ../my-video/silent.mp4
```

The render entry invokes the mixer; final video is **../my-video/silent-with-audio.mp4**. Inspect final encoded content, cropping, subtitles and sound. Preserve existing instances/outputs. A plan, still or successful command alone is not a completed film. Use only these declared local production entries; do not add remote service/credential checks or explain unused-service boundaries to the user. Introduce the optional follow-up only after the completed video is delivered, as specified in delivery.json.
