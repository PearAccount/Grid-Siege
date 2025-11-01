import pygame, sys
from enum import Enum
from .settings import WIDTH, HEIGHT, FPS, LEVELS
from .scenes import MenuScreen, LevelSelectScreen, GameScene, VictoryScreen

class GameState(Enum): 
    MENU = 0
    LEVEL_SELECT = 1
    PLAYING = 2
    PAUSED = 3
    VICTORY = 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Grid Siege')
    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('consolas',18)
    state = GameState.MENU
    current_scene = None
    victory_screen = None

    def goto_menu():
        nonlocal state 
        state = GameState.MENU
        pygame.mouse.set_visible(True)

    def goto_level_select():
        nonlocal state
        state = GameState.LEVEL_SELECT
        
    def start_play(level_path):
        nonlocal state,current_scene
        current_scene = GameScene(screen,font,level_path)
        current_scene.load_level(level_path)
        victory_screen = None
        state = GameState.PLAYING
        pygame.mouse.set_visible(False)

    def goto_victory():
        nonlocal state, victory_screen
        pygame.mouse.set_visible(True)
        victory_screen = VictoryScreen(screen, on_menu=goto_menu)
        state = GameState.VICTORY

    def quit_game(): 
        pygame.quit()
        sys.exit(0)

    menu = MenuScreen(screen, go_to_level_select=goto_level_select, quit_game=quit_game)
    level_select = LevelSelectScreen(screen, levels=LEVELS, on_choose_level=start_play, on_back=goto_menu)
    paused_font = pygame.font.SysFont(None,56)
    paused_small = pygame.font.SysFont(None,30)
    
    running=True
    while running:
        dt = clock.tick(FPS)/1000.0
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT: 
                running=False
            if state == GameState.MENU: 
                menu.handle_event(e)
            elif state == GameState.LEVEL_SELECT:
                level_select.handle_event(e)
            elif state == GameState.PLAYING:
                if e.type == pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                    state=GameState.PAUSED
            elif state == GameState.PAUSED:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        state=GameState.PLAYING
                    elif e.key == pygame.K_r:
                        if current_scene:
                            current_scene.load_level(current_scene.level_path); state = GameState.PLAYING
                    elif e.key==pygame.K_m:
                        goto_menu()
            elif state == GameState.VICTORY:
                if victory_screen:
                    victory_screen.handle_event(e)
            

        if state == GameState.MENU:
            menu.draw()
        elif state == GameState.LEVEL_SELECT:
            level_select.draw()
        elif state == GameState.PLAYING:
            if current_scene is None:
                goto_level_select()
            else:
                result = current_scene.step(dt, events)   # <-- capture result
                if result == "victory":                   # <-- handle win signal
                    goto_victory()
        elif state == GameState.VICTORY:
            if current_scene: current_scene.step(0, [])
            if victory_screen: victory_screen.draw()
        elif state == GameState.PAUSED:
            if current_scene: current_scene.step(0, [])
            veil = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            veil.fill((0,0,0,150))
            screen.blit(veil,(0,0))
            pausetext = paused_font.render('Paused',True,(240,240,240))
            pausesub = paused_small.render('ESC: Resume   R: Restart   M: Menu',True,(230,230,230))
            w,h = screen.get_size()
            screen.blit(pausetext,(w//2-pausetext.get_width()//2,h//2-60))
            screen.blit(pausesub,(w//2-pausesub.get_width()//2,h//2))
        pygame.display.flip()
    pygame.quit(); sys.exit(0)
