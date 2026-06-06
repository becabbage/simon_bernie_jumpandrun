"""
Level Editor for creating and editing .map files
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from pathlib import Path
from level_manager import get_map_files, load_level, save_level, get_level_name

# Tile type definitions
TILE_TYPES = {
    0: ("Sky", "#87CEEB"),
    1: ("Dirt", "#8B4513"),
    2: ("Grass", "#228B22"),
    3: ("Enemy", "#FF0000"),
    4: ("Coin", "#FFD700"),
    5: ("Coin2", "#FFA500"),
    6: ("Lava", "#FF4500"),
    8: ("Special", "#9932CC"),
}

DEFAULT_WIDTH = 40
DEFAULT_HEIGHT = 20
TILE_BUTTON_SIZE = 25


class LevelEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Level Editor")
        self.root.geometry("1000x800")
        
        self.world_data = None
        self.current_file = None
        self.tile_buttons = []
        self.selected_tile_type = 0
        self.has_unsaved_changes = False
        self.status_label = None  # Initialize first
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top menu frame
        menu_frame = tk.Frame(main_frame)
        menu_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(menu_frame, text="New Map", command=self.new_map).pack(side=tk.LEFT, padx=2)
        tk.Button(menu_frame, text="Open Map", command=self.open_map).pack(side=tk.LEFT, padx=2)
        tk.Button(menu_frame, text="Save", command=self.save_map).pack(side=tk.LEFT, padx=2)
        tk.Button(menu_frame, text="Save As", command=self.save_map_as).pack(side=tk.LEFT, padx=2)
        tk.Button(menu_frame, text="Discard Changes", command=self.discard_changes).pack(side=tk.LEFT, padx=2)
        
        self.title_label = tk.Label(menu_frame, text="No map loaded", font=("Arial", 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # Status bar FIRST
        self.status_label = tk.Label(main_frame, text="Ready", font=("Arial", 9))
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Tile type selection frame
        tile_frame = tk.LabelFrame(main_frame, text="Tile Types", font=("Arial", 10, "bold"))
        tile_frame.pack(fill=tk.X, pady=5)
        
        self.tile_type_buttons = {}
        for tile_id, (name, color) in TILE_TYPES.items():
            btn = tk.Button(
                tile_frame,
                text=f"{name}\n({tile_id})",
                bg=color,
                width=12,
                command=lambda t=tile_id: self.select_tile_type(t),
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.tile_type_buttons[tile_id] = btn
        
        # Now it's safe to call select_tile_type
        self.select_tile_type(0)
        
        # Grid canvas
        canvas_frame = tk.LabelFrame(main_frame, text="Level Grid", font=("Arial", 10, "bold"))
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def select_tile_type(self, tile_id):
        """Select the active tile type"""
        # Reset all buttons
        for btn_id, btn in self.tile_type_buttons.items():
            btn.config(relief=tk.RAISED, bd=2)
        
        # Highlight selected
        self.selected_tile_type = tile_id
        self.tile_type_buttons[tile_id].config(relief=tk.SUNKEN, bd=3)
        self.update_status(f"Selected: {TILE_TYPES[tile_id][0]} (ID: {tile_id})")
    
    def new_map(self):
        """Create a new map"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Map")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Map Name:", font=("Arial", 10)).pack(pady=5)
        name_entry = tk.Entry(dialog, font=("Arial", 10), width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        tk.Label(dialog, text="Width (tiles):", font=("Arial", 10)).pack(pady=5)
        width_var = tk.StringVar(value=str(DEFAULT_WIDTH))
        width_entry = tk.Entry(dialog, font=("Arial", 10), width=30, textvariable=width_var)
        width_entry.pack(pady=5)
        
        tk.Label(dialog, text="Height (tiles):", font=("Arial", 10)).pack(pady=5)
        height_var = tk.StringVar(value=str(DEFAULT_HEIGHT))
        height_entry = tk.Entry(dialog, font=("Arial", 10), width=30, textvariable=height_var)
        height_entry.pack(pady=5)
        
        def create():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a map name")
                return
            
            try:
                width = int(width_var.get())
                height = int(height_var.get())
                if width <= 0 or height <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Width and Height must be positive numbers")
                return
            
            # Check if file already exists
            filepath = f"{name}.map"
            if Path(filepath).exists():
                if not messagebox.askyesno("Confirm", f"{filepath} already exists. Overwrite?"):
                    return
            
            # Create new map with all sky tiles (0)
            self.world_data = [[0 for _ in range(width)] for _ in range(height)]
            self.current_file = filepath
            self.has_unsaved_changes = True
            self.render_grid()
            self.title_label.config(text=f"Editing: {name} (NEW)")
            self.update_status(f"Created new map: {name} ({width}x{height})")
            dialog.destroy()
        
        tk.Button(dialog, text="Create", command=create, font=("Arial", 10), width=20).pack(pady=10)
    
    def open_map(self):
        """Open an existing map"""
        map_files = get_map_files()
        
        if not map_files:
            messagebox.showerror("Error", "No .map files found in current directory")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Open Map")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select a map to open:", font=("Arial", 10)).pack(pady=5)
        
        # Listbox with maps
        listbox = tk.Listbox(dialog, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for map_file in map_files:
            name = get_level_name(map_file)
            listbox.insert(tk.END, name)
        
        def open_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a map")
                return
            
            map_file = map_files[selection[0]]
            try:
                self.world_data = load_level(map_file)
                self.current_file = str(map_file)
                self.has_unsaved_changes = False
                self.render_grid()
                name = get_level_name(map_file)
                self.title_label.config(text=f"Editing: {name}")
                self.update_status(f"Loaded map: {name}")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load map:\n{str(e)}")
        
        tk.Button(dialog, text="Open", command=open_selected, font=("Arial", 10), width=20).pack(pady=5)
    
    def render_grid(self):
        """Render the level grid as clickable buttons"""
        if self.world_data is None:
            return
        
        # Clear canvas
        self.canvas.delete("all")
        self.tile_buttons = []
        
        height = len(self.world_data)
        width = len(self.world_data[0]) if height > 0 else 0
        
        total_width = width * TILE_BUTTON_SIZE + 20
        total_height = height * TILE_BUTTON_SIZE + 20
        
        self.canvas.config(width=total_width, height=total_height)
        
        for row in range(height):
            button_row = []
            for col in range(width):
                tile_id = self.world_data[row][col]
                color = TILE_TYPES.get(tile_id, ("Unknown", "#CCCCCC"))[1]
                
                x1 = col * TILE_BUTTON_SIZE + 10
                y1 = row * TILE_BUTTON_SIZE + 10
                x2 = x1 + TILE_BUTTON_SIZE - 2
                y2 = y1 + TILE_BUTTON_SIZE - 2
                
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                self.canvas.tag_bind(rect, "<Button-1>", lambda e, r=row, c=col: self.paint_tile(r, c))
                self.canvas.tag_bind(rect, "<Button-3>", lambda e, r=row, c=col: self.show_tile_info(r, c, e))
                
                button_row.append(rect)
            
            self.tile_buttons.append(button_row)
        
        self.update_status(f"Grid: {width}x{height}")
    
    def paint_tile(self, row, col):
        """Paint a tile with the selected tile type"""
        if self.world_data is None or row >= len(self.world_data) or col >= len(self.world_data[0]):
            return
        
        self.world_data[row][col] = self.selected_tile_type
        self.has_unsaved_changes = True
        self.render_grid()
        self.title_label.config(text=self.title_label.cget("text") + " *")
    
    def show_tile_info(self, row, col, event):
        """Show tile information on right-click"""
        tile_id = self.world_data[row][col]
        tile_name = TILE_TYPES.get(tile_id, ("Unknown", ""))[0]
        messagebox.showinfo("Tile Info", f"Position: ({col}, {row})\nType: {tile_name} (ID: {tile_id})")
    
    def save_map(self):
        """Save the current map"""
        if self.world_data is None:
            messagebox.showerror("Error", "No map loaded")
            return
        
        if not self.current_file:
            self.save_map_as()
            return
        
        try:
            save_level(self.world_data, self.current_file)
            self.has_unsaved_changes = False
            name = get_level_name(self.current_file)
            self.title_label.config(text=f"Editing: {name}")
            self.update_status(f"Map saved: {self.current_file}")
            messagebox.showinfo("Success", f"Map saved: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save map:\n{str(e)}")
    
    def save_map_as(self):
        """Save the current map with a new name"""
        if self.world_data is None:
            messagebox.showerror("Error", "No map loaded")
            return
        
        name = simpledialog.askstring("Save As", "Enter map name (without .map extension):")
        if not name:
            return
        
        name = name.strip()
        if not name:
            messagebox.showerror("Error", "Please enter a valid name")
            return
        
        filepath = f"{name}.map"
        
        if Path(filepath).exists():
            if not messagebox.askyesno("Confirm", f"{filepath} already exists. Overwrite?"):
                return
        
        try:
            save_level(self.world_data, filepath)
            self.current_file = filepath
            self.has_unsaved_changes = False
            self.title_label.config(text=f"Editing: {name}")
            self.update_status(f"Map saved as: {filepath}")
            messagebox.showinfo("Success", f"Map saved: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save map:\n{str(e)}")
    
    def discard_changes(self):
        """Discard unsaved changes"""
        if not self.has_unsaved_changes:
            messagebox.showinfo("Info", "No unsaved changes")
            return
        
        if messagebox.askyesno("Confirm", "Discard all unsaved changes?"):
            if self.current_file:
                try:
                    self.world_data = load_level(self.current_file)
                    self.has_unsaved_changes = False
                    self.render_grid()
                    name = get_level_name(self.current_file)
                    self.title_label.config(text=f"Editing: {name}")
                    self.update_status(f"Changes discarded")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to reload map:\n{str(e)}")
            else:
                self.world_data = None
                self.canvas.delete("all")
                self.title_label.config(text="No map loaded")
                self.update_status("Changes discarded")
    
    def update_status(self, message):
        """Update the status bar"""
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = LevelEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
