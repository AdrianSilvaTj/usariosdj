# Funciones extras de la aplicación 'user'

import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """ Genera un código aleatorio de letras y números """
    return ''.join(random.choice(chars) for _ in range(size))