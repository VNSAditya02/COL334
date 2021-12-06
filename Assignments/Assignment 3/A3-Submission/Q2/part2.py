import matplotlib.pyplot as plt
import pandas as pd

def parta():
	file1 = "part2_2.0_2.0.csv"
	df1 = pd.read_csv(file1, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file2 = "part2_4.0_2.0.csv"
	df2 = pd.read_csv(file2, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file3 = "part2_10._2.0.csv"
	df3 = pd.read_csv(file3, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file4 = "part2_20._2.0.csv"
	df4 = pd.read_csv(file4, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])
	
	file5 = "part2_50._2.0.csv"
	df5 = pd.read_csv(file5, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	df1.plot(x = 'Time', y = 'New Cwnd', label = "Channel Data Rate: 2")
	plt.legend()
	plt.title("Channel Data Rate:2 - Application Data Rate:2 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("cdr_2_plot.png", index = False)
	
	df2.plot(x = 'Time', y = 'New Cwnd', label = "Channel Data Rate: 4")
	plt.legend()
	plt.title("Channel Data Rate:4 - Application Data Rate:2 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("cdr_4_plot.png", index = False)
	
	df3.plot(x = 'Time', y = 'New Cwnd', label = "Channel Data Rate: 10")
	plt.legend()
	plt.title("Channel Data Rate:10 - Application Data Rate:2 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("cdr_10_plot.png", index = False)
	
	df4.plot(x = 'Time', y = 'New Cwnd', label = "Channel Data Rate: 20")
	plt.legend()
	plt.title("Channel Data Rate:20 - Application Data Rate:2 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("cdr_20_plot.png", index = False)
	
	df5.plot(x = 'Time', y = 'New Cwnd', label = "Channel Data Rate: 50")
	plt.legend()
	plt.title("Channel Data Rate:50 - Application Data Rate:2 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("cdr_50_plot.png", index = False)

def partb():
	file1 = "part2_6.0_0.5.csv"
	df1 = pd.read_csv(file1, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file2 = "part2_6.0_1.0.csv"
	df2 = pd.read_csv(file2, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file3 = "part2_6.0_2.0.csv"
	df3 = pd.read_csv(file3, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	file4 = "part2_6.0_4.0.csv"
	df4 = pd.read_csv(file4, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])
	
	file5 = "part2_6.0_10..csv"
	df5 = pd.read_csv(file5, header = None, names = ["Time", "Old Cwnd", "New Cwnd"])

	df1.plot(x = 'Time', y = 'New Cwnd', label = "Application Data Rate: 0.5")
	plt.legend()
	plt.title("Channel Data Rate:6 - Application Data Rate:0.5 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("adr_0.5_plot.png", index = False)
	
	df2.plot(x = 'Time', y = 'New Cwnd', label = "Application Data Rate: 1")
	plt.legend()
	plt.title("Channel Data Rate:6 - Application Data Rate:1 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("adr_1_plot.png", index = False)
	
	df3.plot(x = 'Time', y = 'New Cwnd', label = "Application Data Rate: 2")
	plt.legend()
	plt.title("Channel Data Rate:6 - Application Data Rate:2 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("adr_2_plot.png", index = False)
	
	df4.plot(x = 'Time', y = 'New Cwnd', label = "Application Data Rate: 4")
	plt.legend()
	plt.title("Channel Data Rate:6 - Application Data Rate:4 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("adr_4_plot.png", index = False)
	
	df5.plot(x = 'Time', y = 'New Cwnd', label = "Application Data Rate: 10")
	plt.legend()
	plt.title("Channel Data Rate:6 - Application Data Rate:10 ")
	plt.xlabel("Time(sec)")
	plt.ylabel("Cwnd size")
	plt.savefig("adr_10_plot.png", index = False)


parta()
partb()
