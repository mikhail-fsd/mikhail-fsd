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
        if len(self.contents) < number_of_balls:
            return self.contents
        draw_list = random.sample(self.contents, number_of_balls)
        for ball in draw_list:
            self.contents.remove(ball)
        return draw_list

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    hat_contents = copy.copy(hat.contents)
    if len(hat_contents) <= num_balls_drawn: return float(1)
    total_balls_expect = sum(v for v in expected_balls.values())
    success = 0
    mat = 0
    for _ in range(num_experiments):
        draw_list = random.sample(hat_contents, num_balls_drawn)
        for ball, value in expected_balls.items():
            if value > draw_list.count(ball):
                continue
            mat += value
        if mat == total_balls_expect: success += 1
        mat = 0
    probability = success / num_experiments
    return probability


print()
print()
hat = Hat(blue=3,red=2,green=6)
probability = experiment(hat=hat,
                  expected_balls={"blue":2,"green":1},
                  num_balls_drawn=44,
                  num_experiments=5)

#hat = Hat(black=1, red=1, green=1)
#probability = experiment(hat=hat,
                  #expected_balls={"red":1},
                  #num_balls_drawn=1,
                  #num_experiments=2000)

print(probability)
