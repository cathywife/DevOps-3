# -*- coding:utf-8 -*-
from mns.account import Account
from mns.topic import DirectSMSInfo, TopicMessage, MNSExceptionBase
import sys

AccessId = "******"
AccessKey = "******"
MNSEndpoint = "http://******.mns.cn-beijing.aliyuncs.com"
sign_name = "******"
template_name = "******"
recv_phone = "******"
monitor_params = {
    "hostname": "web",
    "resource": "cpu",
    "details": "CpuLoad"
}

my_account = Account(MNSEndpoint, AccessId, AccessKey)
my_topic = my_account.get_topic("sms.topic-cn-beijing")
msg_body = "sms-message."

sms = DirectSMSInfo(free_sign_name=sign_name,
    template_code=template_name, single=False)
sms.add_receiver(receiver=recv_phone, params=monitor_params)

msg = TopicMessage(msg_body, direct_sms=sms)

try:
    re_msg = my_topic.publish_message(msg)
    print "Publish Message Succeed.MessageBody:%s MessageID: %s" % (msg_body, re_msg.message_id)
except MNSExceptionBase, e:
    if e.typem == "TopicNotExist":
        print "Topic not exist, please create it."
        sys.exit(1)
    print "Publish Message Fail. Exception:%s" % e
