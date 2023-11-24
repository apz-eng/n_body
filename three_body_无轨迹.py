''' 二维 '''
import matplotlib.pyplot as plt
from matplotlib import animation
import math

class Planet:
    Number = 0

    def __init__(self, color, mass, position, v_init):
        Planet.Number += 1
        self.color = color
        self.mass = mass
        self.x, self.y = position
        self.vx, self.vy = v_init

    def v_change(self, f, t=1e-3):
        fx, fy = f
        ax, ay = fx / self.mass, fy / self.mass
        self.vx += ax * t
        self.vy += ay * t

    def p_change(self, t=1e-3):
        self.x += self.vx * t
        self.y += self.vy * t

    def gravity(self, other_planet):
        distance = math.sqrt((self.x - other_planet.x) ** 2 + (self.y - other_planet.y) ** 2)
        f = self.mass * other_planet.mass / (distance ** 2)
        fx = (other_planet.x - self.x) / distance * f
        fy = (other_planet.y - self.y) / distance * f
        return fx, fy
    

fig = plt.figure()

'''
# 红 蓝 绿
# 原版
point_1 = Planet('r', 100, (-3, -3), (0, 0.3))
point_2 = Planet('r', 10, (5, -5), (0, -3))
point_3 = Planet('r', 0.1, (0, 10), (3, 0))


# 稳恒态

point_1 = Planet('r', 100, (0, 0), (0, 0)) # 两个小质量的质点绕一个大质量质点旋转（公转）
point_2 = Planet('r', 0.000000000001, (10, -3.12), (-2, -2.891))
point_3 = Planet('r', 0.000000000001, (1, 13), (-2, -0.02))

# 半稳恒态
point_1 = Planet('r', 100, (-3, -3), (0, 0.2)) # 两个小质量的质点绕一个大质量质点旋转（公转）
point_2 = Planet('r', 5, (5, -5), (-2, -3))
point_3 = Planet('r', 5, (0, 10), (3, 0))
'''
# 实验
point_1 = Planet('r', 100, (0, 0), (0, 0))
point_2 = Planet('r', 0.000000000001, (10, -3.12), (-2, -2.891))
point_3 = Planet('r', 0.000000000001, (-1, 13), (-2, -0.02))

def animate(i):
    fig.clear()
    for _ in range(500):
        f_21 = point_1.gravity(point_2)
        f_31 = point_1.gravity(point_3)
        f_12 = point_2.gravity(point_1)
        f_32 = point_2.gravity(point_3)
        f_13 = point_3.gravity(point_1)
        f_23 = point_3.gravity(point_2)

        point_1.p_change()
        point_1.v_change(f_21)
        point_1.v_change(f_31)

        point_2.p_change()
        point_2.v_change(f_12)
        point_2.v_change(f_32)

        point_3.p_change()
        point_3.v_change(f_13)
        point_3.v_change(f_23)

    plt.scatter(point_1.x, point_1.y, c='r')  # 红色星球
    plt.scatter(point_2.x, point_2.y, c='b')  # 蓝色星球
    plt.scatter(point_3.x, point_3.y, c='g')  # 绿色星球
    
    '''
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    
    plt.xlim(-175, 175)
    plt.ylim(-175, 175)
    
    plt.xlim(-250, 250)
    plt.ylim(-250, 250)
    '''
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.draw()


ani = animation.FuncAnimation(fig=fig, func=animate, frames=100, interval=1, blit=False)
plt.show()
