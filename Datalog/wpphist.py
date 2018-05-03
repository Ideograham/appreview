#wpphist.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def plot(data, ylabel='', xlabel='', title='', color='blue', sizex=7, sizey=10):
#todo - add axis labels and units

	#data = avail_restr_series
	fig, ax = plt.subplots()
	counts, bins, patches = ax.hist(data, facecolor=color, edgecolor='gray')

	fig.set_size_inches(sizex, sizey)
	
	# Set the ticks to be at the edges of the bins.
	ax.set_xticks(bins)
	
	ax.grid(True)
	ax.set_title(title)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	ax.xaxis.labelpad = 35
	
	# Set the xaxis's tick labels to be formatted with 1 decimal place...
	ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

	# Change the colors of bars at the edges...
	fifth, ninetyfifth = np.percentile(data, [5, 95])
	for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
	    if rightside < fifth:
	        patch.set_facecolor('red')
	    elif leftside > ninetyfifth:
	        patch.set_facecolor('red')

	# Label the raw counts and the percentages below the x-axis...
	bin_centers = 0.5 * np.diff(bins) + bins[:-1]
	for count, x in zip(counts, bin_centers):
	    # Label the raw counts
	    ax.annotate(str(count), xy=(x, 0), xycoords=('data', 'axes fraction'),
	        xytext=(0, -18), textcoords='offset points', va='top', ha='center')

	    # Label the percentages
	    percent = '%0.0f%%' % (100 * float(count) / counts.sum())
	    ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
	        xytext=(0, -32), textcoords='offset points', va='top', ha='center')


	# Give ourselves some more room at the bottom of the plot
	plt.subplots_adjust(bottom=0.15)
	
	return(plt.show())