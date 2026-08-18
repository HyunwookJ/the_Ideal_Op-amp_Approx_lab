import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('data/results.txt', usecols = (0, 1, 3), dtype = str, comments='#')

acl = data[:, 0].astype(float)
f_break = data[:, 1].astype(float)
group = data[:, 2].astype(str)

is_real = (group == 'real')
is_vcvs = (group == 'vcvs')

product = acl * f_break

plt.figure(figsize = (10, 5))
plt.scatter(acl[is_real], product[is_real], label = 'Real circuit')
plt.scatter(acl[is_vcvs], product[is_vcvs], label = 'Ideal (VCVS)')

plt.scatter(acl[is_real], product[is_real], color = 'C0')
plt.plot(acl[is_real], product[is_real], color = 'C0', alpha = 0.5)
plt.scatter(acl[is_vcvs], product[is_vcvs], color = 'C1')
plt.plot(acl[is_vcvs], product[is_vcvs], color = 'C1', alpha = 0.5)

gbw = 4.812241e6
plt.axhline(0.329 * gbw, linestyle = '--', color = 'gray', label = '0.329 x GBW')

plt.xscale('log')
plt.xlabel('Closed-loop gain  A_cl')
plt.ylabel('A_cl x f_break  (Hz)')
plt.legend()

plt.savefig('Fig_1/fig1_2.png', dpi=300, bbox_inches='tight')