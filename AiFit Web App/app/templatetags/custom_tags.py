from django import template
register = template.Library()

@register.filter(name='len_dic')
def len_dic(dic):
    l = len(dic.keys())
    return l
