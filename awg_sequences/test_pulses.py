# optical T1 sequence
import os
import sys
sys.path.insert(0, os.path.abspath('D:/users/moleq/code/Easy-Wave/'))
from easy_wave import AWG_Writer, Channel, REAL_CHANNELS
from wave_library import *
from visual_wave import plot_line


def genseq(init_t ,rate):
	# First let's give names to our channels

	chs = {
	    'ch1a1' : Channel.ch1_a,
	    'ch1m1' : Channel.ch1_m1,
	    'ch1m2': Channel.ch1_m2,
	    
	    'ch2a1'  : Channel.ch2_a,
	    'ch2m1' : Channel.ch2_m1,
	    'readout': Channel.ch2_m2,
	    
	    'pico_trig': Channel.ch3_a,
	    'aom'      : Channel.ch3_m1,
	    'res'   : Channel.ch3_m2,
	    
	    'res_analog': Channel.ch4_a,
	    '1550'     : Channel.ch4_m1,
	    '980'     : Channel.ch4_m2,
	}

	limits_awg = {Channel.ch3_m1:(0.0,1.0)}

	writer = AWG_Writer()
	aomch = [1,1,0,0]
	readch = [1,0,1,0]
	for i in range(len(aomch)):
		if aomch[i]:
			line = Rect(t=init_t, ch=chs['aom'])+Zero(t=init_t, ch=chs['aom'])
		else:
			line = Zero(t=init_t, ch=chs['aom'])+Rect(t=init_t, ch=chs['aom'])

		if readch[i]:
			line &= Rect(t=init_t, ch=chs['readout'])+Zero(t=init_t, ch=chs['readout'])
		else:
			line &= Zero(t=init_t, ch=chs['readout'])+Rect(t=init_t, ch=chs['readout'])
		writer.add_line(line,'test')

	writer.generate_and_upload('192.168.0.251', 'temp/temp.awg',rate,limits=limits_awg)
	return writer

if __name__ == "__main__":
	init_t = 100e-7
	writer = generatesquence(init_t)
	# writer.generate_and_upload('192.168.0.251', 'temp/binary_readout.awg',rate = 1e9,limits=limits_awg)

	print('test sequence uploaded.')