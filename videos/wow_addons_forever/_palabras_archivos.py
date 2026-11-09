from faster_whisper import WhisperModel
S = r"D:\wowforever\World of Warcraft\_forever_\Interface\AddOns\SpokenQuestsAudio_esMX\generated\sounds\quests"
M = r"D:\wowForeverVoces\addon\WoWForeverVoces\sonidos"
m = WhisperModel("small", device="cuda", compute_type="float16")
for f in [S + r"\783-accept.ogg", M + r"\783_desc_m.mp3", S + r"\33-accept.ogg", M + r"\33_desc.mp3"]:
    segs, _ = m.transcribe(f, language="es", word_timestamps=True)
    ws = [w for s in segs for w in s.words if w.start < 12]
    print(f.split("\\")[-1], " ".join(f"{w.word.strip()}[{w.start:.1f}-{w.end:.1f}]" for w in ws))
