import requests
import json
import time
import base64

header = {'content-type': 'application/json'}
source = 'mobile'

def getGlipBaseUrl(portID):
    glipBaseUrl= "https://aws21-g43-udp01.asialab.glip.net:" + portID
    return glipBaseUrl



def getRCToken(ENV,userName,extNum,passWord,grant_Type): #定义方法，传env,用户名，密码，认证方式
    baseUrl = ENV + "/restapi/oauth/token" #定义字符串变量
    if ENV == 'http://api-up.lab.rcch.ringcentral.com' or 'https://api-up.lab.rcch.ringcentral.com':
        rcSecurtyCode = 'TWtDZGxTVnFRMDZINmk3S1ljdjliZzo1X3RGQlhCUVRMV2FWY1BGNjFMVUdnbmdCZmM4S0dRQ2FaMF9VVHc4MHZzdw=='
    elif ENV == 'https://api.ringcentral.com':
        rcSecurtyCode = 'MDJiNzI5MTgwMDRhOWVkMzM2YjlDRUJDNDhlNjAzOGJlM2YyMTk2NDI2MjFBODA0MjA3MmY5N2MyQzg0MkZBQTpGQkQzRENBMDk5N2JFQTlCMGI4MWY4NTZlY2NiOWNkMmIxOWQ2MDYwNzc3NmE4NjFDOUM0N2RiNWVkMDU0ODcy'
    elif ENV == 'https://platform.devtest.ringcentral.com':
        rcSecurtyCode = 'TWtDZGxTVnFRMDZINmk3S1ljdjliZzo1X3RGQlhCUVRMV2FWY1BGNjFMVUdnbmdCZmM4S0dRQ2FaMF9VVHc4MHZzdw=='
    rcAuthCode = 'Basic ' + rcSecurtyCode #定义字符串变量
    payload = {'username':userName, 'password':passWord, 'extension':extNum,'grant_type':grant_Type} #定义一个json的map结构的对象（key：value）
    header = {'content-type':'application/x-www-form-urlencoded','authorization':rcAuthCode} #定义一个json的map结构的对象（key：value）
    getRCTokenresponse=requests.post(baseUrl, data= payload, headers=header) #调用api，获取请求结果
    #print(getRCTokenresponse.text) #在控制台打印请求对象结果，使用对象的文本属性
    rcTokenJsonText = getRCTokenresponse.json() #取得json结构的结果
    rcTokenText = getRCTokenresponse.text #取得文本结果
    rc_access_token_data = "";
    if getRCTokenresponse.ok: #如果请求是成功，取得acess_token, 并做base64位加密
        rc_access_token_data =str(base64.b64encode(bytes(rcTokenText,encoding="utf-8")),encoding="utf-8")
        print(rc_access_token_data)
    else:
        print("failed to get access_token, the reason is" + json.dumps(rcTokenJsonText)) #
    return rc_access_token_data




def glipLogin(rc_access_token, portID):
    baseUrl = getGlipBaseUrl(portID) + "/api/login"
    payload = {'rc_access_token_data':rc_access_token,'mobile': True, 'for_mobile': True}
    header = {'content-type':'application/json'}
    glipLoginResponse = requests.put(baseUrl,data=json.dumps(payload),headers=header)

    if glipLoginResponse.ok:
        #print(glipLoginResponse.text)
        #print( glipLoginResponse.headers)
        tk = glipLoginResponse.headers['X-Authorization']
        creator_id = glipLoginResponse.json()['user_id']
        loginUserInfo = {'tk':tk,'creator_id':creator_id} #定义数组对象，保存获取的glip token和user_id
    else:
        print("failed to get glipLoginResponse, the reason is " + glipLoginResponse.text)
    return loginUserInfo

def replyPost(tk, portID, creator_id,group_id, txtContent):
    baseUrl = getGlipBaseUrl(portID) + "/api/post"
    new_version = ''
    created_at = time.time()
    is_new = True
    version = ''
    paras = {'new_version':new_version,'source':source, 'group_id':group_id,'tk':tk, 'created_at':created_at,'creator_id':creator_id,'is_new':is_new, 'text':txtContent,'version':version}
    payload=json.dumps(paras)
    replyPost = requests.post(baseUrl,data=payload, headers=header)
    #print(replyPost.json())
    #print(replyPost.status_code)
    if replyPost.ok:
        print('The Sent Text is: ' )
        print(txtContent)
    else:
        print('Failed to reply post, the status code is ' + str(replyPost.status_code))
    return

def createTask(tk, portID, creator_id,group_ids, messageCount,text):
    baseUrl = getGlipBaseUrl(portID) + "/api/task"
    complete_type = 'boolean'
    start = 0
    section = ''
    version = ''
    created_at = 1493964645503
    repeat =''
    color = ''
    notes = ''
    is_new = True
    has_due_time = False
    complete = False
    assigned_to_ids = []
    due = 0
    new_version = 2871284691396310
    paras = { 'complete_type': complete_type, 'start': start,'tk': tk, 'section': section,'version': version,'group_ids': group_ids,'created_at': created_at,'repeat': repeat,'source': source,'color': color,'notes': notes,'text': text,'creator_id': creator_id,'is_new': is_new,'has_due_time': has_due_time,'complete': complete,'assigned_to_ids': assigned_to_ids,'due': due,'new_version': new_version}
    payload=json.dumps(paras)
    createTask = requests.post(baseUrl,data=payload, headers=header)
    if createTask.ok:
        print('The new task is: ' )
        print(text)
    else:
        print('Failed to create task, the status code is ' + str(createTask.status_code))
    return

