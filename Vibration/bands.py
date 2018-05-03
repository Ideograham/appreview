#!/usr/bin/env python
import numpy
"""
Demonstrate and work around the fiddliness of translating between DFT
coefficients and accurate amplitude estimates (scaling; special handling
of DC component; signal-length-dependent special handling of Nyquist
component).
"""


def fft2ap(X, samplingfreq_hz=2.0, axis=0):
	"""
	Given discrete Fourier transform(s) <X> (with frequency along the
	specified <axis>), return a dict containing a properly scaled
	amplitude spectrum, a phase spectrum in degrees and in radians,
	and a frequency axis. Copes with all the edge conditions and
	fiddly bits that tend to go wrong when you try to do it by hand,
	namely:
	    (1) scaling according to Parseval's Theorem;
	    (2) special rescaling of the DC component;
	    (3) signal-length-dependent special rescaling of the Nyquist
	        component;
	    (4) removing the negative-frequency part of the spectrum.
	
	The inverse of   d=fft2ap(X)  is  X = ap2fft(**d)
	"""
	fs = float(samplingfreq_hz)	
	nsamp = int(X.shape[axis])
	biggest_pos_freq = float(numpy.floor(nsamp/2))       # floor(nsamp/2)
	biggest_neg_freq = -float(numpy.floor((nsamp-1)/2))  # -floor((nsamp-1)/2)
	posfreq = numpy.arange(0.0, biggest_pos_freq+1.0) * (float(fs) / float(nsamp))
	negfreq = numpy.arange(biggest_neg_freq, 0.0) * (float(fs) / float(nsamp))
	fullfreq = numpy.concatenate((posfreq,negfreq))
	sub = [slice(None)] * max(axis+1, len(X.shape))
	sub[axis] = slice(0,len(posfreq))
	X = project(X, axis)[sub]
	ph = numpy.angle(X)
	amp = numpy.abs(X) * (2.0 / float(nsamp))  # scaling according to Parseval's Theorem
	sub[axis] = 0
	amp[sub] /= 2.0  # DC is represented only once, and hence at double amplitude relative to others
	if nsamp%2 == 0:    # ...and if-and-only-if the number of samples is even, the same logic applies to the Nyquist frequency
		sub[axis] = -1  #    
		amp[sub] /= 2.0 #
	return {'amplitude':amp, 'phase_rad':ph, 'phase_deg':ph*(180.0/numpy.pi), 'freq_hz':posfreq, 'fullfreq_hz':fullfreq, 'samplingfreq_hz':fs, 'axis':axis}

def ap2fft(amplitude,phase_rad=None,phase_deg=None,samplingfreq_hz=2.0,axis=0,freq_hz=None,fullfreq_hz=None,nsamp=None):
	"""
	Keyword arguments match the fields of the dict
	output by fft2ap().

	The inverse of   d=fft2ap(X)  is  X = ap2fft(**d)
	"""
	fs = float(samplingfreq_hz)	
	if nsamp==None:
		if fullfreq_hz is not None: nsamp = len(fullfreq_hz)
		elif freq_hz is not None:   nsamp = len(freq_hz) * 2 - 2 # assume even number of samples if no other info
		else: nsamp = amplitude.shape[axis] * 2 - 2 # assume even number of samples if no other info
	
	amplitude = project(numpy.array(amplitude,dtype='float'), axis)
	if phase_rad is None and phase_deg is None: phase_rad = numpy.zeros(shape=amplitude.shape,dtype='float')
	if phase_rad is not None:
		if not isinstance(phase_rad, numpy.ndarray) or phase_rad.dtype != 'float': phase_rad = numpy.array(phase_rad,dtype='float')
		phase_rad = project(phase_rad, axis)
	if phase_deg is not None:
		if not isinstance(phase_deg, numpy.ndarray) or phase_deg.dtype != 'float': phase_deg = numpy.array(phase_deg,dtype='float')
		phase_deg = project(phase_deg, axis)
	if phase_rad is not None and phase_deg is not None:
		if phase_rad.shape != phase_deg.shape: 
			raise(ValueError, "conflicting phase_rad and phase_deg arguments")
		if numpy.max(numpy.abs(phase_rad * (180.0/numpy.pi) - phase_deg) > 1e-10): 
			raise(ValueError, "conflicting phase_rad and phase_deg arguments")
		
	if phase_rad is None:
		phase_rad = phase_deg * (numpy.pi/180.0)
	f = phase_rad * 1j
	f = numpy.exp(f)
	f = f * amplitude
	f *= float(nsamp)/2.0 # scaling according to Parseval's Theorem
	sub = [slice(None)] * max(axis+1, len(f.shape))
	sub[axis] = 0
	f[sub] *= 2.0
	if nsamp%2 == 0:
		sub[axis] = -1
		f[sub] *= 2.0
	sub[axis] = slice((nsamp%2)-2, 0, -1)
	f = numpy.concatenate((f, numpy.conj(f[sub])), axis=axis)
	return f

# helper function
def project(a, maxdim):
	"""
	Return a view of the numpy array <a> that has at least <maxdim>+1
	dimensions.
	"""
	if isinstance(a, numpy.matrix) and maxdim > 1: a = numpy.asarray(a)
	else: a = a.view()
	a.shape += (1,) * (maxdim-len(a.shape)+1)
	return a

if __name__ == '__main__':
	# Test code.
	
	# The following three parameters can be overridden by command-line args:
	freq_hz = 2.0  # with samplingfreq_hz=10 or 11, set freq_hz to 5.0 to test the Nyquist
	seconds = 1.0  # 
	samplingfreq_hz = 10.0 # with default seconds=1.0, set this to 11 instead of 10 to test the odd-number-of-samples case
	
	import sys
	args = getattr( sys, 'argv', [] )[ 1: ]
	if args: freq_hz = float( args.pop( 0 ) )
	if args: seconds = float( args.pop( 0 ) )
	if args: samplingfreq_hz = float( args.pop( 0 ) )
	
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