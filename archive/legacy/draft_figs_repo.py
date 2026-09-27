import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from numpy import shape
import os



plt.rcParams.update({"text.usetex" : True, 'font.size' : 9, 
                     'mathtext.fontset':'cm', "axes.linewidth" : 0.75, 
                     "xtick.major.width" : 0.75, "ytick.major.width" : 0.75, 
                     "xtick.major.size" : 1, "ytick.major.size" : 1, 
                     "savefig.dpi":100, "font.family" : "serif",
                     'text.latex.preamble' : 
                    
                         r'\usepackage{amsmath}\usepackage{amssymb} '})

path = os.getcwd()

def make_fig_5():

    data3 = np.loadtxt(path + '/submission/double_ocupany_bos_fermi_couple5.txt')
    data1 = np.loadtxt(path + '/submission/double_ocupany_bos_fermi_couple0.1.txt')
    data4 = np.loadtxt(path + '/submission/total_boson_num0.1.txt' )
    data6 = np.loadtxt(path + '/submission/total_boson_num5.txt' )

    fig = plt.figure(figsize=(3.29, 0.75*6))

    gs = fig.add_gridspec(3, 1)

    ax1 = fig.add_subplot(gs[0, 0])
    ax3 = fig.add_subplot(gs[1, 0], sharex=ax1)
    ax4 = fig.add_subplot(gs[2, 0], sharex=ax1)

    ax1.plot(data1[:,0], data1[:,1], marker='o', linestyle='-', lw=1.25, markersize=0, color='black', label=r'$j=1$')
    ax3.plot(data3[:,0], data3[:,1], marker='o', linestyle='-', lw=1.25, markersize=0, color='black', label=r'$j=1$')

    ax1.plot(data1[:,0], data1[:,2], marker='^', linestyle='--', lw=1.25, markersize=0, color='darkgoldenrod', label=r'$j=2$')
    ax3.plot(data3[:,0], data3[:,2], marker='^', linestyle='--', lw=1.25, markersize=0, color='darkgoldenrod', label=r'$j=2$')

    ax1.plot(data1[:,0], data1[:,1] + data1[:,2], marker='^', linestyle=':', lw=0.75, markersize=0, color='blue', label=r'total')
    ax3.plot(data3[:,0], data3[:,1] + data3[:,2], marker='^', linestyle=':', lw=0.75, markersize=0, color='blue', label=r'total')

    ax4.plot(data4[:,0], data4[:,1] + data4[:,2], marker='o', linestyle='--', lw=1.5, markersize=0, color='red', label=r'$g/k=0.1$')
    ax4.plot(data6[:,0], data6[:,1] + data6[:,2], marker='^', linestyle='-', lw=0.75, markersize=0, color='deepskyblue', label=r'$g/k=5.0$')

    ax4.set_xlabel(r'$t\: k$')

    ax1.set_xlim(0, 20)
    ax3.set_xlim(0, 20)
    ax4.set_xlim(0, 20)

    ax1.set_ylabel(r'$\langle \hat{n}_{j, \uparrow}\hat{n}_{j, \downarrow} \rangle$')
    ax3.set_ylabel(r'$\langle \hat{n}_{j, \uparrow}\hat{n}_{j, \downarrow} \rangle$')
    ax4.set_ylabel(r'$\langle \hat{n}_{ph} \rangle$')

    ax1.set_ylim(0, 1.4)
    ax3.set_ylim(0, 1.4)
    ax4.set_ylim(-0.2, 6.75)

    ax1.set_yticks([0, 0.5, 1.0], [r'0', r'0.5', r'1.0'])
    ax3.set_yticks([0, 0.5, 1.0], [r'0', r'0.5', r'1.0'])

    ax3.legend(labelspacing=0, frameon=False, borderpad=-0.4)
    ax4.legend(labelspacing=0, frameon=False, borderpad=-0.4)

    ax1.text(0.5, 1.2, r'a.')
    ax3.text(0.5, 1.2, r'b.')
    ax4.text(0.5, 5.8, r'c.')

    ax1.text(10, 1.2, r'$g/k=0.1$', ha='center')
    ax3.text(10, 1.2, r'$g/k=5.0$', ha='center')

    gs.update(hspace=0)

    ax1.tick_params(labelbottom=False)
    ax3.tick_params(labelbottom=False)

    plt.tight_layout()
    plt.show()

    return 

