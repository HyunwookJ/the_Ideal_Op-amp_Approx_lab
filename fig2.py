import matplotlib.pyplot as plt
import numpy as np

# Curves of Open-loop cir
ol = np.loadtxt('data/openloop.txt')
freq_ol = ol[:, 0]
gain_ol = ol[:, 1]

plt.figure(figsize = (10, 5))
plt.plot(freq_ol, gain_ol, 'k-', linewidth = 2, label = 'Open-loop')

# find f_break
res = np.loadtxt('data/results.txt', usecols = (0, 1, 3), dtype = str, comments = '#')

acl_r = res[:, 0].astype(float)   
fb_r  = res[:, 1].astype(float)   
group_r = res[:,2].astype(str)                 

f_break = {int(a): f for a, f, g in zip(acl_r, fb_r, group_r) if g == 'real'}

# Curves of Closed-loop cir
acl_list = [2, 3, 4, 5, 7, 10, 15, 20, 30, 50]

for acl in acl_list:
    data = np.loadtxt(f'data/cl_acl{acl}.txt')
    freq = data[:, 0]
    gain = data[:, 1]
    plt.plot(freq, gain, label = f'A_cl = {acl}')

    fb = f_break[acl]
    gain_marker = 20 * np.log10(acl * 0.95)
    plt.scatter(fb, gain_marker, color='red', zorder=5, s=30)

plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.legend()
plt.grid(True, which='both', alpha=0.3)

plt.savefig('Fig_2/fig2_5.png', dpi=300, bbox_inches='tight')