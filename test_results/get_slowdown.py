from math import nan
import pandas as pd
import numpy as np
import json 

RES_FOLDER = "1697182227_test/"

no_mod_times = pd.read_csv(RES_FOLDER + "no_mod.csv")
no_sync_times = pd.read_csv(RES_FOLDER + "no_sync.csv")
sync_times = pd.read_csv(RES_FOLDER + "sync.csv")

languages = no_mod_times["Language"].unique()
tests = no_mod_times["Test Name"].unique()

medians = {}
slowdown = {
    "Language":[],
    "Test Name":[],
    "LKM No Sync":[],
    "LKM Sync":[],
}
for l in languages:
    if medians.get(l) == None:
        medians[l] = {}
    for t in tests:
        # no_mod = np.median(np.array())
        # print(no_mod_times.loc[(no_mod_times["Test Name"] == t) & (no_mod_times["Language"] == l), ["Real Time"]])
        no_mod_med = np.median(np.array(no_mod_times.loc[
            (no_mod_times["Test Name"] == t) & (no_mod_times["Language"] == l), 
            ["Real Time"]]))
        no_sync_med = np.median(np.array(no_sync_times.loc[
            (no_sync_times["Test Name"] == t) & (no_sync_times["Language"] == l), 
            ["Real Time"]]))
        sync_med = np.median(np.array(sync_times.loc[
            (sync_times["Test Name"] == t) & (sync_times["Language"] == l), 
            ["Real Time"]]))

        medians[l][t] = (no_mod_med, no_sync_med, sync_med)

        if no_mod_med != nan:
            slowdown["Language"].append(l)
            slowdown["Test Name"].append(t)
            slowdown["LKM No Sync"].append((no_sync_med-no_mod_med)/no_mod_med)
            slowdown["LKM Sync"].append((sync_med-no_mod_med)/no_mod_med)
        
        print(f"{l} & {t} & ${(no_sync_med-no_mod_med)/no_mod_med*100:.2f}\\%$ & ${(sync_med-no_mod_med)/no_mod_med*100:.2f}\\%$ \\\\")

# print(json.dumps(medians, indent=1))

slow_pd = pd.DataFrame(slowdown)

# print(slow_pd)