def make_fig_2():

    data1 = np.loadtxt(path + '/submission/fidelity_5.txt')
    data2 = np.loadtxt(path + '/submission/fidelity_0.1.txt')
    data3 = np.loadtxt(path + '/submission/noisy_fidelity_Juan.txt')

    fig = plt.figure(figsize=(6.5, 1.5))
    gs = fig.add_gridspec(1, 3, wspace=0.4)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    ax3.plot(data1[:, 0], data1[:, 1], marker='o', lw=0.5, markersize=3, color='red', label=r'DAQC(Ideal)')
    ax3.plot(data1[:, 0], data1[:, 2], marker='*', lw=0.5, markersize=3, color='black', label=r'DAQC(Noisy)')
    ax3.plot(data1[:, 0], data1[:, 3], marker='^', lw=0.5, markersize=3, color='orange', label=r'Digital(Ideal)')
    ax3.plot(data1[:, 0], data1[:, 4], marker='H', lw=0.5, markersize=3, color='cornflowerblue', label=r'Digital(Noisy)')
    ax3.set_xlim(min(data1[:,0]), max(data1[:,0]))
    ax3.set_xlabel(r'$t\: k$')
    ax3.set_ylabel(r'Fidelity', labelpad=0)
    ax3.set_ylim(-0.05, 1.15)
    ax3.text(2.5, 1.05, r'$g=5k$')
    ax3.text(0.25, 1.05, r'c.')
    ax3.set_yticklabels([])
    ax3.set_xticks([0, 1, 2, 3, 4, 5], [r'0', r'1', r'2', r'3', r'4', r'5'])

    ax1.plot(data2[:, 0], data2[:, 1], marker='o', lw=0.5, markersize=3, color='red', label=r'DAQC(Ideal)')
    ax1.plot(data2[:, 0], data2[:, 2], marker='*', lw=0.5, markersize=3, color='black', label=r'DAQC(Noisy)')
    ax1.plot(data2[:, 0], data2[:, 3], marker='^', lw=0.5, markersize=3, color='orange', label=r'Digital(Ideal)')
    ax1.plot(data2[:, 0], data2[:, 4], marker='H', lw=0.5, markersize=3, color='cornflowerblue', label=r'Digital(Noisy)')
    ax1.set_xlim(min(data1[:,0]), max(data1[:,0]))
    ax1.set_ylabel(r'Fidelity', labelpad=0)
    ax1.legend(labelspacing=0, frameon=True, loc=0, ncol=1, borderaxespad=0, handlelength=1.5)
    ax1.text(2.5, 1.05, r'$g=0.1k$')
    ax1.text(0.25, 1.05, r'a.')
    ax1.set_ylim(-0.05, 1.15)
    ax1.set_xlabel(r'$t\: k$')
    ax1.set_xticks([0, 1, 2, 3, 4], [r'0', r'1', r'2', r'3', r'4'])

    

    ax2.plot(data3[:, 0], data3[:, 1], marker='o', lw=0.5, markersize=3, color='red', label=r'DAQC(Ideal)')
    ax2.plot(data3[:, 0], data3[:, 2], marker='*', lw=0.5, markersize=3, color='black', label=r'DAQC(Noisy)')
    ax2.plot(data3[:, 0], data3[:, 3], marker='^', lw=0.5, markersize=3, color='orange', label=r'Digital(Ideal)')
    ax2.plot(data3[:, 0], data3[:, 4], marker='H', lw=0.5, markersize=3, color='cornflowerblue', label=r'Digital(Noisy)')
    ax2.set_xlim(min(data1[:,0]), max(data1[:,0]))
    ax2.set_ylabel(r'Fidelity', labelpad=0)
    ax2.set_yticklabels([])
    ax2.set_xticks([0, 1, 2, 3, 4], [r'0', r'1', r'2', r'3', r'4'])
    ax2.text(2.5, 1.05, r'$g=k$')
    ax2.text(0.25, 1.05, r'b.')
    ax2.set_ylim(-0.05, 1.15)
    ax2.set_xlabel(r'$t\: k$')

    plt.tight_layout()
    plt.show()


def main():
    print('Reproducing Fig.2')
    make_fig_2()
    
    print('Reproducing Fig.5')
    make_fig_5()
    
    input('Press any key to exit.')
    
if __name__ == '__main__':
    main()
