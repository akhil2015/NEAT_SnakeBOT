import random
import curses
#from genome import Genome
import datetime
import numpy as np
import neat

class Snake:

    def __init__(self, nome = None):
        self.s = curses.initscr()
        curses.curs_set(0)
        self.sh, self.sw = self.s.getmaxyx()
        self.sh -= 2
        self.w = curses.newwin(self.sh, self.sw, 2, 0)
        self.score_w = curses.newwin(2, int(self.sw/2)-5, 0, 0)
        self.generation_w = curses.newwin(2, int(self.sw/2)-5, 0, int(self.sw/2))
        self.w.keypad(1)
        self.w.timeout(10)
        self.w.box()
        self.generation = 0
        self.genome = nome
    def play(self):
#        s = curses.initscr()
#        curses.curs_set(0)
#        sh, sw = s.getmaxyx()
#        sh -= 2
#        w = curses.newwin(sh, sw, 2, 0)
#        score_w = curses.newwin(2,int(sw/2),0,0)
#        w.keypad(1)
#        w.timeout(50)
#        w.box()
        #score_w.box()
        self.w.refresh()
        self.score_w.refresh()
        self.generation_w.refresh()
        g = self.generation
        snk_x = int(self.sw/4)
        snk_y = int(self.sh/2)
        snake = [
            [snk_y, snk_x],
            [snk_y, snk_x-1],
            [snk_y, snk_x-2]
        ]

        food = [random.randint(1, self.sh-2), random.randint(1, self.sw-2)]
        self.w.addch(food[0], food[1], curses.ACS_PI)
        self.w.addch(snake[0][0], snake[0][1],curses.ACS_DIAMOND)
        self.w.addch(snake[1][0], snake[1][1],curses.ACS_DIAMOND)
        self.w.addch(snake[2][0], snake[2][1],curses.ACS_DIAMOND)
        key = curses.KEY_RIGHT
#        genome = Genome()
#        genome.initialize()
#        net = Neural_Net(genome)
        moves = 0
        moves_loop = 0
        output = 9
        start = datetime.datetime.now()
        distance_wall = 0
        while True:
            if self.genome != None:
                next_key_dummy = self.w.getch()
                next_key = -1
                '''
                du = 0
                dl = 0
                dd = 0
                dr = 0
                distance_wall = abs(self.sw - snake[0][1])
                if key == curses.KEY_UP:
                    du += 1
                    distance_wall = snake[0][0]
                if key == curses.KEY_DOWN:
                    dd += 1
                    distance_wall = abs(self.sh - snake[0][0])
                if key == curses.KEY_LEFT:
                    dl += 1
                    distance_wall = snake[0][1]
                if key == curses.KEY_RIGHT:
                    dr += 1
                    distance_wall = abs(self.sw - snake[0][1])
                '''

                #input = [1, snake[0][0], snake[0][1], food[0], food[1], output, abs(self.sh - snake[0][0]), abs(self.sw - snake[0][1])]
                #input = [1, du, dl, dd, dr, food[0], food[1], distance_wall]
                vision = np.zeros((4,3))
                for h in range(self.sh):
                    if h == food[0]:
                        if h < snake[0][0]:
                            vision[1][0] = abs(h - snake[0][0])
                        else:
                            vision[0][0] = abs(h - snake[0][0])
                    if [h, snake[0][1]] in snake[1:]:
                        if h < snake[0][0]:
                            vision[1][1] = abs(h - snake[0][0])
                        else:
                            vision[0][1] = abs(h - snake[0][0])

                    vision[0][2] = abs(snake[0][0] - self.sh)
                    vision[1][2] = snake[0][0]

                for w in range(self.sw):
                    if w == food[1]:
                        if w < snake[0][1]:
                            vision[2][0] = abs(w - snake[0][1])
                        else:
                            vision[3][0] = abs(w - snake[0][1])
                    if [snake[0][0], w] in snake[1:]:
                        if w < snake[0][1]:
                            vision[2][1] = abs(w - snake[0][1])
                        else:
                            vision[3][1] = abs(w - snake[0][1])

                    vision[2][2] = abs(snake[0][1] - self.sw)
                    vision[3][2] = snake[0][1]
                input = vision.flatten()

                output = self.genome.activate(input)
                output = output.index(max(output))
                if output == -1:
                    output = random.randint(0,3)
                elif output == 0:
                    next_key = -1 if key == curses.KEY_UP else curses.KEY_DOWN
                elif output == 1:
                    next_key = -1 if key == curses.KEY_DOWN else curses.KEY_UP
                elif output == 2:
                    next_key = -1 if key == curses.KEY_RIGHT else curses.KEY_LEFT
                elif output == 3:
                    next_key = -1 if key == curses.KEY_LEFT else curses.KEY_RIGHT
                #move = open("moves.txt", "w+")
                #move.write(repr(output))

            else:
                next_key = self.w.getch()
            if key != next_key:
                moves += 1
                moves_loop += 1
            key = key if next_key == -1 else next_key

            if snake[0][0] in [0, self.sh-1] or snake[0][1]  in [0, self.sw-1] or snake[0] in snake[1:] or moves_loop >= 100:
                curses.endwin()
                end = datetime.datetime.now()
                tt = end - start
                if moves_loop >=100:
                    return 0
                if len(snake) <= 5:
                    return 3**tt.total_seconds() + len(snake)*2 + 3*moves
                elif len(snake) <=10:
                    return 0.5*tt.total_seconds() + 3**(len(snake)-3)
                else:
                    return 0.5*tt.total_seconds() + 0.5*(len(snake)-3)
                quit()

            new_head = [snake[0][0], snake[0][1]]

            if key == curses.KEY_DOWN:
                new_head[0] += 1
            if key == curses.KEY_UP:
                new_head[0] -= 1
            if key == curses.KEY_LEFT:
                new_head[1] -= 1
            if key == curses.KEY_RIGHT:
                new_head[1] += 1

            snake.insert(0, new_head)

            if snake[0] == food:
                moves_loop = 0
                food = None
                while food is None:
                    nf = [
                        random.randint(1, self.sh-2),
                        random.randint(1, self.sw-2)
                    ]
                    food = nf if nf not in snake else None
                self.w.addch(food[0], food[1], curses.ACS_PI)
            else:
                tail = snake.pop()
                self.w.addch(tail[0], tail[1], ' ')

            self.w.addch(snake[0][0], snake[0][1], curses.ACS_DIAMOND)
            self.score_w.addstr(1,3,"Score = "+repr(len(snake)-3))
            self.generation_w.addstr(1,5,"Generation = {}".format(self.generation))
            self.w.refresh()
            self.score_w.refresh()
            self.generation_w.refresh()

if __name__ == "__main__":
    peter = Snake()
    score = peter.play()
    print("End Score = {}".format(score))
