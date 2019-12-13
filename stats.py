#!/usr/bin/env python
# encoding: utf-8
"""
Gets stats and plots stuff given a protocol
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid", {'axes.grid' : False})
import numpy as np
np.set_printoptions(precision=2, suppress=True)

from pyannote.database import get_protocol

DATABASE="Plumcot-Friends"
TASK="SpeakerDiarization"
PROTOCOL="UEM"
SET='train'
FIGURE_DIR='/people/lerner/Images'
protocol_str='{}.{}.{}'.format(DATABASE,TASK,PROTOCOL)
filter_unk=False
crop=None
hist=False

def plot_speech_duration(values,hist=True,crop=None):
    keep_n=len(values) if crop is None else int(len(values)*crop)
    values.sort()
    values=values[-keep_n:]
    plt.figure(figsize=(12,10))
    title=(
        f"of the speech duration in {protocol_str}.{SET} "
        f"of the {keep_n} biggest speakers"
    )
    if hist:
        sns.distplot(values,kde=False,norm_hist=True)
        plt.ylabel("density")
        plt.xlabel("speech duration")
        plt.title("Normed histogram "+title)
    else:
        plt.title("Plot "+title)
        plt.ylabel("speech duration")
        plt.xlabel("speaker #")
        plt.plot(values,".")
    fig_type="hist" if hist else "plot"
    plt.savefig(os.path.join(FIGURE_DIR,f"speech_duration.{protocol_str}.{SET}.{fig_type}.{keep_n}.png"))

if __name__=='__main__':

    protocol = get_protocol(protocol_str)
    print(f"gettings stats from {protocol_str}.{SET}...")
    stats=protocol.stats(SET)
    for key,value in stats.items():
        if key=='labels':
            break
        print(key,value)

    print("speech duration quartiles :")
    if filter_unk:
        values=[value for label,value in stats['labels'].items() if '#unknown#' not in label]
    else:
        values=list(stats['labels'].values())
    print("n_speakers:",len(values))
    print("quartiles:")
    print(np.quantile(values,[0.,0.25,0.5,0.75,1.0]))

    print("deciles:")
    print(np.quantile(values,np.arange(0,1.1,0.1)))

    plot_speech_duration(values,hist,crop)
