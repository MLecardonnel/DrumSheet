import os
import shutil
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from scipy.io import wavfile
import librosa

drums_notes = {
    'CY': 'cymc',
    'HH': 'hh',
    'KD': 'bd',
    'SD': 'sn',
    }

def create_note(parts, part1, part2, note_time):
  if part1==1 and part2==1:
    note_string = f'  <{drums_notes[parts[0]]}  {drums_notes[parts[1]]}>{note_time}'
  elif part1==1:
    note_string = f'  {drums_notes[parts[0]]}{note_time}'
  elif part2==1:
    note_string = f'  {drums_notes[parts[1]]}{note_time}'
  else:
    note_string = f'  r{note_time}'
  return note_string

def get_single_voice_quarter_transcription(segment_time, spb, transcription, voice):
  transcription = transcription[(transcription['time']>=segment_time) & (transcription['time']<segment_time+spb)].copy()
  transcription['time'] = transcription['time']-segment_time
  voice_string = ''
  if voice=='up':
    parts = ['CY','HH']
  elif voice=='down':
    parts = ['KD','SD']
  transcription = transcription[['time']+parts]
  transcription = transcription[(transcription[parts[0]]!=0) | (transcription[parts[1]]!=0)].reset_index(drop=True)
  if len(transcription)==0:
    voice_string = '  r4'
  else:
    if len(transcription[transcription['time']>=spb/2])==0:
      if len(transcription[transcription['time']>=spb/4])==0:
        part1 = transcription.loc[transcription['time']<spb/4, parts[0]].values[0]
        part2 = transcription.loc[transcription['time']<spb/4, parts[1]].values[0]
        voice_string = create_note(parts,part1, part2, 4)
      else:
        try:
          part1 = transcription.loc[transcription['time']<spb/4, parts[0]].values[0]
        except:
          part1 = 0
        try:
          part2 = transcription.loc[transcription['time']<spb/4, parts[1]].values[0]
        except:
          part2 = 0
        voice_string = create_note(parts,part1, part2, 16)
        part1 = transcription.loc[transcription['time']>=spb/4, parts[0]].values[0]
        part2 = transcription.loc[transcription['time']>=spb/4, parts[1]].values[0]
        voice_string += create_note(parts,part1, part2, 16)
        voice_string += ' r8'
    else:
      if len(transcription[(transcription['time']>=spb/4) & (transcription['time']<spb/2)])==0:
        try:
          part1 = transcription.loc[transcription['time']<spb/4, parts[0]].values[0]
        except:
          part1 = 0
        try:
          part2 = transcription.loc[transcription['time']<spb/4, parts[1]].values[0]
        except:
          part2 = 0
        voice_string = create_note(parts,part1, part2, 8)
      else:
        try:
          part1 = transcription.loc[transcription['time']<spb/4, parts[0]].values[0]
        except:
          part1 = 0
        try:
          part2 = transcription.loc[transcription['time']<spb/4, parts[1]].values[0]
        except:
          part2 = 0
        voice_string = create_note(parts,part1, part2, 16)
        part1 = transcription.loc[transcription['time']>=spb/4, parts[0]].values[0]
        part2 = transcription.loc[transcription['time']>=spb/4, parts[1]].values[0]
        voice_string += create_note(parts,part1, part2, 16)
      if len(transcription[transcription['time']>=3*spb/4])==0:
        part1 = transcription.loc[transcription['time']>=spb/2, parts[0]].values[0]
        part2 = transcription.loc[transcription['time']>=spb/2, parts[1]].values[0]
        voice_string += create_note(parts,part1, part2, 8)
      else:
        try:
          part1 = transcription.loc[(transcription['time']>=spb/2) & (transcription['time']<3*spb/4), parts[0]].values[0]
        except:
          part1 = 0
        try:
          part2 = transcription.loc[(transcription['time']>=spb/2) & (transcription['time']<3*spb/4), parts[1]].values[0]
        except:
          part2 = 0
        voice_string += create_note(parts,part1, part2, 16)
        part1 = transcription.loc[transcription['time']>=3*spb/4, parts[0]].values[0]
        part2 = transcription.loc[transcription['time']>=3*spb/4, parts[1]].values[0]
        voice_string += create_note(parts,part1, part2, 16)
  return voice_string

