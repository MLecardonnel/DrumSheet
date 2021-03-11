import os
import shutil
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from scipy.io import wavfile

class DrumAudio():
  def __init__(
        self,
        audio_path: str,
        **kwargs
        ):
    super(DrumAudio, self).__init__(**kwargs)

    self.freq_rate, self.signal = wavfile.read(audio_path)

    size = self.signal.shape[0]
    secs = size / self.freq_rate
    T = 1.0/self.freq_rate
    self.time_range = np.arange(0, secs, T).round(6)
  
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