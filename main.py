import pygame
import os
import random
import math 
import sys
import numpy as np

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird3.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('Fonts/PressStart2P.ttf', 16)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.score = 0
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.jump_vel = self.JUMP_VEL
            self.dino_jump = False
            self.dino_run = True
            self.rect.y = self.Y_POS 

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS + 40
        self.step_index += 1

    def draw(self, SCREEN, line=True, border=True):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        if border:
            if not self.dino_duck:
                pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
            else:
                pygame.draw.rect(SCREEN, self.color, (self.rect.x + 20, self.rect.y, self.rect.width, self.rect.height), 2)
        if line:
            for obstacle in obstacles:
                pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)
    
class Obstacle:
    def __init__(self, image, num_ob):
        self.image = image
        self.type = num_ob
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH * game_speed / 20

    def update(self):
        self.rect.x -= game_speed*0.9
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, num_ob):
        super().__init__(image, num_ob)
        self.rect.y = 325
        self.id = 'sc'

class LargeCactus(Obstacle):
    def __init__(self, image, num_ob):
        super().__init__(image, num_ob)
        self.rect.y = 300
        self.id = 'lc'

class Bird(Obstacle):
    def __init__(self, image, num_ob):
        super().__init__(image, num_ob)
        self.rect.y = 250 + random.choice([-50,50,15,-75])
        self.id = 'b'

class HighBird(Obstacle):
    def __init__(self, image, typex):
        super().__init__(image, typex)
        self.rect.y = 250 - 50

class LowBird(Obstacle):
    def __init__(self, image, typex):
        super().__init__(image, typex)
        self.rect.y = 250 +10

def remove(index):
    dinosaurs.pop(index)
    if len(weights):
        weights.pop(index)
  
def play_game(dinosaurs,human = True, line = True, border = True,generation = 0):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20
    points = 0
    obstacles = []

    def score():
        global points, game_speed
        points += 1
        for dino in dinosaurs:
            if dino.dino_run==False:
                dino.score+=0.1
            else:
                dino.score+=1
        if points % 300 == 0:
            game_speed += 1
            game_speed = min(40, game_speed)
        text = FONT.render("Points: " + str(points), True, (0, 0, 0))
        SCREEN.blit(text, (800, 50))
        if not human:
            text = FONT.render("Generation: " + str(generation) + " Alive: " + str(len(dinosaurs)), True, (0, 0, 0))
            SCREEN.blit(text, (100, 50))
            
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if human:
                if event.type == pygame.KEYDOWN:
                    if dinosaurs[0].rect.y == dinosaurs[0].Y_POS or dinosaurs[0].rect.y == dinosaurs[0].Y_POS+40:
                        if event.key==pygame.K_UP:
                            dinosaurs[0].dino_jump = True
                            dinosaurs[0].dino_run = False 
                            dinosaurs[0].dino_duck = False
                        elif event.key==pygame.K_DOWN:
                            dinosaurs[0].dino_jump = False
                            dinosaurs[0].dino_run = False
                            dinosaurs[0].dino_duck = True
                        elif event.key==pygame.K_RIGHT:
                            dinosaurs[0].dino_jump = False
                            dinosaurs[0].dino_run = True
                            dinosaurs[0].dino_duck = False


        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN,line,border)

        if len(obstacles) == 0 :
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD, random.randint(0, 1)))
        
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)

            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    if not human:
                        W = weights[i]
                        scores.append((dinosaur.score, W))
                    remove(i)
                    if len(dinosaurs)==0:
                        return
                    
                elif human == False:
                    dinosaur_pos = (dinosaurs[i].rect.x, dinosaurs[i].rect.y)
                    obstacle_pos = (obstacle.rect.x, obstacle.rect.y)
                    s = distance(dinosaur_pos, obstacle_pos)

                    X = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
                    X[0] = dinosaurs[i].rect.y
                    X[1] = obstacle.rect.x
                    X[2] = obstacle.rect.y
                    X[3] = distance((dinosaur.rect.x, dinosaur.rect.y),obstacle.rect.midtop)
                    X[4] = game_speed
                    
                    X_reshaped = X.reshape(1, -1)

                    W1, W2 = weights[i]

                    action = Decide(dinosaurs[i], X_reshaped, W1, W2)
                    if dinosaurs[i].rect.y == dinosaurs[i].Y_POS or dinosaurs[i].rect.y == dinosaurs[i].Y_POS+40:
                        if action == 0:
                            dinosaurs[i].dino_jump = True
                            dinosaurs[i].dino_run = False 
                            dinosaurs[i].dino_duck = False
                        elif action == 1:
                            dinosaurs[i].dino_jump = False
                            dinosaurs[i].dino_run = False
                            dinosaurs[i].dino_duck = True
                        else:
                            dinosaurs[i].dino_jump = False
                            dinosaurs[i].dino_run = True
                            dinosaurs[i].dino_duck = False

                        
        background()
        score()
        clock.tick(30)
        pygame.display.update()

