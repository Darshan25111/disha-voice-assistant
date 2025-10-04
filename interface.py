import tkinter as tk
import threading
import time
import random
import numpy as np
import speech_recognition as sr

def interpolate_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

class DishaInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Disha Assistant")
        self.root.geometry("500x400")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Circle and halo
        self.circle = self.canvas.create_oval(200, 150, 300, 250, fill="#1f77b4", outline="")
        self.halo = self.canvas.create_oval(190, 140, 310, 260, outline="#00ffff", width=4)
        self.status_text = self.canvas.create_text(250, 350, text="Idle", fill="white", font=("Helvetica", 14))

        # Voice amplitude bars
        self.bars = [self.canvas.create_rectangle(50 + i*40, 250, 70 + i*40, 250, fill="#ff6347", outline="") for i in range(10)]

        # Particles
        self.particles = []
        for _ in range(30):
            x = 250
            y = 200
            dx = random.uniform(-2,2)
            dy = random.uniform(-2,2)
            size = random.randint(2,5)
            particle = {'x':x,'y':y,'dx':dx,'dy':dy,'size':size,
                        'id':self.canvas.create_oval(x,x+size,y,y+size,fill="#00ffff", outline="")}
            self.particles.append(particle)

        self.running = True
        self.listening = False
        self.processing = False
        self.error = False
        self.voice_amplitude = 0

        # Animation thread
        self.thread = threading.Thread(target=self.animate)
        self.thread.daemon = True
        self.thread.start()

        # Mic amplitude thread
        self.mic_thread = threading.Thread(target=self.listen_to_mic)
        self.mic_thread.daemon = True
        self.mic_thread.start()

    def set_status(self, text):
        self.canvas.itemconfig(self.status_text, text=text)

    def set_listening(self, state=True):
        self.listening = state
        self.processing = False
        self.error = False

    def set_processing(self, state=True):
        self.processing = state
        self.listening = False
        self.error = False

    def set_error(self, state=True):
        self.error = state
        self.listening = False
        self.processing = False

    def update_particles(self):
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            if p['x'] < 200 or p['x'] > 300: p['dx'] *= -1
            if p['y'] < 150 or p['y'] > 250: p['dy'] *= -1
            self.canvas.coords(p['id'], p['x'], p['y'], p['x']+p['size'], p['y']+p['size'])

    def listen_to_mic(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        while self.running:
            try:
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=1)
                    samples = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    self.voice_amplitude = np.abs(samples).mean()/5000
            except:
                self.voice_amplitude = 0

    def animate(self):
        size = 50
        halo_offset = 0
        halo_growing = True
        while self.running:
            if self.error: target_color = (255,0,0)
            elif self.processing: target_color = (255,255,0)
            elif self.listening: target_color = (0,255,0)
            else: target_color = (31,119,180)

            current_color = self.hex_to_rgb(self.canvas.itemcget(self.circle,"fill"))
            new_color = interpolate_color(current_color, target_color, 0.1)
            self.canvas.itemconfig(self.circle, fill=rgb_to_hex(new_color))

            dynamic_size = size + self.voice_amplitude*50
            self.canvas.coords(self.circle,250-dynamic_size,200-dynamic_size,250+dynamic_size,200+dynamic_size)

            if halo_growing: halo_offset += 1
            else: halo_offset -=1
            if halo_offset>15: halo_growing=False
            if halo_offset<0: halo_growing=True
            self.canvas.coords(self.halo,250-dynamic_size-halo_offset,200-dynamic_size-halo_offset,
                               250+dynamic_size+halo_offset,200+dynamic_size+halo_offset)

            self.update_particles()
            self.root.update()
            time.sleep(0.02)

    def hex_to_rgb(self, hex_color):
        hex_color=hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2],16) for i in (0,2,4))

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.running=False
        self.root.destroy()
