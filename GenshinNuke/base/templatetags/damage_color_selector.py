from django.template.defaulttags import register

@register.filter
def damage_color_selector(damage_type):
    match damage_type:
        case 'ELEMENT_PYRO':
            return '#EC4923'
        case 'ELEMENT_HYDRO':
            return '#00BFFF'
        case 'ELEMENT_ANEMO':
            return '#359697'
        case 'ELEMENT_ELECTRO':
            return '#945dc4'
        case 'ELEMENT_DENDRO':
            return '#608a00'
        case 'ELEMENT_CRYO':
            return '#4682B4'        
        case 'ELEMENT_GEO':
            return '#debd6c'
        case _:
            return ''

@register.filter
def noneable(value):
    if value: return value
    return ''

@register.filter
def to_int(value):
    if value: return int(value)
    return None