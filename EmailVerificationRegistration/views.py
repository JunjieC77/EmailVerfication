from base64 import urlsafe_b64decode
import base64
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser
from verifyRegist.forms import UserRegistrationForm


# Create your views here.







def register(request):
    if request.method == 'POST':
        # 处理表单提交
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # 保存用户数据但不提交到数据库
            user = form.save(commit=False)
            # 设置密码
            user.password = form.cleaned_data['password']
            # 保存用户数据到数据库
            user.save()

            # 发送激活邮件
            subject = 'Activate Your Account'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.activation_token,
            })
            import pdb; pdb.set_trace()
            print("User ID:", user.pk)
            send_mail(subject, message, '357578704@qq.com', [user.email],)

            return redirect('registration_activation_sent')
    else:
        # 显示注册表单
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        import pdb; pdb.set_trace()
        print("UIDB64:", uidb64)
        # 解码用户ID
        uid = base64.b64decode(uidb64, '-_').decode()
        print('UID:',uid)
        #uid = base64.urlsafe_b64decode(uidb64)
        #uid = urlsafe_b64decode(uidb64).decode()
        # 通过用户ID获取用户
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, 'activation_invalid.html')

    if user is not None and token == user.activation_token:
        # 激活用户
        user.is_active = True
        user.save()
        # 自动登录用户
        #login(request, user)
        return redirect('registration_activation_complete')
    else:
        return render(request, 'activation_invalid.html')
    




def registration_activation_sent(request):
    return render(request, 'registration_activation_sent.html')

def registration_activation_complete(request):
    return render(request, 'registration_activation_complete.html')