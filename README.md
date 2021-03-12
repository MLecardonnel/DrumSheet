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

As several strokes can occure at the same time on different parts of the drums, I choosed to create a model for each following part : cymbal, hi-hat, kick drum, snare drum. The models are binary classifiers that indicates whether or not the drum part is struck given a spectrogram. Bellow are the performance results on the validation dataset : 

|Models       | Well detected percussions | Wrongly detected percussions |
| ----------- |:-------------------------:|:----------------------------:|
|CY_60epochs  | 69.7%                     | 2.4%                         |
|HH_ResNet    | 93.4%                     | 2.3%                         |
|KD_ResNet    | 94.8%                     | 0.5%                         |
|SD_ResNet    | 93.4%                     | 2.6%                         |
|**AVERAGE**  | **87.8%**                 | **1.95%**                    |

I used the ResNet50V2 model for the hi-hat, the kick drum and the snare drum classifiers as it gave me great performances. However I kept my simple convolutional neural network for the cymbal because the ResNet increased the percentage of wrongly detected percussions despite well increasing the percentage of well detected percussions. The performance are worse because there are less cymbal strokes in the dataset.

## Drum audio transcription

From a given drum audio wav file, the tool processes the segmentation of the signal where it detects strokes and then transforms the segments into spectrograms. Each spectrogram goes through all the models to predict which drums parts are struck. It then returns the times of the different strokes with a one hot encoding indicating the types of percussions. Bellow is an example for the 80sRock track from the MedleyDB dataset :

![transcription](https://github.com/MLecardonnel/DrumSheet/blob/main/reports/figures/transcription.PNG?raw=true)

## Future improvements

The next step is to learn how to use [Lilypond](http://lilypond.org/) to generate the drumming score sheets.

## References

| **[1]** |                  **[C. Southall, C. Wu, A. Lerch, J. Hockman, MDB Drums - An Annotated Subset of MedleyDB for Automatic Drum Transcription, Proceedings of the 18th International Society for Music Information Retrieval Conference (ISMIR), 2017.](https://carlsouthall.files.wordpress.com/2017/12/ismir2017mdbdrums.pdf)**|
| :---- | :--- |