class DrumAudio():
  def __init__(
        self,
        audio_path: str,
        **kwargs
        ):
    super(DrumAudio, self).__init__(**kwargs)

    self.file_name = audio_path.split('/')[-1].split('.')[0]
    self.freq_rate, self.signal = wavfile.read(audio_path)

    size = self.signal.shape[0]
    secs = size / self.freq_rate
    T = 1.0/self.freq_rate
    self.time_range = np.arange(0, secs, T).round(6)

    tempo, _ = librosa.beat.beat_track(self.signal.astype(float))
    self.spb = 60/(2*tempo)
  
  def detect_percussions(self):
    dataset = pd.DataFrame(np.array([self.signal,self.time_range]).T, columns=['signal','time'])
    dataset['index_position'] = dataset.index

    mean = 0
    step = 1.01
    thresholds = [mean - step, mean + step]
    dataset['label'] = 1
    dataset.loc[(dataset['signal'] <= thresholds[0]) | (dataset['signal']>= thresholds[1]), 'label'] = 0
    dataset['new_index'] = dataset['label'].cumsum()
    new_dataset = dataset[(dataset['label']==0)].groupby('new_index').first()
    new_dataset['size'] = dataset[(dataset['label']==0)].groupby('new_index').size()
    new_dataset = new_dataset[new_dataset['size']>=1024].groupby(new_dataset['time'].round(1)).first().reset_index(drop=True)
    new_dataset['new_index'] = (new_dataset['time']/0.1).round()

    percussions = new_dataset[['time','index_position']]

    return percussions
  
  def predict_kits(self, CY_model, HH_model, KD_model, SD_model):
    transcription = self.detect_percussions()

    transcription['CY'] = 0
    transcription['HH'] = 0
    transcription['KD'] = 0
    transcription['SD'] = 0

    os.makedirs('../data/predictions')
    for index, row in transcription.iterrows():
      fig, ax = plt.subplots(figsize=(8, 8))
      if row['index_position']<1024:
        _, _, _, _ = ax.specgram(self.signal[0:int(row['index_position'])+4096+1024], Fs=self.freq_rate, scale_by_freq=True)
      else:
        _, _, _, _ = ax.specgram(self.signal[int(row['index_position'])-1024:int(row['index_position'])+4096+1024], Fs=self.freq_rate, scale_by_freq=True)
      ax.axis('tight')
      ax.axis('off')
      fig.savefig(f'../data/predictions/{index}.png', bbox_inches='tight', pad_inches=0.0)
      plt.close(fig)
      img = tf.keras.preprocessing.image.load_img(
        f'../data/predictions/{index}.png', target_size=(100, 100)
      )
      img_array = tf.keras.preprocessing.image.img_to_array(img)
      img_array = tf.expand_dims(img_array, 0)
      transcription.loc[index, 'CY'] = int(CY_model.predict(img_array)[0] > 0.5)
      transcription.loc[index, 'HH'] = int(HH_model.predict(img_array)[0] > 0.5)
      transcription.loc[index, 'KD'] = int(KD_model.predict(img_array)[0] > 0.5)
      transcription.loc[index, 'SD'] = int(SD_model.predict(img_array)[0] > 0.5)

    shutil.rmtree('../data/predictions')

    transcription = transcription[(transcription['CY']!=0) | (transcription['HH']!=0) | (transcription['KD']!=0) | (transcription['SD']!=0)].reset_index(drop=True)

    return transcription

  def get_lilypond_transcription(self, transcription, music_title=None):

    if music_title==None:
      music_title = self.file_name

    up_median = transcription[(transcription['CY']==1) | (transcription['HH']==1)]['time'].diff().median()
    if up_median*0.9 < self.spb:
      self.spb = self.spb*2
    
    times_segment = np.arange(transcription.loc[0,'time']-0.06,self.time_range[-1],self.spb)

    ly_string = '\\version "2.18.2"\n' 

    ly_string += '''
    \paper {
      top-margin = 10
      markup-system-spacing =
        #'((padding . 10))
    }
    '''

    ly_string += '\header {\n      title = "' + music_title + '"\n    }'

    up_string = '''
    up = \drummode {
    '''
    down_string = '''
    down = \drummode {
    '''

    for segment_time in times_segment:
      up_string += get_single_voice_quarter_transcription(segment_time, self.spb, transcription, 'up')
      down_string += get_single_voice_quarter_transcription(segment_time, self.spb, transcription, 'down')

    up_string += '''
    }
    '''
    down_string += '''
    }
    '''

    ly_string += up_string
    ly_string += down_string

    ly_string += '''
    \\new DrumStaff <<
      \\new DrumVoice { \\voiceOne \\up }
      \\new DrumVoice { \\voiceTwo \down }
    >>
    '''

    f = open(f'../data/lilypond_files/{self.file_name}.ly', 'w')
    f.write(ly_string)
    f.close()

  def get_pdf_transcription(self):
    
    subprocess.Popen(f'lilypond --output=../data/pdf_files/ ../data/lilypond_files/{self.file_name}.ly', shell=True)