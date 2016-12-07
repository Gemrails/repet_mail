#!/usr/bin/python
#coding=utf-8

import imaplib
import email
import ConstArgv as ca

from sendmail import SendMail
import re

_Debug = True

def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def my_unicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)

class ImapMail(object):

    def __init__(self):
        self.conn = imaplib.IMAP4_SSL(host=ca.IMAPHOST, port=993)
        self.conn.login(ca.USERNAME, ca.PASSWD)
        select_status, self.data = self.conn.select('INBOX')

    def _get_login_status(self):
        if self.conn.login(ca.USERNAME, ca.PASSWD) == 'OK':
            return self.conn
        return 1

    def _get_box_list(self):
        return self.conn.list()

    def _select_box(self):
        rc = self.conn.select('INBOX')
        if _Debug:
            print rc
        return self.conn.select('INBOX')

    def extract_body(self, payload):
        if isinstance(payload,str):
            return payload
        else:
            return '\n'.join([extract_body(part.get_payload()) for part in payload])

    def get_from(self):
        '''
            取最新15封邮件
        '''
        last_ten = int(self._select_box()[1][0])
        typ, data = self.conn.search(None, 'ALL')
        _list = data[0].split()[(last_ten - 15):]

        try:
            for num in _list[::-1]:
                typ, msg_data = self.conn.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        subject = email.Header.decode_header(msg['subject'])
                        to_me = email.Header.decode_header(msg['To'])
                        usubject = my_unicode(subject[0][0], subject[0][1])
                        #status_fetch, self.body = self.conn.fetch(self.data[0], '(UID BODY[TEXT])')
                        self.body = extract_body(msg.get_payload())
                        if _Debug:
                            print usubject
                        uto = my_unicode(to_me[0][0], to_me[0][1])

                        #if '上线邮件'.decode(encoding='utf-8') in usubject and ('崔斌'.decode(encoding='utf-8') in uto or 'cuibin'.decode(encoding='utf-8') in uto):
                        if '上线邮件'.decode(encoding='utf-8') in usubject:
                            print "start to repet."
                            mail_from = msg['From']
                            #Cc = "develop@dongqiudi.com"
                            Cc = "cuibin@dongqiudi.com"
                            sm = SendMail()
                            print self.body
                            rc = sm._send_mail(mail_from, Cc, usubject, self.body)
                            if _Debug:
                                print type(mail_from)
                                print "rc, %d" % rc
                                #print body
                            return rc

                typ, response = self.conn.store(num, '+FLAGS', r'(\Seen)')
                print response
        finally:
            try:
                print "fina"
                self.conn.close()
            except:
                print "----"
                pass
                self.conn.logout()


    def close_conn(self):
        return self.conn.close()

    def logout(self):
        return self.conn.logout()

if __name__ == '__main__':
    im = ImapMail()
    im.get_from()