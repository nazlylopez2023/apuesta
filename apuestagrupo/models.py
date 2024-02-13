from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'apuestagrupo'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 8
    initial_endowment = 100
class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == C.NUM_ROUNDS:
            return 'apuestagrupo'

    def after_all_players_arrive(self):
        self.group.count_choices()
        self.group.set_winning_choice()
class Group(BaseGroup):

    hoja_A_count = models.IntegerField(initial = 0)
    hoja_B_count = models.IntegerField(initial = 0)
    winning_choice = models.StringField()

    # Método para contar las veces que los participantes eligen las hojas de vida

    def count_choices(self):
        for player in self.get_players(): # arroja la lista de lo que hace un jugador dentro de las elecciones que los otros jugadores hacen en el grupo
            if player.choice == 'Hoja de Vida A':
                self.hoja_A_count += 1
            else:
                self.hoja_B_count += 1

    def set_winning_choice(self):
        hoja_A_count = sum(1 for player in self.get_players() if player.choice == 'Hoja de Vida A')
        hoja_B_count = sum(1 for player in self.get_players() if player.choice == 'Hoja de Vida B')

        if hoja_A_count > hoja_B_count:
            self.winning_choice = 'Hoja de Vida A'
        else:
            self.winning_choice = 'Hoja de Vida B'

    def calculate_earnings(self):
        for player in self.get_players():
            player.update_endowment()

class Player(BasePlayer):
    result = models.StringField()
    choice = models.StringField(
        choices = [
            'Hoja de Vida A',
            'Hoja de Vida B'
        ],
        label = 'Elige una hoja de vida',
        initial='Hoja de Vida A'
    )

    bet_percentage = models.IntegerField(
        min = 0,
        max = 100,
        initial = 0
    )
    earnings = models.CurrencyField(initial=0)
    bet = models.CurrencyField()  # Agrega el campo "bet" aquí
    round_number = models.IntegerField(initial=1)  # Número de ronda actual
    winning_choice = models.StringField()

   # Define un método para calcular el valor apostado en cada ronda
    def calculate_bet(self):
        return (self.bet_percentage / 100) * C.initial_endowment

# Define un método para actualizar la dotación en función de las ganancias y pérdidas
    def update_endowment(self):
        if self.choice == self.group.winning_choice:
            self.earnings += self.calculate_bet()  # Ganancias si eligen "Hoja de Vida A"
        else:
            self.earnings -= self.calculate_bet()  # Pérdidas si eligen "Hoja de Vida B"

    def before_next_page(self):
        self.bet = self.calculate_bet()
        self.group.set_winning_choice()
        self.update_endowment()
        self.save_round_result()

        # Define un método para guardar los resultados de cada ronda
    def save_round_result(self):
        result = "Ganó" if self.choice == self.group.winning_choice else "Perdió"
        self.participant.vars.setdefault('round_results', []).append({
            'round_number': self.round_number,
            'result': result,
            'winning_choice': self.group.winning_choice,
            'earnings': self.earnings,
            'choice': self.choice
        })







