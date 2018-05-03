from nptdms import tdms

class drivetdms(object):
    
    def __init__(self, tdpath):
        self.tdmspath = tdpath
        self.tdmsfile = tdms.TdmsFile(self.tdmspath)
        self.data_dict = {}
        self.build_channels()
    
    def __clean_channel_name(self, group, ch_in):
        l = ch_in
        l = l.replace("'","")             #first get rid of quotes
        l = l.replace(group + " - ","")   #next get rid of the group name followed by sp - sp
        l = l.replace("(", "")            #finally get rid of symbols and spaces
        l = l.replace(")", "")
        l = l.replace("%", "Percent")
        l = l.replace("#", "")
        l = l.replace("-", "_")
        l = l.replace(" ", "_")
        return l
        
    def get_data_channels(self):
        return self.data_dict.keys()
        

    def build_channels(self):
        self.data_dict = {}
        for group in self.tdmsfile.groups():
            if group == 'CAN 1':
                for channel in self.tdmsfile.group_channels(group):
                    
                    label = channel.path.split('/')
                    group_label = label[-2]
                    group_label = group_label.replace("'","")[0:1]
                    
                    l = label[-1]
                    l = self.__clean_channel_name(group, l)
                    
                    table_label = group_label + l
                    table_label = l
                    
                    if table_label.find("Timestamp") >= 0:
                        self.data_dict.update({table_label : channel.data})
                    elif table_label.find("04") >= 0:
                        self.data_dict.update({"cEngineRPM" : channel.data})
                    elif table_label.find("06") >= 0:
                        self.data_dict.update({"cEngineLoad" : channel.data})
                    elif table_label.find("28") >= 0:
                        self.data_dict.update({"cAirInletTemp" : channel.data})
                    elif table_label.find("23") >= 0:
                        self.data_dict.update({"cCACOutTemp" : channel.data})
                    elif table_label.find("22") >= 0:
                        self.data_dict.update({"cCoolantTemp" : channel.data})
                    elif table_label.find("24") >= 0:
                        self.data_dict.update({"cFuelTemp" : channel.data})

                    #else:
                        #print "ignoring %s" %(table_label)
            
            elif (group == 'Temperatures') or (group == 'Pressures') :
                
                for channel in self.tdmsfile.group_channels(group):
                    label = channel.path.split('/')
                    group_label = label[-2]
                    group_label = group_label.replace("'","")[0:1]
                    group_label = group_label.lower()
                    
                    l = label[-1]
                    l = self.__clean_channel_name(group, l)
                    
                    table_label = group_label + l

                    if table_label.find("Timestamp") <= 0:
                        self.data_dict.update({table_label : channel.data})
                    
                            
#Quick Test 
#t = drivetdms("c:/appReview/AOF.tdms")
#print(t.data_dict)
