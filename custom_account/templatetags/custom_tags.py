from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount

from django import template

register = template.Library()


@register.simple_tag
def check_email_phone(email_phone):
    if email_phone.isnumeric():
        return True
    return False


@register.filter(name='check_social_user')
def check_social_user(user):
    if user.socialaccount_set.filter(provider='facebook').exists():
        return True
    elif user.socialaccount_set.filter(provider='google').exists():
        return True
    else:
        return False


@register.simple_tag
def image_return(user):  # only one parameter
    # SocialAccount does have user as foreign key
    if user.socialaccount_set.filter(provider='facebook').exists():
        id = user.socialaccount_set.filter(provider='facebook')[0].uid

        # SocialToken does not have user as foreign key
        access_token = SocialToken.objects.filter(account__user=user, app__provider='facebook')[0]
        # use filter and [0](you need only the first token object)
        picture_url = "http://graph.facebook.com/" + id + "/picture?type=large&access_token=" + str(access_token)
        return picture_url

    if user.socialaccount_set.filter(provider='google').exists():
        extra_data = user.socialaccount_set.filter(provider='google')[0].extra_data

        picture_url = extra_data['picture']
        return picture_url


@register.filter(name='check')
def check_email_phone(email_phone):
    if email_phone.isnumeric():
        return True
    return False
