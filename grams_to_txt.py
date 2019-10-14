import os

class data_point():
    def __init__(self, num, pressure, a_range, datasum = 0):
        self.num = num
        self.pressure = pressure
        self.peak_height_list = list(a_range)
        self.datasum = datasum

def check_file_input_func(filepath):
    #print('1 ', filepath)
    filepath = repr(filepath) #转换为python字符串，忽略转义字符
    #print('2 ', filepath)
    filepath = filepath.replace('\\', '/') #替换反斜杠'\'
    #print('3 ', filepath)
    filepath = eval(filepath) #转换为普通字符串
    #print('4 ', filepath)
    filepath = filepath.rstrip('///') #去除末尾'/'
    return filepath

def eachfile(filepath,num):
    pathdir = os.listdir(filepath) #将目录下所有文件（夹）名称，编入list
    #print(len(pathdir))
    x = 0
    child = list(range(num)) #需要遍历的文件的路径的list
    for alldir in pathdir:
        child[x] = os.path.join('%s/%s' % (filepath, alldir)) #拼接父级目录和文件（夹）名称
        #print(child[x], x)
        x = x + 1
    #print(child)
    return child


def getpressure(fstr):
    bar_l = fstr.rfind('bar') #获取压力单位'bar'位置
    pressure_num_l = fstr.rfind('-') #获取数字之前的'-'的位置
    pstr = fstr[pressure_num_l+1:bar_l] #获取数值字符串
    #print(pstr)
    if '_' in pstr: #将可能的'_'替换为'.'
        pstr = pstr.replace('_', '.')
        #print(pstr)
        pstr = pstr[:pstr.find('.')] + '.' + pstr[pstr.rfind('.')+1:]
    return pstr 

def gettemperature(fstr):
    c_l = fstr.rfind('c') #获取摄氏度'c'位置
    temp_num_l = fstr.rfind('-') #获取数字之前的'-'的位置
    pstr = fstr[temp_num_l+1:c_l] #获取数值字符串
    #print(pstr)
    if '_' in pstr: #将可能的'_'替换为'.'
        pstr = pstr.replace('_', '.')
        #print(pstr)
        pstr = pstr[:pstr.find('.')] + '.' + pstr[pstr.rfind('.')+1:]
    return pstr 

def print_data(flist, filepath):
    # for line in flist:
    #     print(line.pressure, end=' ')
    #     for i in line.peak_height_list:
    #         print(i, end=' ')
    #     print('\n')
    parent_path = os.path.dirname(filepath) #获取父级目录
    ff = open(f'{parent_path}/output.txt', 'w') #以只写方式打开
    for line in flist:
        ff.write(f'{line.pressure}') 
        for i in line.peak_height_list:
            ff.write(f' {i}')
        ff.write('\n')
    ff.close

print('请输入文件夹路径：', end=' ')
filepath = input()
filepath = check_file_input_func(filepath) #检查文件夹路径末尾是否有不合格的'\''/'
print('请输入文件数：', end=' ')
filenum = int(input())
allfiles = eachfile(filepath, filenum) #提取所有文件的路径
#print(allfiles)
dic_pster_to_num = {} #初始化查找字典
data_num = -1 #初始化总的行索引
finaldata = [] #初始化总数据列表，data_point
present_index = -1 #当前处理的行索引
for f in allfiles: #遍历所有文件
    ff = open(f, 'r')
    fname = f[f.rfind('/')+1:] #获取文件名
    #print(fname)
    get_pressure = getpressure(fname) #获得当前文件的压力
    if get_pressure in dic_pster_to_num: 
        present_index = dic_pster_to_num[get_pressure] #如果字典中有当前压力的键值对，找到对应行索引
        finaldata[present_index].datasum = finaldata[present_index].datasum + 1 #该行压力对应的元素值总索引+1
    else:
        data_num = data_num + 1 #字典中没有当前压力的键值对，总索引数+1
        dic_pster_to_num[get_pressure] = data_num #在字典中添加该键值对
        finaldata.append(data_point(data_num, get_pressure, [], 0)) #初始化该行
        present_index = data_num #当前处理的行索引为总索引数
    x = 0
    string = list(range(50))
    for line in ff: #遍历该文件每一行
        string[x] = line
        if line.find('Height', 0, 6) != -1: #找到含有‘Height’这一行
            string[x] = string[x].rstrip('\n ') #去除行尾空格和回车，一般没有
            lphstr = string[x].rfind(' ') #找到值前的空格
            phstr = string[x][lphstr:] #得到数字
            finaldata[present_index].peak_height_list.append(phstr) #添加表元素表末尾     
            break
    #print(f,' ',float(phstr))   
    ff.close() 
print_data(finaldata, filepath)