import numpy as np
from scipy import signal

# note definitions, note names to frequencies
# format
#   first letter is the note
#   if there is an "S", means sharp
#   number is octave on the keyboard, 0-lowest, 8-highest
note_freq = {
"NOTE_A0"  : 27.5,
"NOTE_AS0" : 29.14,
"NOTE_B0"  : 30.87,
"NOTE_C1"  : 32.7,
"NOTE_CS1" : 34.65,
"NOTE_D1"  : 36.71,
"NOTE_DS1" : 38.89,
"NOTE_E1"  : 41.2,
"NOTE_F1"  : 43.65,
"NOTE_FS1" : 46.25,
"NOTE_G1"  : 49,
"NOTE_GS1" : 51.91,
"NOTE_A1"  : 55,
"NOTE_AS1" : 58.27,
"NOTE_B1"  : 61.74,
"NOTE_C2"  : 65.41,
"NOTE_CS2" : 69.3,
"NOTE_D2"  : 73.42,
"NOTE_DS2" : 77.78,
"NOTE_E2"  : 82.41,
"NOTE_F2"  : 87.31,
"NOTE_FS2" : 92.5,
"NOTE_G2"  : 98,
"NOTE_GS2" : 103.83,
"NOTE_A2"  : 110,
"NOTE_AS2" : 116.54,
"NOTE_B2"  : 123.47,
"NOTE_C3"  : 130.81,
"NOTE_CS3" : 138.59,
"NOTE_D3"  : 146.83,
"NOTE_DS3" : 155.56,
"NOTE_E3"  : 164.81,
"NOTE_F3"  : 174.61,
"NOTE_FS3" : 185,
"NOTE_G3"  : 196,
"NOTE_GS3" : 207.65,
"NOTE_A3"  : 220,
"NOTE_AS3" : 233.08,
"NOTE_B3"  : 246.94,
"NOTE_C4"  : 261.63,
"NOTE_CS4" : 277.18,
"NOTE_D4"  : 293.66,
"NOTE_DS4" : 311.13,
"NOTE_E4"  : 329.63,
"NOTE_F4"  : 349.23,
"NOTE_FS4" : 369.99,
"NOTE_G4"  : 392,
"NOTE_GS4" : 415.3,
"NOTE_A4"  : 440,
"NOTE_AS4" : 466.16,
"NOTE_B4"  : 493.88,
"NOTE_C5"  : 523.25,
"NOTE_CS5" : 554.37,
"NOTE_D5"  : 587.33,
"NOTE_DS5" : 622.25,
"NOTE_E5"  : 659.26,
"NOTE_F5"  : 698.46,
"NOTE_FS5" : 739.99,
"NOTE_G5"  : 783.99,
"NOTE_GS5" : 830.61,
"NOTE_A5"  : 880,
"NOTE_AS5" : 932.33,
"NOTE_B5"  : 987.77,
"NOTE_C6"  : 1046.5,
"NOTE_CS6" : 1108.73,
"NOTE_D6"  : 1174.66,
"NOTE_DS6" : 1244.51,
"NOTE_E6"  : 1318.51,
"NOTE_F6"  : 1396.91,
"NOTE_FS6" : 1479.98,
"NOTE_G6"  : 1567.98,
"NOTE_GS6" : 1661.22,
"NOTE_A6"  : 1760,
"NOTE_AS6" : 1864.66,
"NOTE_B6"  : 1975.53,
"NOTE_C7"  : 2093,
"NOTE_CS7" : 2217.46,
"NOTE_D7"  : 2349.32,
"NOTE_DS7" : 2489.02,
"NOTE_E7"  : 2637.02,
"NOTE_F7"  : 2793.83,
"NOTE_FS7" : 2959.96,
"NOTE_G7"  : 3135.96,
"NOTE_GS7" : 3322.44,
"NOTE_A7"  : 3520,
"NOTE_AS7" : 3729.31,
"NOTE_B7"  : 3951.07,
"NOTE_C8"  : 4186.01,
}