def createEvent(tk, portID, creator_id,group_id,messageCount,text):
    baseUrl = getGlipBaseUrl(portID) + "/api/event"
    description = ''
    start = 1489467646000
    invitee_ids =[]
    version = 1489467348596
    created_at = 1489467348596
    repeat = 'none'
    color = ''
    location = ''
    type_id = 14
    end = 1489471246000
    new_version = ''
    paras = {'description':description,'start':start,'tk':tk,'invitee_ids':invitee_ids,'version':version,'group_ids':group_id,'created_at':created_at,'repeat':'repeat','source':'source','color':color,'all_day':False,'location':location,'text':text,'type_id':type_id,'creator_id':creator_id,'end':end,'is_new':True,'new_version':new_version}
    payload=json.dumps(paras)
    createEvent = requests.post(baseUrl,data=payload, headers=header)
    if createEvent.ok:
        print('The new event is: ' )
        print(text)
    else:
        print('Failed to create event, the status code is ' + str(createEvent.status_code))
    return

def createNote(tk, portID, creator_id,group_id, messageCount,title):
    baseUrl = getGlipBaseUrl(portID) + "/api/page"
    body = 'Note text content'+str(time.time())
    version = ''
    created_at = ''
    new_version = ''
    paras = {'body':body,'tk':tk,'version':version,'group_ids':group_id,'created_at':created_at,'source':source,'title':title,'is_draft':False,'creator_id':creator_id,'is_new':True,'no_post':False,'new_version':new_version}
    payload=json.dumps(paras)
    createNote = requests.post(baseUrl,data=payload, headers=header)
    if createNote.ok:
        print('The new Note is: ' )
        print(title)
    else:
        print('Failed to create Note, the status code is ' + str(createNote.status_code))
    return

def createTeam(tk, portID, creator_id,email_friendly_abbreviation,members,set_abbreviation,messageCount,type):
    baseUrl = getGlipBaseUrl(portID) +"/api/team"
    is_new = True
    is_public =False
    is_privacy = "private"
    is_team = True
    new_version = ''
    _csrf = 0
    paras = {'creator_id': creator_id, 'is_new': is_new, 'email_friendly_abbreviation': email_friendly_abbreviation, 'members': members, 'is_public': is_public, 'privacy': is_privacy, 'is_team': is_team, 'set_abbreviation': set_abbreviation, 'new_version': new_version, '_csrf': 0, 'tk': tk}
    payload=json.dumps(paras)
    createTeamResonse = requests.post(baseUrl,data=payload, headers=header)
    #print(createTeamResonse.json())
    #print(createTeamResonse.status_code)19701766

    if createTeamResonse.ok:
        print('Created Team Name is: ')
        print(set_abbreviation)
        data = createTeamResonse.json();
        if type == 'post' or type == 'Post':
            teamId = data['_id'] #传一个字符串对象
            for index in range(0, messageCount):
                replyPost(tk,portID, creator_id,teamId,'repiedtestToday_' + str(index))
        elif type == 'task' or type == 'Task':
            group_ids = [data['_id']] #数据格式为数组，
            tCreator_id = data['creator_id']
            for index in range(0, messageCount):
                text = 'Task' + str(index)
                createTask(tk, portID, tCreator_id,group_ids,messageCount,text)
        elif type == 'event' or type == 'Event':
            group_ids = [data['_id']]
            tCreator_id = data['creator_id']
            for index in range(0, messageCount):
                text = 'Event'+ str(index)
                createEvent(tk, portID, tCreator_id,group_ids, messageCount,text)
        elif type == 'note' or type == 'Note':
            group_ids = [data['_id']]
            tCreator_id = data['creator_id']
            for index in range(0, messageCount):
                title = 'Note' + str(index)
                createNote(tk, portID, tCreator_id,group_ids,messageCount,title)
    else:
        print('Failed to create team, the status_code is' +str(createTeamResonse.status_code))
    return




def run(ENV,userName,extNum,passWord,portID, createTeamCount,messageCount,type):
    rc_access_token = getRCToken(ENV,userName,extNum,passWord,'password')
    glip_token = glipLogin(rc_access_token, portID)
    #teamName = "AdelaTeam"+str(time.time())+"_No."
    teamName = "aaa"+"_No."
    for index in range(0, createTeamCount):
        members = [glip_token['creator_id'], 241090562 + index]
        createTeam(glip_token['tk'],portID, glip_token['creator_id'], teamName + str(index), members, teamName + str(index),messageCount,type)
        time.sleep(0.15)


run('https://platform.devtest.ringcentral.com','18582571753','101','Test!123','32004',1,1, 'task')
#run('http://api-up.lab.rcch.ringcentral.com','18003396668','102','Test!123','23304',50,50, 'task')
