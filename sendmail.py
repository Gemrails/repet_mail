#!/usr/bin/python
#coding=utf-8

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import ConstArgv as ca
import base64

_Debug = True

class SendMail(object):

    def __init__(self):
        self.ca = ca
        self.conn = smtplib.SMTP_SSL(host=ca.SMTPHOST, port=465)
        login_rc = self._loginsmtp()

    def _loginsmtp(self):
        return self.conn.login(ca.USERNAME, ca.PASSWD)

    def __format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def close_conn(self):
        return self.conn.close()

    def _send_mail(self, to, cc, subj, oldcontent):

        try:
            content = base64.decodestring(oldcontent)
            msg = MIMEText("发布完成\n\n" + "------------------ 原始邮件 ------------------\n\n" + content, 'plain', 'utf-8')
            msg['From'] = self.__format_addr(u'<%s>' % self.ca.USERNAME)
            #msg['To'] = self.__format_addr('%s' % to)
            msg['To'] = to
            msg['Cc'] = self.__format_addr(u'<%s>' % cc)
            msg['Subject'] = subj

            if _Debug:
                print msg['To']
                print "start to send Email"


            #exit()
            tye =  self.conn.sendmail(ca.USERNAME, [to], msg.as_string())

            self.close_conn()
            return 0
        except smtplib.SMTPConnectError, e:
            errmsg = "class SendMail err: %s" % e
            if _Debug:
                print errmsg
            return 1

if __name__ == '__main__':
    sm = SendMail()
    sm._send_mail('cuibin@dongqiudi.com', 'cuibin@dongqiudi.com', u'Re: 12月上线邮件')