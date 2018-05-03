import numpy as np
import pandas as pd
from nptdms import tdms
from datetime import datetime
from dateutil.parser import parse

class ChData(object):
	def __init__(self, tdchannel):
		self.initialized = False
		self.name = tdchannel.properties['NI_ChannelName']
		self.timestart = tdchannel.properties['wf_start_time']
		self.dt = np.float32(tdchannel.properties['wf_increment'])
		self.fs = np.float32(1.0 / self.dt)
		self.sensitivity = np.float32(tdchannel.properties['Sensor Sensitivity (mV/EU)'])
		self.units = tdchannel.properties['Engineering Units']
		
		self.data = np.array(1000 * tdchannel.raw_data / self.sensitivity, dtype=np.float32)

		if self.data.shape is not None:
			self.initialized = True
	
	def __str__(self):
		return str(self.__class__) +':' + str(self.__dict__)

	def __repr__(self):
		return (self.__str__())


class VibData(object):
	def __init__(self, tdfile_path=None):
		self.initialized = False
		if tdfile_path is not None:
			self.tdfile = tdms.TdmsFile(tdfile_path)
			self.td_vib_channels = self.tdfile.group_channels('Vibration')
			self.td_channel_count = len(self.td_vib_channels)

			if self.td_channel_count < 1:
				print('Specified file is not a vibration TDMS file of understood format\n')
			else:
				self.initialize()

		else:
			self.tdfile = None

	def initialize(self):
		if not self.initialized:
			self.channels = []
			for channel in self.td_vib_channels:
				self.channels.append(ChData(channel))

	def __str__(self):
		return str(self.__class__) +':' + str(self.__dict__)

	def __repr__(self):
		return (self.__str__())

def dB(data, ref):
        """Return the dB equivelant of the input data"""
        return 20*np.log10(data / ref)

if __name__ == '__main__':
	import numpy as np
	import scipy.signal as sig
	import matplotlib
	import matplotlib.pyplot as plt

	tdmspath = './TDMS/'
	tdms_file_name = 'vib.tdms'

	vib = VibData(tdmspath+tdms_file_name)
	
	#for channel in vib.channels:
	channel = vib.channels[0]

	fft_master = 2**13
	win_size = np.int32(fft_master)
	fft_size = np.int32(fft_master)

	next_pow_2 = np.power(2, np.int32(np.ceil(np.log2(channel.data.shape[0]))))
	pad = np.zeros(next_pow_2 - channel.data.shape[0])
	y = np.append(channel.data, pad)
	window = np.hanning(y.shape[0])
	y = y * window

	spectrum = np.fft.fft(y)
	spectrum = dB(spectrum, 1.0)
	print(spectrum.shape)

	autopower = np.empty(int(spectrum.shape[0]/2), dtype=np.float32)
	autopower[:] = np.abs(spectrum * np.conj(spectrum))[:autopower.shape[0]]
	plt.subplot(1,2,1)

	spectrum_freqs = np.arange(spectrum.shape[0]) / np.float32(next_pow_2) * channel.fs
	plt.plot(spectrum_freqs, spectrum)

	plt.subplot(1,2,2)
	autopower_freqs = np.arange(autopower.shape[0]) / np.float32(next_pow_2) * channel.fs 
	plt.plot(autopower_freqs, autopower)

	print ("Highest frequency is:", np.argmax(autopower) * channel.fs / np.float32(next_pow_2), "Hz")
	plt.show()

	freqs = np.fft.fftfreq(y.shape[0], channel.dt)
	print('\n',freqs.shape)