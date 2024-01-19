import pygame
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Subject name
subject_name = "Lea"
session = 2
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
        pertubation_type = 'sudden' 
    elif attempts == a3:
        pertubation_mode = False
    elif attempts == a4:
        pertubation_mode = True    
        pertubation_type = 'sudden'         
    elif attempts == a5:
        pertubation_mode = False    
    elif attempts >= a6:
        running = False        

    collect_attempts = [a2, a3, a4, a5, a6]
    string_attempts = ['No Peturbation', 'Sudden Perturbation 1', 'No Peturbation', 'Sudden Perturbation 2', 'No Peturbation']
    
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
                angle = (counter//4 + 1) * delta_angle 
                
        
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
a1, a2, a3, a4, a5, a6 = 0, 40, 80, 120, 160, ATTEMPTS_LIMIT
collect_attempts = [a1, a2, a3, a4, a5, a6]
number_types = [np.array(collect_attempts[1:]) - np.array(collect_attempts[:-1])]

number_attempts = np.array(collect_attempts[1:]) - np.array(collect_attempts[:-1])

string_trials = []
for trial, number in zip(string_attempts, number_attempts):
    string_trials += [trial] * number
data = {'subject_name': [subject_name] * len(string_trials),
        'target_mode': [target_mode] * len(string_trials),
        'perturbation_type': ["sudden"] * len(string_trials),
        'trial_number': np.arange(1, len(string_trials)+1),
        'trial_name' : string_trials,
        'target_angles': [0] * len(string_trials),
        'circle_angles': error_angles,
        'error_angles': error_angles
        }

""" Write the attempts and error_angles to a csv file. Write also the mean and CI for each pertubation_types to a csv file."""
data = pd.DataFrame(data)
data.to_csv('HW2/error_angles_baseline_trial_{}_{}.csv'.format(session, subject_name), header=True, index=False,)


sys.exit()