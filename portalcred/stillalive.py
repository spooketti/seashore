subWindowWidth = 55
mainWindowHeight = 28
creditWindowHeight = 14
workspace = [[' ' for _ in range(112)] for _ in range(59)]

def drawHorizontalBars():
    offset = -(subWindowWidth + 1)
    subOffset = 30
    for j in range(2):
        offset += (subWindowWidth + 1)
        subOffset -= 30
        for i in range(subWindowWidth):
            workspace[0][i+offset] = "-"
            workspace[58+subOffset][i+offset] = "_"

def drawSideBars():
    y = 2
    amountDrawn = 0
    while(amountDrawn<mainWindowHeight):
        amountDrawn += 1
        workspace[y][0] = "|"
        workspace[y][subWindowWidth-1] = "|"
        workspace[y][subWindowWidth] = "|"
        if(amountDrawn<=creditWindowHeight):
            workspace[y][111] = "|"
        y += 2

def driver():
    drawHorizontalBars()
    drawSideBars()
    result = "\n".join("".join(row) for row in workspace)
    print(result)

driver()