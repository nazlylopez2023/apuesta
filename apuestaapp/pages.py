import random

from otree.api import  Page
from .models import C



class Choice1(Page):
    form_model = 'player'
    form_fields = ['choice', 'bet_percentage']

    def is_displayed(self):
        return self.player.round_number <= C.NUM_ROUNDS

    def before_next_page(self):
        self.player.generate_winning_choice()
        self.player.update_endowment()
        self.player.save_round_result()
        #self.player.choice


    def vars_for_template(self):
        return {
            'tokens_disponibles': C.initial_endowment,
        }
class Results1(Page):
    def is_displayed(self):
        return self.player.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        participant = self.participant
        round_results = participant.vars.get('round_results', [])
        #round_results accede al diccionario (vars) de las variables de los participantes definido en models.py
        #el diccionario vars se usa para almacenar los datos específicos del participante que no están directamente relacionados
        #con el modelo de la base de datos del experimento. [] implica que va a devolver una lista de resultados vacía
        #si no hay un valor asociado a round_results. O sea, si no hay resultados.Esta línea de código funciona para recuperar
        #la lista de resultados que se van obteniendo en las rondas que van siendo guardados en el diccionario vars.

        random_results = random.sample(round_results, 4) if len(round_results) >=4 else round_results
        #una expresión condicional que se usa para seleccionar 4 elementos al azar de la lista round_results
        #Si la longitud (len) de round_results es mayor o igual a 4, de los contrario si la longitud es menor que 4
        #entonces se van a entregar todas las rondas de resultados disponibles.
        #random.sample se usa para seleccionar los 4 elementos al azar

        total_earnings = sum(result['earnings'] for result in random_results)
        #[] se usa para para indicar que se está creando una lista con los elementos producidos por la compresión de lista
        #La compresión de lista se usa para crear listas. En este caso, ara sumar las ganancias del jugador en las 4 rondas

        return {
            'round_results': random_results,
            'total_earnings': total_earnings
        }


page_sequence = [Choice1,
                 Results1,
                 ]

