import bands
import nptdms
import vib_tdms

if __name__ == '__main__':
	# Test code.
	
	# The following three parameters can be overridden by command-line args:




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
	print(spectrum.shape)


	freq_hz = channel.fs  # with samplingfreq_hz=10 or 11, set freq_hz to 5.0 to test the Nyquist
	seconds = channel.data.shape[0]*channel.dt  # 
	samplingfreq_hz = 10.0 # with default seconds=1.0, set this to 11 instead of 10 to test the odd-number-of-samples case
	
	
	nsamples = int( round( samplingfreq_hz * seconds ) )
	theta = numpy.linspace( 0, 1, nsamples, endpoint=0 )
	x = numpy.cos( 2 * numpy.pi * freq_hz * theta ) # generate wave
	x = x[ numpy.newaxis, : ] * [ [ 1 ], [ 2 ] ] + [ [ 3 ], [ 5 ] ]  # create an array with two rows, each row a scaled shifted version of the wave 
	X = numpy.fft.fft( x, axis=1 )
	d = fft2ap( X, 	samplingfreq_hz=samplingfreq_hz , axis=1 )
	
	# reconstruct	
	Xr = ap2fft( **d )
	xr = numpy.fft.ifft( Xr, axis=1 ).real
	print( 'err = %g' % numpy.abs(x-xr).max() ) # reconstruction error should be tiny (say 1e-14)
	
	# Check output:  DC components should be exactly 3 and 5; chosen freq_hz components
	# should have amplitude 1 and 2, regardless of whether they're the Nyquist or not,
	# and of whether nsamples is even or odd	
	for k,v in sorted( d.items() ): print( '%s = %s' % ( k, str( v ) ) )
	# plot amplitude spectrum.
	#import pylab
	import matplotlib.pyplot as plt
	#pylab.ion()
	plt.bar( d[ 'freq_hz' ]-0.5, d[ 'amplitude' ][ 0 ], width=0.5, color='b' )
	plt.bar( d[ 'freq_hz' ],     d[ 'amplitude' ][ 1 ], width=0.5, color='r' )
	plt.title( 'number of samples = %d' % nsamples )
	plt.ylabel( 'amplitude' )
	plt.xlabel( 'frequency (Hz)' )
	plt.grid( True )
	plt.show()