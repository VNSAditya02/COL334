import matplotlib.pyplot as plt
import pandas as pd

def plot(config):
	file1 = "part3_sender1a_" + str(config) + ".csv"
	df1 = pd.read_csv(file1, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file2 = "part3_sender1b_" + str(config) + ".csv"
	df2 = pd.read_csv(file2, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file3 = "part3_sender2_" + str(config) + ".csv"
	df3 = pd.read_csv(file3, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	toSave1 = "sender1a_" + str(config) + ".png"
	toSave2 = "sender1b_" + str(config) + ".png"
	toSave3 = "sender2_" + str(config) + ".png"
	df1.plot(x = 'Time', y = 'New Cwnd', label = "cwnd size")
	plt.legend()
	plt.title("Connection 1 - Configuration - " + str(config))
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig(toSave1, index = False)
	
	df2.plot(x = 'Time', y = 'New Cwnd', label = "cwnd size")
	plt.legend()
	plt.title("Connection 2 - Configuration - " + str(config))
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig(toSave2, index = False)
	
	df3.plot(x = 'Time', y = 'New Cwnd', label = "cwnd size")
	plt.legend()
	plt.title("Connection 3 - Configuration - " + str(config))
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig(toSave3, index = False)
	
plot(1)
plot(2)
plot(3)
