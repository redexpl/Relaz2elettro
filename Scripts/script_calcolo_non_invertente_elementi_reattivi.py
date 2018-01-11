import math

debug = False

#define gain value of the amplfier
a = 9.33
#define the absolute error of gain 10%
da = 0.933
#define the value of the resistor in series of the output port of the amplifier
ru = 1000
#define the absolute error of Ru 5%
dru = 0.05*ru
#define the value of C6
csei = 10E-9
#define the absolute error of C6 20%
dcsei = 0.2*csei
#define value of Cin (sum of the capacitors in input)
cin = 13.3 * 1E-9
#define the error of Cin
dcin = 0.2*cin
#define Rin
rin = 10E3
#define the error of Rin 5%
drin = 0.05*rin
#define the error of the frequency
df = 0
#define k, a usefull costant
k = 20/math.log(10)
#calc the frequency of the first pole
fp = 1/(2 * math.pi * ru * csei)
#calc the frequency of the second pole
fp2 = 1/(2 * math.pi * rin * cin)
#calc the error of the first pole
dfp = 2*math.pi*math.pow(fp,2)*((ru * dcsei)+(dru * csei))
if debug: print ("fp %f") % fp
if debug: print ("dfp %f") % dfp
#calc the error of the second pole
dfp2 = 2*math.pi*math.pow(fp2,2)*((rin * dcin)+(cin * drin))
if debug: print ("fp2 %f") % fp2
if debug: print ("dfp2 %f") % dfp2
#calc the costant gain value in dB
avdb = 20*math.log(a * cin * rin,10)
#calc the error costant gain value in dB
davdb = k*((da/a)+(drin/rin)+(dcin/cin))
if debug: print ("av dB %f") % avdb
if debug: print ("dav dB %f") % davdb

#define the frequency where we'll calc the gain and the error
f = [300,1000,3000,10000,30000,100000,300000,1000000]

#for each frequency defined above
for i in f:
	#calc the modulo of the first pole at a specific frequency
	mfp = math.sqrt(1+math.pow(i/fp,2))
	if debug: print("mfp %f") % mfp
	#calc the modulo of the second pole at a specific frequency
	mfp2 = math.sqrt(1+math.pow(i/fp2,2))
	if debug: print("mfp2 %f") % mfp2
	#calc the gain of the amplifier at a specific frequency
	av = avdb + (20*math.log(2*math.pi*i,10)) - (20*math.log(mfp,10)) - (20*math.log(mfp2,10))
	#calc a usefull costant for the first pole
	kp = (k*i)/(math.pow(fp,2)*mfp)
	if debug: print ("kp %f") % kp
	#calc a usefull costant for the second pole
	kp2 = (k*i)/(math.pow(fp2,2)*mfp2)
	if debug: print ("kp2 %f") % kp2
	#calc the absolute error of the gain given by the frequence uncertainty
	ddf = (k/i) * df
	if debug: print ("ddf %f") % ddf
	#calc the absolute error of the gain given by the first pole uncertainty
	ddfp = (kp/mfp)*(df + ((i/fp)*dfp))
	if debug: print ("ddfp %f") % ddfp
	#calc the absolute error of the gain given by the second pole uncertainty
	ddfp2 = (kp2/mfp2)*(df + ((i/fp2)*dfp2))
	if debug: print ("ddfp2 %f") % ddfp2
	#calc the absolute error of the gain (summing the error calculated before)
	dav = davdb + ddf + ddfp + ddfp2
	#printn, in a shitting way, the results
	print("@%dHz\tAv = (%.2f +- %.2f)dB") % (i, round(av,2), round(dav,2))
