#!/usr/bin/env python3
"""
WhisperOSX - Audio/Video Transcription App
Uses faster-whisper for efficient CPU-based transcription
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
from pathlib import Path
import threading
import multiprocessing
import platform
from faster_whisper import WhisperModel


class WhisperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Transcription Tool")
        self.root.geometry("1000x600")

        # Model will be loaded lazily
        self.model = None
        self.loaded_model_size = None  # Track which model is currently loaded
        self.model_size = tk.StringVar(value="base")
        self.language = tk.StringVar(value="Auto")
        self.current_file = None
        self.segments_data = []  # Store segments with timestamps for SRT export
        self.stop_event = threading.Event()  # Event to signal transcription stop

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Whisper Transcription",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Controls frame
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        # Model selection
        model_frame = tk.Frame(controls_frame)
        model_frame.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(model_frame, text="Model Size:", font=("Helvetica", 11)).pack(side=tk.LEFT, padx=(0, 5))
        self.model_dropdown = tk.OptionMenu(
            model_frame,
            self.model_size,
            "tiny", "base", "small", "medium", "large-v2", "large-v3"
        )
        self.model_dropdown.config(
            font=("Helvetica", 11),
            bg="white",
            fg="black",
            highlightthickness=1,
            relief=tk.RAISED,
            width=12
        )
        self.model_dropdown.pack(side=tk.LEFT)

        # Language selection
        language_frame = tk.Frame(controls_frame)
        language_frame.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(language_frame, text="Language:", font=("Helvetica", 11)).pack(side=tk.LEFT, padx=(0, 5))
        self.language_dropdown = tk.OptionMenu(
            language_frame,
            self.language,
            "Auto",
            "English", "Spanish", "French", "German", "Italian", "Portuguese",
            "Dutch", "Russian", "Chinese", "Japanese", "Korean",
            "Arabic", "Hindi", "Turkish", "Polish", "Ukrainian",
            "Swedish", "Danish", "Norwegian", "Finnish"
        )
        self.language_dropdown.config(
            font=("Helvetica", 11),
            bg="white",
            fg="black",
            highlightthickness=1,
            relief=tk.RAISED,
            width=12
        )
        self.language_dropdown.pack(side=tk.LEFT)

        # Buttons frame (to organize on next row)
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=(10, 10))

        # Select file button
        self.btn_select = tk.Button(
            buttons_frame,
            text="Select File",
            command=self.select_file,
            bg="#E8F5E9",
            fg="#2E7D32",
            font=("Helvetica", 13, "bold"),
            padx=30,
            pady=12,
            relief=tk.RAISED,
            bd=2,
            activebackground="#C8E6C9",
            activeforeground="#1B5E20",
            highlightthickness=0
        )
        self.btn_select.pack(side=tk.LEFT, padx=5)

        # Start button
        self.btn_start = tk.Button(
            buttons_frame,
            text="Start Transcription",
            command=self.start_transcription,
            bg="#E3F2FD",
            fg="#1565C0",
            font=("Helvetica", 13, "bold"),
            padx=30,
            pady=12,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            disabledforeground="#BBDEFB",
            activebackground="#BBDEFB",
            activeforeground="#0D47A1",
            highlightthickness=0
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)

        # Stop button
        self.btn_stop = tk.Button(
            buttons_frame,
            text="Stop",
            command=self.stop_transcription,
            bg="#FFEBEE",
            fg="#C62828",
            font=("Helvetica", 13, "bold"),
            padx=30,
            pady=12,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            disabledforeground="#FFCDD2",
            activebackground="#FFCDD2",
            activeforeground="#B71C1C",
            highlightthickness=0
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        # Save button
        self.btn_save = tk.Button(
            buttons_frame,
            text="Save Text",
            command=self.save_transcription,
            bg="#FFF3E0",
            fg="#E65100",
            font=("Helvetica", 13, "bold"),
            padx=20,
            pady=12,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            disabledforeground="#FFCCBC",
            activebackground="#FFE0B2",
            activeforeground="#BF360C",
            highlightthickness=0
        )
        self.btn_save.pack(side=tk.LEFT, padx=5)

        # Save SRT button
        self.btn_save_srt = tk.Button(
            buttons_frame,
            text="Save SRT",
            command=self.save_srt,
            bg="#F3E5F5",
            fg="#6A1B9A",
            font=("Helvetica", 13, "bold"),
            padx=20,
            pady=12,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            disabledforeground="#CE93D8",
            activebackground="#E1BEE7",
            activeforeground="#4A148C",
            highlightthickness=0
        )
        self.btn_save_srt.pack(side=tk.LEFT, padx=5)

        # Save SRT Words button
        self.btn_save_srt_words = tk.Button(
            buttons_frame,
            text="Save SRT (Words)",
            command=self.save_srt_words,
            bg="#E8F5E9",
            fg="#2E7D32",
            font=("Helvetica", 13, "bold"),
            padx=20,
            pady=12,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            disabledforeground="#A5D6A7",
            activebackground="#C8E6C9",
            activeforeground="#1B5E20",
            highlightthickness=0
        )
        self.btn_save_srt_words.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status = tk.Label(
            main_frame,
            text="Ready. Select a file to begin transcription.",
            fg="#666",
            font=("Helvetica", 10)
        )
        self.status.pack(pady=(0, 5))

        # Hardware info label
        self.hw_info = tk.Label(
            main_frame,
            text="",
            fg="#888",
            font=("Helvetica", 9, "italic")
        )
        self.hw_info.pack(pady=(0, 5))

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=760
        )
        self.progress.pack(pady=(0, 10))

        # Text area for transcription
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(text_frame, text="Transcription:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)

        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            height=20,
            width=80,
            font=("Courier", 11),
            wrap=tk.WORD
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio or Video File",
            filetypes=[
                ("Audio/Video files", "*.mp3 *.mp4 *.wav *.m4a *.avi *.mov *.flac *.ogg *.wma *.aac"),
                ("Audio files", "*.mp3 *.wav *.m4a *.flac *.ogg *.wma *.aac"),
                ("Video files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            # Reset everything when a new file is selected
            self.current_file = file_path
            self.segments_data = []

            # Clear text area
            self.text_area.delete(1.0, tk.END)

            # Reset button states
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.btn_save.config(state=tk.DISABLED)
            self.btn_save_srt.config(state=tk.DISABLED)
            self.btn_save_srt_words.config(state=tk.DISABLED)

            # Update status
            filename = Path(file_path).name
            self.status.config(text=f"Ready: {filename}", fg="#1565C0")

    def start_transcription(self):
        """Start transcription when user clicks Start button"""
        if self.current_file:
            # Clear stop event
            self.stop_event.clear()

            # Start transcription in separate thread
            threading.Thread(target=self.transcribe, args=(self.current_file,), daemon=True).start()

    def stop_transcription(self):
        """Stop ongoing transcription"""
        self.stop_event.set()
        self.status.config(text="Stopping transcription...", fg="#FF9800")

    def detect_hardware(self):
        """Detect available hardware acceleration for Whisper"""
        # Try to detect CUDA (NVIDIA GPU) by checking if ctranslate2 has CUDA support
        try:
            import ctranslate2
            # Check if CUDA is available in ctranslate2
            if hasattr(ctranslate2, 'get_cuda_device_count'):
                cuda_count = ctranslate2.get_cuda_device_count()
                if cuda_count > 0:
                    # Get GPU name if possible
                    try:
                        import torch
                        if torch.cuda.is_available():
                            gpu_name = torch.cuda.get_device_name(0)
                            return "cuda", "float16", f"GPU: {gpu_name} (CUDA)"
                    except ImportError:
                        pass
                    return "cuda", "float16", "GPU: CUDA available"
        except (ImportError, AttributeError):
            pass

        # Fallback to CPU - determine OS for better description
        system = platform.system()
        machine = platform.machine()

        if system == "Darwin":
            # macOS
            if machine == "arm64":
                return "cpu", "int8", "CPU: Apple Silicon (int8 optimized)"
            else:
                return "cpu", "int8", "CPU: Intel Mac (int8 optimized)"
        elif system == "Windows":
            return "cpu", "int8", "CPU: Windows (int8 optimized)"
        elif system == "Linux":
            return "cpu", "int8", "CPU: Linux (int8 optimized)"

        # Default to CPU
        return "cpu", "int8", "CPU (int8 optimized)"

    def load_model(self):
        """Load the Whisper model (lazy loading)"""
        requested_model = self.model_size.get()

        # Only reload if model hasn't been loaded or if a different model is requested
        if self.model is None or self.loaded_model_size != requested_model:
            try:
                self.root.after(0, lambda name=requested_model: self.status.config(text=f"Loading {name} model...", fg="#FF9800"))
                self.root.after(0, lambda: self.root.update())

                # Detect hardware and choose appropriate settings
                device, compute_type, hw_description = self.detect_hardware()

                # Load model with detected settings
                self.model = WhisperModel(
                    requested_model,
                    device=device,
                    compute_type=compute_type
                )

                # Track which model is loaded
                self.loaded_model_size = requested_model

                # Display hardware info
                hw_info_text = f"Running on: {hw_description}"
                self.root.after(0, lambda text=hw_info_text: self.hw_info.config(text=text))

                return True
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Model Error", f"Failed to load model: {msg}"))
                return False
        return True

    def get_language_code(self, language_name):
        """Convert language name to ISO code for Whisper"""
        language_map = {
            "Auto": None,
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Dutch": "nl",
            "Russian": "ru",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko",
            "Arabic": "ar",
            "Hindi": "hi",
            "Turkish": "tr",
            "Polish": "pl",
            "Ukrainian": "uk",
            "Swedish": "sv",
            "Danish": "da",
            "Norwegian": "no",
            "Finnish": "fi"
        }
        return language_map.get(language_name, None)

    def transcribe(self, file_path):
        """Transcribe audio/video file"""
        try:
            # Disable buttons during transcription (on main thread)
            self.root.after(0, lambda: self.btn_select.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_start.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_stop.config(state=tk.NORMAL))  # Enable stop button
            self.root.after(0, lambda: self.btn_save.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_save_srt.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_save_srt_words.config(state=tk.DISABLED))

            # Clear previous transcription
            self.root.after(0, lambda: self.text_area.delete(1.0, tk.END))

            # Clear previous segments data
            self.segments_data = []

            # Start progress bar
            self.root.after(0, lambda: self.progress.start(10))

            filename = Path(file_path).name
            self.root.after(0, lambda fn=filename: self.status.config(text=f"Transcribing: {fn}...", fg="#FF9800"))

            # Load model if needed
            if not self.load_model():
                return

            # Get selected language
            selected_lang = self.language.get()
            lang_code = self.get_language_code(selected_lang)

            # Transcribe with streaming output and word-level timestamps
            # On Windows, use num_workers=1 to avoid multiprocessing issues with PyInstaller
            num_workers = 1 if platform.system() == "Windows" else 2

            segments, info = self.model.transcribe(
                file_path,
                beam_size=5,
                language=lang_code,
                word_timestamps=True,  # Enable word-level timestamps for SRT export
                vad_filter=True,  # Use voice activity detection
                vad_parameters=dict(min_silence_duration_ms=500),
                num_workers=num_workers  # Windows needs 1 worker to avoid crashes
            )

            # Display segments as they're transcribed (streaming)
            detected_lang = "unknown"
            for segment in segments:
                # Check if stop was requested
                if self.stop_event.is_set():
                    self.root.after(0, lambda: self.status.config(text="Transcription stopped by user", fg="#FF9800"))
                    return  # Exit transcription early

                # Store segment data for SRT export
                self.segments_data.append(segment)

                # Format: [00:00:00] Text
                start_time = self.format_timestamp(segment.start)
                line = f"[{start_time}] {segment.text.strip()}\n"

                # Insert text at the end and auto-scroll
                self.root.after(0, lambda text=line: self._append_text(text))

            # Get detected language from info
            detected_lang = info.language if hasattr(info, 'language') else "unknown"
            if lang_code is None:
                status_text = f"✓ Transcription complete! Detected language: {detected_lang}"
            else:
                status_text = f"✓ Transcription complete! Language: {selected_lang}"

            self.root.after(0, lambda st=status_text: self.status.config(text=st, fg="#4CAF50"))

            # Enable save buttons (on main thread)
            self.root.after(0, lambda: self.btn_save.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_save_srt.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_save_srt_words.config(state=tk.NORMAL))

        except Exception as e:
            import traceback
            error_msg = str(e)
            error_traceback = traceback.format_exc()
            print(f"Transcription error: {error_msg}")
            print(f"Traceback:\n{error_traceback}")
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("Transcription Error", f"An error occurred:\n{msg}\n\nCheck console for details."))
            self.root.after(0, lambda msg=error_msg: self.status.config(text=f"Error: {msg}", fg="#F44336"))

        finally:
            # Stop progress bar and re-enable buttons (on main thread)
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.btn_stop.config(state=tk.DISABLED))  # Disable stop button
            self.root.after(0, lambda: self.btn_select.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_start.config(state=tk.NORMAL))

            # Enable save buttons if we have transcribed segments
            if self.segments_data:
                self.root.after(0, lambda: self.btn_save.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.btn_save_srt.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.btn_save_srt_words.config(state=tk.NORMAL))

    def _append_text(self, text):
        """Append text to text area and auto-scroll (must be called on main thread)"""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)  # Auto-scroll to bottom

    def format_timestamp(self, seconds):
        """Convert seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def format_srt_timestamp(self, seconds):
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def generate_srt(self):
        """Generate SRT subtitle format from segments"""
        if not self.segments_data:
            return ""

        srt_content = []
        for i, segment in enumerate(self.segments_data, start=1):
            start_time = self.format_srt_timestamp(segment.start)
            end_time = self.format_srt_timestamp(segment.end)
            text = segment.text.strip()

            srt_content.append(f"{i}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(text)
            srt_content.append("")  # Empty line between entries

        return "\n".join(srt_content)

    def generate_srt_words(self):
        """Generate SRT subtitle format with word-level timestamps (karaoke style)"""
        if not self.segments_data:
            return ""

        srt_content = []
        subtitle_index = 1

        for segment in self.segments_data:
            # Check if segment has word-level timestamps
            if hasattr(segment, 'words') and segment.words:
                words = list(segment.words)

                # Create a subtitle for each word, showing full segment text with current word underlined
                for i, word in enumerate(words):
                    start_time = self.format_srt_timestamp(word.start)
                    end_time = self.format_srt_timestamp(word.end)

                    # Build the text with the current word underlined
                    text_parts = []
                    for j, w in enumerate(words):
                        word_text = w.word.strip()
                        if j == i:
                            # Underline the current word
                            text_parts.append(f"<u>{word_text}</u>")
                        else:
                            text_parts.append(word_text)

                    text = " ".join(text_parts)

                    srt_content.append(f"{subtitle_index}")
                    srt_content.append(f"{start_time} --> {end_time}")
                    srt_content.append(text)
                    srt_content.append("")  # Empty line between entries

                    subtitle_index += 1
            else:
                # Fallback to segment-level if words not available
                start_time = self.format_srt_timestamp(segment.start)
                end_time = self.format_srt_timestamp(segment.end)
                text = segment.text.strip()

                srt_content.append(f"{subtitle_index}")
                srt_content.append(f"{start_time} --> {end_time}")
                srt_content.append(text)
                srt_content.append("")

                subtitle_index += 1

        return "\n".join(srt_content)

    def save_transcription(self):
        """Save transcription to a text file"""
        if not self.current_file:
            return

        # Suggest filename based on input file
        input_path = Path(self.current_file)
        default_name = input_path.stem + "_transcription.txt"

        save_path = filedialog.asksaveasfilename(
            title="Save Transcription",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if save_path:
            try:
                transcription = self.text_area.get(1.0, tk.END).strip()
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(transcription)

                messagebox.showinfo("Success", f"Transcription saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")

    def save_srt(self):
        """Save transcription as SRT subtitle file"""
        if not self.current_file or not self.segments_data:
            return

        # Suggest filename based on input file
        input_path = Path(self.current_file)
        default_name = input_path.stem  # Don't add extension, defaultextension will handle it

        save_path = filedialog.asksaveasfilename(
            title="Save SRT Subtitles",
            defaultextension=".srt",
            initialfile=default_name,
            filetypes=[
                ("SRT files", "*.srt"),
                ("All files", "*.*")
            ]
        )

        if save_path:
            try:
                srt_content = self.generate_srt()
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(srt_content)

                messagebox.showinfo("Success", f"SRT subtitles saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save SRT file: {str(e)}")

    def save_srt_words(self):
        """Save transcription as SRT subtitle file with word-level timestamps"""
        if not self.current_file or not self.segments_data:
            return

        # Suggest filename based on input file
        input_path = Path(self.current_file)
        default_name = input_path.stem + "_words"  # Don't add extension, defaultextension will handle it

        save_path = filedialog.asksaveasfilename(
            title="Save Word-level SRT Subtitles",
            defaultextension=".srt",
            initialfile=default_name,
            filetypes=[
                ("SRT files", "*.srt"),
                ("All files", "*.*")
            ]
        )

        if save_path:
            try:
                srt_content = self.generate_srt_words()
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(srt_content)

                messagebox.showinfo("Success", f"Word-level SRT subtitles saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save SRT file: {str(e)}")


def main():
    multiprocessing.freeze_support()  # Required for PyInstaller on macOS
    root = tk.Tk()
    app = WhisperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
