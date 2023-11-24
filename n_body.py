#原版见 https://fanyi.baidu.com/?aldtype=16047#en/zh/Calculate%20the%20acceleration%20on%20each%20particle%20due%20to%20Newton's%20Law%20%0A%09pos%20%20is%20an%20N%20x%203%20matrix%20of%20positions%0A%09mass%20is%20an%20N%20x%201%20vector%20of%20masses%0A%09G%20is%20Newton's%20Gravitational%20constant%0A%09softening%20is%20the%20softening%20length%0A%09a%20is%20N%20x%203%20matrix%20of%20accelerations%0A%0AGet%20kinetic%20energy%20(KE)%20and%20potential%20energy%20(PE)%20of%20simulation%0A%09pos%20is%20N%20x%203%20matrix%20of%20positions%0A%09vel%20is%20N%20x%203%20matrix%20of%20velocities%0A%09mass%20is%20an%20N%20x%201%20vector%20of%20masses%0A%09G%20is%20Newton's%20Gravitational%20constant%0A%09KE%20is%20the%20kinetic%20energy%20of%20the%20system%0A%09PE%20is%20the%20potential%20energy%20of%20the%20system
import numpy as np
import matplotlib.pyplot as plt

def getAcc( pos, mass, G, softening ):
    x = pos[:,0:1]
    y = pos[:,1:2]
    z = pos[:,2:3]

    dx = x.T - x
    dy = y.T - y
    dz = z.T - z

    inv_r3 = (dx**2 + dy**2 + dz**2 + softening**2)
    inv_r3[inv_r3>0] = inv_r3[inv_r3>0]**(-1.5)

    ax = G * (dx * inv_r3) @ mass
    ay = G * (dy * inv_r3) @ mass
    az = G * (dz * inv_r3) @ mass

    a = np.hstack((ax,ay,az))

    return a
	
def getEnergy( pos, vel, mass, G ):
	KE = 0.5 * np.sum(np.sum( mass * vel**2 ))

	x = pos[:,0:1]
	y = pos[:,1:2]
	z = pos[:,2:3]

	dx = x.T - x
	dy = y.T - y
	dz = z.T - z

	inv_r = np.sqrt(dx**2 + dy**2 + dz**2)
	inv_r[inv_r>0] = 1.0/inv_r[inv_r>0]

	PE = G * np.sum(np.sum(np.triu(-(mass*mass.T)*inv_r,1)))
	
	return KE, PE;


def main():
    '''原数据
	N = 100
	t = 0
	tEnd = 10.0
	dt = 0.01
	softening = 0.1
	G = 1.0
    '''
    N = 50
    t = 0
    tEnd = 10.0
    dt = 0.01
    softening = 0.1
    G = 3.209

    plotRealTime = True

    np.random.seed(17)

    mass = 20.0*np.ones((N,1))/N
    pos  = np.random.randn(N,3)
    vel  = np.random.randn(N,3)

    vel -= np.mean(mass * vel,0) / np.mean(mass)

    acc = getAcc( pos, mass, G, softening )

    KE, PE  = getEnergy( pos, vel, mass, G )

    Nt = int(np.ceil(tEnd/dt))

    pos_save = np.zeros((N,3,Nt+1))
    pos_save[:,:,0] = pos
    KE_save = np.zeros(Nt+1)
    KE_save[0] = KE
    PE_save = np.zeros(Nt+1)
    PE_save[0] = PE
    t_all = np.arange(Nt+1)*dt

    fig = plt.figure(figsize=(4,5), dpi=80)
    grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.3)
    ax1 = plt.subplot(grid[0:2,0])
    ax2 = plt.subplot(grid[2,0])

    for i in range(Nt):
        vel += acc * dt/2.0
        pos += vel * dt
        acc = getAcc( pos, mass, G, softening )
        vel += acc * dt/2.0
        t += dt
        KE, PE  = getEnergy( pos, vel, mass, G )
        pos_save[:,:,i+1] = pos
        KE_save[i+1] = KE
        PE_save[i+1] = PE
        
        if plotRealTime or (i == Nt-1):
            plt.sca(ax1)
            plt.cla()
            xx = pos_save[:,0,max(i-50,0):i+1]
            yy = pos_save[:,1,max(i-50,0):i+1]
            plt.scatter(xx,yy,s=1,color=[.7,.7,1])
            plt.scatter(pos[:,0],pos[:,1],s=10,color='blue')
            ax1.set(xlim=(-2, 2), ylim=(-2, 2))
            ax1.set_aspect('equal', 'box')
            ax1.set_xticks([-2,-1,0,1,2])
            ax1.set_yticks([-2,-1,0,1,2])
            
            plt.sca(ax2)
            plt.cla()
            plt.scatter(t_all,KE_save,color='red',s=1,label='KE' if i == Nt-1 else "")
            plt.scatter(t_all,PE_save,color='blue',s=1,label='PE' if i == Nt-1 else "")
            plt.scatter(t_all,KE_save+PE_save,color='black',s=1,label='Etot' if i == Nt-1 else "")
            ax2.set(xlim=(0, tEnd), ylim=(-300, 300))
            ax2.set_aspect(0.007)
            
            plt.pause(0.001)
    
    plt.sca(ax2)
    plt.xlabel('time')
    plt.ylabel('energy')
    ax2.legend(loc='upper right')

    plt.savefig('D:/xixi/image/nbody.png',dpi=240)
    plt.show()
        
    return 0


if __name__== "__main__":
    main()
