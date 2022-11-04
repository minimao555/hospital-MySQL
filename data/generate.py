import random
import csv
import base64
sexList = ["男","女"]
officeList = "内科、外科、儿科、妇科、眼科、耳鼻喉科、口腔科、皮肤科、中医科、针灸推拿科".split('、')
doctorList = list() #doctorId+office
patientList = list() #patientID+name
headDoctorList = list() #id
prescriptionList = list() #paymentID+patientID
registrationList = list() #paymentID+patientID
inspectionList = list() #paymentID+patientID
medicalRecordsList = list() #medicalRecordsID+patientID+name

def generate_name(sex):
    lastNameList = "赵 钱 孙 李 周 吴 郑 王 贾 路 娄 危 江 童 颜 郭 冯 陈 褚 卫 蒋 沈 韩 杨".split(' ')
    manFirstNameList = "益嘉、远尚、方伟、灿瑜、峻尚、哲铭、峻野、顺钧、峰瑜、乐轩、彬义、晟宸、伯泽、志睿、智靖、轩雷、方华、晨铭、展楠、凯珺、少仁、轩祥、少华、文豪、川豪、卓霖、鸿月、堇文、铭智、伦乾、泰鸿、祟名、超瑾".split('、')
    womanFirstNameList = "凤柔、新怡、纹华、秋柔、妙雪、翠微、晴岚、依莹、纹娜、书雪、雁卉、万云、晓玉、凝雁、向珊、云灵、忆香、甜悠、水惠、甜巧、珊花、黛玉、柏晴、寻芹、紫怡、香蝶、云芳、碧桃、欣雅、书倚、夏青、语凤、香薇、新巧、惜霜、芳菲、馨蕊、佳怡、菲颖、依叶、诗柳、谷菱、香柏、初瑶、惜纹、涵蕾".split('、')
    name = ""
    name += lastNameList[random.randint(0,len(lastNameList) - 1)]
    if(not sex):
        name += manFirstNameList[random.randint(0,len(manFirstNameList) - 1)]
    else:
        name += womanFirstNameList[random.randint(0,len(womanFirstNameList) - 1)]
    return name

def generate_num(length):
    num = ""
    for i in range(length):
        num += str(random.randint(0,9))
    return num

def generate_ID(firstChar,length):
    return firstChar + generate_num(length)

def generate_phone():
    isPersonal = random.randint(0,1)
    if(isPersonal):
        return '1' + generate_num(10)
    else:
        return generate_num(random.randint(3,4)) + '-' + generate_num(random.randint(7,8))

def generate_txt(index,patientName):
    txt = ''
    which = ['病人描述','诊断','治疗方案','处方单内容','检查结果','检查分析']
    symptomList = "呕吐 头晕 恶心 发烧 四肢无力 食欲不振 出虚汗 腹泻 牙床出血 体重下降 面色苍白 嗓子疼 皮疹 头疼 咳嗽".split(' ')
    timeList = "昨天 最近一周 最近一个月 这几年 前天 早晨 中午 晚上 饭后 起床后".split(' ')
    diseaseList = "糖尿病 甲状腺疾病 痛风 癫痫 阿尔兹海默症 脑梗死 先天性心脏病 心律失常 心肌炎 肺结核 肺炎 肺脓肿 哮喘 肺气肿 胃炎 胃食管反流 消化性溃疡 输尿管结石 急性膀胱炎 尿道炎".split(' ')
    medicineList = "健胃消食片 肠炎宁 速效救心丸 藿香正气水 连花清瘟胶囊 快克 感冒冲剂 白加黑 伪麻黄碱 咖啡因 布洛芬 硫糖铝混悬液".split(' ')
    treatmentList = "预防继发感染 监测血常规 保证充分的能量摄入 呼吸支持 卧床休息 抗病毒治疗 糖皮质激素治疗".split(' ')
    if(which[index] == '病人描述'):
        for i in range(random.randint(1,6)):
            txt += '我' + timeList[random.randint(0,len(timeList) - 1)] + '感到' + symptomList[random.randint(0,len(symptomList) - 1)] + '。'
    elif(which[index] == '诊断'):
        for i in range(random.randint(1,6)):
            txt += patientName + '可能患有' + diseaseList[random.randint(0,len(diseaseList) - 1)] + '。'
    elif(which[index] == '治疗方案'):
        for i in range(random.randint(1,3)):
            txt += '进行' + treatmentList[random.randint(0,len(treatmentList) - 1)] + '。'
    elif(which[index] == '处方单内容'):
        for i in range(random.randint(1,6)):
            txt += '服用' + medicineList[random.randint(0,len(medicineList) - 1)] + '。'
    elif(which[index] == '检查结果'):
        for i in range(random.randint(1,6)):
            txt += patientName + '有' + symptomList[random.randint(0,len(symptomList) - 1)] + '。'
    else:
        for i in range(random.randint(1,6)):
            txt += patientName + '可能患有' + diseaseList[random.randint(0,len(diseaseList) - 1)] + '。'
    return txt

