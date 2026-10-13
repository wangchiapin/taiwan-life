# 每個場景一首（原創小曲）。bpm 是四分音符的速度；每個字是一個八分音符。
SONGS = {
'map': """{ bpm: 112, tracks: [
  { wave: 'square', vol: 0.32, notes: 'E5 - G5 - A5 G5 E5 - | D5 - E5 - G5 - - . | E5 - G5 - A5 C6 A5 G5 | E5 - D5 - C5 - - .' },
  { wave: 'triangle', vol: 0.7, notes: 'C3 . G3 . C3 . G3 . | A2 . E3 . A2 . E3 . | F2 . C3 . F2 . C3 . | G2 . D3 . G2 . B2 .' },
  { vol: 0.45, notes: 'k . h . s . h . k k h . s . h .' }] }""",
'drinks': """{ bpm: 124, tracks: [
  { wave: 'square', vol: 0.3, notes: 'B4 D5 E5 D5 B4 - G4 - | E5 - D5 B4 D5 - - . | C5 E5 G5 E5 D5 - B4 - | A4 B4 D5 - - - . .' },
  { wave: 'triangle', vol: 0.7, notes: 'G2 . G2 D3 G2 . D3 . | E2 . E2 B2 E2 . B2 . | C3 . C3 G2 C3 . G2 . | D3 . D3 A2 D3 . F#3 .' },
  { vol: 0.45, notes: 'k . h k s . h . k . h k s h h .' }] }""",
'breakfast': """{ bpm: 116, tracks: [
  { wave: 'square', vol: 0.28, notes: 'F#5 - A5 - D6 - A5 - | E5 - A5 - C#6 - A5 - | F#5 - D5 - B4 - D5 - | G5 - F#5 - E5 - - .' },
  { wave: 'triangle', vol: 0.7, notes: 'D3 . A2 . D3 . A2 . | A2 . E3 . A2 . E3 . | B2 . F#3 . B2 . F#3 . | G2 . D3 . A2 . C#3 .' },
  { vol: 0.4, notes: 'k . h . s . h h' }] }""",
'bakery': """{ bpm: 100, tracks: [
  { wave: 'triangle', vol: 0.55, notes: 'A4 - C5 - F5 - | E5 - - - G5 - | F5 - D5 - A4 - | Bb4 - - - C5 .' },
  { wave: 'triangle', vol: 0.6, notes: 'F2 . C3 . C3 . | C3 . G3 . G3 . | D3 . A3 . A3 . | Bb2 . F3 . C3 .' },
  { vol: 0.3, notes: 'k . h . h .' }] }""",
'clinic': """{ bpm: 84, tracks: [
  { wave: 'sine', vol: 0.55, notes: 'E5 - - - C5 - - - | A4 - - - C5 - D5 - | E5 - - - G5 - - - | D5 - - - - - . .' },
  { wave: 'triangle', vol: 0.55, notes: 'A2 - - - E3 - - - | F2 - - - C3 - - - | C3 - - - G2 - - - | G2 - - - D3 - - -' },
  { vol: 0.2, notes: 'h . . . h . . .' }] }""",
'mrt': """{ bpm: 128, tracks: [
  { wave: 'square', vol: 0.26, notes: 'G5 . E5 . C5 . E5 G5 | D5 . B4 . G4 . B4 D5 | E5 . C5 . A4 . C5 E5 | F5 - E5 - D5 - . .' },
  { wave: 'triangle', vol: 0.65, notes: 'C3 C3 C3 C3 C3 C3 C3 C3 | G2 G2 G2 G2 G2 G2 G2 G2 | A2 A2 A2 A2 A2 A2 A2 A2 | F2 F2 F2 F2 G2 G2 G2 G2' },
  { vol: 0.45, notes: 'k . h . s . h . k . h k s . h h' }] }""",
'nightmarket': """{ bpm: 120, tracks: [
  { wave: 'square', vol: 0.28, notes: 'D5 E5 G5 E5 D5 B4 A4 B4 | D5 - E5 D5 B4 - G4 - | A4 B4 D5 E5 G5 E5 D5 B4 | A4 - G4 - - - . .' },
  { wave: 'triangle', vol: 0.7, notes: 'G2 . D3 . G2 . D3 . | E2 . B2 . E2 . B2 . | C3 . G2 . C3 . G2 . | D3 . A2 . G2 . . .' },
  { vol: 0.5, notes: 'k . s k k . s .' }] }""",
'parcel': """{ bpm: 118, tracks: [
  { wave: 'square', vol: 0.28, notes: 'C5 E5 G5 E5 C6 - G5 - | A5 G5 E5 G5 D5 - - . | C5 E5 G5 E5 A5 - G5 - | E5 D5 C5 D5 C5 - - .' },
  { wave: 'triangle', vol: 0.7, notes: 'C3 . . . G2 . . . | F2 . . . G2 . . . | C3 . . . F2 . . . | G2 . . . C3 . . .' },
  { vol: 0.4, notes: 'k . h . s . h .' }] }""",
'reserva': """{ bpm: 96, tracks: [
  { wave: 'sine', vol: 0.5, notes: 'E5 - G5 - B5 - A5 - | G5 - E5 - C5 - - . | F5 - A5 - C6 - B5 - | A5 - G5 - - - . .' },
  { wave: 'triangle', vol: 0.6, notes: 'C3 . . E3 . . G3 . | A2 . . C3 . . E3 . | D3 . . F3 . . A3 . | G2 . . B2 . . D3 .' },
  { vol: 0.25, notes: 'h . h h h . h h' }] }""",
'street': """{ bpm: 132, tracks: [
  { wave: 'square', vol: 0.26, notes: 'A4 C5 E5 C5 D5 - C5 B4 | A4 - E4 - G4 - A4 - | C5 D5 E5 G5 E5 - D5 C5 | B4 - G4 - A4 - - .' },
  { wave: 'triangle', vol: 0.65, notes: 'A2 A2 . A2 E3 . A2 . | F2 F2 . F2 C3 . F2 . | C3 C3 . C3 G3 . C3 . | G2 G2 . G2 E3 . E3 .' },
  { vol: 0.45, notes: 'k . h k s . h .' }] }"""
}
