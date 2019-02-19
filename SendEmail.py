import typing

def sendEmail(msg : str=None):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        my_sender = ""
        my_pass = ""
        my_user = ""
        if self._email == None:
            my_sender = '641645560@qq.com'
            my_pass = 'kybizypkzjicbbjf'
            my_user = '641645560@qq.com'
        elif len(self._email) == 2:
            my_sender = self._email[0]    # 发件人邮箱账号
            my_pass = self._email[1]      # 发件人邮箱密码
            my_user = self._email[0]      # 收件人邮箱账号，我这边发送给自己
        elif len(self._email) == 1:
            logger.info("lack email parameter! It consists of sender address and passward.")
            return

        if msg == None:
            msg = "finish train"

        def mail():
            ret=True
            try:
                msgsend=MIMEText(msg,'plain','utf-8')
                msgsend['From']=formataddr(["wxy",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                msgsend['To']=formataddr(["name",my_user])     # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msgsend['Subject']="AllenNLP Result"         # 邮件的主题，也可以说是标题

                server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                server.sendmail(my_sender,[my_user,],msgsend.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.quit()  # 关闭连接
            except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                ret=False
            return ret

        ret=mail()
        if ret:
            logger.info("email successed")
        else:
            logger.info("email failed")