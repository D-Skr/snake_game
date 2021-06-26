from tkinter import *
import random

# init global vars
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


def create_block():
    """ Create apples """
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy,
                          posx + SEG_SIZE, posy + SEG_SIZE,
                          fill="red")

# Score counter
class Score(object):

    # display score
    def __init__(self):
        self.score = 0
        self.x = 55
        self.y = 15
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="White", tag="score", state='hidden')

    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="White", tag="score")

    # reset score at new game
    def reset(self):
        c.delete("score")
        self.score = 0

# Manage game process
def main():
    """ Game Process Model """
    global IN_GAME
    if IN_GAME:
        s.move()

        # snake head coordination
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # hit the boards
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # eating apple
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        # eat yourself
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False

        # speed
        root.after(100, main)
    # IN_GAME -> stop the game and display message
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')

class Segment(object):
    """ snake segment """
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x + SEG_SIZE, y + SEG_SIZE,
                                           fill="green")
                                           
class Snake(object):
    """ snake class """
    def __init__(self, segments):
        self.segments = segments

        # move directions
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}

        # start moving
        self.vector = self.mapping["Right"]

    def move(self):
        """ move snake to the chosen direction """
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * SEG_SIZE, y1 + self.vector[1] * SEG_SIZE,
                 x2 + self.vector[0] * SEG_SIZE, y2 + self.vector[1] * SEG_SIZE)

    def add_segment(self):
        """ add segment """
        score.increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ change direction """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    # Reset snake with new game
    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)

# display message
def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(BLOCK, state='hidden')


# New game button
def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    c.itemconfigure(close_but, state='hidden')
    start_game()

# Start the game
def start_game():
    global s
    create_block()
    s = create_snake()

    # Button click behavior
    c.bind("<KeyPress>", s.change_direction)
    main()


# Create segments and snake
def create_snake():
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(segments)
    
# Exit
def close_win(root):
    exit()

# Main window
root = Tk()
root.title("Incredible Adventures of the Super Snake III: Resurrection of the Legend")

# create Canvas object
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
c.grid()

# Catch focus to catch button press
c.focus_set()

# Total score text
game_over_text = c.create_text(WIDTH / 2, HEIGHT / 2, text="You loose!",
                               font='Arial 20', fill='red',
                               state='hidden')
                               
# New game text after loose
restart_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3,
                             font='Arial 25',
                             fill='green',
                             text="New Game",
                             state='hidden')

# Text for exit after loose
close_but = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 5, font='Arial 25',
                          fill='yellow',
                          text="Exit",
                          state='hidden')

# Events handler for buttons
c.tag_bind(restart_text, "<Button-1>", clicked)
c.tag_bind(close_but, "<Button-1>", close_win)

# Score counter
score = Score()

# Game start
start_game()

# open the window
root.mainloop()