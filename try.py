import wave, struct, math, cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

src = wave.open("22.wav")
decSrc = [[],[]]
numOfFrames = src.getnframes()
for i in range(numOfFrames):
    currFrame = src.readframes(1)
    decSrc[0].append(struct.unpack("<h", currFrame[:2])[0])
    decSrc[1].append(struct.unpack("<h", currFrame[2:])[0])
I = len(decSrc[0])
#M = input("Input Message: \n")
Lm = 8*len('Privet')
v = math.ceil(math.log(Lm,2)+1)
K = 2 ** (v+1)
N = math.ceil(I/K)
for i in range(N*K-I):
    decSrc[0].append(0)
    decSrc[1].append(0)
I = len(decSrc[0])
S = []
for n in range(N):
    S.append(decSrc[0][(n*K):(n+1)*K])
sigm = []
for n in range(N):
    sigm.append(np.fft.fft(S[n])[0:K/2+1])
A = []
ph = []
for i in range(N):
    tmp = []
    for n in range(int(K/2+1)):
        tmp.append(abs(sigm[i][n]))
    A.append(tmp)
    tmp = []
    for n in range(int(K/2+1)):
        tmp.append(cmath.phase(sigm[i][n]))
        ph.append(tmp)
phaseDiff = [[0 for i in range(K)]]
for i in range(1, N):
    tmp = []
    for n in range(int(K/2+1)):
        tmp.append(ph[i][n]-ph[i-1][n])
        phaseDiff.append(tmp)
m="".join(["{0:0>8b}".format(ord(i)) for i in M])
newPh = []
data = [0 for i in range(0, int(K/2+1))]
for k in range(int(K/2+1)):
    if k<=len(m):
        if k==0 or k==K/2:
            data[int(K/2)] = ph[0][int(K/2)]
        if 0 < k < K/2:
            data[int(K/2-k)] = (math.pi/2) * (1-2*int(m[k-1]))
    else:
        data[int(K / 2 - k)] = ph[0][int(K/2-k)]
newPh.append(data)
for n in range(1, N):
    tmp = []
    for i in range(int(K / 2 + 1)):
        tmp.append(newPh[n-1][i]+phaseDiff[n][i])
        newPh.append(tmp)
newS = []
for n in range(N):
    tmp = []
    for k in range(int(K / 2 + 1)):
        tmp.append(A[n][k]*np.exp(1j*newPh[n][k]))
    negative = []
    for i in tmp[1:-1]:
        negative.append(i.real + i.imag * (-1) * 1j)
    tmp = tmp + negative[::-1]
    newS.append(np.fft.ifft(tmp).real)
res = wave.open("output_original.wav","wb")
res.setparams(src.getparams())
output = b''
n = 0
for i in newS:
    for k in i:
       res.writeframes(struct.pack("<h", cutNum(int(k)))+struct.pack("<h",decSrc[1][n]))
    n+= 1

import wave, struct, math, cmath
import numpy as np
#name = input("file name: \n")
src = wave.open("22.wav")
if not (src.getnchannels() == 2 and src.getsampwidth() == 2 and src.getframerate() == 44100):
    print("Incorrect file")
exit()
decSrc = [[],[]]
K = int(input("Input segment lenth: \n"))
numOfFrames = K

for i in range(numOfFrames):
    currFrame = src.readframes(1)
    decSrc[0].append(struct.unpack("<h", currFrame[:2])[0])
src.close()
print("File uploaded")
print("File divided...")
S = decSrc[0][0:K]
print("FFT...")
sigm = np.fft.fft(S)[0:K/2+1]
print("Phase search...")
ph = []
for n in range(int(K/2+1)):
    ph.append(cmath.phase(sigm[n]))
print("Data uploading...")
lph = len(ph) - 1
b = ""
for t in range(1, int(K/2)):
    d = ph[lph - t]
    if d < -math.pi/3:
        b += "1"
    elif d > math.pi/3:
        b += "0"
    else:
        break
M = ""
b = (b[0:len(b)-(len(b)%8)])
for i in range(0, len(b)-1,8):
    if int(b[i:i+8],2)==0:
        break
    print("{} | {:>3d} | {}".format(b[i:i+8], int(b[i:i+8], 2), chr(int(b[i:i+8], 2))))
    M += chr(int(b[i:i+8], 2))
print("\nResult:\n" + M)
input()