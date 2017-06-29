import time
import numpy as np

def central_force(m, G, other_bodies, n):
    """
    takes in the mass of the object in question, newton's constant, a tuple of tuples
    containing the mass r, and v values for said mass, the r value for the mass in
    question, and n, the exponent on r in Newton's law of Gravitation
    """
    # print(m)
    x_0 = m[1][0]
    y_0 = m[1][1]
    z_0 = m[1][2]

    Force_list = [0,0,0]

    for mass_tuple in other_bodies:
        other_mass = mass_tuple[0]

        x_M = mass_tuple[1][0]
        y_M = mass_tuple[1][1]
        z_M = mass_tuple[1][2]

        x = x_0 - x_M
        y = y_0 - y_M
        z = z_0 - z_M

        k = G*other_mass

        Force_list[0] = Force_list[0]+(-k*m[0]*x/(((x**2)+(y**2)+(z**2))**((n+1)/2)))
        Force_list[1] = Force_list[1]+(-k*m[0]*y/(((x**2)+(y**2)+(z**2))**((n+1)/2)))
        Force_list[2] = Force_list[2]+(-k*m[0]*z/(((x**2)+(y**2)+(z**2))**((n+1)/2)))

    return Force_list

def euler_step(state_vector, derivative_vector, step_size):
    new_x = state_vector[0]+step_size*derivative_vector[0]
    new_y = state_vector[1]+step_size*derivative_vector[1]
    new_z = state_vector[2]+step_size*derivative_vector[2]

    new_state = (new_x, new_y, new_z)

    return new_state

def one_step(G, m_list, n, step_size):
    new_m_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        other_bodies = m_list[:i]+m_list[i+1:]
        force = central_force(m,G,other_bodies,n)
        new_position = euler_step(m[1], m[2], step_size)
        new_velocity = euler_step(m[2], force, step_size)
        new_m_list.append([m[0],new_position,new_velocity])
    return new_m_list

def simulate(G, m_list, n, step_size, num_steps):
    num_m = len(m_list)
    traj_list = [[] for k in range(num_m)]
    start_time = time.time()
    steps = 0
    new_m_list = m_list
    while steps < num_steps:
        new_m_list = one_step(G, new_m_list, n, step_size)
        # pos_list = []
        for k in range(len(new_m_list)):
            # pos_list.append(m[1])
            traj_list[k].append(np.asarray(new_m_list[k][1]))
            steps += 1
            # print(new_m_list)
            # print(pos_list)
    stop_time = time.time()
    print("runtime is", stop_time-start_time)
    trajectories_array = np.asarray(traj_list)
    return trajectories_array

# G = 6.67*(10**(-11))
# m_list =[[5000000000,(0,0,0),(0,.001,0)], [3,(0,1,0), (0,1,0)]]
# # m_list =[[5000000000,(0,-1,0),(0,.5,0)]]
# n=2
# step_size = 0.001
# num_steps = 100000
# step_size = .01
# a=simulate(G, m_list, 2, step_size, num_steps)
