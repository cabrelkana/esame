class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name
            
    def get_data(self):
            try:
                my_file = open(self.name, 'r')
            except Exception as e:
                print("Errore! File non esistente: {}".format(e))

            values = []
            my_file = open(self.name, 'r')

            while True:
                lineaFile = my_file.readline()
                
                if lineaFile!='':
                    linea = lineaFile.strip('\n').split(',')
                    if lineaFile.strip('\n')!='' and len(linea)>=2 and linea[0]!='' and linea[0]!='date' and linea[1]!='':                    
                        annoMese = linea[0].split('-')
                        if len(annoMese)==2 and annoMese[0]!='' and annoMese[1]!='' and linea[1].isnumeric()==True and annoMese[0].isnumeric()==True and annoMese[1].isnumeric()==True:
                            break
                else:
                    raise ExamException("Errore! File vuoto")
            
            primaRilevazione = []
            primaRilevazione.append(linea[0])
            primaRilevazione.append(int(linea[1]))
            values.append(primaRilevazione)
            currentYear = int(linea[0].split('-')[0])
            currentMonth = int(linea[0].split('-')[1])

            for line in my_file:
                elements = line.strip('\n').split(',')           
                annoMese = elements[0].split('-')
                
                if len(elements)>=2 and len(annoMese)==2 and elements[0] != 'date':
                    if elements[0]!='' and elements[1]!='' and elements[1].isnumeric()==True and annoMese[0].isnumeric()==True and annoMese[1].isnumeric()==True:                    
                        if int(annoMese[0])<currentYear or (int(annoMese[0])==currentYear and int(annoMese[1])<=currentMonth):
                            raise ExamException("Errore! Valori non ordinati")
                        
                        rilevazione = []
                        rilevazione.append(elements[0])
                        rilevazione.append(int(elements[1]))
                        values.append(rilevazione)
                        currentYear = int(elements[0].split('-')[0])
                        currentMonth = int(elements[0].split('-')[1])
            my_file.close()

            return values
    
def find_min_max(time_series):
    i=0
    diz = {}
    while i<len(time_series):
        dizInterno = {}
        mesiMin = []
        mesiMax = []
        mesiCounter = 0
        min = time_series[i][1]
        max = time_series[i][1]
        anno = time_series[i][0].split('-')[0]

        while i<len(time_series) and int(time_series[i][0].split('-')[0]) == int(anno):
            if time_series[i][1]<min:
                min = time_series[i][1]
                mesiMin.clear()
                mesiMin.append(time_series[i][0].split('-')[1])
            elif time_series[i][1]==min:
                mesiMin.append(time_series[i][0].split('-')[1])

            if(time_series[i][1]>max):
                max = time_series[i][1]
                mesiMax.clear()
                mesiMax.append(time_series[i][0].split('-')[1])
            elif time_series[i][1]==max:
                mesiMax.append(time_series[i][0].split('-')[1])

            i=i+1
            mesiCounter = mesiCounter+1
        
        if mesiCounter==1:
            diz[anno] = {}
        else:
            dizInterno["min"] = mesiMin
            dizInterno["max"] = mesiMax
            diz[anno] = dizInterno
    return diz
