from errno import ESTALE


class Block:
    SQUARE = 1  # constant
    TRIANGLE = 2
    TABLE = 3

    def __init__(self, type, id):
        self.type = type
        self.id = id
        self.on = None
        if not (type == 2):
            self.clear = True
        else:
            self.clear = False
        self.air = False

    # place self block onto onto block
    def place(self, onto):

        if self.on:
            self.on.clear() #it is no longer placed on the previous block
        self.on = onto  
        if not onto.id == 'table': #The table is always clear
            self.on.unclear() #make sure the onto block in unclear after the action
            #print(f"{self.on} is clear: {self.on.clear}")


    # set the block to not clear
    def unclear(self):
        self.clear = False

    # set the block to clear
    def clear(self):
        self.clear = True

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        try:
            return self.id == other.id
        except Exception:
            return False