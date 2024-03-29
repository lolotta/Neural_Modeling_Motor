import pygame
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime

import random as rand
import scipy.stats as stats

# Subject name
subject_name = "Hannah"
# Game parameters
experimenter = "Lotta"
if experimenter == "Lotta":
    SCREEN_X, SCREEN_Y = 1920, 1080 # your screen resolution
    WIDTH, HEIGHT = SCREEN_X // 1.25  , SCREEN_Y // 1.25 # be aware of monitor scaling on windows (150%)

elif experimenter == "Flo":
    SCREEN_X, SCREEN_Y = 3840, 2160 # your screen resolution
    WIDTH, HEIGHT = SCREEN_X // 2.5  , SCREEN_Y // 2.5 # be aware of monitor scaling on windows (150%)
CIRCLE_SIZE = 20
TARGET_SIZE = CIRCLE_SIZE * 1.5
TARGET_RADIUS = 300
MASK_RADIUS = 1 * TARGET_RADIUS
ATTEMPTS_LIMIT = 320
START_POSITION = (WIDTH // 2, HEIGHT // 2)
START_ANGLE = 0
PERTURBATION_ANGLE= 30
TIME_LIMIT = 1000 # time limit in ms

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (100,100,100)

# Initialize Pygame
pygame.init()

# Set up the display
test_mode= False # test_mode=False for recording of unbiased subjects 
if test_mode:
    screen = pygame.display.set_mode((WIDTH-50, HEIGHT-50))
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Reaching Game")


# Initialize game metrics
score = 0
attempts = 0
new_target = None
start_time = 0
move_faster = False 
clock = pygame.time.Clock()

# Initialize game modes
mask_mode= True
target_mode = 'sequence'  # Mode for angular shift of target: random, fix, sequence, dynamic
start_target=math.radians(START_ANGLE)
sequence_target=START_ANGLE
perturbation_mode= False
perturbation_type= 'sudden' # Mode for angular shift of controll: random, gradual or sudden
perturbation_angle = math.radians(PERTURBATION_ANGLE)  # Angle between mouse_pos and circle_pos

perturbed_mouse_angle = 0
gradual_step = 0
gradual_attempts = 1
perturbation_rand=random.uniform(-math.pi/4, +math.pi/4)
""" Mean and Std for normal distribution in the lession condition """
mean, std = 0, 1

""" Weight the perturbation angles with a normal distribution """
angles = np.linspace(-math.pi/4, math.pi/4, 100)
""" Create  a normal distribution with mean and std """
weights = stats.norm.pdf(angles, mean, std)
perturbation_lession = rand.choices(angles, weights=weights, k=1)[0]

 # Lists to store important angles per attempt
error_angles = [] 
target_angles = []
circle_angles = []
target_pos = []
perturbed_angels = []
""" Create a 2d list for solving the trajoctories per attempt. """
trajactory = [[] for i in range(ATTEMPTS_LIMIT)]


target_reached_bool = []

#Choose experimental setup
exp_setup='feedback' #'perturbation_types' (HW1),'generalization' (HW2,A),'interference' (HW2,B)
feedbacks_types = ['rl', 'rl-gradient']
# Function to generate a new target position
def generate_target_position():
    if target_mode == 'random':
        angle = random.uniform(0, 2 * math.pi)

    elif target_mode == 'fix':   
        angle=start_target;  
    elif target_mode == 'sequence':   
        angle=math.radians(sequence_target);  

    new_target_x = WIDTH // 2 + TARGET_RADIUS * math.sin(angle)
    new_target_y = HEIGHT // 2 + TARGET_RADIUS * -math.cos(angle) # zero-angle at the top
    return [new_target_x, new_target_y]

def draw_old_trajactory(trajactory, attempts, screen):
    last_trajactory = trajactory[attempts-1]
    for i in range(len(last_trajactory)-1):
        pygame.draw.line(screen, WHITE, last_trajactory[i], last_trajactory[i+1], 1)


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
                perturbation_mode = True
            elif event.key == pygame.K_5: # Press '5' to end pertubation_mode
                perturbation_mode = False

    if exp_setup == 'feedback':
        #TASK 1: DESIGN YOUR OWN EXPERIMENT (HW2_A OR HW2_B)      
        # Design experiment A
        
        trial_number = [0, 20, 80, 100,
                        120, 180, 200]
        
        NEXT_ANGLES = [40, -30]
        
        """ Tripel every element and flatten the list """
        Collected_angels = sum([[i] * 3 for i in NEXT_ANGLES],[])
        Collected_feedbacks = sum([[i] * 3 for i in feedbacks_types],[])
        
        #trial_number = (np.array(trial_number) // 10).tolist()
        
        """ Block 0 """
        if attempts == trial_number[0]:
            perturbation_mode = False
            sequence_target =  NEXT_ANGLES[0]
            feedback = feedbacks_types[0]
        
        elif attempts == trial_number[1]:
            perturbation_mode = True
            perturbation_type = 'gradual'
            sequence_target =  NEXT_ANGLES[0]
            feedback = feedbacks_types[0]
        
        elif attempts == trial_number[2]:
            perturbation_mode = False
            sequence_target =  NEXT_ANGLES[0]
            feedback = feedbacks_types[0]
            
            """ Block 1 """
        elif attempts == trial_number[3]:
            perturbation_mode = False
            sequence_target =  NEXT_ANGLES[1]
            feedback = feedbacks_types[1]
            
        elif attempts == trial_number[4]:
            perturbation_mode = True
            perturbation_type = 'gradual'
            sequence_target =  NEXT_ANGLES[1]
            feedback = feedbacks_types[1]
            
        elif attempts == trial_number[5]:
            perturbation_mode = False
            sequence_target =  NEXT_ANGLES[1]
            feedback = feedbacks_types[1]
            
         
        elif attempts >= trial_number[6]:
            running = False 
        
        
        """ Numbers of attempts for each perturbation type """
        number_attempts = np.array(trial_number[1:]) - np.array(trial_number[:-1])
        string_attempts = ['No Perturbation', 'Gradual Perturbation', 'Aftereffect',
                           'No Perturbation', 'Gradual Perturbation', 'Aftereffect'
                           ]  


        
    # Hide the mouse cursor
    pygame.mouse.set_visible(False)
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    if new_target:
        trajactory[attempts] += [mouse_pos]

    # Calculate distance from START_POSITION to mouse_pos
    deltax = mouse_pos[0] - START_POSITION[0]
    deltay = mouse_pos[1] - START_POSITION[1]
    distance = math.hypot(deltax, deltay)
    mouse_angle = math.atan2(deltay, deltax) 
    

    if perturbation_mode:
        # calculate perturbed_mouse_angle for each perturbation_type condition
        if perturbation_type == 'sudden':
            perturbed_mouse_angle = mouse_angle + perturbation_angle

        elif perturbation_type == 'gradual':   
            gradual_step = np.min([np.ceil(gradual_attempts/3),10])
            perturbed_mouse_angle = mouse_angle - (gradual_step*perturbation_angle / 10);  
        
        elif perturbation_type == 'random':   
            perturbed_mouse_angle = mouse_angle + perturbation_rand 
                        
        else:
            perturbed_mouse_angle = np.nan
    
        # calculate perturbed_mouse_pos 
        perturbed_mouse_pos = [
        START_POSITION[0] + distance * math.cos(perturbed_mouse_angle),
        START_POSITION[1] + distance * math.sin(perturbed_mouse_angle)
         ]
        circle_pos = perturbed_mouse_pos
    else:
        circle_pos = pygame.mouse.get_pos()
        perturbed_mouse_angle = np.nan
    
    # Check if target is hit or missed
    # hit if circle touches target's center
    if check_target_reached():
        MASK_RADIUS = 1 * TARGET_RADIUS
        score += 1
        attempts += 1
        

        # CALCULATE AND SAVE ERRORS between target and circle end position for a hit
        target_angle = math.atan2(new_target[1] - START_POSITION[1], new_target[0] - START_POSITION[0])    
        circle_end_angle = math.atan2(circle_pos[1] - START_POSITION[1], circle_pos[0] - START_POSITION[0])
        
        if move_faster:
            error_angle = np.nan
            
            """ Create a boolean list with True for each target reached and False for miss or move faster. """
            target_reached_bool += [False]
        else:
            error_angle = circle_end_angle - target_angle
            """ Create a boolean list with True for each target reached and False for miss or move faster. """
            target_reached_bool += [True]
            

        target_pos.append(new_target)
        target_angles.append(target_angle)
        circle_angles.append(circle_end_angle)
        error_angles.append(error_angle)
        perturbed_angels.append(gradual_step)

        new_target = None  # Set target to None to indicate hit
        start_time = 0  # Reset start_time after hitting the target
        if perturbation_type == 'gradual' and perturbation_mode:   
            gradual_attempts += 1
            

    #miss if player leaves the target_radius + 1% tolerance
    elif new_target and math.hypot(circle_pos[0] - START_POSITION[0], circle_pos[1] - START_POSITION[1]) > TARGET_RADIUS*1.01:
        MASK_RADIUS = 1 * TARGET_RADIUS
        attempts += 1
        
        """ Create a boolean list with True for each target reached and False for miss or move faster. """
        target_reached_bool += [False]

        # CALCULATE AND SAVE ERRORS between target and circle end position for a miss
        target_angle = math.atan2(new_target[1] - START_POSITION[1], new_target[0] - START_POSITION[0])    
        circle_end_angle = math.atan2(circle_pos[1] - START_POSITION[1], circle_pos[0] - START_POSITION[0])
        
        if move_faster:
            error_angle = np.nan
        else:
            error_angle = circle_end_angle - target_angle
        
        target_pos.append(new_target)
        target_angles.append(target_angle)
        circle_angles.append(circle_end_angle)
        error_angles.append(error_angle)
        perturbed_angels.append(gradual_step)

        new_target = None  # Set target to None to indicate miss
        start_time = 0  # Reset start_time after missing the target

        if perturbation_type == 'gradual' and perturbation_mode:   
            gradual_attempts += 1
        


    # Check if player moved to the center and generate new target
    if not new_target and at_start_position_and_generate_target(mouse_pos):
        MASK_RADIUS = 0
        new_target = generate_target_position()
        move_faster = False
        start_time = pygame.time.get_ticks()  # Start the timer for the attempt
        perturbation_rand=random.uniform(-math.pi/4, +math.pi/4) # generate new random perturbation for type 'random'
        
        """ Task 4: Create a perturbation angle drawn from a normal distribution with mean and std""" 
    
        
        """ Weight the perturbation angles with a normal distribution """
        angles = np.linspace(-math.pi/4, math.pi/4, 100)
        """ Create  a normal distribution with mean and std """
        weights = stats.norm.pdf(angles, mean, std)
        perturbation_lession = rand.choices(angles, weights=weights, k=1)[0]
        
        


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

    """ Draw the different feedback types"""
    # if attempts > 0:
    #     if feedback == 'trajectory':
    #         draw_old_trajactory(trajactory, attempts, screen)
    #     elif feedback == 'endpos':
    #         pygame.draw.circle(screen, GREY, trajactory[attempts-1][-1], CIRCLE_SIZE // 2)
        
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
    if feedback == 'rl' and attempts > 0:
        if target_reached_bool[-1]:
            color = GREEN
        else:
            color = RED

    elif feedback == 'rl-gradient' and attempts > 0:
        if target_reached_bool[-1]:
            color = GREEN
        else:
            error_angle_degrees = np.abs(np.degrees(error_angles[-1]))
            near_goal_ratio = np.min((error_angle_degrees/30, 1))
            color = near_goal_ratio*np.array(RED) + (1-near_goal_ratio) * np.array(GREEN)
    else:
        color = WHITE

    pygame.draw.circle(screen, color, START_POSITION, 5)        

    # Show attempts
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Attempts: {attempts}", True, WHITE)
    screen.blit(score_text, (10, 40))

    if test_mode:
        # Show score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Show Mouse_angle
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Mouse_Ang: {np.rint(np.degrees(mouse_angle))}", True, WHITE)
        screen.blit(score_text, (10, 70))

        # Show pert_angle
        if perturbation_mode:
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Pert_Ang: {np.rint(np.degrees(perturbed_mouse_angle-mouse_angle))}", True, WHITE)
            screen.blit(score_text, (10, 100))
            if perturbation_type == 'gradual':
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Grad_step: {gradual_step}", True, WHITE)
                screen.blit(score_text, (10, 130))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()

## TASK 1, SAVE IMPORTANT VARIABLES IN .CSV 

# Save important variables in CSV file if test_mode==False:
import pandas as pd
if not test_mode:
    # Create a dictionary containing all variables
    
    """ Multiple attempts for each perturbation type"""
    string_trials = []
    for trial, number in zip(string_attempts, number_attempts):
        string_trials += [trial] * number
        
    changed_feedbacks = []
    for feedback, number in zip(Collected_feedbacks, number_attempts):
        changed_feedbacks += [feedback] * number
    
    changed_angles = []
    for angel, number in zip(Collected_angels, number_attempts):
        changed_angles += [angel] * number
    
    data = {'subject_name': [subject_name] * len(string_trials),
            'target_mode': [target_mode] * len(string_trials),
            'perturbation_type': [perturbation_type] * len(string_trials),
            'trial_number': np.arange(1, len(string_trials)+1),
            'trial_name' : string_trials,
            'feedback_type': changed_feedbacks,
            'target_pos': target_pos,
            'changed_angels': changed_angles,
            'error_angles': error_angles,
            'perturbed_angels': perturbed_angels
            }

        
    # TASK 2 GENERATE A BETTER PLOT


    # Create a dataframe from the dictionary
    df = pd.DataFrame(data)
    # Save dataframe to CSV
    

    
    import os
    if not os.path.exists('Savings'):
        os.makedirs('Savings')
    
    df.to_csv('HW3/Savings/error_angles_gradient_rl_{}.csv'.format(subject_name), header=True, index=False, 
              na_rep=np.NaN)


sys.exit()