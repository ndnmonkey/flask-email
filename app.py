from flask import Flask,render_template,g,request
from flask_mail import Mail, Message
import config
import random
from emai_content import code_to_html

app = Flask(__name__)
app.config.from_object(config)

mail = Mail(app)
#设置验证池
vercoede_pool = []

#产生email验证码
def generate_verification_code():
    while True:
        emai_key = str(random.random() * 1000000).split(".")[0]
        if emai_key[0] != 0:
            return emai_key

@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "GET":
        #最多刷新1次,因为每刷新一次都会发一条邮件，所以限制发送次数。
        if len(vercoede_pool) < 1:
            msg = Message(subject='Hello user!',  # 邮件主题
                          sender="1257266527@qq.com",  # 需要使用默认发送者则不用填
                          recipients=['smile_luffy@126.com'])  # 接受邮箱，可以多个
            # 产生6位首位不为0的验证码
            verification_code = generate_verification_code()
            print("get:",verification_code)
            vercoede_pool.append(verification_code)

            # 将验证码放入html中，当成邮件内容发送出去
            # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
            msg.body = code_to_html(verification_code)
            msg.html = code_to_html(verification_code)
            mail.send(msg)

        return render_template('index.html')
    else:
        vcoede = request.form.get("vcode")
        #填错了怎么办？
        if vcoede == vercoede_pool[-1]:  #最新发送的代码才有效，所以是[-1]。
            print(vcoede)
            vercoede_pool.pop() #输入值与最新验证码一样才能pop
            return render_template('success.html')
        else:
            return '验证码错误！'



if __name__ == '__main__':
    app.run(debug=True)
