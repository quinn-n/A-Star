#!/usr/bin/env python3

"""
getpath.py
uses astar to find a path from a red pixel in an image to a blue pixel in an image
"""

import os
from sys import argv
import time

import math

from PIL import Image

from node import Node, dist

def a_star(nodes, start_pos: tuple, end_pos: tuple):
    """Finds a path from start_pos to end_pos using a*
    it is up to the user to follow the path back up the parent tree from the end node"""
    end_node = nodes[end_pos[0]][end_pos[1]]
    start_node = nodes[start_pos[0]][start_pos[1]]
    open_nodes = [start_node]
    while not end_node.closed:
        cur_idx = lowest_f_idx(open_nodes)
        cur_node = open_nodes[cur_idx]
        #print("Cur f: " + str(cur_node.f) + " " * 40, end="\r", flush=True)
        cur_node.closed = True
        x, y = cur_node.pos
        #Calculate g, h, and f values for the 8 nodes around the adjacent node
        for y_offset in range(-1, 2):
            #Check y bondary
            if y + y_offset < 0 or y + y_offset >= len(nodes):
                continue
            for x_offset in range(-1, 2):
                #Check x boundary
                if x + x_offset < 0 or x + x_offset >= len(nodes):
                    continue
                if (x_offset, y_offset) == (0, 0):
                    continue
                offset_node = nodes[x + x_offset][y + y_offset]
                #Skip non-walkable and/or closed nodes
                if not offset_node.walkable or offset_node.closed:
                    continue
                new_g = dist(cur_node.pos, offset_node.pos)
                if new_g < offset_node.g:
                    offset_node.g = new_g
                    offset_node.calc_h(end_pos)
                    offset_node.calc_f()
                    offset_node.parent = cur_node
                    if not offset_node in open_nodes:
                        open_nodes.append(offset_node)
        del open_nodes[cur_idx]

def lowest_f(nodes: list):
    """Returns the node in nodes with the lowest f value
    Returns None if nodes is empty"""
    if not len(nodes):
        return None

    lowest = nodes[0]
    for node in nodes[1:]:
        if node.f < lowest.f:
            lowest = node
    return lowest

def lowest_f_idx(nodes: list):
    """Returns the index of the node with the lowest f value
    returns None if nodes is an empty list"""
    if not len(nodes):
        return None
    
    idx = 0
    for i in range(1, len(nodes)):
        if nodes[i].f < nodes[idx].f:
            idx = i
    return idx

def load_image(img):
    """Loads an image into nodes"""
    px = img.load()
    nodes = []
    for x in range(img.size[0]):
        nodes.append([])
        for y in range(img.size[1]):
            nodes[-1].append(Node((x, y)))
            if px[x, y] == (0, 0, 0):
                nodes[-1][-1].walkable = False
        
    target_pos = find_pixel(img, (0, 0, 255))
    start_pos = find_pixel(img, (255, 0, 0))
    if target_pos == None:
        print("Couldn't find target pixel")
        exit(3)
    if start_pos == None:
        print("Couldn't find start pixel")
        exit(3)
    start_node = nodes[start_pos[0]][start_pos[1]]
    start_node.g = 0
    start_node.calc_h(target_pos)
    start_node.calc_f()
    nodes[target_pos[0]][target_pos[1]].h = 0

    return nodes

def write_path(img, nodes, end_pos):
    """Writes the path from the nodes to img"""
    cur_node = nodes[end_pos[0]][end_pos[1]]
    n = 0
    while cur_node != None:
        img.putpixel(cur_node.pos, (0, 255, 0))
        cur_node = cur_node.parent
        n += 1
    print("Got " + str(n) + " nodes in the path")

def find_pixel(img, target: tuple):
    """Returns the position of a target pixel as a tuple
    Returns None if the pixel is not found"""
    px = img.load()
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if px[x, y] == target:
                return (x, y)
    return None

def print_help():
    """Prints out help message"""
    print("Usage: getpath.py <input img> <output img>")
    print("Uses a* to find a path from the red pixel to the blue pixel in an image")

#Verify inputs
if len(argv) < 3 or "-h" in argv or "--help" in argv:
    print_help()
    exit(1)

input_path = argv[1]
output_path = argv[2]
if not os.path.exists(input_path):
    print(input_path + " does not exist!")
    exit(2)

img = Image.open(input_path).convert("RGB")
nodes = load_image(img)
start_pos = find_pixel(img, (255, 0, 0))
end_pos = find_pixel(img, (0, 0, 255))

s_time = time.time()
a_star(nodes, start_pos, end_pos)
e_time = time.time()
print("Found path in " + str(e_time - s_time) + "s")


write_path(img, nodes, end_pos)
img.putpixel(start_pos, (255, 0, 0))
img.putpixel(end_pos, (0, 0, 255))
img.save(output_path)
