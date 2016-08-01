import pyfits as py
import numpy as np
from pylab import *
import os 
from cobra_sub import smooth
from read_output import *



def read_xshooter(name, plot=False):
	"""    
	Read ESO Xshooter spectra fits. Plotting capability.

    :INPUTS:
       name: Filename of fits spectra
       
       plot: True|False - Simple plot of the spectra
    :OUTPUTS:
       wave: wavelength array

       flux: flux array
	"""
	#w1delta=py.getval(name,'CDELT1',0)
	#w1start=py.getval(name,'CRVAL1',0)
	#flux=py.getdata(name,0)
	#wave=[]
	#nuu=len(flux)

	#for i in range(nuu):
	#	wave.append((i-1)*w1delta+w1start)

	data=py.getdata(name,0)
	wave = 10.0*data[0][0]
	flux = data[0][1]
	#SNR = 

	return(np.array(wave),np.array(flux))



def plot_all(folder):

	os.system("ls %s/*.fits > _temprd" % folder)
	os.system("mkdir %s_out" % folder)

	names = np.loadtxt("_temprd", dtype="string")

	nplots = len(names)

	if folder=="SWSex":
		ymin = 0
		ymax = 2e-14

	ymin = 0
	ymax = 2e-16

	lines = [6563,4686,4861,3646, 3203]
	label = [r"H$\alpha$", "He II", r"H$\beta$", "Jump", "He II"]

	for i in range(nplots):

		w,f = read_xshooter(names[i])

		#subplot(nplots/2,2,i+1)
		select = (w > 3000) * (w < 7000)

		print np.sum(select)

		if np.sum(select) > 0:

			try: 
				plot(w,smooth(f, window_len=10))
				xlim(3000,7000)
			
				ylim(ymin,ymax)
				xlabel("Wavelength")
				ylabel("Flux")
				vlines(lines, 0.8*ymax, 0.9*ymax)

				for j in range(len(lines)):
					text(lines[j]+20,0.9*ymax, label[j])

				print i, names[i]
				savefig("%s_out/%s_%i.png" % (folder,folder, i))

			except ValueError:
				print "Value Error on run %i" % i
				os.system("mv "+names[i]+" do_not_plot/")

			#try:
				#semilogy()
			
			#except ValueError:
			#	print "Couldn't log scale, not saving"

			

			clf()
	#os.system("rm -f _temprd")

setpars()
#plot_all("SWSex")
plot_all("V442Oph")

