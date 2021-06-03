import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime as dt
import matplotlib.animation as animation
import matplotlib.ticker as mticker
from matplotlib.patches import Arrow
from matplotlib.dates import DateFormatter

def get_CellVoltages(bmu,i):
    out_BMU = [data[bmu+'_Cell_1_Voltage'][i], data[bmu+'_Cell_2_Voltage'][i],
                    data[bmu+'_Cell_3_Voltage'][i], data[bmu+'_Cell_4_Voltage'][i],
                    data[bmu+'_Cell_5_Voltage'][i], data[bmu+'_Cell_6_Voltage'][i],
                    data[bmu+'_Cell_7_Voltage'][i], data[bmu+'_Cell_8_Voltage'][i], 
                    data[bmu+'_Cell_9_Voltage'][i], data[bmu+'_Cell_10_Voltage'][i], 
                    data[bmu+'_Cell_11_Voltage'][i], data[bmu+'_Cell_12_Voltage'][i]]
    return out_BMU

def get_Theta(v,i):
    warnings = ((33, 34, 47.5, 48.5, 50.4), (2.2, 2.3, 4.1, 4.2, 6.5))
    splits = (225,190,142,39,-10,-46)
    intercepts = ((225, 1774, 401.41, 2366.5, 908.95), (225, 1246, 273.61, 2048, 55.74))
    if i<2: 
        w = warnings[0]
        intercept = intercepts[0]
    else: 
        w = warnings[1]
        intercept = intercepts[1]

    if v < w[0]:
        dV = w[0]
        dT = splits[1]-splits[0]
        b = intercept[0]
    elif v < w[1]:
        dV = w[1] - w[0] 
        dT = splits[2] - splits[1]
        b = intercept[1]
    elif v < w[2]:
        dV =  w[2] - w[1]
        dT = splits[3] - splits[2]
        b = intercept[2]
    elif v < w[3]:
        dV = w[3] - w[2]
        dT = splits[4] - splits[3]
        b = intercept[3]
    else:
        dV = w[4] - w[3]
        dT = splits[5] - splits[4]
        b = intercept[4]
    
    theta = v*dT/dV + b
    return theta

# # read in all logs and combine into one log
# folder = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot'
# logs = [l[2] for l in os.walk(folder)]
# all_logs = [folder + '/' + l for l in logs[0]]
# combined_logs = pd.concat([pd.read_csv(l) for l in all_logs])
# combined_logs.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

data_file = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot/combined_logs.csv'
# data_file = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot/full_day.csv'
# data = pd.read_csv(data_file)
# data.sort_values('time')

# # Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# plt.style.use('dark_background')
fig = plt.figure(figsize=(14,8))
ax_main = fig.add_axes([0,0,1,1])
ax_main.axis('off')
im = plt.imread("/Users/quiana/Documents/UCSD/CER/Data_Processing/Processing/Cummins/realtime_plot_background.png")
implot = plt.imshow(im)
fig.suptitle("UCSD Cummins Site Monitoring", fontsize=20, y=0.92, fontweight='bold', color='white')
plt.xticks([])
plt.yticks([])

# choose background
# im = plt.imread("/Users/quiana/Documents/UCSD/CER/Data_Processing/Processing/Cummins/realtime_plot_background.png")
# implot = plt.imshow(im)
# fig.patch.set_facecolor('#030764')
# fig.patch.set_alpha(0.7)

# axmodV = plt.axes([.06, .5, .3, .3])
axmodV = plt.axes([.06, .5, .875, .3])
axmodP = axmodV.twinx()
# axmodC = plt.axes([.54, .5, .3, .3])

xs = []
ysmodP = []
ysmodV = []
ysmodC = []
# minCell = 0
# maxCell = 0
# minMod = 0
# maxMod = 0

# interval = 45
interval = 10*60
shift = -.06
shift2 = -.05
shift3 = -0.017
timestamp_var = plt.figtext(.03, .85, 'timestamp: ', fontsize=12, color='white')

minMod_var = plt.figtext(0.16 + shift + shift3, .09, 'Min: 0 V', fontsize=12, color='white')
maxMod_var = plt.figtext(0.335 + shift + shift3, .09, 'Max: 0 V', fontsize=12, color='white')
minCell_var = plt.figtext(0.595 + shift + shift2 + shift3, .09, 'Min: 0 V', fontsize=12, color='white')
maxCell_var = plt.figtext(0.77 + shift + shift2 + shift3, .09, 'Max: 0 V', fontsize=12, color='white')

