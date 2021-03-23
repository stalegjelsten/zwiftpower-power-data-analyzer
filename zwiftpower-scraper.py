# %%
import json
import pandas as pd
import urllib.request
import time
import datetime
import re
from bs4 import BeautifulSoup


# Below are some constants you might want to change. I recommend 
# analysis_data_cache = True for performance reasons, and to limit the
# burden on the ZwiftPower servers

# max_rank: max zwiftpower rank for rider to be included in analysis
# print_progress = n: print progress for every n'th rider
# all_riders = False: use top ~1000 ranked riders. If True, use all ZP 
#   riders
# analysis_data_cache = True: use cached data for analysis. 
# power_tolerance is the max discrepancy between power meter reading
#   and smart trainer reading you are willing to accept. A value of 0.15
#   means that any race with a larger discrepancy than 15 % will be 
#   discarded

########################################################################
# START USER CONFIG ZONE
########################################################################

max_rank = 500                      
print_progress = 20                  
all_riders = False                  
analysis_data_cache = True          
power_tolerance = 0.15

# regex dictionary replacing any match of the regex key with the value
power_meter_replace_dict = {
    r"quarq" : "quarq",
    r"favero" : "favero",
    r"assioma" : "favero",
    r"srm" : "srm",
    r"power2max" : "power2max",
    r"p2m" : "power2max",
    r"4iiii" : "4iiii",
    r"shimano.*dura.*ace" : "dura_ace",
    r"vector" : "vector",
    r"v3" : "vector",
    r"rotor" : "rotor",
    r"powertap" : "powertap",
    r"stages" : "stages",
    r"pioneer" : "pioneer",
    r"xcadey" : "xcadey",
    r"giant.*power" : "giant_power",
    r"infocra.*k" : "infocrank",
    r"^sram.*axs" : "sram_axs"
}

# regex dictionary replacing any match of the regex key with the value
smart_trainer_replace_dict = {
    r"h3" : "saris_h3",
    r"h2" : "saris_h2",
    r"hammer" : "saris_hammer",
    r"saris.*m2" : "saris_m2",
    r"magnus" : "saris_magnus",
    r"direto.*(2|ii)" : "elite_direto_2",
    r"direto.*xr" : "elite_direto_xr",
    r"(?!.*xr)(?=.*direto.*x)" : "elite_direto_x",
    r"(?!.*(x|xr|2|ii))(?=.*direto)" : "elite_direto",
    r"(?!.*(2|ii))(?=.*drivo.*)" : "elite_drivo",
    r"drivo.*(2|ii)" : "elite_drivo_2",
    r"muin" : "elite_muin",
    r"suito" : "elite_suito",
    r"qubo" : "elite_qubo",
    r"novo" : "elite_novo",
    r"flux.*2" : "tacx_flux_2",
    r"(?!.*ux\ssmart.*)(?=flux.*s)" : "tacx_flux_s",
    r"(?!(.*2.*|.*ux\ss.*))(?=flux)" : "tacx_flux",
    r"(?!(.*2.*|.*ii.*))(?=neo)" : "tacx_neo",
    r"(?!.*2t.*)(?=neo.*(2[^\d]|ii))" : "tacx_neo_2",
    r"neo.*2t" : "tacx_neo_2t",
    r"neo.*bike" : "tacx_neo_bike",
    r"(?!.*(core|snap|bike).*)(?=kickr)" : "wahoo_kickr",
    r"kickr.*core" : "wahoo_kickr_core",
    r"kickr.*snap" : "wahoo_kickr_snap",
    r"kickr.*bike" : "wahoo_kickr_bike",
    r"wattbike.*atom" : "wattbike_atom",
    r"bkool.*classic" : "bkool_classic",
    r"bkool.*smart" : "bkool_smart_pro",
    r"road.*machine" : "kinetic_road_machine",
    r"rock.*and.*roll" : "kinetic_rock_and_roll",
    r"kagura" : "minoura_kagura",
    r"bushido" : "tacx_bushido",
    r"vortex" : "tacx_vortex",
    r"genius" : "tacx_genius",
    r"satori" : "tacx_satori"
}                                   
########################################################################
# END USER CONFIG ZONE
########################################################################

if analysis_data_cache:
    base_url = "https://www.zwiftpower.com/cache3/profile/"
    base_url_appendix = "_analysis_list.json"
else:
    base_url = "https://www.zwiftpower.com/api3.php?do=analysis_list&zwift_id="
    base_url_appendix = ""

if all_riders:
    # all riders JSON is located here ↓
    # https://www.zwiftpower.com/cache3/global/rider_list.json
    # A version of the list from 2021-03-17 with most of the JSON attributes
    # stripped (only inlcuding name, zwift id, ftp and rank) is available in
    # the github repo as minified_rider_list.json
    with open("minified_rider_list.json") as file:
        json_top_riders = json.load(file)
        del file

else:
    # top ~1000 riders list JSON is situated here ↓
    # https://www.zwiftpower.com/cache3/lists/2_standings_.json .
    with urllib.request.urlopen("https://www.zwiftpower.com/"\
                                "cache3/lists/2_standings_.json") as response:
        json_top_riders = json.load(response)


# We are interested in the the top zwifters personal data (name and ID)
top_zwifter = json_top_riders.get("data")
top_zwids, riders = [], []

# make lists of zwift_ids and rider names
for zwifter in top_zwifter:
    
    # we only want to check riders with zwiftpower rank less than variable
    # rank string is converted to int without decimal part (last 3 chars)
    if int(zwifter.get("rank")[:-3]) < max_rank:
        top_zwids.append(zwifter.get("zwid"))
        riders.append(zwifter.get("name"))


