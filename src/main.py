import os
import shutil
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from scipy.io import wavfile
import click

from drum_audio import DrumAudio

def load_model(model_path):
  return tf.keras.models.load_model(model_path)

CY_model = load_model('models/CY_60epochs')
HH_model = load_model('models/HH_ResNet')
KD_model = load_model('models/KD_ResNet')
SD_model = load_model('models/SD_ResNet')

@click.command()
@click.argument('file_name', default='data/drums_audio/MusicDelta_80sRock_Drum.wav')
@click.argument('music_title', default=None)
def get_transcription(file_name, music_title):
    audio = DrumAudio(file_name)
    transcription = audio.predict_kits(CY_model,HH_model,KD_model,SD_model)
    audio.get_lilypond_transcription(transcription, music_title)
    audio.get_pdf_transcription()

if __name__ == '__main__':
    get_transcription()


