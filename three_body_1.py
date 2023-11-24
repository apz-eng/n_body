''' 二维 '''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from itertools import product

def main():
    m,x,y,u,v = [np.random.rand(3) for _ in range(5)]
    ''' 设置m、x、y '''
    import random as rd
    # m
    
    # x
    
    # y
    
    ''' '''
    N = 1000
    dt = 36000
    ts =  np.arange(0,N*dt,dt) / 3600 / 24
    xs,ys = [],[]
    for _ in ts:
        x_ij = (x-x.reshape(3,1))
        y_ij = (y-y.reshape(3,1))
        r_ij = np.sqrt(x_ij ** 2 + y_ij ** 2)
        for i,j in product(range(3),range(3)):
            if i != j :
                u[i] += (m[j] * x_ij[i,j] * dt/r_ij[i,j] ** 3)
                v[i] += (m[j] * y_ij[i,j] * dt/r_ij[i,j] ** 3)
        x += u * dt
        y += v * dt
        xs.append(x.tolist())
        ys.append(y.tolist())

    xs = np.array(xs)
    ys = np.array(ys)
    fig = plt.figure(figsize = (12,12))
    ax = fig.add_subplot(xlim = (-2e11,2e11),ylim = (-2e11,2e11))
    ax.grid()
    traces = [ax.plot([],[],'-', lw = 0.5)[0] for _ in range(3)]
    pts = [ax.plot([x[i]],[y[i]] ,marker = 'o')[0] for i in range(3)]
    k_text = ax.text(0.05,0.85,'',transform = ax.transAxes)
    textTemplate = 't = %.3f days\n'

    def animate(n):
        for i in range(3):
            traces[i].set_data(xs[:n,i],ys[:n,i])
            pts[i].set_data([xs[n,i]],[ys[n,i]])
        k_text.set_text(textTemplate % ts[n])
        return traces[0], traces[1], traces[2], pts[0], pts[1], pts[2], k_text

    ani = animation.FuncAnimation(fig, animate, range(N), interval=10, blit=True)
    plt.show()
    ani.save("3.gif")

main()
