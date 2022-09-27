import random
import copy


class Hat:
    def __init__(self, **balls):
        self.balls = balls
        contents = []
        for k, v in balls.items():
            for _ in range(v):
               contents.append(k)
        self.contents = contents

    def draw(self, number_of_balls):
        draw_list = random.sample(self.contents, number_of_balls)
        return draw_list

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    hat_contents = copy.copy(hat.contents)
    success = 0
    for _ in range(num_experiments):
        draw_list = hat.draw(num_balls_drawn)
        for ball in draw_list:
            #print(ball)
            #print(draw_list.count(ball))
            #print(expected_balls.get(ball, 0))

            #print(draw_list.count(ball) >= expected_balls.get(ball, 0))
            if draw_list.count(ball) > expected_balls.get(ball, 0):
                #print('-')
                continue
            success += 1
    probability = success / num_experiments
    return probability


print()
print()
#hat = Hat(black=6, red=4, green=3)
#probability = experiment(hat=hat,
#                  expected_balls={"red":2,"green":1},
#                  num_balls_drawn=5,
#                  num_experiments=2000)

hat = Hat(black=1, red=1, green=1)
probability = experiment(hat=hat,
                  expected_balls={"red":1},
                  num_balls_drawn=1,
                  num_experiments=2000)

print(probability)
