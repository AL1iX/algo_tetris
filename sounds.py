import pygame
import struct
import math
import os

SOUNDS_DIR = "sound_cache"

def generate_square_wave(frequency, duration, volume=0.3, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    samples = []
    period = sample_rate / frequency
    
    for i in range(n_samples):
        if (i // (period / 2)) % 2 == 0:
            val = int(32767 * volume)
        else:
            val = int(-32767 * volume)
        samples.append(struct.pack('<h', val))
    
    return b''.join(samples)

def generate_noise(duration, volume=0.2, sample_rate=22050):
    import random
    n_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(n_samples):
        val = int(random.randint(-32767, 32767) * volume)
        samples.append(struct.pack('<h', val))
    
    return b''.join(samples)

def generate_sweep(freq_start, freq_end, duration, volume=0.3, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(n_samples):
        t = i / n_samples
        freq = freq_start + (freq_end - freq_start) * t
        period = sample_rate / freq
        
        if (i // (period / 2)) % 2 == 0:
            val = int(32767 * volume * (1 - t * 0.5))
        else:
            val = int(-32767 * volume * (1 - t * 0.5))
        samples.append(struct.pack('<h', val))
    
    return b''.join(samples)

def create_wav_file(filename, audio_data, sample_rate=22050):
    with open(filename, 'wb') as f:
        n_samples = len(audio_data) // 2
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(audio_data)))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', len(audio_data)))
        f.write(audio_data)

def init_sounds():
    if not os.path.exists(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR)
    
    sounds = {}
    
    move_file = os.path.join(SOUNDS_DIR, "move.wav")
    if not os.path.exists(move_file):
        data = generate_square_wave(200, 0.05, 0.15)
        create_wav_file(move_file, data)
    sounds['move'] = pygame.mixer.Sound(move_file)
    
    rotate_file = os.path.join(SOUNDS_DIR, "rotate.wav")
    if not os.path.exists(rotate_file):
        data = generate_sweep(300, 600, 0.08, 0.2)
        create_wav_file(rotate_file, data)
    sounds['rotate'] = pygame.mixer.Sound(rotate_file)
    
    drop_file = os.path.join(SOUNDS_DIR, "drop.wav")
    if not os.path.exists(drop_file):
        data = generate_sweep(400, 100, 0.15, 0.25)
        create_wav_file(drop_file, data)
    sounds['drop'] = pygame.mixer.Sound(drop_file)
    
    clear_file = os.path.join(SOUNDS_DIR, "clear.wav")
    if not os.path.exists(clear_file):
        data1 = generate_square_wave(523, 0.1, 0.25)
        data2 = generate_square_wave(659, 0.1, 0.25)
        data3 = generate_square_wave(784, 0.15, 0.25)
        create_wav_file(clear_file, data1 + data2 + data3)
    sounds['clear'] = pygame.mixer.Sound(clear_file)
    
    gameover_file = os.path.join(SOUNDS_DIR, "gameover.wav")
    if not os.path.exists(gameover_file):
        data1 = generate_square_wave(400, 0.2, 0.3)
        data2 = generate_square_wave(300, 0.2, 0.3)
        data3 = generate_square_wave(200, 0.4, 0.3)
        create_wav_file(gameover_file, data1 + data2 + data3)
    sounds['gameover'] = pygame.mixer.Sound(gameover_file)
    
    levelup_file = os.path.join(SOUNDS_DIR, "levelup.wav")
    if not os.path.exists(levelup_file):
        data1 = generate_square_wave(523, 0.1, 0.2)
        data2 = generate_square_wave(659, 0.1, 0.2)
        data3 = generate_square_wave(784, 0.1, 0.2)
        data4 = generate_square_wave(1047, 0.2, 0.25)
        create_wav_file(levelup_file, data1 + data2 + data3 + data4)
    sounds['levelup'] = pygame.mixer.Sound(levelup_file)
    
    return sounds

def play_sound(sounds, name):
    if sounds and name in sounds:
        sounds[name].play()
