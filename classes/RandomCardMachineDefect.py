"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import random


class RandomCardMachineDefect:
    def __init__(self, controller, root):
        self.controller = controller
        self.root = root
        self.break_random_card_machine()

    def break_random_card_machine(self):
        self.controller.log("break_random_card_machine()")
        machine = random.choice(self.controller.cardMachineList)
        if machine.defect == "Defect":
            self.break_random_card_machine()
        else:
            self.controller.break_card_machine(machine)

        self.root.after(120000, self.break_random_card_machine)