temp_warn_var = plt.figtext(.87, .2, 'Temp: -°C\nHigh Temp Warning:\nNot Triggered', fontsize=12, 
                horizontalalignment='center',color='white', fontweight='bold')

plt.figtext(.67, .03, 'Center for Energy Research - Energy Storage Innovation', color='white', fontweight='bold')
plt.figtext(.124, .315, 'Module Voltage Min/Max', fontsize=12, color='white', fontweight='bold')
plt.figtext(.514, .315, 'Cell Voltage Min/Max', fontsize=12, color='white', fontweight='bold')

# axes for arrows
# ax1 = plt.axes([.135, .08, .128, .22], frameon=False)
# ax1.set_xticks([])
# ax1.set_yticks([])
# ax1.patch.set_alpha(0.3)
# ax1.set_xlim(-5,5)
# ax1.set_ylim(-5,5)
ax1 = plt.axes([.116+shift, .08, .728, .22])
# ax1.set_xticks([])
# ax1.set_yticks([])
# ax1.patch.set_alpha(0.5)
# ax1.set_xlim(0,10)
# ax1.set_ylim(0,.22/.7*10)
# ax1.patch.set_alpha(0)
# ax1.axis('off')   

# ax1.plot(0.89,2.5,marker='.',markersize=12)
# ax1.plot(3.33,2.5,marker='.',markersize=12)
# ax1.plot(6.72,2.5,marker='.',markersize=12)
# ax1.plot(9.13,2.5,marker='.',markersize=12)
shift3 = -.59
origins = (0.89+shift, 3.33+shift, 6.725+shift+shift3, 9.15+shift+shift3)


# arrow1 = ax1.arrow(0,0,0,0,length_includes_head=True, head_width=.5, width=.5, facecolor='black')

# Initiate Plots
P = axmodP.plot(xs,ysmodP, 'b', label='Power')
C = axmodP.plot(xs,ysmodC, 'r', label='Current')
V = axmodV.plot(xs,ysmodV, 'g', label='Voltage')


# Format Plots
axmodP.tick_params(direction='in', labelcolor='white')
axmodV.tick_params(direction='in', labelcolor='white')
# axmodV.set_xticklabels(axmodV.get_xticks(), rotation=60)
axmodV.set_yticks(np.arange(0,601,75))

axmodV.yaxis.grid()

lns = V + P + C
labs = [l.get_label() for l in lns]
axmodV.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', 
                ncol=3, facecolor='white', edgecolor='black', framealpha=1)
axmodP.set_ylim(-80, 80)
axmodV.set_ylim(0,600)

axmodP.set_title('Modbus Power, Current, and Voltage', color='white')

# axmodP.set_ylabel('Power [W]', color='white')
axmodV.set_ylabel('Voltage [V]', color='white')
axmodP.set_ylabel('Power [W], Current [A]', color='white')
axmodV.set_xlabel('Time [minutes]', color='white')


