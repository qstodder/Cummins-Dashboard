import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime as dt
import matplotlib.animation as animation
import matplotlib.ticker as mticker

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
data = pd.read_csv(data_file)
data.sort_values('time')

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

axmodV = plt.axes([.06, .5, .3, .3])
axmodP = axmodV.twinx()
axV = plt.axes([.54, .5, .3, .3])
axMP = plt.axes([.06, .1, .3, .3])
axmP = plt.axes([.54, .1, .3, .3])

axmodV.set_xticklabels([])
axmodP.set_xticklabels([])
axV.set_xticklabels([])
axmodV.tick_params(direction='in', labelcolor='white')
axmodP.tick_params(direction='in', labelcolor='white')
axV.tick_params(direction='in', labelcolor='white')
axMP.tick_params(labelrotation=60, direction='in', labelcolor='white')
axmP.tick_params(labelrotation=60, direction='in', labelcolor='white')



axmodP.set_title('Modbus Power and Voltage', color='white')
axV.set_title('Cell Voltage', color='white')  
axMP.set_title('Max Cell Voltage per Module', color='white')
axmP.set_title('Min Cell Voltage per Module', color='white')

axmodP.set_ylabel('Power [W]', color='white')
axmodV.set_ylabel('Voltage [V]', color='white')
axV.set_ylabel('Voltage [V]', color='white')
axMP.set_ylabel('Power [W]', color='white')
axmP.set_ylabel('Power [W]', color='white')

axMP.set_xlabel('Time [seconds]', color='white')
axmP.set_xlabel('Time [seconds]', color='white')
# axMP.set_xticklabels(rotation=45, ha='right')
# plt.xticks(rotation=45, ha='right')
# plt.subplots_adjust(bottom=0.30)


xs = []
ysmodP = []
ysmodV = []
ysV = []
ysMP = []
ysmP = []

interval = 30
# ysPV.append(data['modbus_Current'][0:interval])
# ysV.append(data['modbus_Voltage'][0:interval])
# ysMP.append(data['modbus_Power'][0:interval])
textvar = plt.figtext(.03, .95, 'timestamp: ', fontsize=12, color='white')
plt.figtext(.71, .97, 'Center for Energy Research - Energy Storage Innovation', color='white')

modP = axmodP.plot(np.arange(len(xs)),ysmodP, 'b', label='Power')
modV = axmodV.plot(np.arange(len(xs)),ysmodV, 'g', label='Voltage')
# V = axV.plot(np.arange(len(xs)),ysV)
MP = axMP.plot(np.arange(len(xs)),ysMP)
mP = axmP.plot(np.arange(len(xs)),ysmP)

axmodP.set_ylim(-80, 80)
axmodV.set_ylim(0,500)
axV.set_ylim(3.7, 4)
axMP.set_ylim(3.7, 4)
axmP.set_ylim(3.7, 4)

# This function is called periodically from FuncAnimation
def animate(i, xs, ysmodP, ysmodV, ysV, ysMP, ysmP):

    # # Read temperature (Celsius) from TMP102
    # temp_c = round(tmp102.read_temp(), 2)

    # Get datetime
    dt_now = dt.datetime.now().strftime('%H:%M:%S')
    second = int(dt.datetime.now().strftime('%S'))
    xs.append(second)
    textvar.set_text('timestamp: ' + dt_now)
    # textvar = plt.figtext(.03, .95, , fontsize=12)

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

    # Get max and min cell voltages
    max_voltages = [data['BMU01_Max_Cell_Voltage'][i], data['BMU02_Max_Cell_Voltage'][i],
                    data['BMU03_Max_Cell_Voltage'][i], data['BMU04_Max_Cell_Voltage'][i],
                    data['BMU05_Max_Cell_Voltage'][i], data['BMU06_Max_Cell_Voltage'][i],
                    data['BMU07_Max_Cell_Voltage'][i], data['BMU08_Max_Cell_Voltage'][i]]
    min_voltages = [data['BMU01_Min_Cell_Voltage'][i], data['BMU02_Min_Cell_Voltage'][i],
                    data['BMU03_Min_Cell_Voltage'][i], data['BMU04_Min_Cell_Voltage'][i],
                    data['BMU05_Min_Cell_Voltage'][i], data['BMU06_Min_Cell_Voltage'][i],
                    data['BMU07_Min_Cell_Voltage'][i], data['BMU08_Min_Cell_Voltage'][i]]

    # xs.append(data['time'][i])
    ysmodP.append(data['modbus_Power'][i])
    ysmodV.append(data['modbus_Voltage'][i])
    ysV.append(BMU_cellV)
    ysMP.append(max_voltages)
    ysmP.append(min_voltages)

    # get min value
    low = max(0,len(xs)-interval)

    # Limit x and y lists to 20 items
    xs = xs[low:]
    ysmodP = ysmodP[low:]
    ysmodV = ysmodV[low:]
    ysV = ysV[low:]
    ysMP = ysMP[low:]
    ysmP = ysmP[low:]

    x_plot = np.arange(len(xs))

    modP[0].set_xdata(np.arange(len(xs)))
    modP[0].set_ydata(ysmodP)

    modV[0].set_xdata(np.arange(len(xs)))
    modV[0].set_ydata(ysmodV)

    # V[0].set_xdata(np.arange(len(xs)))
    # V[0].set_ydata(ysV)

    MP[0].set_xdata(np.arange(len(xs)))
    MP[0].set_ydata(ysMP)

    mP[0].set_xdata(np.arange(len(xs)))
    mP[0].set_ydata(ysmP)

    axmodP.set_xlim(x_plot[0], x_plot[-1:])
    axmodV.set_xlim(x_plot[0], x_plot[-1:])

    lns = modP + modV
    labs = [l.get_label() for l in lns]
    axmodV.legend(lns, labs, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    axMP.legend(['BMU01', 'BMU02', 'BMU03', 'BMU04', 'BMU05', 'BMU06', 'BMU07', 'BMU08'],
            bbox_to_anchor=(1.05, 1.0), loc='upper left')
    axmP.legend(['BMU01', 'BMU02', 'BMU03', 'BMU04', 'BMU05', 'BMU06', 'BMU07', 'BMU08'],
            bbox_to_anchor=(1.05, 1.0), loc='upper left')



# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ysmodP, ysmodV, ysV, ysMP, ysmP), interval=10)
plt.show()