midi_freq = {
0	:	8.18,
1	:	8.66,
2	:	9.18,
3	:	9.72,
4	:	10.3,
5	:	10.91,
6	:	11.56,
7	:	12.25,
8	:	12.98,
9	:	13.75,
10	:	14.57,
11	:	15.43,
12	:	16.35,
13	:	17.32,
14	:	18.35,
15	:	19.45,
16	:	20.6,
17	:	21.83,
18	:	23.12,
19	:	24.5,
20	:	25.96,
21	:	27.5,
22	:	29.14,
23	:	30.87,
24	:	32.7,
25	:	34.65,
26	:	36.71,
27	:	38.89,
28	:	41.2,
29	:	43.65,
30	:	46.25,
31	:	49,
32	:	51.91,
33	:	55,
34	:	58.27,
35	:	61.74,
36	:	65.41,
37	:	69.3,
38	:	73.42,
39	:	77.78,
40	:	82.41,
41	:	87.31,
42	:	92.5,
43	:	98,
44	:	103.83,
45	:	110,
46	:	116.54,
47	:	123.47,
48	:	130.81,
49	:	138.59,
50	:	146.83,
51	:	155.56,
52	:	164.81,
53	:	174.61,
54	:	185,
55	:	196,
56	:	207.65,
57	:	220,
58	:	233.08,
59	:	246.94,
60	:	261.63,
61	:	277.18,
62	:	293.66,
63	:	311.13,
64	:	329.63,
65	:	349.23,
66	:	369.99,
67	:	392,
68	:	415.3,
69	:	440,
70	:	466.16,
71	:	493.88,
72	:	523.25,
73	:	554.37,
74	:	587.33,
75	:	622.25,
76	:	659.26,
77	:	698.46,
78	:	739.99,
79	:	783.99,
80	:	830.61,
81	:	880,
82	:	932.33,
83	:	987.77,
84	:	1046.5,
85	:	1108.73,
86	:	1174.66,
87	:	1244.51,
88	:	1318.51,
89	:	1396.91,
90	:	1479.98,
91	:	1567.98,
92	:	1661.22,
93	:	1760,
94	:	1864.66,
95	:	1975.53,
96	:	2093,
97	:	2217.46,
98	:	2349.32,
99	:	2489.02,
100	:	2637.02,
101	:	2793.83,
102	:	2959.96,
103	:	3135.96,
104	:	3322.44,
105	:	3520,
106	:	3729.31,
107	:	3951.07,
108	:	4186.01,
109	:	4434.92,
110	:	4698.64,
111	:	4978.03,
112	:	5274.04,
113	:	5587.65,
114	:	5919.91,
115	:	6271.93,
116	:	6644.88,
117	:	7040,
118	:	7458.62,
119	:	7902.13,
120	:	8372.02,
121	:	8869.84,
122	:	9397.27,
123	:	9956.06,
124	:	10548.08,
125	:	11175.3,
126	:	11839.82,
127	:	12543.85,
128	:	13289.75
}


# determines the waveform type of audio wave
def wave_func(s, waveform):
    if waveform == 'sinusoid':
        return np.sin(s)
    elif waveform == 'sawtooth':
        return signal.sawtooth(s)
    elif waveform == 'square':
        return signal.square(s)
    elif waveform == 'triangle':
        return signal.sawtooth(s, width=.5)


# writes individual note wave to global variable
def play_note(song, bpm, note, duration, midi=False, waveform='sinusoid'):
    # calculate seconds per beat
    spb = 1 / bpm * 60 * 4
    dur = spb / duration
    volume = 1  # 0.0 - 1.0
    fs = 44100  # sampling rate

    # rest
    if note == "REST":
        # generate samples with no soung
        samples = np.cumsum(2.0 * np.pi * 0 / fs * np.ones(int(fs * float(dur))))
        samples = np.sin(samples)  # sinusoid
    else:
        if midi:
            freq = midi_freq[note]
        else:
            freq = note_freq[note]
        # generate samples, note conversion
        samples = np.cumsum(2.0 * np.pi * freq / fs * np.ones(int(fs * float(dur))))
        samples = wave_func(samples, waveform)
        samples = volume * samples

    # append note to the song
    return np.append(song, samples)