zwift_ids, setids, names, dates, titles, device_pm, device_st, power300_pm, \
    power300_st, pm_simplified, st_simplified  =  \
           [], [], [], [], [], [], [], [], [], [], []
race_values_list = [zwift_ids, setids, names, dates, titles, device_pm, \
    device_st, power300_pm, power300_st]

pm_regex_list = list(power_meter_replace_dict.keys())
pm_value_list = list(power_meter_replace_dict.values())
pm_regex_compiled = [re.compile(r".*" + i +".*", re.I) for i in pm_regex_list]

st_regex_list = list(smart_trainer_replace_dict.keys())
st_value_list = list(smart_trainer_replace_dict.values())
st_regex_compiled = [re.compile(r".*" + i +".*", re.I) for i in st_regex_list]

progress = 0

print(f"Selected {len(top_zwids)} Zwifters with rank below 500 from"\
    f" {len(top_zwifter)} Zwifters total.")

# Delete some quite large objects
del top_zwifter, json_top_riders


# %%
time_start, time_request = time.time(), 0

# iterate over all zwifters, starting from index = progress (default=0)
for zwifter, rider in zip(top_zwids[progress:], riders[progress:]):

    # calculate remaining time
    time_rem = datetime.timedelta(seconds=((time.time() - time_start) / \
                         ((progress+1) / len(top_zwids)) - (time.time() \
                          - time_start)))

    # print progress
    if progress % print_progress == 0:
        print(f"# {progress:4}. ID: {zwifter:8}."\
            f" {progress/len(top_zwids) * 100:5.2f} % finished."\
            f" Request time: {time_request:.2f} s. Est."\
            f" {time_rem} remaining.")

    
    # wait for some seconds – don't flood the server
    #time.sleep(0.5)
    
    time_request_start = time.time()
    
    progress += 1
    
    # request analysis JSON for rider
    request = urllib.request.Request(base_url + str(zwifter) + \
                                     base_url_appendix)
    
    # try to open the URL. Skip to next rider if there is an error
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        try:
            response = urllib.request.urlopen("https://www.zwiftpower.com/" \
                "api3.php?do=analysis_list&zwift_id=" + str(zwifter))
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read()) 
            continue
    except urllib.error.URLError as e:
        continue
    
    analysis_json_obj = json.load(response)
    time_request_end = time.time()
    time_request = time_request_end - time_request_start

    # get every race for current rider
    races = analysis_json_obj.get("data")


    # iterate over each race
    for race in races:

        pm_search, st_search, subst_pm, subst_st = None, None, \
                                                    None, None
    
        # if the race has exactly 2 power values for 300s power...
        # ... and none of the values are zero
        if race.get("power300") and 0 not in race.get("power300"):
            num_devices = len(race.get("power300"))
        else:
            num_devices = 0

        # if we have 2 devices and max 10 % difference between
        # device power readings, add values to lists.
        if num_devices == 2 and abs(race.get("power300")[0]/\
                    race.get("power300")[1] - 1) < power_tolerance:
            devices = []
        else:
            continue

        # device names are stored as name1, name2 etc.
        for i in range(num_devices):
            devices.append(race.get("name" + str(i+1)))
        

        # if one of the devices is unnamed, skip race.            
        if 0 in devices:
            continue


        # checking for matches in devices list. Iterating in reverse
        # for the smart trainer, to minimize probability for both pm_regex
        # and st_regex matching the same device

        for i in devices:
            for j in pm_regex_compiled:
                if not pm_search:
                    pm_search = re.search(j,i)
        
        for i in devices[::-1]:
            for k in st_regex_compiled:
                if not st_search:
                    st_search = re.search(k,i)



        if pm_search and st_search:
            pm_index = devices.index(pm_search[0])
            st_index = devices.index(st_search[0])

            # skip race if pm_regex and st_regex have
            # matched the same device
            if pm_index == st_index:
                continue



            setids.append(race.get("set_id"))
            zwift_ids.append(zwifter)
            names.append(rider)
            dates.append(race.get("date"))
            titles.append(race.get("title"))
            device_pm.append(devices[pm_index])
            device_st.append(devices[st_index])
            power300_pm.append(race.get("power300")[pm_index])
            power300_st.append(race.get("power300")[st_index])
            for regex, repl_pm, in zip(pm_regex_compiled, pm_value_list):
                subst_pm = re.search(regex, devices[pm_index])
                if subst_pm:
                    pm_simplified.append(repl_pm)
                    break
            
            for regex, repl_st in zip(st_regex_compiled, st_value_list):
                subst_st = re.search(regex, devices[st_index])
                if subst_st:
                    st_simplified.append(repl_st)
                    break
            if not subst_pm or not subst_st:
                print(f"{setids[-1]}. Power meter: \n{subst_pm} \n Smart"\
                        f"trainer: \n, {subst_st}")

                    

print(f"Finished! Saved {len(zwift_ids)} rows in {time.time()-time_start} s.")


# %%
# mash all of the lists into a much more efficient pandas dataframe structure
dataframe_columns = {
    "zwift_id": zwift_ids,
    "name": names,
    "time": pd.to_datetime(dates, unit="s"),
    "title": titles,
    "pm": device_pm,
    "st": device_st,
    "pm_simplified": pm_simplified,
    "st_simplified": st_simplified,
    "p300s_pm": power300_pm,
    "p300s_st": power300_st
}
df = pd.DataFrame(dataframe_columns, index=setids)

# drop the duplicate values. no mercy!
df = df[~df.duplicated(keep="first")]

# calculate the delta (diffrence) between power meter and smart trainer
df["delta"] = df["p300s_pm"] - df["p300s_st"]


# %%
# export to csv without rider names
df.drop("name", axis = 1).to_csv("data_full_dataset.csv")
#df.drop("name", axis = 1).to_excel("data_full_dataset.xlsx")


