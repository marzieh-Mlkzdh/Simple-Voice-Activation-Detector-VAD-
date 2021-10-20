from __future__ import division
import numpy as np
import statistics
from scipy.io import wavfile
from numpy import linspace
import matplotlib.pyplot as plot
import numpy as n


class myClass:
    fName = ''  # sentence5.sp13.wav
    feature = ''  # ZCR, Energy

    def __init__(self, fName, feature):
        self.fName = fName
        self.feature = feature

    def details(self):
        self.fs, self.signal = wavfile.read(self.fName)
        self.signal = self.signal / max(abs(self.signal))
        assert min(self.signal) >= -1 and max(self.signal) <= 1
        res = {}
        res['fs'] = self.fs
        res['length of signal'] = len(self.signal)
        return res

    def signalPlot(self):
        _, (sp1, sp2) = plot.subplots(1, 2, figsize=(16, 4))

        # plot raw signal
        sp1.plot(self.signal)
        sp1.set_title('Raw Signal')
        sp1.set_xlabel('SAMPLE\n(a)')
        sp1.autoscale(tight='both')

        # plot spectrogram
        sp2.specgram(self.signal, Fs=self.fs)
        sp2.set_title('Spectogram')
        sp2.set_xlabel('TIME\n(b)')
        nSecs = len(self.signal) / self.fs
        ticksPerSec = 3

        # add 1 to include time=0
        nTicks = nSecs * ticksPerSec + 1
        xTickMax = sp2.get_xticks()[-1]
        sp2.set_xticks(linspace(0, xTickMax,int( nTicks)))
        sp2.set_xticklabels([round(x, 2) for x in linspace(0, int(nSecs), int(nTicks))])
        sp2.set_ylabel('FREQ')
        maxFreq = self.fs / 2

        # add 1 to include freq=0
        nTicks = maxFreq / 1000 + 1
        sp2.set_yticks(linspace(0, 1, int(nTicks)))
        sp2.set_yticklabels(linspace(0, int(maxFreq), int(nTicks)))
        sp2.autoscale(tight='both')
        plot.show()


    def showPlot(self):
        if self.feature == 'Energy':
            self.energyplot()
        elif self.feature == 'ZCR':
            self.zcrplot()

    def STEss(self):
        # list of short-time energies
        self.STEs = []
        assert self.fs % 1000 == 0

        sampsPerMilli = int(self.fs / 1000)
        millisPerFrame = 20
        sampsPerFrame = sampsPerMilli * millisPerFrame

        # number of non-overlapping _full_ frames
        nFrames = int(len(self.signal) / sampsPerFrame)

        for k in range(nFrames):
            startIdx = k * sampsPerFrame
            stopIdx = startIdx + sampsPerFrame
            window = np.zeros(self.signal.shape)

            # rectangular window
            window[startIdx:stopIdx] = 1
            STE = sum((self.signal ** 2) * (window ** 2))
            self.STEs.append(STE)
        return self.STEs

    def energyplot(self):
        self.STEss()
        x = [i for i in range(len(self.STEs))]
        for x1, x2, y1, y2 in zip(x, x[1:], self.STEs, self.STEs[1:]):
            if y2 >= y1 and y2 <= 5:
                plot.plot([x1, x2], [y1, y2], 'r')
            elif y2 <= y1 and y1 <= 5:
                plot.plot([x1, x2], [y1, y2], 'r')
            else:
                plot.plot([x1, x2], [y1, y2], 'g')

        plot.title('Short-Time Energy')
        plot.ylabel('ENERGY')
        plot.xlabel('FRAME')
        plot.autoscale(tight='both')
        plot.show()

    def ZCR(self):
        assert self.fs % 1000 == 0

        sampsPerMilli = int(self.fs / 1000)
        millisPerFrame = 20
        sampsPerFrame = sampsPerMilli * millisPerFrame

        # number of non-overlapping _full_ frames
        nFrames = int(len(self.signal) / sampsPerFrame)

        DC = statistics.mean(self.signal)

        # create a new signal, preserving old
        newSignal = self.signal - DC

        # list of short-time zero crossing counts
        self.ZCCs = []
        for i in range(nFrames):
            startIdx = i * sampsPerFrame
            stopIdx = startIdx + sampsPerFrame

            # /s/ is the frame, named to correspond to the equation
            s = newSignal[startIdx:stopIdx]
            ZCC = 0
            for k in range(1, len(s)):
                ZCC += 0.5 * abs(np.sign(s[k]) - np.sign(s[k - 1]))
            self.ZCCs.append(ZCC)
        return self.ZCCs

    def zcrplot(self):
        self.ZCR()
        x = [i for i in range(len(self.ZCCs))]
        for x1, x2, y1, y2 in zip(x, x[1:], self.ZCCs, self.ZCCs[1:]):
            if y2 >= y1 and y2 <= 60:
                plot.plot([x1, x2], [y1, y2], 'g')
            elif y2 <= y1 and y1 <= 60:
                plot.plot([x1, x2], [y1, y2], 'g')
            else:
                plot.plot([x1, x2], [y1, y2], 'r')

        plot.title('Short-Time Zero Crossing Counts')
        plot.ylabel('ZCC')
        plot.xlabel('FRAME')
        plot.autoscale(tight='both')
        plot.show()


