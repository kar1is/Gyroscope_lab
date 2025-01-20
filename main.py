import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy
import glob
import os
import re

p=glob.glob(r'path*')
for folder in p:
    regexp = re.compile(r'unknown|dont|EPS')
    if regexp.search(folder):
        continue
    if os.path.isdir(folder):
        file = glob.glob(folder + r'\*.csv')[0]
        file_data = pd.read_csv(file)
        fig, ax1 = plt.subplots()
        
        ax2 = ax1.twinx()
        
        #ax1.set_title(os.path.basename(folder))
        ax1.set_xlabel(r'Time$^2$, s$^2$')
        ax1.set_ylabel(r'Angular velocity $\omega$, rad/s', color='k')
        ax2.set_ylabel(r'Angle $\phi$, degrees', color='r')
        
        time_col = r'Time (s)'
        data_col = r'Angular velocity x (rad/s)'
        
        t = []
        signal = []
        t = np.array(pd.read_csv(file, usecols=[time_col], skip_blank_lines=True)).ravel()
        signal = np.array(pd.read_csv(file, usecols=[data_col], skip_blank_lines=True)).ravel()
        
        integ = []
        ingtegerr = []
        for i in range(0,len(t)):
            integ.append(scipy.integrate.trapezoid(signal[:i], t[:i])/(2*np.pi)*360)
            if i == 0:
                ingtegerr.append(0.00001)
            else:
                ingtegerr.append(np.sqrt(ingtegerr[-1]**2+0.25*(0.1)**2*(signal[i] + signal[i-1])**2))
        
        [k, b], res1 = scipy.optimize.curve_fit(lambda t,k,b: k*t+b,  (t-t[0])**2,  integ)#, sigma=ingtegerr, absolute_sigma=True)
        db = np.sqrt(res1[0][0])
        dk = np.sqrt(res1[1][1])
        
        [aa, bb, cc], res2 = scipy.optimize.curve_fit(lambda t,aa,bb,cc: aa*(t**2)+bb*t+cc,  (t-t[0]),  integ)
        x = np.linspace(t[0]-t[0],t[-1]-t[0],1000)
        
        #print(2*np.pi/(k*np.pi/180), abs(2*np.pi/((k-dk)*np.pi/180)-2*np.pi/(k*np.pi/180)))
        y = 2*(aa*np.pi/180)*x+(bb*np.pi/180)
        y = (k*np.pi/180) + 0*x
        #y2 = aa*(x**2)+bb*x+cc
        y2 = k*(x**2)+b
        y3 = (k*np.pi/180)+0*x
        
        ax1.plot((t-t[0])**2, signal, 'k-')
        ax2.errorbar((t-t[0])**2, integ, yerr=ingtegerr, fmt='r-')
        ax2.plot(x**2,y2, 'b', linestyle='dashed')
        #ax1.plot(x, y3, 'k', linestyle='dashed')
        
        plt.savefig('C:\\Users\\Kārlis\\Videos\\Gyroscope\\EPS\\' + os.path.basename(folder)+'_quadratic.eps', format="eps")
        plt.show()
