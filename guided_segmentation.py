import cv2
import sys
import math
import numpy as np

from filter_bank import filter_bank

def compute_costs(grayscale):
    """
    Computes the costs for each edge in the graph represented by the grayscale input image.

    @param      grayscale           A grayscale input image
    @return     adj_list            A weighted adjacency list representation of the pixel graph represented by the input image
    """
    # Create a set of images that result from convolution of "grayscale" with each of the cross-correlation filters.        
    filtered_images = {}
    for direction, filt in filter_bank.items():
        filtered_images[direction] = np.absolute(cv2.filter2D(grayscale, -1, filt))
    max_filter_response = max(np.max(f_img) for f_img in filtered_images.values())
    
    # Initialize the adjacency list representation of the weighted pixel graph.
    adj_list = {}        

    # Specify a pixel in the image. Recall that the "x" direction is vertical and "y" direction is horizontal, by convention.
    for x in xrange(1, len(grayscale) - 1):
        for y in xrange(1, len(grayscale[0]) - 1):
            adj_list[(x, y)] = []
            # Specify the direction to one of its neighbors.
            for delta_x in range(-1, 2):
                for delta_y in range(-1, 2):
                    if delta_x != 0 and delta_y != 0:
                        # Cost[neigbhor] = (max - filter_response) * distance_to_neighbor
                        cost = (max_filter_response - filtered_images[(delta_x, delta_y)][x][y]) * math.sqrt(delta_x ** 2 + delta_y ** 2)
                        adj_list[(x, y)].append(((x + delta_x, y + delta_y), cost))
    return adj_list

def main(image_filename):    
    """
    Executes interactive segmentation on an input image using Dijkstra's algorithm.

    @param      image_filename      The path to the input image
    """
    # Read in the image and convert to grayscale for ease of computation.
    color_image = cv2.imread(image_filename)         
    grayscale = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
    # Precompute the cost matrix (and by extension, the adjacency list) for the input image.
    compute_costs(grayscale)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print >>sys.stderr, "Please specify an appropriate set of command-line arguments. Run with -h flag for more details."
        sys.exit(1)
    if args[1] == "-h":
        print "guided_segmentation.py"
        print "Author: Sujay Tadwalkar"
        print
        print "Command Syntax:"
        print "python guided_segmentation.py [options]"
        print
        print "Options:"
        print "-h".ljust(40), "shows this help message".ljust(50)
        print "<input_filepath>".ljust(40), "input_filepath  is the path (absolute or relative) to the input image".ljust(50)
        print 
        sys.exit(0)            
    main(args[1])