import pygame
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Game parameters
SCREEN_X, SCREEN_Y = 1920, 1080 # your screen resolution
WIDTH, HEIGHT = SCREEN_X // 1.25  , SCREEN_Y // 1.25 # be aware of monitor scaling on windows (150%)
CIRCLE_SIZE = 20
TARGET_SIZE = CIRCLE_SIZE
TARGET_RADIUS = 300
MASK_RADIUS = 0.75 * TARGET_RADIUS
ATTEMPTS_LIMIT = 200
START_POSITION = (WIDTH // 2, HEIGHT // 2)
START_ANGLE = 0
PERTUBATION_ANGLE= 30
TIME_LIMIT = 1000 # time limit in ms

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Reaching Game")


# Initialize game metrics
score = 0
attempts = 0
new_target = None
start_time = 0

new_target = None
start_target=math.radians(START_ANGLE)
move_faster = False 
clock = pygame.time.Clock()

# Initialize game modes
mask_mode= True
target_mode = 'fix'  # Mode for angular shift of target: random, fix, dynamic
pertubation_mode= False
pertubation_type= 'sudden' # Mode for angular shift of controll: random, gradual or sudden
perturbation_angle = math.radians(PERTUBATION_ANGLE)  # Angle between mouse_pos and circle_pos

error_angles = []  # List to store error angles
error_distances = []

""" For plotting """
attempts_plotting_baseline = []
attempts_plotting_gradual = []
attempts_plotting_random = []
attempts_plotting_sudden = []

error_gradual = []
error_sudden = []
error_random = []
error_baseline = []



# Function to generate a new target position
def generate_target_position():
    if target_mode == 'random':
        angle = random.uniform(0, 2 * math.pi)

    elif target_mode == 'fix':   
        angle=start_target;  

    new_target_x = WIDTH // 2 + TARGET_RADIUS * math.sin(angle)
    new_target_y = HEIGHT // 2 + TARGET_RADIUS * -math.cos(angle) # zero-angle at the top
    return [new_target_x, new_target_y]

# Function to check if the current target is reached
def check_target_reached():
    if new_target:
        distance = math.hypot(circle_pos[0] - new_target[0], circle_pos[1] - new_target[1])
        return distance <= CIRCLE_SIZE // 2
    return False

# Function to check if player is at starting position and generate new target
def at_start_position_and_generate_target(mouse_pos):
    distance = math.hypot(mouse_pos[0] - START_POSITION[0], mouse_pos[1] - START_POSITION[1])
    if distance <= CIRCLE_SIZE:
        return True
    return False

# Main game loop
running = True
show_end_position = False
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press 'esc' to close the experiment
                running = False
            elif event.key == pygame.K_4: # Press '4' to test pertubation_mode
                pertubation_mode = True
            elif event.key == pygame.K_5: # Press '5' to end pertubation_mode
                pertubation_mode = False
            
    # Design experiment
    a1, a2, a3, a4, a5, a6 = 0, 40, 80, 120, 160, ATTEMPTS_LIMIT
    if attempts == a1:
        pertubation_mode = False
    elif attempts == a2:
        pertubation_mode = True
        pertubation_type = 'gradual' 
    elif attempts == a3:
        pertubation_mode = False
    elif attempts == a4:
        pertubation_mode = True    
        pertubation_type = 'sudden'         
    elif attempts == a5:
        pertubation_mode = True    
        pertubation_type = 'random' 
    elif attempts >= a6:
        running = False        

    collect_attempts = [a2, a3, a4, a5, a6]
    string_attempts = ['False', 'Gradual Perturbation', 'False', 'Sudden Perturbation', 'Random Perturbation']
    
    # Hide the mouse cursor
    pygame.mouse.set_visible(False)
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Calculate distance from START_POSITION to mouse_pos
    deltax = mouse_pos[0] - START_POSITION[0]
    deltay = mouse_pos[1] - START_POSITION[1]
    distance = math.hypot(deltax, deltay)
        
    if pertubation_mode:
        # TASK1: CALCULATE perturbed_mouse_pos 
       
        if pertubation_type == 'sudden':
            angle = perturbation_angle
            
            """ Rotate the current_mouse_pos by the perturbation_angle clockwise. """
            deflection_x = math.cos(angle) * deltax - math.sin(angle) * deltay
            deflection_y = math.sin(angle) * deltax + math.cos(angle) * deltay

        elif pertubation_type == 'gradual':
            """ Check if the current attempt is in the list of collected attempts."""
            if attempts in collect_attempts:
                """ Get index of the current attempt in the list of collected attempts."""
                start_index = collect_attempts.index(attempts)
                start_gradual = attempts 
                
                
            """ Find the end attempt of the gradual perturbation. """
            end_gradual = collect_attempts[start_index + 1] - 1
            
            """ Increase the angle gradually from 0 to perturbation_angle by taking into account the attempts. """
            #angle = perturbation_angle * ((attempts - start_gradual) / (end_gradual - start_gradual))
            
            counter = attempts - start_gradual
            
            if counter % 4 == 0:
                delta_angle = perturbation_angle / 10
                angle = (counter//4 + 1)* delta_angle 
                
            """ Rotate the current_mouse_pos by the perturbation_angle counter-clockwise. """
            deflection_x = math.cos(angle) * deltax - math.sin(angle) * deltay
            deflection_y = math.sin(angle) * deltax + math.cos(angle) * deltay
            
        elif pertubation_type == 'random':
            if start == 0:
                """ Find a random angle between 0 and perturbation_angle. But for the whole attempt. """
                angle = random.uniform(0, perturbation_angle)
                start = -1                              
        
            """ Rotate the current_mouse_pos by the perturbation_angle clockwise. """
            deflection_x = math.cos(angle) * deltax + math.sin(angle) * deltay
            deflection_y = math.sin(angle) * deltax + math.cos(angle) * deltay
                            
            
        """ Include the deflection in the perturbed_mouse_pos"""
        perturbed_mouse_pos = (START_POSITION[0] + deflection_x, START_POSITION[1] + deflection_y)
        circle_pos = perturbed_mouse_pos

            
    else:
        circle_pos = pygame.mouse.get_pos()
    
    # Check if target is hit or missed
    # hit if circle touches target's center
    if check_target_reached():
        score += 1
        attempts += 1
        target_pos = new_target
        new_target = None  # Set target to None to indicate hit
        
        start_time = 0  # Reset start_time after hitting the target

        # CALCULATE AND SAVE ERRORS between target and circle end position for a hit
        """ Calulate the euclidean distance between the target and the circle end position"""
        error_distance = ((target_pos[0] - circle_pos[0])**2 / SCREEN_X) + ((target_pos[1] - circle_pos[1])**2 / SCREEN_Y)
        
        if target_pos[0] < circle_pos[0]:
            error_distance = error_distance * -1
        error_distances.append(error_distance)
        
        """ Get from the target_pos and circle_pos the angle. """
        #error = target_pos[0] - circle_pos[0], target_pos[1] - circle_pos[1]
        """ Get the angle of the error vector. """
        #error_angle = math.degrees(math.atan2(error[1], error[0]))
        
        """ Get the vector from the starting point to the target. """
        vector_start_to_target = np.subtract(target_pos, START_POSITION)

        """ Get the vector from the starting point to the circle. """
        vector_start_to_circle = np.subtract(circle_pos, START_POSITION)

        """ Calculate the angle between the two vectors. """
        error_angle = np.arccos(np.dot(vector_start_to_target, vector_start_to_circle) / (np.linalg.norm(vector_start_to_target) * np.linalg.norm(vector_start_to_circle)))
        error_angle = np.degrees(error_angle)
        
        if move_faster:
            error_angle = np.nan
            
        if target_pos[0] < circle_pos[0]:
            error_angle = error_angle * -1
        error_angles.append(error_angle)       
                
        """ Bin the data accorind to the pertubation_type and collect the errors"""
        if pertubation_type == 'gradual':
            attempts_plotting_gradual += [attempts] * len(error_angles)
            error_gradual += error_angles

            
        elif pertubation_type == 'sudden':
            attempts_plotting_sudden += [attempts] * len(error_angles)
            error_sudden += error_angles
       
            
        elif pertubation_type == 'random':
            attempts_plotting_random += [attempts] * len(error_angles)
            error_random += error_angles

            
        if pertubation_mode == False:
            attempts_plotting_baseline += [attempts] * len(error_angles)
            error_baseline += error_angles
    
  
        
    #miss if player leaves the target_radius + 1% tolerance
    elif new_target and math.hypot(circle_pos[0] - START_POSITION[0], circle_pos[1] - START_POSITION[1]) > TARGET_RADIUS*1.01:
        attempts += 1
        target_pos = new_target
        new_target = None  # Set target to None to indicate miss
        start_time = 0  # Reset start_time after missing the target

        # CALCULATE AND SAVE ERRORS between target and circle end position for a hit
        """ Calulate the euclidean distance between the target and the circle end position"""
        error_distance = ((target_pos[0] - circle_pos[0])**2 / SCREEN_X) + ((target_pos[1] - circle_pos[1])**2 / SCREEN_Y)
        if target_pos[0] < circle_pos[0]:
            error_distance = error_distance * -1
        
        error_distances.append(error_distance)
        
        """ Get from the target_pos and circle_pos the angle. """
        #error = target_pos[0] - circle_pos[0], target_pos[1] - circle_pos[1]
        """ Get the angle of the error vector. """
        #error_angle = math.degrees(math.atan2(error[1], error[0]))
        
        """ Get the vector from the starting point to the target. """
        vector_start_to_target = np.subtract(target_pos, START_POSITION)

        """ Get the vector from the starting point to the circle. """
        vector_start_to_circle = np.subtract(circle_pos, START_POSITION)

        """ Calculate the angle between the two vectors. """
        error_angle = np.arccos(np.dot(vector_start_to_target, vector_start_to_circle) / (np.linalg.norm(vector_start_to_target) * np.linalg.norm(vector_start_to_circle)))
        error_angle = np.degrees(error_angle)
                
        if move_faster:
            error_angle = np.nan
            
        if target_pos[0] < circle_pos[0]:
            error_angle = error_angle * -1
        error_angles.append(error_angle)
        
        
        """ Bin the data accorind to the pertubation_type and collect the errors"""
        if pertubation_type == 'gradual':
            attempts_plotting_gradual += [attempts] * len(error_angles)
            error_gradual += error_angles
      
            
        elif pertubation_type == 'sudden':
            attempts_plotting_sudden += [attempts] * len(error_angles)
            error_sudden += error_angles
 
            
        elif pertubation_type == 'random':
            attempts_plotting_random += [attempts] * len(error_angles)
            error_random += error_angles
            
            
        if pertubation_mode == False:
            attempts_plotting_baseline += [attempts] * len(error_angles)
            error_baseline += error_angles
            


    # Check if player moved to the center and generate new target
    if not new_target and at_start_position_and_generate_target(mouse_pos):
        new_target = generate_target_position()
        move_faster = False
        # Start the timer for the attempt
        start = 0

    # Check if time limit for the attempt is reached
    current_time = pygame.time.get_ticks()
    if start_time != 0 and (current_time - start_time) > TIME_LIMIT:
        move_faster = True
        start_time = 0  # Reset start_time
        
    # Show 'MOVE FASTER!'
    if move_faster:
        font = pygame.font.Font(None, 36)
        
        
        text = font.render('MOVE FASTER!', True, RED)
        text_rect = text.get_rect(center=(START_POSITION))
        screen.blit(text, text_rect)

# Generate playing field
    # Draw current target
    if new_target:
        pygame.draw.circle(screen, BLUE, new_target, TARGET_SIZE // 2) 

    # Draw circle cursor
    if mask_mode:
        if distance < MASK_RADIUS:
            pygame.draw.circle(screen, WHITE, circle_pos, CIRCLE_SIZE // 2)
    else:
        pygame.draw.circle(screen, WHITE, circle_pos, CIRCLE_SIZE // 2)
    
    # Draw start position
    pygame.draw.circle(screen, WHITE, START_POSITION, 5) 

    # Show score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Show attempts
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Attempts: {attempts}", True, WHITE)
    screen.blit(score_text, (10, 30))

    # Update display
    pygame.display.flip()
    clock.tick(60)



# Quit Pygame
pygame.quit()

## TASK 2, CALCULATE, PLOT AND SAVE ERRORS from error_angles
import pandas as pd
df0 = pd.DataFrame({'attempts': range(attempts), 'error_angles': error_angles})
df0_0 = pd.DataFrame({'attempts': range(attempts), 'error_distances': error_distances})

import seaborn as sns
g0 = sns.scatterplot(data = df0, x = 'attempts', y = 'error_angles') 
""" Add vertical lines to show the different pertubation_types."""
g0.vlines(np.array(collect_attempts) - 0.5, ymin = -180, ymax = 180, color = 'blue', alpha = 0.5)
""" Add labels to the vertical lines."""
for i in range(len(collect_attempts)):
    g0.text(collect_attempts[i] - 1.5, -170, string_attempts[i], rotation = 90, color = 'blue', alpha = 0.5)
g0.set(xlabel='attempts', ylabel='error_angles', title = 'Error_angles over attempts')
plt.show()

g0_0 = sns.scatterplot(data = df0_0, x = 'attempts', y = 'error_distances')
""" Add vertical lines to show the different pertubation_types."""
g0_0.vlines(np.array(collect_attempts) - 0.5, ymin = 0, ymax = 1, color = 'blue', alpha = 0.5)
""" Add labels to the vertical lines."""
for i in range(len(collect_attempts)):
    g0_0.text(collect_attempts[i] - 1.5, 0.5, string_attempts[i], rotation = 90, color = 'blue', alpha = 0.5)
g0_0.set(xlabel='attempts', ylabel='error_distances', title = 'Error_distances over attempts')
plt.show()



""" Calulate the mean and CI for each pertubation_types and plot it. """
mean_baseline = np.mean(error_baseline)
mean_gradual = np.mean(error_gradual)
mean_sudden = np.mean(error_sudden)
mean_random = np.mean(error_random)

CI_baseline = 1.96 * np.std(error_baseline) / np.sqrt(len(error_baseline))
CI_gradual = 1.96 * np.std(error_gradual) / np.sqrt(len(error_gradual))
CI_sudden = 1.96 * np.std(error_sudden) / np.sqrt(len(error_sudden))
CI_random = 1.96 * np.std(error_random) / np.sqrt(len(error_random))

df1 = pd.DataFrame({'pertubation_type': ['baseline', 'gradual', 'sudden', 'random'], 
                    'mean': [mean_baseline, mean_gradual, mean_sudden, mean_random], 
                    'CI': [CI_baseline, CI_gradual, CI_sudden, CI_random]})

g1 = sns.barplot(data = df1, x = 'pertubation_type', y = 'mean', yerr = df1['CI'])
g1.set(xlabel='pertubation_type', ylabel='error_angles', title = 'Error_angles over pertubation_types')
plt.show()

""" Save the plots."""
g0.figure.savefig('error_angles.svg')
g1.figure.savefig('error_angles_over_pertubation_types.svg')


""" Write the attempts and error_angles to a csv file. Write also the mean and CI for each pertubation_types to a csv file."""
df0.index.name = 'index'
df0.to_csv('error_angles.csv', header=True, index=True,)
df0_0.index.name = 'index'
df0_0.to_csv('error_distances.csv', header=True, index=True,)
df1.index.name = 'index'
df1.to_csv('error_angles_over_pertubation_types.csv', header=True, index=True,)


sys.exit()