import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime as dt
import matplotlib.animation as animation
import matplotlib.ticker as mticker
from matplotlib.patches import Arrow

def get_CellVoltages(bmu,i):
    out_BMU = [data[bmu+'_Cell_1_Voltage'][i], data[bmu+'_Cell_2_Voltage'][i],
                    data[bmu+'_Cell_3_Voltage'][i], data[bmu+'_Cell_4_Voltage'][i],
                    data[bmu+'_Cell_5_Voltage'][i], data[bmu+'_Cell_6_Voltage'][i],
                    data[bmu+'_Cell_7_Voltage'][i], data[bmu+'_Cell_8_Voltage'][i], 
                    data[bmu+'_Cell_9_Voltage'][i], data[bmu+'_Cell_10_Voltage'][i], 
                    data[bmu+'_Cell_11_Voltage'][i], data[bmu+'_Cell_12_Voltage'][i]]
    return out_BMU

# # read in all logs and combine into one log
# folder = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot'
# logs = [l[2] for l in os.walk(folder)]
# all_logs = [folder + '/' + l for l in logs[0]]
# combined_logs = pd.concat([pd.read_csv(l) for l in all_logs])
# combined_logs.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

data_file = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot/combined_logs.csv'
# data_file = r'/Users/quiana/Documents/UCSD/CER/Data_Processing/Data/Cummins/realtime_plot/full_day.csv'
data = pd.read_csv(data_file)
data.sort_values('time')

# # Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# plt.style.use('dark_background')
fig = plt.figure(figsize=(14,8))
ax_main = fig.add_axes([0,0,1,1])
ax_main.axis('off')
im = plt.imread("/Users/quiana/Documents/UCSD/CER/Data_Processing/Processing/Cummins/realtime_plot_background_gauge_fan_logo.png")
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
minCell = 0
maxCell = 0
minMod = 0
maxMod = 0

interval = 45
# intverval = 10*60
shift = -.075
timestamp_var = plt.figtext(.03, .85, 'timestamp: ', fontsize=12, color='white')

minMod_var = plt.figtext(0.16 + shift, .09, 'Min: 0 V', fontsize=12, color='white')
maxMod_var = plt.figtext(0.335 + shift, .09, 'Max: 0 V', fontsize=12, color='white')
minCell_var = plt.figtext(0.59 + shift, .09, 'Min: 0 V', fontsize=12, color='white')
maxCell_var = plt.figtext(0.765 + shift, .09, 'Max: 0 V', fontsize=12, color='white')

temp_warn_var = plt.figtext(.89, .2, 'High Temp Warning:\nNot Triggered', fontsize=12, 
                horizontalalignment='center',color='white', fontweight='bold')

plt.figtext(.71, .03, 'Center for Energy Research - Energy Storage Innovation', color='white')

# axes for arrows
# ax1 = plt.axes([.135, .08, .128, .22], frameon=False)
# ax1.set_xticks([])
# ax1.set_yticks([])
# ax1.patch.set_alpha(0.3)
# ax1.set_xlim(-5,5)
# ax1.set_ylim(-5,5)
ax1 = plt.axes([.135+shift, .08, .728, .22])
ax1.set_xticks([])
ax1.set_yticks([])
ax1.patch.set_alpha(0.5)
ax1.set_xlim(0,10)
ax1.set_ylim(0,.22/.728*10)

# ax1.plot(0.89,2.5,marker='.',markersize=12)
# ax1.plot(3.33,2.5,marker='.',markersize=12)
# ax1.plot(6.72,2.5,marker='.',markersize=12)
# ax1.plot(9.13,2.5,marker='.',markersize=12)

origins = (0.89+shift, 3.33+shift, 6.72+shift, 9.13+shift)

# arrow1 = ax1.arrow(0,0,0,0,length_includes_head=True, head_width=.5, width=.5, facecolor='black')




