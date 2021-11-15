import time
import requests
#填写预约相关信息
脚本执行时间="0630"#图书馆6点30开始允许预约
预约开始时间="2120"
预约结束时间="2200"
座位号=""#另说
账号=""#图书馆系统的账号密码
密码=""

#格式
#脚本执行时间,开始时间和结束时间 "1040" "2200" String
#座位号 "115786429" String
#账号 密码都是String

def main():
    活阻塞到可预约时间()
    预约函数(预约开始时间,预约结束时间,座位号,获取登录cookie(账号,密码))


def 获取登录cookie(账号,密码):
    try:
            登录url = "http://self_service.lib.cnu.edu.cn/ClientWeb/pro/ajax/login.aspx"
            登录头 = { 'Content-Type': 'application/x-www-form-urlencoded'}
            登录信息='id='+账号+'&pwd='+密码+'&act=login'
            登录响应 = requests.request("POST", 登录url, headers=登录头, data=登录信息)
            return 登录响应.cookies
    except:
        print("登录函数出错")


def 预约函数(开始时间,结束时间,座位号,登录成功的cookie):
        t=time.gmtime()
        日=str(time.strftime("%Y-%m-%d+",t))
        开始时间1=日+开始时间[0:2]+"%3A"+开始时间[2:4]
        结束时间1=日+结束时间[0:2]+"%3A"+结束时间[2:4]
        url = "http://self_service.lib.cnu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dialogid=&dev_id="+座位号+"&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&number=&test_name=0&start="+开始时间1+"&end="+结束时间1+"&start_time="+开始时间+"&end_time="+结束时间+"&up_file=&memo=&act=set_resv"
        try:
            response = requests.request("GET", url,cookies=登录成功的cookie, data={})
            if(response.json()["msg"]=="操作成功！"):
                print("预约执行成功")
            else:
                print("预约失败,服务器消息:\n"+response.json()["msg"])
        except:
            print("预约函数执行出错")


def 活阻塞到可预约时间():
    while 1:
        time_now = time.strftime("%H%M", time.localtime()) 
        if time_now == 脚本执行时间 : # 设置要执行的时间
            print("时间已到，退出阻塞程序")
            return
        print("现在是 "+time_now+" ,程序仍在执行中")        
        time.sleep(30)

if __name__=="__main__" :
    main()