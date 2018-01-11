import math

debug = False

a = 9.33
da = 0.933
ru = 1000
dru = 0.05*ru
csei = 10E-9
dcsei = 0.2*csei
cin = 13.3 * 1E-9
dcin = 0.2*cin
rin = 10E3
drin = 0.05*rin

df = 0

k = 20/math.log(10)

fp = 1/(2 * math.pi * ru * csei)
fp2 = 1/(2 * math.pi * rin * cin)

dfp = 2*math.pi*math.pow(fp,2)*((ru * dcsei)+(dru * csei))
if debug: print ("fp %f") % fp
if debug: print ("dfp %f") % dfp
dfp2 = 2*math.pi*math.pow(fp2,2)*((rin * dcin)+(cin * drin))
if debug: print ("fp2 %f") % fp2
if debug: print ("dfp2 %f") % dfp2

avdb = 20*math.log(a * cin * rin,10)
davdb = k*((da/a)+(drin/rin)+(dcin/cin))
if debug: print ("av dB %f") % avdb
if debug: print ("dav dB %f") % davdb


f = [300,1000,3000,10000,30000,100000,300000,1000000]




for i in f:

	mfp = math.sqrt(1+math.pow(i/fp,2))
	if debug: print("mfp %f") % mfp
	mfp2 = math.sqrt(1+math.pow(i/fp2,2))
	if debug: print("mfp2 %f") % mfp2
	
	av = avdb + (20*math.log(2*math.pi*i,10)) - (20*math.log(mfp,10)) - (20*math.log(mfp2,10))

	kp = (k*i)/(math.pow(fp,2)*mfp)

	if debug: print ("kp %f") % kp

	kp2 = (k*i)/(math.pow(fp2,2)*mfp2)

	if debug: print ("kp2 %f") % kp2
	
	ddf = (k/i) * df
	
	if debug: print ("ddf %f") % ddf

	ddfp = (kp/mfp)*(df + ((i/fp)*dfp))

	if debug: print ("ddfp %f") % ddfp

	ddfp2 = (kp2/mfp2)*(df + ((i/fp2)*dfp2))

	if debug: print ("ddfp2 %f") % ddfp2
	
	dav = davdb + ddf + ddfp + ddfp2

#	if debug: print("@" + str(i) + "Hz\t\tAv = (" + str(av) + " +- " + str(dav) + " dB")
	print("@%dHz\tAv = (%.2f +- %.2f)dB") % (i, round(av,2), round(dav,2))
