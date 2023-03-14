# optical T1 sequence
import os
import sys
sys.path.insert(0, os.path.abspath('D:/users/moleq/code/Easy-Wave/'))
from easy_wave import AWG_Writer, Channel, REAL_CHANNELS
from wave_library import *
from visual_wave import plot_line


def genseq(init_t =2e-3, read_t = 10e-6, tstart = 5e-6,tend=500e-6, reset_t = 500e-6, read_delay=10e-6, npoints=18, rate = 1e7):
	# First let's give names to our channels

	chs = {
	    'ch1a1' : Channel.ch1_a,
	    'swabian' : Channel.ch1_m1,
	    'ch1m2': Channel.ch1_m2,
	    
	    'ch2a1'  : Channel.ch2_a,
	    'ctr1' : Channel.ch2_m1,
	    'ctr2': Channel.ch2_m2,
	    
	    'pico_trig': Channel.ch3_a,
	    'aom'      : Channel.ch3_m1,
	    'res'   : Channel.ch3_m2,
	    
	    'res_analog': Channel.ch4_a,
	    '1550'     : Channel.ch4_m1,
	    '980'     : Channel.ch4_m2,
	}

	limits_awg = {Channel.ch3_m1:(0.0,1.0)}

	writer = AWG_Writer()

	base_t = (tend/tstart)**(1.0/float(npoints))
	rtimes = np.round(np.logspace(1,npoints,base=base_t,endpoint=True,num=npoints),1)*tstart
	print(rtimes)
	max_interp_t = rtimes[-1]

	seq_len = 2*init_t+rtimes[-1]+reset_t
	# make first line an AOM on/READ on line
	line1 = Rect(t=seq_len,ch = chs['aom'])
	line1 &= Rect(t=seq_len,ch = chs['ctr1'])
	line1 &= Zero(t=seq_len,ch = chs['ctr2'])
	line1 &= Zero(t=seq_len,ch = chs['swabian'])
	writer.add_line(line1,'AOM ON/READ ON CTR 1')

	# make first line an AOM on/READ on line
	line1 = Rect(t=seq_len,ch = chs['aom'])
	line1 &= Zero(t=seq_len,ch = chs['ctr1'])
	line1 &= Rect(t=seq_len,ch = chs['ctr2'])
	line1 &= Zero(t=seq_len,ch = chs['swabian'])
	writer.add_line(line1,'AOM ON/READ ON  CTR 2')



	for i,rtime in enumerate(rtimes):
		wait_t = (tend-rtime)+reset_t
		delta_t = max_interp_t-rtime
		line = Rect(t=init_t,ch=chs['aom'])+Zero(t=rtime,ch=chs['aom'])+Rect(t=init_t,ch=chs['aom'])+Rect(t = delta_t,ch=chs['aom'])+Zero(t=reset_t,ch=chs['aom'])
		line &= Rect(t=init_t,ch=chs['swabian'])+Zero(t=rtime,ch=chs['swabian'])+Zero(t=init_t,ch=chs['swabian'])+Zero(t=wait_t,ch=chs['swabian'])
		wait_t2 = init_t+rtime+init_t+wait_t-(init_t+rtime+read_delay+read_t)
		line &= Zero(t=init_t,ch=chs['ctr1'])+Zero(t=rtime,ch=chs['ctr1'])+Zero(t=read_delay,ch=chs['ctr1'])+Rect(t=read_t,ch=chs['ctr1'])+Zero(t=wait_t2,ch=chs['ctr1'])
		wait_t3 = init_t+rtime+init_t+wait_t-(init_t+rtime+(init_t-2*read_delay)+read_t)
		line &= Zero(t=init_t,ch=chs['ctr2'])+Zero(t=rtime,ch=chs['ctr2'])+Zero(t=(init_t-2*read_delay),ch=chs['ctr2'])+Rect(t=read_t,ch=chs['ctr2'])+Zero(t=wait_t3,ch=chs['ctr2'])

		writer.add_line(line,'t1_'+str(round(rtime*1e6,0))+' us')



	writer.generate_and_upload('192.168.0.251', 'temp/optical_T1_500usreset_logpoints.awg',rate,limits=limits_awg)
	return writer
