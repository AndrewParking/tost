import random
import string
from datetime import datetime
from celery import shared_task
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Account, ConfirmationLink


@shared_task
def send_login_email(id):
	user = Account.objects.get(pk=id)
	subject, from_email, to_email = 'Logging_in', 'popow.andrej2009@gmail.com', user.email
	html_content = render_to_string('account/login_email.html', {
		'user': user,
		'now': datetime.now(),
	})
	text_content = strip_tags(html_content)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
	msg.attach_alternative(html_content, 'text/html')
	msg.send()


@shared_task
def send_account_change_email(id, changed_data):
	user = Account.objects.get(pk=id)
	subject, from_email, to_email = 'Account data changed', 'popow.andrej2009@gmail.com', user.email
	changes_list = ['%s is now %s' % (key, changed_data[key]) for key in changed_data]
	changes = ', '.join(changes_list)
	html_content = render_to_string('account/account_change_email.html', {
		'user': user,
		'now': datetime.now(),
		'changes': changes,
	})
	text_content = strip_tags(html_content)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
	msg.attach_alternative(html_content, 'text/html')
	msg.send()


@shared_task
def send_verification_email(id):
	user = Account.objects.get(pk=id)
	subject, from_email, to_email = 'Verification', 'popow.andrej2009@gmail.com', user.email
	link = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	fin_link = reverse('account:verification') + '?link=' + link
	ConfirmationLink.objects.create(account=user, value=link)
	html_content = render_to_string('account/verification_email.html', {
		'user': user,
		'now': datetime.now(),
		'link': fin_link,
	})
	text_content = strip_tags(html_content)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
	msg.attach_alternative(html_content, 'text/html')
	msg.send()

