def move_to_line(driver, size, location, move, player_color):
    # print('bh_size:' + str(size), 'bh_location:' + str(location))
    square_size = int(size / 8 * 1)
    half = square_size / 2

    # print(player_color)

    # Calculate numerical values directly from letters
    sq_l1 = ord(move[0]) - 96
    sq_n1 = int(move[1])
    sq_l2 = ord(move[2]) - 96
    sq_n2 = int(move[3])

    if player_color == 'black':
        # Reverse numerical values if player is black
        sq_l1 = 9 - sq_l1
        sq_l2 = 9 - sq_l2
        sq_n1 = 9 - sq_n1
        sq_n2 = 9 - sq_n2

    x1 = location["x"] + sq_l1 * square_size - half
    y1 = location["y"] + (8 - sq_n1 + 1) * square_size - half
    x2 = location["x"] + sq_l2 * square_size - half
    y2 = location["y"] + (8 - sq_n2 + 1) * square_size - half

    # Check if the canvas element exists
    canvas = driver.execute_script("""
    var canvas = document.getElementById('chessboard-canvas');

    if (canvas) {
        // If the line exists, update its coordinates
        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height); // clear canvas
        ctx.beginPath();
        ctx.moveTo(%s, %s);
        ctx.lineTo(%s, %s);
        ctx.strokeStyle = 'green';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
""" % (x1, y1, x2, y2))


