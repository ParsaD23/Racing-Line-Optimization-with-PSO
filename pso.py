#------------------------------------------------------------------------------+
#
#	Parsa Dahesh (dinoco.parsa23@gmail.com or parsa.dahesh@studio.unibo.it)
#	Racing Line Optimization with PSO
#	MIT License, Copyright (c) 2021 Parsa Dahesh
#
#------------------------------------------------------------------------------+

import random
import time

class Particle:
	def __init__(self, n_dimensions, boundaries):
		self.position = []
		self.best_position = []
		self.velocity = []

		for i in range(n_dimensions):
			self.position.append(random.uniform(0, boundaries[i]))
			self.velocity.append(random.uniform(-boundaries[i], boundaries[i]))

		self.best_position = self.position

	def update_position(self, newVal):
		self.position = newVal

	def update_best_position(self, newVal):
		self.best_position = newVal
	
	def update_velocity(self, newVal):
		self.velocity = newVal

def optimize(cost_func, n_dimensions, boundaries, n_particles, n_iterations, w, cp, cg, verbose=False):
	''' Particle Swarm Optimization

	This function will minimize the cost function

	Parameters
	----------
	cost_func : function
		A function that will evaluate a given input, return a float value
	n_dimension : int
		Dimensionality of the problem
	boundaries : list[float]
		Problem's search space boundaries
	n_particles : int
		Number of particles
	n_iteration : int
		Number of iterations
	w : float
		Inertia parameter
	cp : float
		Constant parameter influencing the cognitive component (how much the current particle's best position will influnce its next iteration)
	cg : float
		Constant parameter influencing the social component (how much the global solution will influnce its next iteration of a particle)
	verbose : bool
		Flag to turn on output prints (default is False)

	Returns
	-------
	global_solution :
		Solution of the optimization
	gs_eval :
		Evaluation of global_solution with cost_func
	gs_history :
		List of the global solution at each iteration of the algorithm
	gs_eval_history :
		List of the global solution's evaluation at each iteration of the algorithm
	'''
	
	particles = []
	global_solution = []
	gs_eval = []
	gs_history = []
	gs_eval_history = []

	if verbose:
		print()
		print("------------------ PARAMETERS -----------------")
		print("Number of dimensions:", n_dimensions)
		print("Number of iterations:", n_iterations)
		print("Number of particles:", n_particles)
		print("w: {}\tcp: {}\tcg: {}".format(w,cp,cg))
		print()
		print("----------------- OPTIMIZATION ----------------")
		print("Population initialization...")
	
	for i in range(n_particles):
		particles.append(Particle(n_dimensions, boundaries))

	global_solution = particles[0].position
	gs_eval = cost_func(global_solution)
	for p in particles:		
		p_eval = cost_func(p.best_position)
		if p_eval < gs_eval:
			global_solution = p.best_position
			gs_eval = cost_func(global_solution)

	gs_history.append(global_solution)
	gs_eval_history.append(gs_eval)
	
	if verbose:
		print("Start of optimization...")
		printProgressBar(0, n_iterations, prefix = 'Progress:', suffix = 'Complete', length = 50)

	start_time = time.time_ns()

	for k in range(n_iterations):
		for p in particles:
			rp = random.uniform(0,1)
			rg = random.uniform(0,1)

			velocity = []
			new_position =[]
			for i in range(n_dimensions):
				velocity.append(w * p.velocity[i] + \
        			cp * rp * ( p.best_position[i] - p.position[i] ) + \
					cg * rg * ( global_solution[i] - p.position[i] ))

				if velocity[i] < -boundaries[i]:
					velocity[i] = -boundaries[i]
				elif velocity[i] > boundaries[i]:
					velocity[i] = boundaries[i]

				new_position.append(p.position[i] + velocity[i])
				if new_position[i] < 0.0:
					new_position[i] = 0.0
				elif new_position[i] > boundaries[i]:
					new_position[i] = boundaries[i]

			p.update_velocity(velocity)
			p.update_position(new_position)

			p_eval = cost_func(p.position)
			if p_eval < cost_func(p.best_position):
				p.update_best_position(p.position)
				if p_eval < gs_eval:
					global_solution = p.position
					gs_eval = p_eval
					
		gs_eval_history.append(gs_eval)
		gs_history.append(global_solution)

		if verbose:
			printProgressBar(k+1, n_iterations, prefix = 'Progress:', suffix = 'Complete', length = 50)
	
	finish_time = time.time_ns()
	elapsed_time = (finish_time-start_time)/10e8
	
	if verbose:
		time.sleep(0.2)
		print("End of optimization...")
		print()
		print("------------------- RESULTS -------------------")
		print("Optimization elapsed time: {:.2f} s".format(elapsed_time))
		print("Solution evaluation: {:.5f}".format(gs_eval))

	return global_solution, gs_eval, gs_history, gs_eval_history

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
