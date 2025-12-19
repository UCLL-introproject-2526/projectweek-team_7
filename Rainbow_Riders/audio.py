import pygame

pygame.mixer.init()

# Globale variabele voor jetpack geluid
jetpack_sound = None

def start_background_music():
    MUSIC_FILE = 'Rainbow_Riders\\Assets\\audio\\cyberpunk_moonlight_sonata.mp3'
    
    try:
        background_music = pygame.mixer.Sound(MUSIC_FILE)
        background_music.play(-1) 
        background_music.set_volume(1)

    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van muziek: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def coin_collect_sound():
    COIN_SOUND_FILE = 'Rainbow_Riders\\Assets\\audio\\coin_collect.wav'
    
    try:
        coin_sound = pygame.mixer.Sound(COIN_SOUND_FILE)
        coin_sound.play()
    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van geluidsbestand: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def game_over_sound():
    GAME_OVER_SOUND_FILE = 'Rainbow_Riders\\Assets\\audio\\obstacle_hit.mp3'
    
    try:
        game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_FILE)
        game_over_sound.play()
        game_over_sound.set_volume(1.3)

    except pygame.error as e:
        print(f"Fout bij het laden or afspelen van geluidsbestand: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def stop_background_music():
    pygame.mixer.stop()

def player_laser():
    player_laser_FILE = 'Rainbow_Riders\\Assets\\audio\\player_laser.wav'
    
    try:
        player_laser = pygame.mixer.Sound(player_laser_FILE)
        player_laser.play()
        player_laser.set_volume(1.3)

    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van geluidsbestand: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def audio_jetpack():
    global jetpack_sound
    audio_jetpack_file = 'Rainbow_Riders\\Assets\\audio\\vuur_jetpack.wav'
    
    try:
        jetpack_sound = pygame.mixer.Sound(audio_jetpack_file)
        jetpack_sound.play()
        jetpack_sound.set_volume(0.4)

    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van geluidsbestand: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

def stop_audio_jetpack():
    global jetpack_sound
    if jetpack_sound:
        jetpack_sound.stop()