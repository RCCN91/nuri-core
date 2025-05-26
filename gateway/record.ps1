param(
  [int]$Duration = 4,
  [string]$Output   = "input.wav",
  [string]$Device   = "Mikrofon (Realtek(R) Audio)"
)

& ffmpeg -f dshow -i "audio=$Device" -t $Duration -ac 1 -ar 16000 $Output -y
