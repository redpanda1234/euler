import time
import numpy as np

def central_force(k,m,r_vec,n):
	x = r_vec[0]
	y = r_vec[1]
	z = r_vec[2]

	F_x = (-k*m*x/(((x**2)+(y**2)+(z**2))**((n+1)/2)))
	F_y = (-k*m*y/(((x**2)+(y**2)+(z**2))**((n+1)/2)))
	F_z = (-k*m*z/(((x**2)+(y**2)+(z**2))**((n+1)/2)))

	return [F_x, F_y, F_z]
# def modded_central_force(k,m,X,Y,Z,n):
# 	a_x = (-k*X/(((X**2)+(Y**2)+(Z**2))**((n+1)/2)))
# 	a_y = (-k*Y/(((X**2)+(Y**2)+(Z**2))**((n+1)/2)))
# 	a_z = (-k*Z/(((X**2)+(Y**2)+(Z**2))**((n+1)/2)))

# 	F_x = m*a_x
# 	F_y = m*a_y
# 	F_z = m*a_z

# 	F_vec = [F_x, F_y, F_z]

# 	return F_vec

# def modded_potential_energy(n,m,r):
# 	U = -m*(1/((n-1)*(r**(n-1))))
# 	return U

# def modded_kinetic_energy(modded_v_vec, m):
# 	vx = modded_v_vec[0]
# 	vy = modded_v_vec[1]
# 	vz = modded_v_vec[2]
# 	KE = .5*m*((vx**2)+(vy**2)+(vz**2))

def potential_energy(k,m, n, r_vec):
	r = (r_vec[0])**2 + (r_vec[1])**2 + (r_vec[2])**2
	numerator = -k*m
	denominator = (n-1)*(r**(n-1))
	PE = numerator/denominator
	return PE

def euler_step(state_vector, derivative_vector, step_size):
	# x_change = step_size*derivative_vector[0]
	# y_change = step_size*derivative_vector[1]
	# z_change = step_size*derivative_vector[2]

	# new_x = state_vector[0]+x_change
	# new_y = state_vector[1]+y_change
	# new_z = state_vector[2]+z_change

	new_x = state_vector[0]+step_size*derivative_vector[0]
	new_y = state_vector[1]+step_size*derivative_vector[1]
	new_z = state_vector[2]+step_size*derivative_vector[2]

	new_state = (new_x, new_y, new_z)

	return new_state

def kinetic_energt(v_vec, m):
	v_square = ((v_vec[0])**2 + (v_vec[1])**2)
	KE = .5*m*v_square
	return KE

def one_step(position, velocity, k, m, n, step_size):
	force = central_force(k,m,position,n)
	new_position = euler_step(position, velocity, step_size)
	new_velocity = euler_step(velocity, force, step_size)
	# new_potential_energy = potential_energy(k,m,n,new_position)
	# new_kinetic_energy = kinetic_energt(new_velocity, m)
	# new_total_energy = new_kinetic_energy+new_potential_energy
	# print("new position is", new_position)
	# print("new velocity is", new_velocity)
	# print("new potential energy is", new_potential_energy)
	# print("new kinetic energy is", new_kinetic_energy)
	# print("new total energy is", new_total_energy, "\n")
	# return [new_position, new_velocity, new_potential_energy, new_kinetic_energy]
	return (new_position, new_velocity)

def simulate(position, velocity, k, m, n, step_size, num_steps):
	start_time = time.time()
	steps = 0
	position_list = []
	while steps < num_steps:
		new_stuff = one_step(position, velocity, k, m, n, step_size)
		position = new_stuff[0]
		velocity = new_stuff[1]
		# current_time = step_size*steps
		position_list.append((np.asarray(position)))
		steps += 1
		# print(new_stuff)
	stop_time = time.time()
	print("runtime is", stop_time-start_time)
	position_array = np.asarray(position_list)
	return position_array
