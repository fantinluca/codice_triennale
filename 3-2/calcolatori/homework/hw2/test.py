import os,re
import numpy as np
import numpy.polynomial.polynomial as poly

#stream = os.popen("ping atl.speedtest.clouvider.net -n 10 -l 100 -i 13")
#output = stream.readlines()
#for i in range(len(output)): print(str(i), output[i])

#a = 'Risposta da 89.84.1.194: byte=10 durata=56ms TTL=54'
#b = re.findall('\d+',a)
#print(b)

a = np.array([np.array([]), np.array([]), np.array([]), np.array([])])
a[0] = np.append(a[0], 4)
print(a)