import time
import re
import requests
import datetime
#填写预约相关信息
脚本执行时间="0630"
预约开始时间="0900"
预约结束时间="2200"
座位号=''
账号=""
密码=""
宽带账号=""
宽带密码=""

#格式
#脚本执行时间,开始时间和结束时间 "1040" "2200" String
#座位号 "115786429" String
#账号 密码都是String

#全局变量


def main():
    
    活阻塞到可预约时间()
    wifi登录()
    预约函数(预约开始时间,预约结束时间,座位号,获取登录cookie(账号,密码))
    活阻塞到即将超时时间(预约开始时间)
    


def 获取登录cookie(账号,密码):
    try:
            登录url = "http://self_service.lib.cnu.edu.cn/ClientWeb/pro/ajax/login.aspx"
            登录头 = { 'Content-Type': 'application/x-www-form-urlencoded'}
            登录信息='id='+账号+'&pwd='+密码+'&act=login'
            登录响应 = requests.request("POST", 登录url, headers=登录头, data=登录信息)
            print("登录函数执行完成,响应信息"+登录响应.text)
            return 登录响应.cookies

    except:
        print("登录函数出错")
        input()




def 预约函数(开始时间,结束时间,座位号,登录成功的cookie):
        t=time.gmtime()
        日=str(time.strftime("%Y-%m-%d+",t))
        开始时间1=日+开始时间[0:2]+"%3A"+开始时间[2:4]
        结束时间1=日+结束时间[0:2]+"%3A"+结束时间[2:4]
        url = "http://self_service.lib.cnu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dialogid=&dev_id="+座位号+"&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&number=&test_name=0&start="+开始时间1+"&end="+结束时间1+"&start_time="+开始时间+"&end_time="+结束时间+"&up_file=&memo=&act=set_resv"
        try:
            response = requests.request("GET", url,cookies=登录成功的cookie, data={})
            if(response.json()["msg"]=="操作成功！"):
                print("预约执行成功,服务器消息:"+response.json()["msg"])
            else:
                print("预约失败,服务器消息:\n"+response.json()["msg"])
                input()
        except:
            print("预约函数执行出错")
            input()


def 活阻塞到可预约时间():
    print("进入阻塞程序，执行时间："+脚本执行时间)
    while 1:
        time_now = time.strftime("%H%M", time.localtime()) 
        if int(time_now) >= int(脚本执行时间) : # 设置要执行的时间
            print("时间已到，退出阻塞程序")
            return
        #print("现在是 "+time_now+" ,程序仍在执行中")        
        time.sleep(30)

def 取消预约(预约号):
    登录成功的cookie=获取登录cookie(账号,密码)
    url="http://self_service.lib.cnu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?act=del_resv&id="+预约号
    response = requests.request("GET", url,cookies=登录成功的cookie, data={})
    print("取消预约函数完成，response为 "+response.text)

def 获取预约座位号和时间列表(cookies1):
    url="http://self_service.lib.cnu.edu.cn/ClientWeb/pro/ajax/center.aspx?act=get_History_resv&strat=90&StatFlag=New"
    response=requests.request("GET",url,cookies=cookies1)
    reget=re.findall(r"rsvId='(\d+)'",response.text,re.M|re.I)
    # for i in reget:
    #      print(i)
    print(len(reget))
    if(len(reget)>1 or len(reget)==0) :
            print("预约列表大于1或等于0，请检查")
            input()
            return "0"
    else: 
        print("获取预约列表完成,预约编号" + reget[0])
        return reget[0]


def 计算剩余时间(开始时间,结束时间):#str ，然后如果开始时间比结束时间早一个小时以上就返回0，否则返回1
    开始时间date=datetime.datetime.strptime(开始时间, "%H%M")
    结束时间date=datetime.datetime.strptime(结束时间, "%H%M")
    剩余时间=结束时间date-开始时间date
    print("计算剩余时间完成，结果为："+str(剩余时间.total_seconds()>=3000))
    return 剩余时间.total_seconds()>=3000


def 活阻塞到即将超时时间(开始时间):
    目标时间=datetime.datetime.strptime(开始时间, "%H%M")-datetime.timedelta(minutes=35)
    目标时间str = 目标时间.strftime("%H%M")
    下一个开始时间=datetime.datetime.strptime(开始时间, "%H%M")+datetime.timedelta(minutes=30)
    下一个开始时间str=下一个开始时间.strftime("%H%M")
    print("下次超时重新预约时间为"+目标时间str)
    while 1:
        time_now = time.strftime("%H%M", time.localtime()) 
        if int(time_now) >= int(目标时间str) : # 设置要执行的时间
            print("时间已到，退出阻塞程序")
            wifi登录()
            A=获取登录cookie(账号,密码)
            取消预约(获取预约座位号和时间列表(A))
            if(计算剩余时间(下一个开始时间str,预约结束时间)):
                预约函数(下一个开始时间str,预约结束时间,座位号,A)
                活阻塞到即将超时时间(下一个开始时间str)
                return
            else:
                return
            
            return
        #print("现在是 "+time_now+" ,程序仍在执行中")        
        time.sleep(30)

def wifi登录():
    try:
        url="http://192.168.1.91/drcom/login?callback=dr1636773843646&DDDDD="+宽带账号+"&upass="+宽带密码+"&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip=&_=1636773833286"
        requests.request("GET",url)

    except:
        None
    print("wifi登录执行完成")

if __name__=="__main__" :
    main()