dinosaurs = []
scores = []
weights = []

def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def forward(X, W1, W2):
    z = np.dot(X, W1)
    a1 = relu(z)
    z = np.dot(a1, W2)
    # a2 = sigmoid(z)
    a2 = z
    return a2

def Decide(dinosaur, X, W1, W2):
    a2 = forward(X, W1, W2)
    # print(a2)
    action = np.argmax(a2)  
    return action
      
def TrainAI():
    POPULATION_SIZE = 100
    GENERATIONS = 500

    global weights, dinosaurs, scores
    
    weights = []
    
    for _ in range(POPULATION_SIZE):    
        input_features = 5
        hidden_layer_features = 16
        weights1 = np.random.randn(input_features, hidden_layer_features)
        weights2 = np.random.randn(hidden_layer_features, 3)
        weights.append((weights1, weights2))      

    for generation in range(GENERATIONS):
        dinosaurs = []  
        
        for i in range(POPULATION_SIZE):
            player = Dinosaur()
            dinosaurs.append(player)
        
        
        play_game(dinosaurs, False, True, True, generation + 1)
        
        
        scores.sort(key=lambda x: x[0], reverse=True)
        
        print(f"Generation {generation + 1} Best solution = {scores[0][0]}")
        # print('W1')
        # print(scores[0][1][0])
        # print('W2')
        # print(scores[0][1][1])
        
        
        if scores[0][0] >= 10000:  # Good enough score to break
            print('\n\n\n\n\n\n\n\n\n')
            print(scores[0][1])
            break
        
        # next gen
        weights = []
        weights = [solution[1] for solution in scores]
        
        def crossover(weights1, weights2):
            W1_1, W2_1 = weights1
            W1_2, W2_2 = weights2
            
            mask_W1 = np.random.randint(2, size=W1_1.shape).astype(bool)
            mask_W2 = np.random.randint(2, size=W2_1.shape).astype(bool)
            
            W1_child = np.where(mask_W1, W1_1, W1_2)
            W2_child = np.where(mask_W2, W2_1, W2_2)
            
            return W1_child, W2_child
        
        def mutation(W):
            W1, W2 = W
            choice1 = np.random.choice([1., 0.], p=[0.9, 0.1], size=W1.shape).astype(bool)
            choice2 = np.random.choice([1., 0.], p=[0.9, 0.1], size=W2.shape).astype(bool)
            W1 = np.where(choice1, W1, np.random.randn(*W1.shape))
            W2 = np.where(choice2, W2, np.random.randn(*W2.shape))
            return W1, W2
        
        NewGen = []
        
        BestSolutions = scores[:10]
        weights_of_best_solutions = []
        for solution in BestSolutions:
            W = solution[1]
            weights_of_best_solutions.append(W)
        
            
        #reproduction
        total_score = sum([solution[0] for solution in BestSolutions])
        
        for _ in range(POPULATION_SIZE - 20 ):
            if np.random.rand()>0.5:
                parent1, parent2 = random.choices(
                        weights_of_best_solutions,
                        weights=[solution[0] for solution in BestSolutions],
                        k=2
                    )
            else:            
                parent1, parent2 = random.choices(weights, k=2)
            child_weights = crossover(parent1, parent2)
            if np.random.rand()<0.5:
                child_weights = mutation(child_weights)
            NewGen.append(child_weights)
        
        #10 best of last
        NewGen.extend(weights_of_best_solutions)
        
        # diversity hire
        for _ in range(10): 
            input_features = 5
            hidden_layer_features = 16
            weights1 = np.random.randn(input_features, hidden_layer_features)
            weights2 = np.random.randn(hidden_layer_features, 3)
            NewGen.append((weights1, weights2))
            
        weights = NewGen
        scores.clear()

  
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs,scores,weights
    
    # player1 = Dinosaur()
    # player2 = Dinosaur()
    # dinosaurs.append(player1)
    # dinosaurs.append(player2)
    # play_game(dinosaurs,True,True,True)
    
    TrainAI()
    
if __name__ == "__main__":
    main()
