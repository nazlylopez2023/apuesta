import random
from otree.api import Page, WaitPage
from .models import C

class GChoice1(Page):
    form_model = 'player'
    form_fields = ['choice', 'bet_percentage']

    def is_displayed(self):
        return self.player.round_number <= C.NUM_ROUNDS

    def before_next_page(self):
        if self.player.round_number < C.NUM_ROUNDS:
            self.group.set_winning_choice()
            self.player.update_endowment()
            self.player.save_round_result()

    def vars_for_template(self):
        return {
            'tokens_disponibles': C.initial_endowment,
        }

class WaitForOthers(WaitPage):
    def after_all_players_arrive(self):
        # Se establece la elección ganadora y se actualizan las dotaciones después de que todos los jugadores hayan hecho su elección
        self.group.set_winning_choice()
        for player in self.group.get_players():
            player.update_endowment()
            player.save_round_result()

class GResult1(Page):
    def is_displayed(self):
        return self.player.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        round_results = self.participant.vars.get('round_results', [])

        # Seleccionar 4 resultados aleatorios de las rondas anteriores, si hay al menos 4 resultados
        random_results = random.sample(round_results, 4) if len(round_results) >= 4 else round_results

        # Calcular las ganancias totales sumando las ganancias de los resultados seleccionados
        total_earnings = sum(result['earnings'] for result in random_results)

        return {
            'round_results': random_results,
            'total_earnings': total_earnings
        }

class WaitForAll(WaitPage):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def after_all_players_arrive(self):
        # Aquí puedes realizar las acciones finales después de la última ronda, si es necesario
        self.group.set_winning_choice()
        for player in self.group.get_players():
            player.update_endowment()
            player.save_round_result()


page_sequence = [GChoice1, WaitForOthers, WaitForAll, GResult1]