# This function is called periodically from FuncAnimation
def animate(i, xs, ysmodP, ysmodV, ysmodC, minCell, maxCell, minMod, maxMod, origins):

    # # Read temperature (Celsius) from TMP102
    # temp_c = round(tmp102.read_temp(), 2)

    # Get datetime
    dt_now = dt.datetime.now().strftime('%H:%M:%S')
    # second = int(dt.datetime.now().strftime('%S'))
    # xs.append(second)
    xs.append(dt.datetime.now().strftime('%S'))

    timestamp_var.set_text('timestamp: ' + dt_now)

    # Get cell voltages, and max/min cell voltages
    BMU1_cellV = get_CellVoltages('BMU01',i)
    BMU2_cellV = get_CellVoltages('BMU02',i)
    BMU3_cellV = get_CellVoltages('BMU03',i)
    BMU4_cellV = get_CellVoltages('BMU04',i)
    BMU5_cellV = get_CellVoltages('BMU05',i)
    BMU6_cellV = get_CellVoltages('BMU06',i)
    BMU7_cellV = get_CellVoltages('BMU07',i)
    BMU8_cellV = get_CellVoltages('BMU08',i)
    BMU_cellV = BMU1_cellV + BMU2_cellV + BMU3_cellV + BMU4_cellV + BMU5_cellV + BMU6_cellV + BMU7_cellV + BMU8_cellV

    # Get max and min cell/module voltages
    max_voltages = [data['BMU01_Max_Cell_Voltage'][i], data['BMU02_Max_Cell_Voltage'][i],
                    data['BMU03_Max_Cell_Voltage'][i], data['BMU04_Max_Cell_Voltage'][i],
                    data['BMU05_Max_Cell_Voltage'][i], data['BMU06_Max_Cell_Voltage'][i],
                    data['BMU07_Max_Cell_Voltage'][i], data['BMU08_Max_Cell_Voltage'][i]]
    min_voltages = [data['BMU01_Min_Cell_Voltage'][i], data['BMU02_Min_Cell_Voltage'][i],
                    data['BMU03_Min_Cell_Voltage'][i], data['BMU04_Min_Cell_Voltage'][i],
                    data['BMU05_Min_Cell_Voltage'][i], data['BMU06_Min_Cell_Voltage'][i],
                    data['BMU07_Min_Cell_Voltage'][i], data['BMU08_Min_Cell_Voltage'][i]]
    module_voltages = [data['BMU01_CMA_Voltage'][i], data['BMU02_CMA_Voltage'][i],
                    data['BMU03_CMA_Voltage'][i], data['BMU04_CMA_Voltage'][i],
                    data['BMU05_CMA_Voltage'][i], data['BMU06_CMA_Voltage'][i],
                    data['BMU07_CMA_Voltage'][i], data['BMU08_CMA_Voltage'][i]]

    # Get pump fan status
    temp_warning = data['isPcanTempWarning'][i]
    if temp_warning:
        temp_warn_var.set_text('High Temp Warning:\nTriggered')
        temp_warn_var.set_color('red')
    else:
        temp_warn_var.set_text('High Temp Warning:\nNot Triggered')
        temp_warn_var.set_color('white')

    # xs.append(data['time'][i])
    ysmodP.append(data['modbus_Power'][i])
    ysmodV.append(data['modbus_Voltage'][i])
    ysmodC.append(data['modbus_Current'][i])
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
        if i<2: 
            deltaV = 32.4-50.4
        else: 
            deltaV = 2.7-4.2
        theta = vals[i]*(240+60)/deltaV+780
        # theta = vals[i]
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

    # Draw x and y lists
    axmodP.clear()
    axmodV.clear()


    # P = axmodP.plot(np.arange(len(xs)),ysmodP, 'b', label='Power')
    # C = axmodP.plot(np.arange(len(xs)),ysmodC, 'r', label='Current')
    # V = axmodV.plot(np.arange(len(xs)),ysmodV, 'g', label='Voltage')
    # axmodV.set_xticklabels(xs)

    P = axmodP.plot(xs,ysmodP, 'b', label='Power')
    C = axmodP.plot(xs,ysmodC, 'r', label='Current')
    V = axmodV.plot(xs,ysmodV, 'g', label='Voltage')


    # Format plot
    # axmodV.set_xticklabels([])
    # axmodP.set_xticklabels([])
    # axmodV.tick_params(direction='in', labelcolor='white')
    axmodP.tick_params(direction='in', labelcolor='white')
    axmodV.tick_params(labelrotation=60, direction='in', labelcolor='white')

    # lns = P + C + V
    # labs = [l.get_label() for l in lns]
    # # axmodV.legend(lns, labs, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    # axmodV.legend(lns, labs, loc='lower left')
    axmodV.legend(loc='lower left')
    axmodP.legend(loc='lower right')

    axmodP.set_ylim(-80, 80)
    axmodV.set_ylim(-5,600)
    axmodV.set_xlim(xs[low], xs[-1])

    axmodP.set_title('Modbus Power, Current, and Voltage', color='white')

    # axmodP.set_ylabel('Power [W]', color='white')
    axmodV.set_ylabel('Voltage [V]', color='white')
    axmodP.set_ylabel('Power [W], Current [A]', color='white')
    axmodV.set_xlabel('Time [seconds]', color='white')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ysmodP, ysmodV, ysmodC, minCell, maxCell, minMod, maxMod, origins), interval=500)
plt.show()

