import random
import pygame

pygame.mixer.init()

def start_background_music():
    MUSIC_FILE = 'Rainbow_joyride-Copy\\audio\\Cyberpunk_Moonlight_Sonata.mp3'
    
    try:
        background_music = pygame.mixer.Sound(MUSIC_FILE)
        background_music.play(-1) 
        background_music.set_volume(1)

    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van muziek: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def coin_collect_sound():
    COIN_SOUND_FILE = 'Rainbow_joyride-Copy\\audio\\coin_collect.wav'
    
    try:
        coin_sound = pygame.mixer.Sound(COIN_SOUND_FILE)
        coin_sound.play()
    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van geluidsbestand: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def game_over_sound():
    GAME_OVER_SOUND_FILE = 'Rainbow_joyride-Copy\\audio\\game_over.mp3'
    
    try:
        game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_FILE)
        game_over_sound.play()
        game_over_sound.set_volume(1.3)

    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van geluidsbestand: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def stop_background_music():
    pygame.mixer.stop()