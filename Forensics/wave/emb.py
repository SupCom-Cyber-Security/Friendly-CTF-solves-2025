import wave
with wave.open(input_wav, "rb") as wav_in:
    n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_in.getparams()
    frames = bytearray(wav_in.readframes(n_frames))

# ---- Convert flag to bits ----
bits = "".join(f"{byte:08b}" for byte in flag)

# ---- Check we have enough audio bytes ----
if len(bits) > len(frames):
    raise ValueError("Not enough audio samples to hide the flag!")

# ---- Embed bits in the least significant bit of each byte ----
for j, bit in enumerate(bits):
    frames[j] = (frames[j] & ~1) | int(bit)

# ---- Write new WAV file with modified frames ----
with wave.open(output_wav, "wb") as wav_out:
    wav_out.setnchannels(n_channels)
    wav_out.setsampwidth(sampwidth)
    wav_out.setframerate(framerate)
    wav_out.setcomptype(comptype, compname)
    wav_out.writeframes(frames)

print(f"Flag embedded into {output_wav}")