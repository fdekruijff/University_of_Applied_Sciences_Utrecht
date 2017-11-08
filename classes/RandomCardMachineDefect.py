"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import random


class RandomCardMachineDefect:
    """ This class will randomly break a CardMachine object for demonstration purposes. """
    def __init__(self, controller, root):
        self.controller = controller
        self.root = root
        self.break_random_card_machine()

    def break_random_card_machine(self):
        """
            Function uses picks pseudo random element from list and recursively calls
            function again with TkInter function
        """
        self.controller.log("break_random_card_machine()")
        machine = random.choice(self.controller.cardMachineList)
        if machine.defect == "Defect":
            # If machine is already defect pick another one
            self.break_random_card_machine()
        else:
            self.controller.break_card_machine(machine)

        self.root.after(120000, self.break_random_card_machine)
