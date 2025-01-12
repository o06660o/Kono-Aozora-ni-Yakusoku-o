from npc import NPC


class NPCUpgrade(NPC):
    def __init__(self, name):
        super().__init__(name)

    def upgrade(self, player):
        player.upgrade()
