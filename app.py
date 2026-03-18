#!/usr/bin/env python3
"""
🏭 Lior Pozin's Branding Factory — Desktop App
=================================================
A visual GUI for Reut to run the branding factory
without touching the terminal.
"""

import os
import sys
import io
import threading
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


# ============================================================
# Stdout capture — pipes agent print() into the GUI log
# ============================================================
class GUILogWriter(io.TextIOBase):
    """Intercepts sys.stdout so agent print() calls appear in the GUI log."""
    def __init__(self, callback, original_stdout):
        super().__init__()
        self.callback = callback
        self.original = original_stdout

    def write(self, text):
        if text and text.strip():
            self.callback(text.rstrip())
        # Also write to original stdout (useful if launched from terminal)
        if self.original:
            try:
                self.original.write(text)
                self.original.flush()
            except Exception:
                pass
        return len(text) if text else 0

    def flush(self):
        if self.original:
            try:
                self.original.flush()
            except Exception:
                pass


# ============================================================
# Color scheme & styling
# ============================================================
COLORS = {
    "bg": "#1a1a2e",
    "surface": "#16213e",
    "card": "#0f3460",
    "accent": "#e94560",
    "accent_hover": "#ff6b81",
    "text": "#ffffff",
    "text_dim": "#a0a0b8",
    "success": "#2ecc71",
    "warning": "#f39c12",
    "border": "#2a2a4a",
}


class BrandingFactoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lior Pozin's Branding Factory")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(800, 600)

        # State
        self.ideas = []
        self.selected_idea = None
        self.is_running = False
        self.final_state = None

        # Thread-safe queue for cross-thread UI updates (macOS Tkinter
        # does not reliably process root.after() calls from non-main threads)
        self._ui_queue = queue.Queue()
        self._poll_ui_queue()

        # Build UI
        self._build_header()
        self._build_main_area()
        self._build_footer()

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 900) // 2
        y = (self.root.winfo_screenheight() - 700) // 2
        self.root.geometry(f"900x700+{x}+{y}")

    # ============================================================
    # Header
    # ============================================================
    def _build_header(self):
        header = tk.Frame(self.root, bg=COLORS["surface"], pady=15)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="🏭  Lior Pozin's Branding Factory",
            font=("Helvetica Neue", 22, "bold"),
            fg=COLORS["text"],
            bg=COLORS["surface"],
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Generate personalized social media content — powered by AI agents",
            font=("Helvetica Neue", 12),
            fg=COLORS["text_dim"],
            bg=COLORS["surface"],
        )
        subtitle.pack(pady=(2, 0))

    # ============================================================
    # Main content area (switches between screens)
    # ============================================================
    def _build_main_area(self):
        self.main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self._show_start_screen()

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ============================================================
    # Thread-safe UI updates (macOS Tk fix)
    # ============================================================
    def _schedule_on_main(self, callback):
        """Queue a callable to run on the Tk main thread.
        
        On macOS, root.after() from a background thread is unreliable.
        Instead we put callbacks in a queue and a main-thread poller
        drains it every 50 ms.
        """
        self._ui_queue.put(callback)

    def _poll_ui_queue(self):
        """Main-thread poller: drain the queue and execute callbacks."""
        try:
            while True:
                callback = self._ui_queue.get_nowait()
                try:
                    callback()
                except Exception as e:
                    sys.stderr.write(f"[UI-QUEUE-ERR] {e}\n")
                    sys.stderr.flush()
        except queue.Empty:
            pass
        # Re-schedule ourselves — always keep polling
        self.root.after(50, self._poll_ui_queue)

    # ============================================================
    # Screen 1: Start
    # ============================================================
    def _show_start_screen(self):
        self._clear_main()

        spacer = tk.Frame(self.main_frame, bg=COLORS["bg"], height=60)
        spacer.pack()

        # Big factory emoji
        emoji = tk.Label(
            self.main_frame,
            text="🏭",
            font=("Helvetica Neue", 64),
            bg=COLORS["bg"],
        )
        emoji.pack(pady=(0, 10))

        info = tk.Label(
            self.main_frame,
            text="Scout trends → Pick an idea → Generate drafts → Save to Obsidian",
            font=("Helvetica Neue", 13),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        info.pack(pady=(0, 30))

        # Start button
        start_btn = tk.Button(
            self.main_frame,
            text="▶  Start the Factory",
            font=("Helvetica Neue", 16, "bold"),
            fg=COLORS["text"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self._on_start,
        )
        start_btn.pack()

        # Last run info
        today = datetime.now().strftime("%A, %B %d, %Y")
        date_label = tk.Label(
            self.main_frame,
            text=f"Today: {today}",
            font=("Helvetica Neue", 11),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        date_label.pack(pady=(20, 0))

    # ============================================================
    # Screen 2: Progress (agents running)
    # ============================================================
    def _show_progress_screen(self):
        self._clear_main()

        self._activity_dots = 0
        self.progress_title = tk.Label(
            self.main_frame,
            text="🔄  Agents are working...",
            font=("Helvetica Neue", 18, "bold"),
            fg=COLORS["text"],
            bg=COLORS["bg"],
        )
        self.progress_title.pack(pady=(20, 10))

        # Animate dots so Reut sees the app is alive
        self._animate_title()

        # Progress bar
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=COLORS["surface"],
            background=COLORS["accent"],
            thickness=8,
        )
        self.progress = ttk.Progressbar(
            self.main_frame,
            style="Custom.Horizontal.TProgressbar",
            length=500,
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(pady=(10, 5))

        self.progress_label = tk.Label(
            self.main_frame,
            text="Loading context...",
            font=("Helvetica Neue", 12),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        self.progress_label.pack()

        # Log area
        log_frame = tk.Frame(self.main_frame, bg=COLORS["surface"], padx=2, pady=2)
        log_frame.pack(fill="both", expand=True, pady=(15, 0))

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("SF Mono", 11),
            bg=COLORS["surface"],
            fg=COLORS["text_dim"],
            insertbackground=COLORS["text"],
            relief="flat",
            wrap="word",
            state="disabled",
        )
        self.log_text.pack(fill="both", expand=True)

    def _log(self, message: str):
        """Append a message to the log area (thread-safe via queue)."""
        def _update():
            try:
                if hasattr(self, 'log_text') and self.log_text.winfo_exists():
                    self.log_text.config(state="normal")
                    self.log_text.insert("end", message + "\n")
                    self.log_text.see("end")
                    self.log_text.config(state="disabled")
            except Exception:
                pass
        self._schedule_on_main(_update)

    def _set_progress(self, value: int, label: str):
        """Update progress bar (thread-safe via queue)."""
        def _update():
            try:
                if hasattr(self, 'progress') and self.progress.winfo_exists():
                    self.progress["value"] = value
                if hasattr(self, 'progress_label') and self.progress_label.winfo_exists():
                    self.progress_label.config(text=label)
            except Exception:
                pass
        self._schedule_on_main(_update)

    def _animate_title(self):
        """Pulse the title dots so Reut sees the app is alive."""
        if not self.is_running:
            return
        self._activity_dots = (self._activity_dots % 3) + 1
        dots = "." * self._activity_dots + " " * (3 - self._activity_dots)
        self.progress_title.config(text=f"🔄  Agents are working{dots}")
        self.root.after(600, self._animate_title)

    # ============================================================
    # Screen 3: Pick an idea (or write your own)
    # ============================================================
    def _show_idea_selection(self, ideas: list):
        self._clear_main()

        title = tk.Label(
            self.main_frame,
            text="💡  Choose Your Content Direction",
            font=("Helvetica Neue", 18, "bold"),
            fg=COLORS["text"],
            bg=COLORS["bg"],
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            self.main_frame,
            text="Pick an AI idea, edit one to make it yours, or write something completely new:",
            font=("Helvetica Neue", 12),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        subtitle.pack(pady=(0, 10))

        # Scrollable area
        canvas = tk.Canvas(self.main_frame, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        self._cards_frame = tk.Frame(canvas, bg=COLORS["bg"])

        self._cards_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self._cards_frame, anchor="nw", tags="inner")

        # Make the inner frame stretch to canvas width
        def _on_canvas_configure(event):
            canvas.itemconfig("inner", width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ── "Write Your Own" section at the top ──
        self._create_custom_idea_section(self._cards_frame)

        # ── Separator ──
        sep_frame = tk.Frame(self._cards_frame, bg=COLORS["bg"], pady=8)
        sep_frame.pack(fill="x", padx=5)
        sep_label = tk.Label(
            sep_frame,
            text="── or pick one of the AI suggestions below ──",
            font=("Helvetica Neue", 11),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        sep_label.pack()

        # ── AI Idea cards ──
        for i, idea in enumerate(ideas):
            self._create_idea_card(self._cards_frame, i, idea)

    def _create_custom_idea_section(self, parent):
        """A text area where Reut can type/paste her own idea."""
        card = tk.Frame(
            parent,
            bg=COLORS["surface"],
            padx=15,
            pady=12,
            highlightbackground=COLORS["accent"],
            highlightthickness=2,
        )
        card.pack(fill="x", pady=6, padx=5)

        header = tk.Label(
            card,
            text="✏️  Write Your Own Idea",
            font=("Helvetica Neue", 14, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["surface"],
            anchor="w",
        )
        header.pack(fill="x")

        hint = tk.Label(
            card,
            text="Type a topic, paste a link, or describe what you want to post about:",
            font=("Helvetica Neue", 11),
            fg=COLORS["text_dim"],
            bg=COLORS["surface"],
            anchor="w",
        )
        hint.pack(fill="x", pady=(2, 5))

        self.custom_idea_text = tk.Text(
            card,
            font=("Helvetica Neue", 12),
            bg=COLORS["card"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            height=4,
            wrap="word",
            padx=8,
            pady=6,
        )
        self.custom_idea_text.pack(fill="x", pady=(0, 8))
        self.custom_idea_text.insert("1.0", "")
        # Placeholder text
        self.custom_idea_text.insert("1.0", "e.g. I just saw a competitor raise $50M — I want to talk about what real scaling looks like vs. fundraising theater...")
        self.custom_idea_text.config(fg=COLORS["text_dim"])

        def _on_focus_in(event):
            if self.custom_idea_text.get("1.0", "end-1c").startswith("e.g."):
                self.custom_idea_text.delete("1.0", "end")
                self.custom_idea_text.config(fg=COLORS["text"])

        def _on_focus_out(event):
            if not self.custom_idea_text.get("1.0", "end-1c").strip():
                self.custom_idea_text.insert("1.0", "e.g. I just saw a competitor raise $50M — I want to talk about what real scaling looks like vs. fundraising theater...")
                self.custom_idea_text.config(fg=COLORS["text_dim"])

        self.custom_idea_text.bind("<FocusIn>", _on_focus_in)
        self.custom_idea_text.bind("<FocusOut>", _on_focus_out)

        btn = tk.Button(
            card,
            text="🚀  Use My Idea",
            font=("Helvetica Neue", 12, "bold"),
            fg=COLORS["text"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=self._on_custom_idea_submitted,
        )
        btn.pack(anchor="e")

    def _on_custom_idea_submitted(self):
        """Called when Reut submits her own idea."""
        text = self.custom_idea_text.get("1.0", "end-1c").strip()
        if not text or text.startswith("e.g."):
            messagebox.showwarning("Empty idea", "Please type your idea first!")
            return
        self._use_idea(text, label="Custom")

    def _create_idea_card(self, parent, index, idea_text):
        card = tk.Frame(
            parent,
            bg=COLORS["card"],
            padx=15,
            pady=12,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        card.pack(fill="x", pady=6, padx=5)

        header = tk.Label(
            card,
            text=f"💡 Idea {index + 1}",
            font=("Helvetica Neue", 14, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["card"],
            anchor="w",
        )
        header.pack(fill="x")

        # Truncate for display but keep full text for selection
        display_text = idea_text[:400] + "..." if len(idea_text) > 400 else idea_text
        body = tk.Label(
            card,
            text=display_text,
            font=("Helvetica Neue", 11),
            fg=COLORS["text"],
            bg=COLORS["card"],
            anchor="w",
            justify="left",
            wraplength=780,
        )
        body.pack(fill="x", pady=(5, 8))

        # Button row: Select as-is | Edit first
        btn_row = tk.Frame(card, bg=COLORS["card"])
        btn_row.pack(fill="x")

        select_btn = tk.Button(
            btn_row,
            text=f"✅  Use As-Is",
            font=("Helvetica Neue", 12, "bold"),
            fg=COLORS["text"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=lambda idx=index: self._use_idea(self.ideas[idx], label=f"Idea {idx+1}"),
        )
        select_btn.pack(side="right", padx=(5, 0))

        edit_btn = tk.Button(
            btn_row,
            text=f"✏️  Edit First",
            font=("Helvetica Neue", 12),
            fg=COLORS["text"],
            bg=COLORS["surface"],
            activebackground=COLORS["card"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=lambda idx=index, c=card, b=body: self._expand_idea_for_editing(idx, c, b, btn_row),
        )
        edit_btn.pack(side="right")

    def _expand_idea_for_editing(self, index, card, body_label, btn_row):
        """Replace the body label with an editable text area."""
        idea_text = self.ideas[index]
        body_label.destroy()
        btn_row.destroy()

        edit_area = tk.Text(
            card,
            font=("Helvetica Neue", 12),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            height=8,
            wrap="word",
            padx=8,
            pady=6,
        )
        edit_area.pack(fill="x", pady=(5, 8))
        edit_area.insert("1.0", idea_text)
        edit_area.focus_set()

        new_btn_row = tk.Frame(card, bg=COLORS["card"])
        new_btn_row.pack(fill="x")

        save_btn = tk.Button(
            new_btn_row,
            text="🚀  Use This Version",
            font=("Helvetica Neue", 12, "bold"),
            fg=COLORS["text"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=lambda: self._use_idea(
                edit_area.get("1.0", "end-1c").strip(),
                label=f"Idea {index+1} (edited)"
            ),
        )
        save_btn.pack(side="right")

    def _use_idea(self, idea_text: str, label: str = ""):
        """Common handler: take the selected/written/edited idea and proceed."""
        if not idea_text.strip():
            messagebox.showwarning("Empty idea", "The idea text is empty!")
            return
        self.selected_idea = idea_text
        self.state["selected_idea"] = idea_text
        self._show_progress_screen()
        self._log(f"✅ Using: {label}")
        self._log(f"   {idea_text[:200]}{'...' if len(idea_text) > 200 else ''}")

        # Re-capture stdout for remaining agent calls
        self._original_stdout = sys.stdout
        sys.stdout = GUILogWriter(self._log, self._original_stdout)
        self._start_time = datetime.now()
        self._tick_timer()

        # Continue the pipeline in background
        thread = threading.Thread(target=self._run_remaining_agents, daemon=True)
        thread.start()

    # ============================================================
    # Screen 4: Reut Reviews Final Drafts (Approve / Edit / Redo)
    # ============================================================
    def _show_review_screen(self, state: dict):
        self._clear_main()
        self.is_running = False

        title = tk.Label(
            self.main_frame,
            text="🛑  Review Before Publishing",
            font=("Helvetica Neue", 20, "bold"),
            fg=COLORS["warning"],
            bg=COLORS["bg"],
        )
        title.pack(pady=(10, 3))

        subtitle = tk.Label(
            self.main_frame,
            text="Read the drafts, edit if needed, then Approve or ask for a Redo",
            font=("Helvetica Neue", 12),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        subtitle.pack(pady=(0, 8))

        # Scores summary
        scores = state.get("validation_scores", {})
        if scores:
            avg = sum(scores.values()) / len(scores)
            score_text = f"Gatekeeper score: {avg:.1f}/5  |  Iterations: {state.get('iteration_count', 0)}"
        else:
            score_text = f"Iterations: {state.get('iteration_count', 0)}"
        score_label = tk.Label(
            self.main_frame,
            text=score_text,
            font=("Helvetica Neue", 11),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        score_label.pack(pady=(0, 8))

        # Draft tabs (EDITABLE — Reut can modify text before approving)
        drafts = state.get("post_drafts", {})
        self._review_text_widgets = {}

        if drafts:
            notebook = ttk.Notebook(self.main_frame)
            notebook.pack(fill="both", expand=True, pady=(5, 8))

            tab_names = {
                "x": "🐦 X (Twitter)",
                "linkedin": "💼 LinkedIn",
                "instagram_slides": "📸 Instagram Slides",
                "instagram_caption": "📝 IG Caption",
            }

            for key, content in drafts.items():
                tab = tk.Frame(notebook, bg=COLORS["surface"])
                notebook.add(tab, text=tab_names.get(key, key))

                text_widget = scrolledtext.ScrolledText(
                    tab,
                    font=("SF Mono", 12),
                    bg=COLORS["surface"],
                    fg=COLORS["text"],
                    insertbackground=COLORS["text"],
                    relief="flat",
                    wrap="word",
                )
                text_widget.pack(fill="both", expand=True, padx=5, pady=5)
                text_widget.insert("1.0", content)
                self._review_text_widgets[key] = text_widget

        # Image preview (if exists)
        image_path = state.get("image_path", "")
        if image_path and os.path.isfile(image_path):
            img_label = tk.Label(
                self.main_frame,
                text=f"🖼️  Image: {os.path.basename(image_path)}",
                font=("Helvetica Neue", 11),
                fg=COLORS["text_dim"],
                bg=COLORS["bg"],
            )
            img_label.pack(pady=(2, 4))

        # --- Redo notes area ---
        redo_frame = tk.Frame(self.main_frame, bg=COLORS["bg"])
        redo_frame.pack(fill="x", pady=(4, 2))

        redo_label = tk.Label(
            redo_frame,
            text="📝 Notes for Redo (optional — tell the Creator what to change):",
            font=("Helvetica Neue", 11),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
            anchor="w",
        )
        redo_label.pack(fill="x")

        self._redo_notes = tk.Text(
            redo_frame,
            font=("Helvetica Neue", 12),
            bg=COLORS["card"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            height=2,
            wrap="word",
            padx=8,
            pady=4,
        )
        self._redo_notes.pack(fill="x", pady=(2, 0))

        # --- Action buttons ---
        btn_frame = tk.Frame(self.main_frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=(8, 0))

        # Approve button (green)
        approve_btn = tk.Button(
            btn_frame,
            text="✅  Approve & Save",
            font=("Helvetica Neue", 14, "bold"),
            fg=COLORS["text"],
            bg=COLORS["success"],
            activebackground="#27ae60",
            activeforeground=COLORS["text"],
            relief="flat",
            padx=24,
            pady=8,
            cursor="hand2",
            command=self._on_approve,
        )
        approve_btn.pack(side="right", padx=(5, 0))

        # Redo button (orange)
        redo_btn = tk.Button(
            btn_frame,
            text="🔄  Redo with Notes",
            font=("Helvetica Neue", 13, "bold"),
            fg=COLORS["text"],
            bg=COLORS["warning"],
            activebackground="#e67e22",
            activeforeground=COLORS["text"],
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._on_redo,
        )
        redo_btn.pack(side="right", padx=(5, 0))

        # Start over button (dimmed)
        restart_btn = tk.Button(
            btn_frame,
            text="⏮  Start Over",
            font=("Helvetica Neue", 12),
            fg=COLORS["text_dim"],
            bg=COLORS["surface"],
            activebackground=COLORS["card"],
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._show_start_screen,
        )
        restart_btn.pack(side="left")

    def _on_approve(self):
        """Reut approves — collect any edits she made, save, run analyst."""
        # Collect edits from text widgets
        for key, widget in self._review_text_widgets.items():
            edited_text = widget.get("1.0", "end-1c").strip()
            if edited_text:
                self.state["post_drafts"][key] = edited_text

        self._show_progress_screen()
        self._log("✅ Reut APPROVED the drafts!")

        # Check if she edited anything
        self._log("📂 Saving to Obsidian + running Analyst...")
        self.is_running = True
        self._original_stdout = sys.stdout
        sys.stdout = GUILogWriter(self._log, self._original_stdout)
        self._start_time = datetime.now()
        self._tick_timer()

        thread = threading.Thread(target=self._run_save_and_learn, daemon=True)
        thread.start()

    def _on_redo(self):
        """Reut wants changes — send her notes back to Creator."""
        notes = self._redo_notes.get("1.0", "end-1c").strip()
        if not notes:
            messagebox.showwarning(
                "No notes",
                "Please type what you want changed in the notes box, "
                "or edit the drafts directly and click Approve."
            )
            return

        # Inject Reut's feedback into state
        self.state["validation_results"] = (
            f"FAIL:\n"
            f"REUT'S DIRECT FEEDBACK (highest priority — override all other rules):\n"
            f"{notes}\n\n"
            f"Rewrite the drafts following Reut's instructions above."
        )

        self._show_progress_screen()
        self._log(f"🔄 Reut requested REDO with notes:")
        self._log(f"   📝 \"{notes[:200]}\"")
        self._log("")

        self.is_running = True
        self._original_stdout = sys.stdout
        sys.stdout = GUILogWriter(self._log, self._original_stdout)
        self._start_time = datetime.now()
        self._tick_timer()

        thread = threading.Thread(target=self._run_redo, daemon=True)
        thread.start()

    def _run_redo(self):
        """Re-run Creator with Reut's feedback, then Validator, then review screen."""
        try:
            from branding_factory.agents.creator import run_creator_agent
            from branding_factory.agents.validator import run_validator_agent

            # Creator rewrites with Reut's feedback
            self._set_progress(40, "✍️ Creator: Rewriting with Reut's feedback...")
            self._log("✍️ CREATOR: Rewriting based on Reut's notes...")
            creator_result = run_creator_agent(self.state)
            self.state.update(creator_result)
            self._log(f"   ✅ New drafts generated")

            # Validator checks the new drafts
            self._set_progress(70, "🛡️ Gatekeeper: Checking revised drafts...")
            self._log("\n🛡️ GATEKEEPER: Evaluating revised drafts...")
            validator_result = run_validator_agent(self.state)
            self.state.update(validator_result)
            validation = self.state.get("validation_results", "")
            scores = self.state.get("validation_scores", {})

            if scores:
                avg = sum(scores.values()) / len(scores)
                self._log(f"   📊 Gatekeeper scores (avg: {avg:.1f}/5)")

            if "FAIL" in validation:
                self._log("   ⚠️ Gatekeeper has concerns — but Reut gets final say")
            else:
                self._log("   ✅ Gatekeeper PASSED")

            self._set_progress(100, "Ready for review")
            self._restore_stdout()
            self.is_running = False
            self._schedule_on_main(lambda: self._show_review_screen(self.state))

        except Exception as e:
            self._restore_stdout()
            self._log(f"\n❌ Error: {e}")
            import traceback
            self._log(traceback.format_exc())
            self.is_running = False
            self._schedule_on_main(lambda: messagebox.showerror("Error", str(e)))

    def _run_save_and_learn(self):
        """After approval: save to Obsidian, run analyst, show final screen."""
        try:
            # --- Save to Obsidian ---
            self._set_progress(40, "📂 Saving to Obsidian...")
            self._log("\n📂 SAVING TO OBSIDIAN...")
            from utils.obsidian_io import save_drafts_to_obsidian
            filepath = save_drafts_to_obsidian(
                self.state.get("post_drafts", {}),
                self.state.get("selected_idea", ""),
                self.state.get("image_path", ""),
            )
            if filepath:
                self._log(f"   ✅ Saved to: {filepath}")
                self.saved_path = os.path.dirname(filepath)
            else:
                self._log("   ⚠️ Saved locally to outputs/")
                self.saved_path = os.path.join(os.path.dirname(__file__), "outputs")

            # --- Analyst: log what worked ---
            self._set_progress(70, "📊 Analyst: Learning from this run...")
            self._log("\n📊 ANALYST: Logging what worked for future runs...")
            from branding_factory.agents.analyst import run_analyst_agent

            # Build engagement data for the analyst
            scores = self.state.get("validation_scores", {})
            avg_score = sum(scores.values()) / len(scores) if scores else 0
            analyst_data = (
                f"Run completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"Selected idea: {self.state.get('selected_idea', '')[:200]}\n"
                f"Gatekeeper avg score: {avg_score:.1f}/5\n"
                f"Iterations needed: {self.state.get('iteration_count', 0)}\n"
                f"Scores: {scores}\n"
                f"Result: APPROVED by Reut\n"
                f"Platforms generated: {', '.join(self.state.get('post_drafts', {}).keys())}\n"
            )
            self.state["engagement_data"] = analyst_data
            analyst_result = run_analyst_agent(self.state)
            self.state.update(analyst_result)
            self._log("   ✅ Analyst logged insights for next run")

            # --- Done! ---
            self._set_progress(100, "🎉 Done!")
            self._log("\n🎉 FACTORY RUN COMPLETE — Content approved and saved!")
            self._restore_stdout()
            self.is_running = False
            self.final_state = self.state
            self._schedule_on_main(lambda: self._show_done_screen(self.state))

        except Exception as e:
            self._restore_stdout()
            self._log(f"\n❌ Error: {e}")
            import traceback
            self._log(traceback.format_exc())
            self.is_running = False
            self._schedule_on_main(lambda: messagebox.showerror("Error", str(e)))

    # ============================================================
    # Screen 5: Final Done (after Reut approved & saved)
    # ============================================================
    def _show_done_screen(self, state: dict):
        self._clear_main()

        title = tk.Label(
            self.main_frame,
            text="🎉  Published!",
            font=("Helvetica Neue", 22, "bold"),
            fg=COLORS["success"],
            bg=COLORS["bg"],
        )
        title.pack(pady=(30, 5))

        info = tk.Label(
            self.main_frame,
            text="Drafts saved to Obsidian  •  Analyst logged insights for next run",
            font=("Helvetica Neue", 13),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        )
        info.pack(pady=(0, 20))

        scores = state.get("validation_scores", {})
        if scores:
            avg = sum(scores.values()) / len(scores)
            for name, score in scores.items():
                bar = "█" * score + "░" * (5 - score)
                s_label = tk.Label(
                    self.main_frame,
                    text=f"  {bar}  {name}: {score}/5",
                    font=("SF Mono", 11),
                    fg=COLORS["success"] if score >= 4 else COLORS["warning"] if score == 3 else COLORS["accent"],
                    bg=COLORS["bg"],
                    anchor="w",
                )
                s_label.pack(anchor="w", padx=100)

        # Action buttons
        btn_frame = tk.Frame(self.main_frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=(30, 0), padx=100)

        open_btn = tk.Button(
            btn_frame,
            text="📂  Open in Obsidian",
            font=("Helvetica Neue", 14, "bold"),
            fg=COLORS["text"],
            bg=COLORS["card"],
            activebackground=COLORS["accent"],
            relief="flat",
            padx=24,
            pady=10,
            cursor="hand2",
            command=self._open_obsidian,
        )
        open_btn.pack(side="left", padx=(0, 10))

        again_btn = tk.Button(
            btn_frame,
            text="🔄  Run Again",
            font=("Helvetica Neue", 14, "bold"),
            fg=COLORS["text"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            relief="flat",
            padx=24,
            pady=10,
            cursor="hand2",
            command=self._show_start_screen,
        )
        again_btn.pack(side="right")

    # ============================================================
    # Footer
    # ============================================================
    def _build_footer(self):
        footer = tk.Frame(self.root, bg=COLORS["surface"], pady=6)
        footer.pack(fill="x", side="bottom")

        text = tk.Label(
            footer,
            text="Built for Lior Pozin  •  Powered by Ollama + SerpAPI + Grok  •  Operated by Reut",
            font=("Helvetica Neue", 10),
            fg=COLORS["text_dim"],
            bg=COLORS["surface"],
        )
        text.pack()

    # ============================================================
    # Actions
    # ============================================================
    def _on_start(self):
        if self.is_running:
            return
        self.is_running = True
        self._show_progress_screen()

        # Capture agent print() statements into the GUI log
        self._original_stdout = sys.stdout
        sys.stdout = GUILogWriter(self._log, self._original_stdout)

        # Start an elapsed-time ticker so Reut sees the app is alive
        self._start_time = datetime.now()
        self._tick_timer()

        # Run the factory in a background thread so UI stays responsive
        thread = threading.Thread(target=self._run_factory, daemon=True)
        thread.start()

    def _tick_timer(self):
        """Update the elapsed time in the progress label every second."""
        if not self.is_running:
            return
        elapsed = datetime.now() - self._start_time
        minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
        time_str = f"{minutes}:{seconds:02d}"
        # Append elapsed time to the current progress label text
        current = self.progress_label.cget("text")
        # Strip any previous time suffix
        base = current.split("  •")[0].split(" (")[0]
        self.progress_label.config(text=f"{base}  •  {time_str} elapsed")
        self.root.after(1000, self._tick_timer)

    def _run_factory(self):
        """Run agents 1-2 (scout + ideator), then wait for idea selection."""
        try:
            from utils.obsidian_io import (
                test_connection, get_ceo_profile, get_voice_dna,
                get_icp_profile, get_learning_log,
            )

            # --- Step 1: Load context ---
            self._set_progress(5, "🔌 Checking Obsidian vault...")
            self._log("🔌 Checking Obsidian vault connection...")
            vault_connected = test_connection()
            if vault_connected:
                self._log("   ✅ Vault connected")
            else:
                self._log("   ⚠️  Vault not found — using fallback defaults")

            self._set_progress(10, "👤 Loading CEO profile...")
            ceo_profile = get_ceo_profile() if vault_connected else {}
            if not ceo_profile:
                ceo_profile = {
                    "name": "Lior Pozin",
                    "company": "AutoDS",
                    "role": "CEO & Serial Entrepreneur",
                    "industry": "E-commerce, SaaS, AI",
                    "topics": ["Scaling", "Pricing Strategy", "Revenue Upselling",
                               "Growth Hacking", "Branding", "AI in Business"],
                    "tone": "Direct, bold, eye-level, no-BS, action-oriented",
                }
            self._log(f"   👤 CEO: {ceo_profile.get('name')} ({ceo_profile.get('company')})")

            self._set_progress(15, "📖 Loading Voice DNA + ICP...")
            voice_dna = get_voice_dna()
            icp_profile = get_icp_profile()
            learning_context = get_learning_log()
            self._log(f"   📖 Voice DNA: {len(voice_dna)} chars")
            self._log(f"   🎯 ICP: {len(icp_profile)} chars")
            self._log(f"   📝 Learning log: {len(learning_context)} chars")

            # Build state
            self.state = {
                "ceo_profile": ceo_profile,
                "voice_dna": voice_dna,
                "icp_profile": icp_profile,
                "trend_report": "",
                "ideas": [],
                "selected_idea": "",
                "post_drafts": {},
                "image_path": "",
                "validation_results": "",
                "iteration_count": 0,
                "learning_context": learning_context,
            }

            # --- Step 2: Scout ---
            self._set_progress(25, "🔍 Scout: Searching Google + X for trends...")
            self._log("\n🔍 SCOUT: Searching for trending topics...")
            from branding_factory.agents.scout import run_scout_agent
            scout_result = run_scout_agent(self.state)
            self.state.update(scout_result)
            self._log("   ✅ Scout found trending topics")

            # --- Step 3: Ideator ---
            self._set_progress(45, "💡 Ideator: Generating content ideas...")
            self._log("\n💡 IDEATOR: Brainstorming content angles...")
            from branding_factory.agents.ideator import run_ideator_agent
            ideator_result = run_ideator_agent(self.state)
            self.state.update(ideator_result)
            self.ideas = self.state.get("ideas", [])
            self._log(f"   ✅ Generated {len(self.ideas)} ideas")

            # --- Step 4: Show ideas for selection ---
            self._set_progress(50, "💡 Pick your favorite idea...")
            self._restore_stdout()
            self._schedule_on_main(lambda: self._show_idea_selection(self.ideas))

        except Exception as e:
            self._restore_stdout()
            self._log(f"\n❌ Error: {e}")
            import traceback
            self._log(traceback.format_exc())
            self.is_running = False
            self._schedule_on_main(lambda: messagebox.showerror("Error", str(e)))

    def _restore_stdout(self):
        """Restore original stdout after agent run."""
        if hasattr(self, "_original_stdout") and self._original_stdout:
            sys.stdout = self._original_stdout
            self._original_stdout = None

    def _run_remaining_agents(self):
        """Run Creator → Validator loop → Graphic Artist → show review screen (Reut decides)."""
        try:
            # --- Step 5: Creator ---
            self._set_progress(55, "✍️ Creator: Writing drafts in Lior's voice...")
            self._log("\n✍️ CREATOR: Writing multi-platform drafts (with self-check)...")
            from branding_factory.agents.creator import run_creator_agent
            creator_result = run_creator_agent(self.state)
            self.state.update(creator_result)
            drafts = self.state.get("post_drafts", {})
            self._log(f"   ✅ Generated drafts for {len(drafts)} platforms")

            # --- Step 6: Validator (agentic — LLM evaluation + hard checks) ---
            self._set_progress(70, "🛡️ Gatekeeper: Evaluating quality...")
            self._log("\n🛡️ GATEKEEPER: Two-phase quality control...")
            from branding_factory.agents.validator import run_validator_agent

            max_retries = 3
            for attempt in range(max_retries):
                validator_result = run_validator_agent(self.state)
                self.state.update(validator_result)
                validation = self.state.get("validation_results", "")
                scores = self.state.get("validation_scores", {})

                # Show scores in the log
                if scores:
                    avg = sum(scores.values()) / len(scores)
                    self._log(f"   📊 Gatekeeper scores (avg: {avg:.1f}/5):")
                    for name, score in scores.items():
                        bar = "█" * score + "░" * (5 - score)
                        self._log(f"      {bar} {name}: {score}/5")

                if "FAIL" not in validation:
                    self._log("   ✅ Gatekeeper PASSED — drafts are ready for Reut!")
                    break
                elif attempt < max_retries - 1:
                    self._log(f"\n   🔄 FAIL → Sending feedback to Creator (retry {attempt + 1}/{max_retries})...")
                    self._log(f"   📝 Creator will fix: {validation[:200]}...")
                    self._set_progress(70, f"✍️ Creator: Rewriting with feedback (attempt {attempt + 2}/{max_retries})...")
                    creator_result = run_creator_agent(self.state)
                    self.state.update(creator_result)
                    self._log(f"   ✅ Creator submitted revised drafts")
                else:
                    self._log("   ⚠️ Max retries reached. Sending to Reut for final call.")

            # --- Step 7: Graphic Artist ---
            self._set_progress(88, "🎨 Graphic Artist: Generating image...")
            self._log("\n🎨 GRAPHIC ARTIST: Generating branded image...")
            from branding_factory.agents.graphic_artist import run_graphic_agent
            graphic_result = run_graphic_agent(self.state)
            self.state.update(graphic_result)
            image_path = self.state.get("image_path", "")
            if image_path:
                self._log(f"   ✅ Image saved: {image_path}")
            else:
                self._log("   ⏭️ Skipped (diffusers not installed)")

            # --- Step 8: Show review screen (Reut decides: Approve / Edit / Redo) ---
            self._set_progress(100, "🛑 Ready for Reut's review!")
            self._log("\n🛑 READY FOR REVIEW — Reut, check the drafts!")
            self._restore_stdout()
            self.is_running = False
            self._schedule_on_main(lambda: self._show_review_screen(self.state))

        except Exception as e:
            self._restore_stdout()
            self._log(f"\n❌ Error: {e}")
            import traceback
            self._log(traceback.format_exc())
            self.is_running = False
            self._schedule_on_main(lambda: messagebox.showerror("Error", str(e)))

    def _open_obsidian(self):
        """Open the Obsidian vault (or the output folder in Finder)."""
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "")
        if vault_path and os.path.isdir(vault_path):
            # Open Obsidian app with the vault
            os.system(f'open "obsidian://open?vault={os.path.basename(vault_path)}"')
        elif hasattr(self, "saved_path") and os.path.isdir(self.saved_path):
            os.system(f'open "{self.saved_path}"')
        else:
            os.system(f'open "{os.path.join(os.path.dirname(__file__), "outputs")}"')


# ============================================================
# Entry point
# ============================================================
def main():
    root = tk.Tk()

    # macOS specific: bring window to front
    try:
        root.lift()
        root.attributes("-topmost", True)
        root.after(100, lambda: root.attributes("-topmost", False))
    except Exception:
        pass

    app = BrandingFactoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
