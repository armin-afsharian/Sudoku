import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
L_GREEN = (150, 255, 150)
RED = (255, 0, 0)
L_RED = (255, 204, 203)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
#
pygame.init()
X = 500
Y = 300
size = (X, Y)
window = pygame.display.set_mode(size)
font = pygame.font.Font('freesansbold.ttf', 25)



def drawButton(left, top, color, textInButton):
    rectSize = pygame.Rect(left, top, 100, 30)
    pygame.draw.rect(window, color, rectSize)  # left, top, width, height
    pygame.draw.rect(window, BLACK, rectSize, 3)
    fontButton = pygame.font.Font('freesansbold.ttf', 20)
    textButton = fontButton.render(textInButton, True, BLACK, )
    textRectButton = textButton.get_rect()
    textRectButton.center = (left + 50, top + 15)
    window.blit(textButton, textRectButton)
    return rectSize


def chooseLevel():
    level = 0
    text = font.render('choose difficulty level', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 - 40)

    pygame.display.set_caption("Sudoku King")

    done = True
    while done:
        window.fill(WHITE)
        window.blit(text, textRect)
        drawButton(40, 100, GRAY, "1")
        drawButton(120, 100, GRAY, "2")
        drawButton(200, 100, GRAY, "3")
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("Click ", pos)
                if (40 <= pos[0] <= 100) and (100 <= pos[1] <= 130):
                    level = 1
                if (120 <= pos[0] <= 180) and (100 <= pos[1] <= 130):
                    level = 2
                if (200 <= pos[0] <= 260) and (100 <= pos[1] <= 130):
                    level = 3
                if level != 0:
                    # print(level)
                    pygame.quit()
                    return level

            # Draws the surface object to the screen.
            pygame.display.update()


def enterName():
    text = font.render('Please enter your name', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 - 100)

    pygame.display.set_caption("Sudoku")

    user_text = '' 
  
    # create rectangle 
    input_rect = pygame.Rect(20, 100, 460, 35)
    cursor1 = pygame.SYSTEM_CURSOR_ARROW
    cursor2 = pygame.SYSTEM_CURSOR_HAND  
    
  
    # color_passive store color(chartreuse4) which is 
    # color of input box. 
    color_passive = pygame.Color('chartreuse4') 
    color = color_passive 
    
    while True:
        window.fill(WHITE)
        window.blit(text, textRect)
        submitButton = drawButton(X // 2 - 50, Y // 2 + 50, L_GREEN, "Submit")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submitButton.collidepoint(event.pos):
                    pygame.mouse.set_cursor(cursor1) 
                    return user_text
            if event.type == pygame.KEYDOWN: 
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
    
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1] 
    
                # Unicode standard is used for string 
                # formation
                elif event.key == pygame.K_RETURN:
                    pygame.mouse.set_cursor(cursor1) 
                    return user_text
                elif event.unicode.isalpha(): 
                    user_text += event.unicode
          
        # draw rectangle and argument passed which should 
        # be on screen 
        pos = pygame.mouse.get_pos()

        if(submitButton.collidepoint(pos)):
            pygame.mouse.set_cursor(cursor2)
        else:
            pygame.mouse.set_cursor(cursor1)
         
        pygame.draw.rect(window, color, input_rect) 
    
        text_surface = font.render(user_text, True, (255, 255, 255)) 
        
        # render at position stated in arguments 
        window.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
        
        # set width of textfield so that text cannot get 
        # outside of user's text input 
        #input_rect.w = max(400, text_surface.get_width()+10)
        pygame.display.update() 
        
        # display.flip() will update only a portion of the 
        # screen to updated, not full area 