"""
Audio system for sound effects and music
"""

import pygame
import os


class AudioManager:
    """Manages game audio"""
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.sounds = {}
        self.music_playing = False
        
        # Initialize mixer if enabled
        if enabled:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            except:
                self.enabled = False
                print("Warning: Audio initialization failed")
    
    def load_sound(self, name: str, filepath: str):
        """Load a sound effect"""
        if not self.enabled:
            return
        
        try:
            if os.path.exists(filepath):
                self.sounds[name] = pygame.mixer.Sound(filepath)
            else:
                # Create silent sound as placeholder
                self.sounds[name] = None
        except Exception as e:
            print(f"Warning: Could not load sound {name}: {e}")
            self.sounds[name] = None
    
    def play_sound(self, name: str, volume=0.5):
        """Play a sound effect"""
        if not self.enabled or name not in self.sounds:
            return
        
        if self.sounds[name]:
            try:
                self.sounds[name].set_volume(volume)
                self.sounds[name].play()
            except:
                pass
    
    def play_music(self, filepath: str, loops=-1, volume=0.3):
        """Play background music"""
        if not self.enabled:
            return
        
        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
                self.music_playing = True
        except Exception as e:
            print(f"Warning: Could not play music: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if self.enabled:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        if self.enabled:
            pygame.mixer.music.set_volume(volume)
            for sound in self.sounds.values():
                if sound:
                    sound.set_volume(volume)


# Create global audio manager instance
audio_manager = AudioManager(enabled=False)  # Disabled by default (no sound files yet)
