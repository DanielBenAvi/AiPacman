
if __name__ == '__main__':
    pos = (1,1)

    direction = (0,1)
    # invert the direction
    direction = (-direction[0], -direction[1])

    # add the direction to the position
    pos = (pos[0] + direction[0], pos[1] + direction[1])


    print(pos)  # (1, 2)
