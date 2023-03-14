# optical T1 sequence
import os
import sys
sys.path.insert(0, os.path.abspath('D:/users/moleq/code/Easy-Wave/'))
from easy_wave import AWG_Writer, Channel, REAL_CHANNELS
from wave_library import *
from visual_wave import plot_line


def genseq(buffer_t = 50e-6, init_t =500e-6, read_t = 10e-6, reset_t = 1e-2, tau = 10e-6, rate = 1e7):
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

	seq_len = buffer_t + init_t + buffer_t + reset_t

	read_len = buffer_t + init_t + buffer_t

	rtimes = np.arange(0,read_len,tau)

	# init_line = Zero(t=buffer_t, ch=chs['aom'])+Rect(t=init_t, ch=chs['aom'])+Zero(t=buffer_t, ch=chs['aom'])+Zero(t=reset_t, ch=chs['aom'])
	init_line = Rect(t = seq_len, ch = chs['aom'])
	# read_line = Rect(t = 50e-6, ch = chs['readout'])+Zero(t = (seq_len-50e-6), ch = chs['readout'])
	# rtimes = np.arange(0,500e-6,10e-6)
	for i in range(1,11):
		line = init_line
		# zero_len = read_len-rtime-read_t
		# read_line = Rect(t = rtime, ch = chs['readout'])+Zero(t = (seq_len-rtime), ch = chs['readout'])
		read_line = Rect(t = i*10e-6, ch = chs['readout'])+Zero(t = (seq_len-i*10e-6), ch = chs['readout'])
		# read_line = Zero(t = rtime, ch = chs['readout']) + Rect(t= read_t, ch = chs['readout']) + Zero(t = zero_len, ch = chs['readout'])+Zero(t=reset_t, ch=chs['readout'])
		line &= read_line
		writer.add_line(line,'test_'+str(i))



	writer.generate_and_upload('192.168.0.251', 'temp/init_sequence.awg',rate,limits=limits_awg)
	return writer

if __name__ == "__main__":
	buffer_t = 50e-6
	init_t = 500e-6
	read_t = 10e-6 # 10 us read time
	reset_t = 10e-3 #10 ms reset time
	tau = 10e-6
	rate = 1e6 #us sampling rate
	writer = generatesquence(buffer_t, init_t , read_t, reset_t, tau, rate)
	# writer.generate_and_upload('192.168.0.251', 'temp/binary_readout.awg',rate = 1e9,limits=limits_awg)

	print('test sequence uploaded.')

	100000e-6