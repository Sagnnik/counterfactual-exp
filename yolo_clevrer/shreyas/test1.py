import csv
import pandas as pd
import math
import numpy as np
import os
import json

import warnings
warnings.filterwarnings("ignore")

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) * 2 + (p1[1] - p2[1]) * 2)

def num(v):
    if v == 1:
        return 'one'
    elif v == 2:
        return 'two'
    elif v == 3:
        return 'three'
    elif v == 4:
        return 'four'
    elif v == 5:
        return 'five'
    elif v == 6:
        return 'six'
    elif v == 7:
        return 'seven'
    elif v == 8:
        return 'eight'
    elif v == 9:
        return 'nine'
    

def get_direction_origin(x_a, y_a):
    direction = ""

    if x_a > 0 and y_a > 0:
        direction = "northeast"
    elif x_a > 0 and y_a < 0:
        direction = "southeast"
    elif x_a < 0 and y_a < 0:
        direction = "southwest"
    elif x_a < 0 and y_a > 0:
        direction = "northwest"
    elif x_a > 0:
        direction = "east"
    elif y_a > 0:
        direction = "north"
    elif x_a < 0:
        direction = "west"
    elif y_a < 0:
        direction = "south"

    return direction

def get_direction(x_a, y_a, x_b, y_b):
    x_diff = x_b - x_a
    y_diff = y_b - y_a
    directions = ""

    angle = math.degrees(math.atan2(y_diff, x_diff))  # Convert negative angles to positive
    if angle<0:
        angle = angle+360

    if angle>337.5 and angle<=22.5 and angle==0 and angle==360:
        directions = 'East'
    elif angle>22.5 and angle<=67.5:
        directions = 'Northeast'
    elif angle>67.5 and angle<=112.5:
        directions = 'North'
    elif angle>112.5 and angle<=157.5:
        directions = 'Northwest'
    elif angle>157.5 and angle<=202.5:
        directions = 'West'
    elif angle>202.5 and angle<=247.5:
        directions = 'Southwest'
    elif angle>247.5 and angle<=292.5:
        directions= 'South'
    elif angle>292.5 and angle<=337.5:
        directions = 'Southeast'

    return directions

def get_direction2(x_a, y_a, x_b, y_b):
    x_diff = x_b - x_a
    y_diff = y_b - y_a
    directions = ""

    angle = math.degrees(math.atan2(y_diff, x_diff))  # Convert negative angles to positive
    if angle<0:
        angle = angle+360

    if angle>337.5 and angle<=22.5 and angle==0 and angle==360:
        directions = 'West'
    elif angle>22.5 and angle<=67.5:
        directions = 'Southwest'
    elif angle>67.5 and angle<=112.5:
        directions = 'South'
    elif angle>112.5 and angle<=157.5:
        directions = 'Southeast'
    elif angle>157.5 and angle<=202.5:
        directions = 'East'
    elif angle>202.5 and angle<=247.5:
        directions = 'Northeast'
    elif angle>247.5 and angle<=292.5:
        directions= 'North'
    elif angle>292.5 and angle<=337.5:
        directions = 'Northwest'

    return directions

def is_colliding(box1, box2):

    x1_box1 = int(box1['x1'].iloc[0])
    y1_box1 = int(box1['y1'].iloc[0])
    x2_box1 = int(box1['x2'].iloc[0])
    y2_box1 = int(box1['y2'].iloc[0])

    x1_box2 = int(box2['x1'])
    y1_box2 = int(box2['y1'])
    x2_box2 = int(box2['x2'])
    y2_box2 = int(box2['y2'])

    centerx_box1 = int((x1_box1 + x2_box1)/2)
    centery_box1 = int((y1_box1 + y2_box1)/2)

    centerx_box2 = int((x1_box2 + x2_box2)/2)
    centery_box2 = int((y1_box2 + y2_box2)/2)

    center_distance = math.sqrt((centerx_box2 - centerx_box1)*2 + (centery_box2 - centery_box1)*2)

    half_width_sum = ((x2_box1 - x1_box1) + (x2_box2 - x1_box2))/2
    half_height_sum = ((y1_box1 - y2_box1) + (y1_box2 - y2_box2))/2

    #print(center_distance, half_width_sum, half_height_sum)

    if half_width_sum >= center_distance:
        return True

    if half_height_sum >= center_distance:
        return True

    else :
        return False

