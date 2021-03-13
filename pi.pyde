# Creates a graphic representing the digits of pi with colors

# 100 rows x 100 columns
rows = 100
row_width = 1500
row_sep = 20
circle_size = 15
# calculate width and height
w = row_width + (row_width // 4)
h = (rows - 1) * row_sep + (row_width // 4)

colors = ['#f5453b', '#ff8a29', '#f6f34e', '#bb1b86', '#b5d2a1',
          '#d11638', '#ffffff', '#6a4a3c', '#52bd97', '#d2f301']

def setup():
    # open file
    with open('pi_dec_1m.txt', 'r') as f:
        dec_pi = f.read()[2:]
    dec_pi = [int(n) for n in dec_pi]
    
    # setup image
    size(w, h)
    global img
    img = createImage(w, h, ARGB)
    
    # increase density
    pixelDensity(2)
    
    # set background color
    background(0)
    
    # start the drawing based on line width 
    x_start = row_width/8
    y_start = row_width/8
    
    # write header
    textFont(createFont("Courier New", 120))
    textAlign(CENTER, TOP)
    fill(255)
    text('Pi', w//2, row_width//32)
    
    # write legend for number colors
    for i in range(10):
        textFont(createFont("Courier New", 48))
        fill(colors[i])
        text(i, x_start//2, y_start + row_sep*i*3)
    
    # for every row, 100 lines
    for i in range(rows):
        # for every circle in row, 100 circles
        for j in range(row_width//15):
            
            # coordinates are center point of circle
            x = x_start + j*15
            y = y_start + (i*row_sep)
            
            # draw circle
            c = colors[dec_pi[i*100+j]]
            fill(c)
            circle(x, y, circle_size)
    
    # save image
    save("pi.png")
    # no loop function necessary
    noLoop()
    
def draw():
    image(img, 0, 0)
