import sys
import os
import ntwork
import configparser
import requests
import codecs
import logging
import nltk
from datetime import date

os.environ['NTWORK_LOG'] = "ERROR"

# 配置日志记录
logging.basicConfig(filename='chatbot.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# 从配置文件中读取API密钥、App ID和会话选项
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# 添加白名单配置
private_chat_whitelist = config.get('PrivateChat', 'whitelist').split(',')
group_chat_whitelist = config.get('GroupChat', 'whitelist').split(',')



conversation = config.getboolean('Conversation', 'use_common_conversation')
group_chat_ad_signature = config.get('GroupChat', 'ad_signature')
private_chat_ad_signature = config.get('PrivateChat', 'ad_signature')
group_chat_interactions_limit = config.getint('GroupChat', 'interactions_limit')
private_chat_interactions_limit = config.getint('PrivateChat', 'interactions_limit')
trigger_word = config.get('GroupChat', 'trigger_word')  # 读取触发词

group_chat_ids = []  # 用于存储群聊ID的列表
private_chat_ids = []  # 用于存储私聊ID的列表
group_chat_interactions = {}  # 用于存储群聊互动次数的字典
private_chat_interactions = {}  # 用于存储私聊互动次数的字典
group_chat_last_date = {}  # 用于存储群聊的最后交互日期的字典
private_chat_last_date = {}  # 用于存储私聊的最后交互日期的字典

# 下载nltk的数据
nltk.download('punkt')

# 上下文感知和对话管理
context = {}
conversation_id_dict = {}


def send_message(query, conversation_id=None):
    global base_url, api_key, app_id

    # SalesGPTAPI URL
    url = "http://127.0.0.1:8000/chat"
    headers = {
        "Content-Type": "application/json"
    }

    # 构建请求体
    body = {
        "human_say": query,
        "conversation_history": []
    }

    # 如果有对话历史，可以将其添加到请求体中
    if conversation_id and conversation_id in context:
        body["conversation_history"] = context[conversation_id]

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        logging.info(f"Request successful. Response status: {response.status_code}, response text: {response.text}")

        if response.status_code == 200:
            res = response.json()
            chat_reply = res.get("say")  # 从 SalesGPTAPI 的返回值中获取回复

            # 更新上下文对话内容
            if conversation_id:
                if conversation_id not in context:
                    context[conversation_id] = []
                context[conversation_id].append(f"User: {query} <END_OF_TURN>")
                context[conversation_id].append(f"SalesGPT: {chat_reply} <END_OF_TURN>")

            return {"answer": chat_reply, "conversation_id": conversation_id}

        return {"answer": "", "conversation_id": None}

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {str(e)}")
        return {"answer": "", "conversation_id": None}



def get_conversation_id(conversation_id, user_id):
    if conversation:
        conv_id = f"{conversation_id}-{user_id}"
        if conv_id not in conversation_id_dict:
            conversation_id_dict[conv_id] = None
        return conversation_id_dict[conv_id]
    else:
        return None


wework = ntwork.WeWork()
print("---------------仅支持企业微信4.0.8.6027版本---------------")
print("---------------启动程序后自动打开企业微信------------------")
wework.open(smart=True)
print("---------------等待手动登录------------------------------")
wework.wait_login()

info_data = (wework.get_self_info())
print(f"手机号码：{info_data.get('mobile')}")
print(f"用户名id：{info_data.get('user_id')}")
print(f"用户名：{info_data.get('username')}")
print("---------------机器人正常工作中---------------")



@wework.msg_register(ntwork.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wework_instance: ntwork.WeWork, message):
    global context
    data = message["data"]

    sender_user_id = data["sender"]
    self_user_id = wework_instance.get_login_info()["user_id"]
    conversation_id: str = data["conversation_id"]

    # 如果消息发送者是自己，直接返回
    if sender_user_id == self_user_id:
        return

    # 判断是群聊还是私聊
    is_group_chat = conversation_id.startswith("R:")
    if is_group_chat:
        conv_id = f"{conversation_id}-{sender_user_id}"  # 组合群ID和用户ID来生成会话ID
    else:
        conv_id = conversation_id

    # 更新互动次数和最后交互日期
    if is_group_chat:
        interactions = group_chat_interactions
        last_date = group_chat_last_date
        interactions_limit = group_chat_interactions_limit
        ad_signature = group_chat_ad_signature
    else:
        interactions = private_chat_interactions
        last_date = private_chat_last_date
        interactions_limit = private_chat_interactions_limit
        ad_signature = private_chat_ad_signature

    today = date.today()
    if conv_id not in interactions:
        interactions[conv_id] = 0
        last_date[conv_id] = today
    else:
        if last_date[conv_id] != today:
            interactions[conv_id] = 0
            last_date[conv_id] = today

    if interactions[conv_id] >= interactions_limit:
        reply_msg = "已达到每日限制，明天再试。"
        if is_group_chat:
            wework_instance.send_room_at_msg(conversation_id=conversation_id, content=reply_msg, at_list=[sender_user_id])
        else:
            wework_instance.send_text(conversation_id=conversation_id, content=reply_msg)
        return

    interactions[conv_id] += 1

    content = data['content']
    if len(content) < 200:
        content_dict = send_message(query=content, conversation_id=conv_id)
    else:
        content_dict = {"answer": "请发送少于200个字符的消息。", "conversation_id": None}

    print(f'回复 content_dict: {content_dict}')

    if content_dict["answer"] != "":
        reply_content = f'{content_dict["answer"]}{ad_signature}'
        try:
            if is_group_chat:
                wework_instance.send_room_at_msg(conversation_id=conversation_id, content=reply_content, at_list=[sender_user_id])
            else:
                wework_instance.send_text(conversation_id=conversation_id, content=reply_content)
        except Exception as e:
            logging.error(f'发送回复时出错: {str(e)}')



if __name__ == '__main__':
    try:
        while True:
            pass
    except KeyboardInterrupt:
        ntwork.exit_()
        sys.exit()