def caldir(center_x1, center_y1, center_x2, center_y2):
    dx = center_x2 - center_x1
    dy = center_y2 - center_y1

    angle_threshold = 22.5
    angle_degrees = (180 / 3.14159265) * math.atan2(dy, dx)
    angle_degrees = (angle_degrees + 360) % 360
    if angle_degrees <= angle_threshold or angle_degrees >= 360 - angle_threshold:
        return "east"
    elif angle_threshold < angle_degrees <= 45 + angle_threshold:
        return "north-east"
    elif 45 + angle_threshold < angle_degrees <= 90 + angle_threshold:
        return "north"
    elif 90 + angle_threshold < angle_degrees <= 135 + angle_threshold:
        return "north-west"
    elif 135 + angle_threshold < angle_degrees <= 180 + angle_threshold:
        return "west"
    elif 180 + angle_threshold < angle_degrees <= 225 + angle_threshold:
        return "south-west"
    elif 225 + angle_threshold < angle_degrees <= 270 + angle_threshold:
        return "south"
    elif 270 + angle_threshold < angle_degrees <= 315 + angle_threshold:
        return "south-east"
    else:
        return "east"

def overlap(center_x, center_y, center_x1, center_y1, height1, width1, heigth2, width2):
    min_distance_x = (width1 / 2) + (width2 / 2)
    min_distance_y = (height1 / 2) + (heigth2 / 2)
    center_distance_x = abs(center_x - center_x1)
    center_distance_y = abs(center_y - center_y1)
 
    if center_distance_x < min_distance_x and center_distance_y < min_distance_y:
        return True
    else:
        return False

df = pd.read_csv('yolo_clevrer/video_15000.csv')
df['class'] = df['class'].apply(lambda x: x.replace('_', ' '))

df['y1'] = -df['y1']
df['y2'] = -df['y2']
df['x1'] -= 256
df['y1'] += 256
df['x2'] -= 256
df['y2'] += 256

df['center_x'] = (df['x1'] + df['x2']) / 2
df['center_y'] = (df['y1'] + df['y2']) / 2

nob = 0
for i in range(125):
    con = df[df['frames'] == f'frame{i}']
    r = len(con)
    if r>nob:
        nob=r
        con2 = con
nob -=1

con = df['frames'] == 'frame0'
class_id = df.loc[con, 'class']
fob = num(len(list(class_id)))

s1=''
s1 = f'Initially there are {fob} static objects. '

frame_0 = df[df['frames'] == 'frame0']
frame_0['center'] = frame_0.apply(lambda row: ((row['x1'] + row['x2']) / 2, (row['y1'] + row['y2']) / 2), axis=1)
s2=''
for index, row in frame_0.iterrows():
    current_center = row['center']
    df_without_current = frame_0[frame_0.index != index]  
    current_object = row['class']
    x1_0 = row['x1']
    y1_0 = row['y1']
    d = get_direction_origin(x1_0, y1_0)
    
    nearest_distance = float('inf')
    nearest_object = None
    nearest_center = None
    
    for _, other_row in df_without_current.iterrows():
        other_center = other_row['center']
        distance = calculate_distance(current_center, other_center)
        
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_object = other_row['class']
            nearest_center = other_center
            x1_1 = other_row['x1']
            y1_1 = other_row['y1']
            

    pos = get_direction2(x1_0, y1_0, x1_1, y1_1)

    s2 = s2+ f'The {current_object} is located in the {d} direction from the origin and {pos} of {nearest_object}. '

    dynamic=[]

