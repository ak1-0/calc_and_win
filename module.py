import tkinter as tk
from tkinter import messagebox
from random import randint

class Enemy:
    def __init__(self):
        self.health = randint(80, 120)

    def take_damage(self, damage):
        self.health -= damage
        # Убедимся, что здоровье врага не опускается ниже 0
        if self.health < 0:
            self.health = 0

    def is_defeated(self):
        # Игрок выигрывает только если здоровье врага равно 10
        return self.health == 10

    def get_attack(self):
        return randint(5, 15)  # Урон врага (можно настраивать)

class Player:
    def __init__(self):
        self.health = 100  # Начальное здоровье игрока
        self.attack_types = {
            'lite': self.get_lite_attack,
            'mid': self.get_mid_attack,
            'hard': self.get_hard_attack,
        }
        self.moves_left = 5

    def attack(self, attack_type):
        attack_value = self.attack_types[attack_type]()
        self.moves_left -= 1
        return attack_value

    def get_lite_attack(self):
        return randint(2, 5)

    def get_mid_attack(self):
        return randint(15, 25)

    def get_hard_attack(self):
        return randint(30, 40)

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Рассчитай и победи!")

        # Разделение интерфейса на две части
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Заголовок в центре сверху
        self.intro_label = tk.Label(master, text="РАССЧИТАЙ И ПОБЕДИ!", font=("Arial", 16))
        self.intro_label.pack(pady=10)

        # Левый интерфейс
        self.enemy = Enemy()
        self.player = Player()

        self.health_label = tk.Label(self.left_frame, text=f"Здоровье врага: {self.enemy.health}", font=("Arial", 14))
        self.health_label.pack()

        self.moves_label = tk.Label(self.left_frame, text=f"Осталось ходов: {self.player.moves_left}", font=("Arial", 14))
        self.moves_label.pack()

        self.attack_label = tk.Label(self.left_frame, text="Выберите тип атаки:")
        self.attack_label.pack()

        self.lite_button = tk.Button(self.left_frame, text="Lite (2-5)", command=lambda: self.make_attack('lite'))
        self.lite_button.pack(pady=5)

        self.mid_button = tk.Button(self.left_frame, text="Mid (15-25)", command=lambda: self.make_attack('mid'))
        self.mid_button.pack(pady=5)

        self.hard_button = tk.Button(self.left_frame, text="Hard (30-40)", command=lambda: self.make_attack('hard'))
        self.hard_button.pack(pady=5)

        self.result_label = tk.Label(self.left_frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Правый интерфейс
        self.player_health_label = tk.Label(self.right_frame, text=f"Здоровье игрока: {self.player.health}", font=("Arial", 14))
        self.player_health_label.pack(pady=10)

        self.explanation_label = tk.Label(self.right_frame, text="Цель игры: нанести урон врагу и выжить!", font=("Arial", 12))
        self.explanation_label.pack(pady=10)

        # Кнопка "Сыграть снова" в центре снизу
        self.reset_button = tk.Button(master, text="Сыграть снова", command=self.reset_game)
        self.reset_button.pack(pady=5)
        self.reset_button.config(state=tk.DISABLED)

    def make_attack(self, attack_type):
        attack_value = self.player.attack(attack_type)
        self.enemy.take_damage(attack_value)
        self.health_label.config(text=f"Здоровье врага: {self.enemy.health}")
        self.moves_label.config(text=f"Осталось ходов: {self.player.moves_left}")
        self.result_label.config(text=f'Вы нанесли {attack_value} урона!')

        # Проверяем победу или проигрыш
        if self.enemy.is_defeated():
            messagebox.showinfo("Победа!", "Ура! Победа за вами!")
            self.reset_button.config(state=tk.NORMAL)
            self.disable_attack_buttons()
        elif self.player.moves_left == 0:
            messagebox.showinfo("Проигрыш", "Вы не смогли победить врага.")
            self.reset_button.config(state=tk.NORMAL)
            self.disable_attack_buttons()
        else:
            self.enemy_attack()  # Враг атакует после хода игрока

    def enemy_attack(self):
        enemy_damage = self.enemy.get_attack()  # Враг наносит урон
        self.player.health -= enemy_damage  # Уменьшаем здоровье игрока
        self.player_health_label.config(text=f"Здоровье игрока: {self.player.health}")

        # Проверка на проигрыш
        if self.player.health <= 0:
            messagebox.showinfo("Проигрыш", "Враг вас победил!")
            self.reset_button.config(state=tk.NORMAL)
            self.disable_attack_buttons()

    def disable_attack_buttons(self):
        self.lite_button.config(state=tk.DISABLED)
        self.mid_button.config(state=tk.DISABLED)
        self.hard_button.config(state=tk.DISABLED)

    def reset_game(self):
        self.player = Player()
        self.enemy = Enemy()
        self.health_label.config(text=f"Здоровье врага: {self.enemy.health}")
        self.moves_label.config(text=f"Осталось ходов: {self.player.moves_left}")
        self.player_health_label.config(text=f"Здоровье игрока: {self.player.health}")
        self.result_label.config(text="")
        self.lite_button.config(state=tk.NORMAL)
        self.mid_button.config(state=tk.NORMAL)
        self.hard_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    root.mainloop()