def draw_solution(image, path, color=None):
    """Given a maze file 'image', draws the solution indicated by 'path'. Returns the manipulated image. Further,
    calculates the total distance traversed by the path we are drawing.
    We can specify the color of the line if we wish; this should be a tuple containing RGB values"""

    # use a variable for the path length so we don't need to call the len() function every time --
    # function calls are more expensive than load operations
    path_length = len(path)
    total_distance = 0

    for i in range(0, path_length - 1):
        # get the current and next node in the path so we know how to draw between them
        current = path[i]
        peek = path[i + 1]

        # if we are comparing values, we can specify what color the line should be; otherwise, draw a gradient
        if color is None:
            # the hue of the line should be a gradient, from blue to red; taken from Mike Pound's implementation
            r = int((i / path_length) * 255)
            px = (r, 0, 255 - r)
        else:
            px = color

        # calculate the distance traversed by the path in the image
        total_distance += (abs(peek[0] - current[0]) + abs(peek[1] - current[1]))

        # if the X values are equal, we have a vertical line
        if current[0] == peek[0]:
            for y in range(min(current[1], peek[1]), max(current[1], peek[1]) + 1):
                image.putpixel((current[0], y), px)

        # otherwise, if the Y values are equal, we have a horizontal line
        elif current[1] == peek[1]:
            for x in range(min(current[0], peek[0]), max(current[0], peek[0])):
                image.putpixel((x, current[1]), px)

    return image, total_distance