# This function is called periodically from FuncAnimation
def animate(i, xs, ysmodP, ysmodV, ysmodC, origins):

    data = pd.read_csv(data_file)

    # Get datetime
    dt_now = dt.datetime.now().strftime('%H:%M:%S')
    minute = int(dt.datetime.now().strftime('%M'))
    second = int(dt.datetime.now().strftime('%S'))
    xs.append(minute + second/60)
    # xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    

    timestamp_var.set_text('timestamp: ' + dt_now)

    # Get max and min cell/module voltages
    max_voltages = [data['BMU01_Max_Cell_Voltage'][-1], data['BMU02_Max_Cell_Voltage'][-1],
                    data['BMU03_Max_Cell_Voltage'][-1], data['BMU04_Max_Cell_Voltage'][-1],
                    data['BMU05_Max_Cell_Voltage'][-1], data['BMU06_Max_Cell_Voltage'][-1],
                    data['BMU07_Max_Cell_Voltage'][-1], data['BMU08_Max_Cell_Voltage'][-1]]
    min_voltages = [data['BMU01_Min_Cell_Voltage'][-1], data['BMU02_Min_Cell_Voltage'][-1],
                    data['BMU03_Min_Cell_Voltage'][-1], data['BMU04_Min_Cell_Voltage'][-1],
                    data['BMU05_Min_Cell_Voltage'][-1], data['BMU06_Min_Cell_Voltage'][-1],
                    data['BMU07_Min_Cell_Voltage'][-1], data['BMU08_Min_Cell_Voltage'][-1]]
    module_voltages = [data['BMU01_CMA_Voltage'][-1], data['BMU02_CMA_Voltage'][-1],
                    data['BMU03_CMA_Voltage'][-1], data['BMU04_CMA_Voltage'][-1],
                    data['BMU05_CMA_Voltage'][-1], data['BMU06_CMA_Voltage'][-1],
                    data['BMU07_CMA_Voltage'][-1], data['BMU08_CMA_Voltage'][-1]]
    temps = [data['BMU01_CMA_Max_Temp'][-1], data['BMU02_CMA_Max_Temp'][-1],
            data['BMU03_CMA_Max_Temp'][-1], data['BMU04_CMA_Max_Temp'][-1],
            data['BMU05_CMA_Max_Temp'][-1], data['BMU06_CMA_Max_Temp'][-1],
            data['BMU07_CMA_Max_Temp'][-1], data['BMU08_CMA_Max_Temp'][-1]]

    # Get pump fan status
    temp_warning = data['isPcanTempWarning'][-1]
    max_temp = max(temps)
    if temp_warning:
        temp_warn_var.set_text('Max Temp: '+str(max_temp)+'°C\nHigh Temp Warning:\nTriggered')
        temp_warn_var.set_color('red')
    else:
        temp_warn_var.set_text('Max Temp: ' + str(max_temp) + '°C\nHigh Temp Warning:\nNot Triggered')
        temp_warn_var.set_color('white')

    # xs.append(data['time'][-1])
    ysmodP.append(data['modbus_Power'][-1])
    ysmodV.append(data['modbus_Voltage'][-1])
    ysmodC.append(data['modbus_Current'][-1])
    minCell = min(min_voltages)
    maxCell = max(max_voltages)
    minMod = min(module_voltages)
    maxMod = max(module_voltages)

    # Update min/max values
    minMod_var.set_text('Min: ' + "{:.2f}".format(minMod) + ' V')
    maxMod_var.set_text('Max: ' + "{:.2f}".format(maxMod) + ' V')
    minCell_var.set_text('Min: ' + "{:.2f}".format(minCell) + ' V')
    maxCell_var.set_text('Max: ' + "{:.2f}".format(maxCell) + ' V')

    # Update gauge arrows
    ax1.clear()
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.patch.set_alpha(0)
    ax1.axis('off')
    ax1.set_xlim(0,10)
    ax1.set_ylim(0,.22/.728*10)
    h = .6
    o = 1.5
    vals = (minMod, maxMod, minCell, maxCell)
    for i in range(4):
        theta = get_Theta(vals[i],i)
        dy = h*np.sin(theta*np.pi/180)
        dx = h*np.cos(theta*np.pi/180)
        ax1.plot(origins[i],o, color='black', marker='.', markersize=15)
        # ax1.arrow(origins[i],o,dx,dy,length_includes_head=True, head_width=.5, width=.5, facecolor='black')
        ax1.arrow(origins[i],o,dx,dy,head_width=.1, width=.1, facecolor='black')

    # get min value
    low = max(0,len(xs)-interval)

    # Limit x and y lists to 20 items
    xs = xs[low:]
    ysmodP = ysmodP[low:]
    ysmodV = ysmodV[low:]
    ysmodC = ysmodC[low:]

    # P[0].set_data(np.arange(len(xs)),ysmodP)
    # C[0].set_data(np.arange(len(xs)),ysmodC)
    # V[0].set_data(np.arange(len(xs)),ysmodV)
    P[0].set_data(xs,ysmodP)
    C[0].set_data(xs,ysmodC)
    V[0].set_data(xs,ysmodV)
    # axmodV.set_xticklabels(xs)
    # axmodV.fmt_xdata="{%:.2f}".format(xs)
    axmodV.set_xlim(xs[low], xs[-1])
    # axmodV.set_xticks(np.arange(xs[low], xs[-1],.1))
    # axmodV.fmt_xdata = DateFormatter('%S') 

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ysmodP, ysmodV, ysmodC, origins), interval=100)
plt.show()

