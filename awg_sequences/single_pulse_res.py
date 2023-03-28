# optical T1 sequence
import os
import sys
sys.path.insert(0, os.path.abspath('D:/users/moleq/code/Easy-Wave/'))
from easy_wave import AWG_Writer, Channel, REAL_CHANNELS
from wave_library import *
from visual_wave import plot_line


def genseq(init_t =50e-6, reset_t = 50e-6, rate = 1e8):
	# First let's give names to our channels

	chs = {
	    'ch1a1' : Channel.ch1_a,
	    'swabian' : Channel.ch1_m1,
	    '980_aom': Channel.ch1_m2,
	    
	    'ch2a1'  : Channel.ch2_a,
	    'ctr1' : Channel.ch2_m1,
	    'ctr2': Channel.ch2_m2,
	    
	    'pico_trig': Channel.ch3_a,
	    'res_aom'      : Channel.ch3_m1,
	    'res'   : Channel.ch3_m2,
	    
	    'res_analog': Channel.ch4_a,
	    '1550'     : Channel.ch4_m1,
	    'ch3m2'     : Channel.ch4_m2,
	}

	limits_awg = {Channel.ch3_m1:(0.0,2.7),Channel.ch1_m2:(0.0,1.0)}

	writer = AWG_Writer()


	seq_len = reset_t+init_t
	# make first line an AOM on/READ on line
	# line1 = Rect(t=seq_len,ch = chs['980_aom'])
	line1 = Rect(t=seq_len,ch = chs['res_aom'])
	line1 &= Zero(t=seq_len,ch = chs['swabian'])
	writer.add_line(line1,'aom on')

	# make first line an AOM on/READ on line
	# line1 = Rect(t=seq_len,ch = chs['980_aom'])
	line1 = Rect(t=seq_len,ch = chs['res_aom'])
	line1 &= Zero(t=seq_len,ch = chs['swabian'])
	writer.add_line(line1,'aom off')




	# line = Rect(t=init_t,ch=chs['980_aom'])+Zero(t=reset_t,ch=chs['980_aom'])
	line = Rect(t=init_t,ch=chs['res_aom'])+Zero(t=reset_t,ch=chs['res_aom'])
	line &= Rect(t=init_t,ch=chs['swabian'])+Zero(t=reset_t,ch=chs['swabian'])
	i=1
	writer.add_line(line,'sp_'+str(i))



	writer.generate_and_upload('192.168.0.251', 'temp/single_pulse_res_20usON_20usOFF.awg',rate,limits=limits_awg)
	return writer

if __name__ == "__main__":
    genseq()