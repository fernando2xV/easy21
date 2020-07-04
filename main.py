import numpy as np
from montecarlo import *
from sarsa import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import utils


max_episodes = 100000
episodes = np.arange(1, max_episodes + 1, 1)


#-------------------------------MONTE CARLO settings-------------------------------------------------------------
q_mc = np.zeros((2,11,22))
counter = np.zeros((2, 11, 22))

#--------------------------------SARSA settings------------------------------------------------------------------
gamma_var = 1
q_sarsa = np.zeros((2, 11,22))
counter_sarsa = np.zeros((2,11,22))
lambda_var = -0.1 
#--------------------------------MSE vs lambda settings------------------------------------------------------------------
mse = np.zeros(11)
lambdas = np.arange(0.0, 1.1, 0.1)



#-------------------------------MONTE CARLO plotting-------------------------------------------------------------

'''
for i in range(max_episodes + 1):
	print(i)
	q_mc, counter = montecarlo(q_mc, counter)



q_function_mc = np.save("mc.npy",q_mc)
'''
q_function_mc = np.load("mc.npy")

#Value function = optimal action-value function
#V*(s) = max-a Q*(s, a)
best_values = np.amax(q_function_mc, axis = 0)

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
plt.title("Monte Carlo: %d iterations"% max_episodes)
ax.set_ylabel("Dealer showing")
ax.set_xlabel("Player sum")
x = range(10)
y = range(21)
X, Y = np.meshgrid(y, x)
ax.plot_wireframe(X + 1, Y + 1, best_values[1:, 1:])
plt.show()

#-------------------------------SARSA plotting-------------------------------------------------------------

for j in range(max_episodes + 1):
	print(j)
	q_sarsa, counter_sarsa = sarsa(q_sarsa, counter_sarsa, 0)

#get maxs at each 11x22 point (v(s))
v_sarsa = np.amax(q_sarsa, axis = 0)

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
plt.title("Sarsa: %d iterations"% j)
ax.set_ylabel("Dealer showing")
ax.set_xlabel("Player sum")
x = range(10)
y = range(21)
X, Y = np.meshgrid(y, x)
ax.plot_wireframe(X + 1, Y + 1, v_sarsa[1:, 1:])
plt.show()

#----------------RESET VALUES
q_mc = np.zeros((2,11,22))
counter = np.zeros((2, 11, 22))
q_sarsa = np.zeros((2, 11,22))
counter_sarsa = np.zeros((2,11,22))
#-----------------------------


#-------------------------------MSE between MC and Sarsa vs. lambda values [0, 1] steps of 0.1-------------------------------------------------------------
for k in range(12):
	print(k)
	lambda_var = lambda_var + 0.1
	for j in range(1001):
		q_mc, counter = montecarlo(q_mc, counter)
		q_sarsa, counter_sarsa = sarsa(q_sarsa, counter_sarsa, lambda_var)
	mse[k - 1] = np.sum(np.square(q_mc - q_sarsa))
print(lambdas)
print(mse)

plt.plot(lambdas, mse)
plt.xlabel("Lambda")
plt.ylabel("MSE")
plt.title("MSE vs Lambda values")
plt.show()


