import math
import matplotlib.pyplot as plt

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

print fp
print fp2

#define the frequency where we'll calc the gain and the error
f = [300,1000,3000,10000,30000,100000,300000,1000000]

x=[]
dx=[]
ph=[]
dph=[]

#Valori ottenuti dalle misure (necessarie per la generazione del diagramma di bode)
mis=[7.00,15.30,18.02,17.20,12.21,2.92,-8.89,-26.9]
dmis=[0.7,0.67,0.62,0.63,0.74,0.69,0.79,1.0]
misp=[0.00121,0.000754,0.000170,-0.503,-1.13,-1.89,-3.77,-3.14]
dmisp=[0.00006,0.000046,0.000022,0.22,0.06,0.10,0.17,0.19]

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
	#calc the absolute error of the gain given by the frequency error
	ddf = (k/i) * df
	if debug: print ("ddf %f") % ddf
	#calc the absolute error of the gain given by the first pole error
	ddfp = (kp/mfp)*(df + ((i/fp)*dfp))
	if debug: print ("ddfp %f") % ddfp
	#calc the absolute error of the gain given by the second pole error
	ddfp2 = (kp2/mfp2)*(df + ((i/fp2)*dfp2))
	if debug: print ("ddfp2 %f") % ddfp2
	#calc the absolute error of the gain (summing the error calculated before)
	dav = davdb + ddf + ddfp + ddfp2
	#calc of the phase
	pi = math.atan( (1 - (math.pow(i,2)/(fp*fp2))) / (i*(fp2 + fp)/(fp2*fp)))
        x.append(round(av,2))
        dx.append(round(dav,2))
        ph.append(round(pi,2))
        dph.append(round(0.00,2))
	print("@%dHz\tAv = (%.2f +- %.2f)dB\tPhase = (%.2f +- %.2f)rad") % (i, x[len(x)-1], dx[len(x)-1],ph[len(ph)-1],dph[-1])

#Rappresento graficamente risultati ottenuti con incertezze
plt.subplot(211)
plt.errorbar(f,x,yerr=dx,color="b",linestyle="--")
plt.errorbar(f,mis,yerr=dmis,color="r",linestyle=":")
plt.xscale('log')
plt.subplot(212)
plt.errorbar(f,ph,yerr=dph,color="b",linestyle="--")
plt.errorbar(f,misp,yerr=dmisp,color="r",linestyle=":")
plt.xscale('log')
plt.show()
