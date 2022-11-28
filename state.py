from scene import Scene
from block import Block


class State:

    def __init__(self):
        self.blocks = []

    @staticmethod
    def find(state, id):
        """
        find the block.Block object based on ID
        :param state: list of blocks
        :param id: Name of the block
        :return: block.Block object if it exists
                 else None
        """
        return next((item for item in state
                     if item.id == id), None)

    def format_args(expr):
        i_open = expr.find('(')
        i_close = expr.find(')')

        arguments = expr[i_open + 1: i_close].replace(' ', '').split(',')

        args = [f'"{arg}"' for arg in arguments]
        args = "(" + ",".join(args) + ")"

        #print(f"{expr[:i_open]}{args}")

        return f"{expr[:i_open]}{args}"

        #print(expr[i_open + 1: i_close].replace(' ', '').split(','))
        #print("")

    @staticmethod
    def display(blocks, message=""):
        print ("\n")
        print("******************")
        print(message)
        print("******************")
        print((str(Scene(blocks))))

    def square(self, id):
        # check if id exists in blocks
        if not id in self.blocks:
            block = Block(Block.SQUARE, id)
            self.blocks.append(block)

    def triangle(self, id):
        # check if id exists in blocks
        if not id in self.blocks:
            block = Block(Block.TRIANGLE, id)
            self.blocks.append(block)

    def on(self, id1, id2):
        try:
            # retrieve id
            block = self.find(self.blocks, id1)

            # retrieve table
            onto_block = self.find(self.blocks, id2)

            if block:
                block.place(onto_block)
            else:
                print (f"Blocks {id1, id2} are not defined")

        except TypeError:
            raise ValueError(f"There is a problem with the state on{id1, id2}")


    def create_state_from_file(self, filename="input.txt"):

        table = Block(Block.TABLE, "table")
        self.blocks.append(table)

        for line in open(filename).readlines():
            line = line.strip()
            if line:
                line = State.format_args(line)
                exec(f"self.{line}")

        return self.blocks



