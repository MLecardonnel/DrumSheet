\version "2.18.2"

    \paper {
      top-margin = 10
      markup-system-spacing =
        #'((padding . 10))
    }
    \header {
      title = "MusicDelta_80sRock_Drum"
    }
    up = \drummode {
      r4  r4  r4  r4  r4  r4  r4  r4  cymc4  r4  r4  r4  r4  r4  r4  r4  hh4  r4  r4  r4  r4  r4  r4  r4  cymc4  r4  r4  r4  r4  r4  r4  r4  cymc4  cymc4  r4  r4  r4  r8  r16  hh16  r4  r4  r8  r16  hh16  r4  r4  r4  cymc4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  cymc4  cymc4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4
    }
    
    down = \drummode {
      bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  bd4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>8  r16  bd16  bd4  <bd  sn>8  r16  bd16  bd4  <bd  sn>4  bd8  r16  bd16  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  sn4  bd4  bd4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>4  bd4  <bd  sn>8  r16  bd16  r4  <bd  sn>16  sn16  sn16  sn16  r4  r4  r4  r4
    }
    
    \new DrumStaff <<
      \new DrumVoice { \voiceOne \up }
      \new DrumVoice { \voiceTwo \down }
    >>
    