from otree.api import *
from otree.models import Session

class C(BaseConstants):
    NAME_IN_URL = 'apuestaapp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 8
    initial_endowment = 100
class Subsession(BaseSubsession):
    def app_after_this_page(self, upcoming_apps):
        if self.round_number==8:
            return 'apuestagrupo'


class Group(BaseGroup):
    pass


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
        if self.choice == self.winning_choice:
            self.earnings += self.calculate_bet()  # Ganancias si eligen "Hoja de Vida A" (quité el +)

        else:
            self.earnings -= self.calculate_bet()  # Pérdidas si eligen "Hoja de Vida B"

# Define un método para establecer las opciones ganadoras por default
    def generate_winning_choice(self):
        if self.round_number == 1:
            self.winning_choice = 'Hoja de Vida A'
        elif self.round_number == 2:
            self.winning_choice = 'Hoja de Vida B'
        elif self.round_number == 3:
            self.winning_choice = 'Hoja de Vida A'
        elif self.round_number == 4:
            self.winning_choice = 'Hoja de Vida B'
        elif self.round_number == 5:
            self.winning_choice = 'Hoja de Vida A'
        elif self.round_number == 6:
            self.winning_choice = 'Hoja de Vida B'
        elif self.round_number == 7:
            self.winning_choice = 'Hoja de Vida A'
        elif self.round_number == 8:
            self.winning_choice = 'Hoja de Vida B'

    def before_next_page(self):
        self.generate_winning_choice()
        self.bet = self.calculate_bet()
        self.save_round_result()

# Define un método para guardar los resultados de cada ronda
    def save_round_result(self):
        result = "Ganó" if self.choice == self.winning_choice else "Perdió"
        self.participant.vars.setdefault('round_results', []).append({
            'round_number': self.round_number,
            'result': result,
            'winning_choice':self.winning_choice,
            'earnings': self.earnings,
            'choice': self.choice
        })


        