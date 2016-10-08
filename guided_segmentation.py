import cv2
import sys
import math
import numpy as np
import dijkstra

from filter_bank import filter_bank

def within_bounds(x, delta_x, y, delta_y, max_x, max_y):
    """
    Returns whether the pixel given by (x + delta_x, y + delta_y) is in the bounds of the image.
    """
    return (x + delta_x) >= 0 and (x + delta_x) < max_x and (y + delta_y) >= 0 and (y + delta_y) < max_y

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
    for x in xrange(len(grayscale)):
        for y in xrange(len(grayscale[0])):
            adj_list[(x, y)] = []
            # Specify the direction to one of its valid neighbors.
            for delta_x in range(-1, 2):
                for delta_y in range(-1, 2):
                    if (delta_x != 0 or delta_y != 0) and within_bounds(x, delta_x, y, delta_y, len(grayscale), len(grayscale[0])):
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
    adj_list = compute_costs(grayscale)
    # Tracks the starting position of the path which the application should draw.
    main.start_point = None
    # mouse callback function
    def draw_path(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            if main.start_point is None:
                main.start_point = (x, y)
            else:
                end_point = (x, y)
                # Draw pixels from start_point to end_point, in color red.
                dist, parent = dijkstra.shortest_path(adj_list, main.start_point)
                # Construct the path itself from the parent dictionary.
                path = []
                temp = end_point
                while temp is not None:
                    path.append(temp)
                    temp = parent[temp]
                # Paint all those pixels red.
                for pixel in path:
                    cv2.circle(color_image, pixel, 1, (0, 0, 255), -1)
                # Get ready for next iteration by refreshing the start_point.
                main.start_point = end_point

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_path)
    while(1):
        cv2.imshow('image', color_image)
        if cv2.waitKey(20) & 0xFF == 27:
            break        
    cv2.destroyAllWindows()


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