def generate_address():
    firstList = "斑驳、思量、迟暮、拂晓、繁花、落花、昔年、拾忆、暖心、花街、荏苒、昭然、冗长、倦怠、落拓、聒噪、叨扰、破败、漫漶、氤氲、凋敝、遒健、翩跹、轻谧、化脓、笙歌、旖旎、悱恻、绚烂、真淳".split('、')
    secondList = "明媚、迷离、深邃、灼热、幻灭、落拓、不羁、傲骨、荟萃、澄澈、资深、清灵、睿智、天籁、泰然、淡雅、彼岸、朴素、内敛、凌然、风靡、搁浅、蜕变".split('、')
    address = firstList[random.randint(0,len(firstList) - 1)] + '区-' + secondList[random.randint(0,len(secondList) - 1)] + '路-' + str(random.randint(1,300)) + '号'
    return address

def generate_time():
    data = ""
    data = str(random.randint(2002,2022)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(1,28))
    time = ""
    time = str(random.randint(1,24)) + ':' + str(random.randint(0,59)) + ':' + str(random.randint(0,59))
    return data + ' ' + time

def generate_picture(which,length):
    path = './img/' + which + '_' + str(random.randint(0,length)) + '.png'
    with open(path,"rb") as f:
        byte_data = f.read()
    base64_str = base64.b64encode(byte_data).decode("ascii")# 二进制转base64
    return base64_str

