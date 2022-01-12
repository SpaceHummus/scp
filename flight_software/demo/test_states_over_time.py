import yaml
from datetime import datetime
#
states_over_time_orig=[]
states_over_time_new=[]
date_diffrences = []
updated_dates=[]
conf_dic=[]

def get_state_over_time():
    global states_over_time_orig
    global conf_dic
    file = open(r'../logic_states2.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    states_over_time_orig = conf_dic["states_over_time"] 
    file.close()
    #logging.info("states_over_time:%s",str(states_over_time))

def hour_date_diffrences():
    global date_diffrences
    date_time_0 = datetime.strptime(states_over_time_orig[0][0],"%Y/%m/%d %H:%M:%S")
    for i in range(len(states_over_time_orig)):
        date_time_str = states_over_time_orig[i][0]
        date_time_obj = datetime.strptime(date_time_str,"%Y/%m/%d %H:%M:%S")
        diffrences = date_time_obj-date_time_0
        print(diffrences)
        date_diffrences.append(diffrences)
    print(date_diffrences)

def hour_from_diffrencesdate_time(date_time):
    global updated_dates
    for i in range(len(date_diffrences)):
        updated_date = date_time +date_diffrences[i]
        updated_date = updated_date.strftime('%Y/%m/%d %H:%M:%S')
        print(updated_date)
        updated_dates.append(updated_date)
    print(updated_dates)


def updated_states_over_time():
    global states_over_time_new
    for i in range(len(states_over_time_orig)):
        states_over_time_new.append([updated_dates[i],states_over_time_orig[i][1]])
    print(states_over_time_new)


def upload_to_logic_states():
    conf_dic["states_over_time"] = states_over_time_new
    with open('../logic_states2.yaml','w') as f:
        yaml.dump(conf_dic, f)


def main():
    get_state_over_time()
    hour_date_diffrences()
    hour_from_diffrencesdate_time(datetime.now())
    updated_states_over_time()
    upload_to_logic_states()
    #print(states_over_time)
    

if __name__ == "__main__":
        main()
