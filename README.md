# DrumSheet
Transcription project from drum audios into drum sheets.

![logo](https://github.com/MLecardonnel/DrumSheet/blob/main/reports/figures/DrumSheet.png?raw=true)

The goal of the DrumSheet project is to create a tool that returns the drumming score sheet from any given drumming audio. The tool is based on image recognition to classify the types of percussion.

## Dataset

To create the classification models I used the annoted [MedleyDB](http://medleydb.weebly.com/) dataset. 

It consists of drum annotations and audio files for 23 tracks. For each of the tracks drum only, full mix and the original multi-track wav files are included. Two annotation files are provided for each track. I choosed to work with the first annotation file that groups the 7994 onsets into 6 classes based on drum instrument.

The audio and annotation files are published under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Audio segmentation process

The segmentation of the drum audio wav files is done by detecting the percussions. Threshold values are chosen for the signal amplitudes to detect where are the percussions. With a defined window size, the signal segments are transformed into spectrograms. The spectrograms give an image representation of the percussions on which we can perform image recognition. Bellow is the spectrogram of a kick drum stroke :

![logo](https://github.com/MLecardonnel/DrumSheet/blob/main/reports/figures/KD_0_MusicDelta_80sRock.png?raw=true)

## Classification method

|Models       | Well detected percussions | Wrongly detected percussions |
| ----------- |:-------------------------:|:----------------------------:|
|CY_60epochs  | 69.7%                     | 2.4%                         |
|HH_ResNet    | 93.4%                     | 2.3%                         |
|KD_ResNet    | 94.8%                     | 0.5%                         |
|SD_ResNet    | 93.4%                     | 2.6%                         |
|**AVERAGE**  | **87.8%**                 | **1.95%**                    |

## Drum audio transcription

![transcription](https://github.com/MLecardonnel/DrumSheet/blob/main/reports/figures/transcription.PNG?raw=true)

## Future improvements

The next step is to learn how to use [Lilypond](http://lilypond.org/) to generate the drumming score sheets.

## References

| **[1]** |                  **[C. Southall, C. Wu, A. Lerch, J. Hockman, MDB Drums - An Annotated Subset of MedleyDB for Automatic Drum Transcription, Proceedings of the 18th International Society for Music Information Retrieval Conference (ISMIR), 2017.](https://carlsouthall.files.wordpress.com/2017/12/ismir2017mdbdrums.pdf)**|
| :---- | :--- |