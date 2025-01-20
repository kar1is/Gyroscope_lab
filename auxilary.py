import matplotlib.pyplot as plt
import numpy as np
import scipy

Tm = [23.3484483738813, 25.103941725815982, 40.14169478286471, 29.135991912011946, 28.870370433324588, 43.57117908140996]
Tmerr = [1.514301528615647e-05, 1.750571967562564e-05, 4.4759704344699e-05, 2.3580694616498477e-05, 2.3152504802226304e-05, 5.2730391388422504e-05]

Tc = [26.0, 30.2, 56, 40, 41, 57]
Tcerr = [0.4, 0.4, 2, 1, 1, 2]

x = np.linspace(0, 60, 1000)
y = x

plt.xlabel(r'$T_{p, calculated}$, s')
plt.ylabel(r'$T_{p, measured}$, s')
plt.errorbar(Tc, Tm, xerr=Tcerr, yerr=Tmerr, fmt='o', color="#000000")
plt.plot(x,y,'k', linestyle='dashed')
[k], res1 = scipy.optimize.curve_fit(lambda t,k: k*t,  Tc,  Tm)
dk = np.sqrt(res1[0][0])
y = k*x
print(k, dk)
plt.plot(x,y,'r', linestyle='dashed')
plt.tight_layout()
plt.savefig('C:\\Users\\Kārlis\\Videos\\Gyroscope\\EPS\\LinearPlot.eps', format="eps")
plt.show()