for i in range(len(class_present)):
    frame_p = df[df['class'] == class_present[i]]
    frame_p = frame_p.reset_index(drop=True)
    c=0
    z=0
    for j in range(len(frame_p)-20):
        centers1 = frame_p[['center_x', 'center_y']].values[j]
        centers2 = frame_p[['center_x', 'center_y']].values[j+20]
        fr_val = frame_p[['frames']].values[j]
        center_x1 = centers1[0]
        center_y1 = centers1[1]
        center_x2 = centers2[0]
        center_y2 = centers2[1]
        d = caldir(center_x1, center_y1, center_x2, center_y2)
    
        if abs(center_x1 - center_x2)>1 and abs(center_y1 - center_y2)>1 and z==0:
            direction = d
            if c==1: 
                dynamic.append((class_present[i], fr_val[0], d, 'static'))
            else:
                dynamic.append((class_present[i], fr_val[0], d))
                
            z=1
        else:
            c=1

        if abs(center_x1 - center_x2)>1 and abs(center_y1 - center_y2)>1 and z==1:
            if d!=direction:
                if c==1: 
                    dynamic.append((class_present[i], fr_val[0], d, 'static'))
                else:
                    dynamic.append((class_present[i], fr_val[0], d))
                direction=d
        
def sort_key(item):
    frame_str = item[1]  # Get the "Frame" column from the tuple
    numeric_part = ''.join(filter(str.isdigit, frame_str))  # Extract numeric part
    return int(numeric_part)

sorted_dynamic = sorted(dynamic, key=sort_key)

classes=[]
stat_classes=[]
for i in range(len(sorted_dynamic)):
    if len(sorted_dynamic[i])<4:
        classes.append(sorted_dynamic[i][0])
    else:
        stat_classes.append(sorted_dynamic[i][0])

col_classes = list(set(classes))
stat_classes= list(set(stat_classes))

collisions=[]
for items in col_classes:
    for i in range(127):
        frame = df[df['frames'] == f'frame{i}']
        row = frame[frame['class'] == items]
        if len(row)>0:
            centers = row[['x1', 'y1','x2', 'y2','center_x', 'center_y']]
            center_x = int(centers['center_x'])
            center_y = int(centers['center_y'])
            width1 = abs(int(centers['x1']) - int(centers['x2']))
            heigth1 = abs(int(centers['y1']) - int(centers['y2'])) 
            for j in class_present:
                if j!=items:
                    row1 = frame[frame['class'] == j]
                    if len(row1)>0:
                        centers2 = row1[['x1', 'y1','x2', 'y2','center_x', 'center_y', 'frames', 'class']]
                        center_x1 = int(centers2['center_x'])
                        center_y1 = int(centers2['center_y'])
                        width2 = abs(int(centers2['x1']) - int((centers2['x2'])))
                        heigth2 = abs(int(centers2['y1']) - int(centers2['y2']))
                        fr = str(centers2['frames'].iloc[0])
                        cl = str(centers2['class'].iloc[0])
                        o = overlap(center_x, center_y, center_x1, center_y1, heigth1, width1, heigth2, width2)
                        if o is True:
                            collisions.append((items, cl, fr))

unique_tuples = {}
for item in collisions:
    key = item[:2]
    frame = int(item[2].replace('frame', ''))
    if key not in unique_tuples or frame < unique_tuples[key]:
        unique_tuples[key] = frame

result = [(key[0], key[1], f'frame{value}') for key, value in unique_tuples.items()]

collisions2 =[]
for item in result:
    collisions2.append(item)

def sort_key2(item):
    frame_str = item[2]  
    numeric_part = ''.join(filter(str.isdigit, frame_str)) 
    return int(numeric_part)

sorted_collisions = sorted(collisions2, key=sort_key2) 

s4=''
index=0
for i in range(len(sorted_dynamic)):
    ob = sorted_dynamic[i][0]
    fr = sorted_dynamic[i][1]
    d = sorted_dynamic[i][2]
    if len(sorted_dynamic[i])<4:
        s4 = s4 + f'The {ob} is moving in the {d} direction. '

    else:
        for j in range(index, len(sorted_collisions)):
            if sorted_collisions[j][1] == ob:
                s4 = s4 + f'{sorted_collisions[j][0]} collides with {ob} and moves in {d} direction. '
                index +=1
                break

s=s1+s2+s4
print(s)