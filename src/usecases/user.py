import datetime
import re
class UCUser:

    def welcome_user(self,message):
        user = message.from_user.first_name
        timestamp = message.date
        date = datetime.datetime.fromtimestamp(timestamp)
        hour = date.hour
        if hour >= 5 and hour < 12:
            greetings = "Bom dia,"
        elif hour >= 12 and hour < 18:
            greetings = "Boa tarde,"
        else:
            greetings = "Boa noite,"

        text = ""
        if user:
            text = f"Ola {user}, {greetings} Tudo bem?\nPor qual opção você prefere validar seu acesso?" \
                   f"\n/email - Para validar por email" \
                   f"\n/codigo_compra - Para validar com o código da compra"

        return text