def doctor(length):
    with open('doctor.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        for i in range(length):
            oneRowList = list()
            oneRowList.append(generate_ID('D',8))
            sex = random.randint(0,1)
            oneRowList.append(generate_name(sex))
            oneRowList.append(sexList[sex])
            oneRowList.append(random.randint(0,150))
            oneRowList.append(generate_phone())
            oneRowList.append(generate_address())
            oneRowList.append(officeList[random.randint(0,len(officeList) - 1)])
            oneRowList.append(generate_picture('doctor',59))
            doctorList.append((oneRowList[0],oneRowList[6]))
            csvFile.writerow(oneRowList)
        for i in range(len(officeList)):           
            oneRowList = list()
            oneRowList.append(generate_ID('D',8))
            sex = random.randint(0,1)
            oneRowList.append(generate_name(sex))
            oneRowList.append(sexList[sex])
            oneRowList.append(random.randint(0,150))
            oneRowList.append(generate_phone())
            oneRowList.append(generate_address())
            oneRowList.append(officeList[i])
            oneRowList.append(generate_picture('doctor',59))
            headDoctorList.append((oneRowList[0]))
            csvFile.writerow(oneRowList)

def patient(length):
    with open('patient.csv','w',encoding='utf-8',newline= '') as fp:
        history = "先天性心脏病 无 糖尿病 青霉素过敏 肺结核 无 无 无".split(' ')
        csvFile = csv.writer(fp)
        for i in range(length):
            oneRowList = list()
            oneRowList.append(generate_ID('P',8))
            sex = random.randint(0,1)
            oneRowList.append(generate_name(sex))
            oneRowList.append(sexList[sex])
            oneRowList.append(random.randint(0,150))
            oneRowList.append(generate_phone())
            oneRowList.append(history[random.randint(0,len(history) - 1)])
            oneRowList.append(generate_address())
            oneRowList.append(generate_picture('patient',33))
            patientList.append((oneRowList[0],oneRowList[1]))
            csvFile.writerow(oneRowList)

def medical_records(length):
    with open('medicalRecords.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        for i in range(length):
            oneRowList = list()
            oneRowList.append(generate_ID('M',8))
            doctorIndex = random.randint(0,len(doctorList) - 1)
            patientIndex = random.randint(0,len(patientList) - 1)
            patientName = patientList[patientIndex][1]
            oneRowList.append(patientList[patientIndex][0])
            oneRowList.append(doctorList[doctorIndex][0])
            oneRowList.append(generate_txt(0,patientName))
            oneRowList.append(generate_txt(1,patientName))
            oneRowList.append(doctorList[doctorIndex][1])
            oneRowList.append(generate_txt(2,patientName))
            medicalRecordsList.append((oneRowList[0],oneRowList[1],patientName))
            csvFile.writerow(oneRowList)

def office():
    with open('office.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        for i in range(len(officeList)):
            oneRowList = list()
            oneRowList.append(officeList[i])
            oneRowList.append(headDoctorList[i])
            oneRowList.append(random.randint(20,100))
            csvFile.writerow(oneRowList)

def payment_slip(length0,length1,length2):
    with open('paymentSlip.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        item = ["处方","挂号","检查"]
        for i in range(length0):
            oneRowList = list()
            prescriptionIndex = i
            oneRowList.append(prescriptionList[prescriptionIndex][0])
            oneRowList.append(prescriptionList[prescriptionIndex][1])
            oneRowList.append(item[0])
            oneRowList.append(random.uniform(0,10000))
            oneRowList.append(generate_time())
            csvFile.writerow(oneRowList)
        for i in range(length1):
            oneRowList = list()
            registrationIndex = i
            oneRowList.append(registrationList[registrationIndex][0])
            oneRowList.append(registrationList[registrationIndex][1])
            oneRowList.append(item[1])
            oneRowList.append(random.uniform(0,10000))
            oneRowList.append(generate_time())
            csvFile.writerow(oneRowList)
        for i in range(length2):
            oneRowList = list()
            inspectionIndex = i
            oneRowList.append(inspectionList[inspectionIndex][0])
            oneRowList.append(inspectionList[inspectionIndex][1])
            oneRowList.append(item[2])
            oneRowList.append(random.uniform(0,10000))
            oneRowList.append(generate_time())
            csvFile.writerow(oneRowList)
            
            

def prescription_list(length):
    with open('prescriptionList.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        for i in range(length):
            oneRowList = list()
            oneRowList.append(generate_ID('PL',8))
            doctorIndex = random.randint(0,len(doctorList) - 1)
            patientIndex = random.randint(0,len(patientList) - 1)
            patientName = patientList[patientIndex][1]
            oneRowList.append(patientList[patientIndex][0])
            oneRowList.append(doctorList[doctorIndex][0])
            oneRowList.append(generate_ID('PS',8))
            oneRowList.append(generate_txt(3,patientName))
            prescriptionList.append((oneRowList[3],oneRowList[1]))
            csvFile.writerow(oneRowList)

def registration_slip(length):
    with open('registrationSlip.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        type = ["专家门诊","特需号","会诊"]
        for i in range(length):
            oneRowList = list()
            oneRowList.append(generate_ID('RS',8))
            doctorIndex = random.randint(0,len(doctorList) - 1)
            patientIndex = random.randint(0,len(patientList) - 1)
            oneRowList.append(patientList[patientIndex][0])
            oneRowList.append(doctorList[doctorIndex][0])
            oneRowList.append(doctorList[doctorIndex][1])
            oneRowList.append(generate_ID('PS',8))
            oneRowList.append(generate_time())
            oneRowList.append(type[random.randint(0,2)])
            registrationList.append((oneRowList[4],oneRowList[1]))
            csvFile.writerow(oneRowList)

def inspection_item(length):
    with open('inspectionItem.csv','w',encoding='utf-8',newline= '') as fp:
        csvFile = csv.writer(fp)
        inspectionName = "血常规 尿常规 便常规 肝功能 肾功能 血脂 血糖 电解质 心肌酶谱 甲状腺功能 胸片 心电图 彩超".split(' ')
        for i in range(length):
            oneRowList = list()
            oneRowList.append(generate_ID('II',8))
            oneRowList.append(inspectionName[random.randint(0,len(inspectionName) - 1)])
            medicalRecordsIndex = random.randint(0,len(medicalRecordsList) - 1)
            oneRowList.append(medicalRecordsList[medicalRecordsIndex][0])
            oneRowList.append(generate_ID('PS',8))
            patientID = medicalRecordsList[medicalRecordsIndex][1]
            patientName = medicalRecordsList[medicalRecordsIndex][2]
            oneRowList.append(generate_txt(4,patientName))
            oneRowList.append(generate_txt(5,patientName))
            oneRowList.append(generate_picture('inspection',25))
            inspectionList.append((oneRowList[3],patientID))
            csvFile.writerow(oneRowList)



doctor(50)
patient(50)
office()
medical_records(100)
prescription_list(100)
registration_slip(100)
inspection_item(100)
payment_slip(100,100,100)