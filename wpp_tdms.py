from nptdms import tdms

class wpptdms(object):
    
    def __init__(self, tdpath):
        self.tdmspath = tdpath
        self.tdmsfile = tdms.TdmsFile(self.tdmspath)
        self.mL = {}
        self.build_channels(self)
    
    def clean_channel_name(self, group, ch_in):
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
        
    def build_channels(self):
        self.mL = {}
        for group in self.tdmsfile.groups():
            if group == 'CAN 1':
                for channel in self.tdmsfile.group_channels(group):
                    
                        label = channel.path.split('/')
                        group_label = label[-2]
                        group_label = group_label.replace("'","")[0:1]
                        
                        l = label[-1]
                        l = self.clean_channel_name(self, group, l)
                        
                        table_label = group_label + l
                        table_label = l
                        
                        if table_label.find("Timestamp") >= 0:
                            self.mL.update({table_label : channel.data})
                        elif table_label.find("04") >= 0:
                            self.mL.update({"cEngineRPM" : channel.data})
                        elif table_label.find("06") >= 0:
                            self.mL.update({"cEngineLoad" : channel.data})
                        elif table_label.find("28") >= 0:
                            self.mL.update({"cAirInletTemp" : channel.data})
                        elif table_label.find("23") >= 0:
                            self.mL.update({"cCACOutTemp" : channel.data})
                        elif table_label.find("22") >= 0:
                            self.mL.update({"cCoolantTemp" : channel.data})
                        #else:
                            #print "ignoring %s" %(table_label)
            
            elif group == 'Temperatures':
                for channel in self.tdmsfile.group_channels(group):
                    
                        label = channel.path.split('/')
                        group_label = label[-2]
                        group_label = group_label.replace("'","")[0:1]
                        group_label = group_label.lower()
                        
                        l = label[-1]
                        l = self.clean_channel_name(self, group, l)
                        
                        table_label = group_label + l
                        
                        if table_label.find("Ambient") >= 0:
                            self.mL.update({table_label : channel.data})

