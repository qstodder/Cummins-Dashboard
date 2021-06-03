import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime as dt
import matplotlib.animation as animation

# # read in all logs and combine into one log
# folder = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot'
# logs = [l[2] for l in os.walk(folder)]
# all_logs = [folder + '/' + l for l in logs[0]]
# combined_logs = pd.concat([pd.read_csv(l) for l in all_logs])
# combined_logs.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

data_file = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot/combined_logs.csv'
data = pd.read_csv(data_file)
data.sort_values('time')

# # Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
plt.style.use('dark_background')
fig, ((axC, axV), (axP, ax4)) = plt.subplots(2, 2, figsize=(14,8))
fig.suptitle("UCSD Cummins Site Monitoring", fontsize=14)

# choose background
# im = plt.imread("/Users/quiana/Documents/UCSD/CER/Data_Processing/Processing/Cummins/realtime_plot_background.png")
# implot = plt.imshow(im)
fig.patch.set_facecolor('#030764')
fig.patch.set_alpha(0.7)

xs = []
ysC = []
ysV = []
ysP = []

interval = 30
# ysC.append(data['modbus_Current'][0:interval])
# ysV.append(data['modbus_Voltage'][0:interval])
# ysP.append(data['modbus_Power'][0:interval])

# This function is called periodically from FuncAnimation
def animate(i, xs, ysC, ysV, ysP):

    # # Read temperature (Celsius) from TMP102
    # temp_c = round(tmp102.read_temp(), 2)

    # Get datetime
    dt_now = dt.datetime.now().strftime('%H:%M:%S')
    xs.append(dt.datetime.now().strftime('%S'))
    # ys.append(temp_c)
    text(x, y, dt_now, fontsize=12)

    # xs.append(data['time'][i])
    ysC.append(data['modbus_Current'][i])
    ysV.append(data['modbus_Voltage'][i])
    ysP.append(data['modbus_Power'][i])


    # get min value
    low = max(0,len(xs)-interval)

    # Limit x and y lists to 20 items
    xs = xs[low:]
    ysC = ysC[low:]
    ysV = ysV[low:]
    ysP = ysP[low:]

    # Draw x and y lists
    axC.clear()
    axV.clear()
    axP.clear()

    axC.plot(xs, ysC)
    axV.plot(xs, ysV)
    axP.plot(xs, ysP)

    axC.set_ylim(-80, 80)
    axV.set_ylim(100, 550)
    axP.set_ylim(-60, 60)

    # Format plot
    axC.set_xticks([])
    axV.set_xticks([])
    ax4.set_xticks([])
    axP.tick_params(labelrotation=60)
    # ax4.tick_params(labelrotation=90)
    # axP.set_xticklabels(rotation=45, ha='right')
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)

    axC.set_title('Modbus Current')
    axV.set_title('Modbus Voltage')  
    axP.set_title('Modbus Power')
    ax4.set_title('Max and Min Module and Cell Power')

    axC.set_ylabel('Current [A]')
    axV.set_ylabel('Voltage [V]')
    axP.set_ylabel('Power [W]')
    ax4.set_ylabel('Power [W]')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ysC, ysV, ysP), interval=500)
plt.show()

# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
# ax1.set_xticks([])
# ax2.set_xticks([])
# ax3.tick_params(labelrotation=45)
# ax4.tick_params(labelrotation=45)

# ax1.set_title('Modbus Power')
# ax2.set_title('Modbus Current')
# ax3.set_title('Modbus Voltage')

# for i in range(data.shape[0]):
#     t = data['time'][i]
#     ax1.plot(t,data['modbus_Power'][i])
#     ax2.plot(t,data['modbus_Current'][i])
#     ax3.plot(t,data['modbus_Voltage'][i])
#     plt.pause(0.05)

# plt.show()



