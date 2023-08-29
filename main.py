"""
File for creating the GUI.
Requires no student import, but will use your implemented classes as part of it's process!
"""

import arcade
import arcade.gui as gui
import json
import sys
import secrets
from copy import copy

from constants import DrawMode
from mountain import Mountain
from mountain_manager import MountainManager
from trail import Trail, TrailSeries, TrailSplit
from draw_trails import TrailDraw
from mountain_organiser import MountainOrganiser
from double_key_table import DoubleKeyTable
from serialize import serialize, deserialize

class MyWindow(arcade.Window):
    """ Painter Window """

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    SIDEBAR_WIDTH = 100
    BUTTONS_HEIGHT = 100
    SCREEN_TITLE = "Paint"

    REPLAY_TIMER_DELTA = 0.05

    GRID_SIZE_X = 32
    GRID_SIZE_Y = 32

    BG = [255, 255, 255]

    ACTIONS = [
        ["img/add.png", "mode", "add_mode_mountain"],
        ["img/remove.png", "mode", "remove_mode"],
        ["img/edit.png", "mode", "edit_mode"],
        ["img/add_branch.png", "mode", "add_mode_branch"],
        ["img/show_graph.png", "click", "on_graph_clicked"],
        ["img/save_file.png", "click", "on_save_file_clicked"],
    ]

    # SCAFFOLD PART
    # Unless you're adding new features, you shouldn't need to touch this.

    GRAPH_WIDTH = 430
    LABEL_WIDTH = 70
    GRAPH_HEIGHT = 300

    def __init__(self) -> None:
        """Initialise visual and logic variables."""
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)
        arcade.set_background_color(self.BG)
        self.init_manager()
        self.init_file_dialog()
        self.init_graph()

    def init_manager(self):
        self.manager = gui.UIManager()
        editor_width = 350
        self.label_mountain_name = gui.UILabel(
            text="Mountain Name",
            width=editor_width,
            height=40,
            font_size=24,
            text_color=(0, 0, 0)
        )
        self.input_mountain_name = gui.UIInputText(
            font_size=24,
            width=editor_width,
        )
        self.label_difficulty_level = gui.UILabel(
            text="Difficulty Level",
            width=editor_width,
            height=40,
            font_size=24,
            text_color=(0, 0, 0)
        )
        self.input_difficulty_level = gui.UIInputText(
            font_size=24,
            width=editor_width,
        )
        self.label_length = gui.UILabel(
            text="Length",
            width=editor_width,
            height=40,
            font_size=24,
            text_color=(0, 0, 0)
        )
        self.input_length = gui.UIInputText(
            font_size=24,
            width=editor_width,
        )
        self.input_box = gui.UIBoxLayout()
        self.input_box.add(self.label_mountain_name.with_space_around(bottom=0))
        self.input_box.add(gui.UIBorder(self.input_mountain_name))
        self.input_box.add(self.label_difficulty_level.with_space_around(bottom=0))
        self.input_box.add(gui.UIBorder(self.input_difficulty_level))
        self.input_box.add(self.label_length.with_space_around(bottom=0))
        self.input_box.add(gui.UIBorder(self.input_length))
        self.input_bg = gui.UIBorder(
            gui.UISpace(width=editor_width + 100, height=400, color=(255, 255, 255, 240)),
            border_width=5,
        )

        self.manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.input_bg
        ))
        self.manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=50,
            child=self.input_box
        ))

        self.save_button = gui.UIFlatButton(
            width=100,
            height=50,
            text="Save",
        )
        self.save_button.on_click = self.on_save_clicked
        self.close_button = gui.UIFlatButton(
            width=100,
            height=50,
            text="Close"
        )
        self.close_button.on_click = self.on_close_clicked

        self.manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_x=editor_width/2 - 10,
            align_y=-170,
            child=self.save_button
        ))
        self.manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_x=-editor_width/2 + 10,
            align_y=-170,
            child=self.close_button
        ))

    def init_file_dialog(self):
        self.file_manager = gui.UIManager()
        editor_width = 350
        self.label_file_name = gui.UILabel(
            text="File Name",
            width=editor_width,
            height=40,
            font_size=24,
            text_color=(0, 0, 0)
        )
        self.input_file_name = gui.UIInputText(
            font_size=24,
            width=editor_width,
        )
        self.input_box = gui.UIBoxLayout()
        self.input_box.add(self.label_file_name.with_space_around(bottom=0))
        self.input_box.add(gui.UIBorder(self.input_file_name))
        self.input_bg = gui.UIBorder(
            gui.UISpace(width=editor_width + 100, height=400, color=(255, 255, 255, 240)),
            border_width=5,
        )

        self.file_manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.input_bg
        ))
        self.file_manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=50,
            child=self.input_box
        ))

        self.save_button_file = gui.UIFlatButton(
            width=100,
            height=50,
            text="Save",
        )
        self.save_button_file.on_click = self.on_file_save_clicked
        self.close_button_file = gui.UIFlatButton(
            width=100,
            height=50,
            text="Close"
        )
        self.close_button_file.on_click = self.on_file_close_clicked

        self.file_manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_x=editor_width/2 - 10,
            align_y=-170,
            child=self.save_button_file
        ))
        self.file_manager.add(gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_x=-editor_width/2 + 10,
            align_y=-170,
            child=self.close_button_file
        ))

    def init_graph(self):
        self.graph = gui.UIManager()
        self.graph.enable()
        self.graph.add(gui.UIAnchorWidget(
            anchor_x="center",
            anchor_y="center",
            child=gui.UISpace(width=self.GRAPH_WIDTH + self.LABEL_WIDTH, height=self.GRAPH_HEIGHT, color=(255, 255, 255, 245))
        ))
        self.graph.add(gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="center",
            align_x=self.SCREEN_WIDTH // 2 - (self.GRAPH_WIDTH + self.LABEL_WIDTH)//2,
            child=gui.UISpace(width=self.GRAPH_WIDTH, height=self.GRAPH_HEIGHT, color=(0, 0, 0, 220))
        ))
        # Each entry in graph data follows this format:
        # [color, start_index, name, [position1, position2, ...]]
        self.graph_data = []

    def draw_graph_elems(self):
        total_y_points = len(self.graph_data)
        total_x_points = max(len(x[3]) for x in self.graph_data)
        left_axis = self.SCREEN_WIDTH // 2 - (self.GRAPH_WIDTH + self.LABEL_WIDTH)//2
        bottom_axis = self.SCREEN_HEIGHT // 2 - self.GRAPH_HEIGHT//2

        for color, start_index, name, positions in self.graph_data:
            points = []
            for i, pos in enumerate(positions):
                xpos = left_axis + (start_index + i + 0.5) * self.GRAPH_WIDTH / total_x_points
                ypos = bottom_axis + (total_y_points - pos - 0.5) * self.GRAPH_HEIGHT / total_y_points
                points.append((xpos, ypos))
                arcade.draw_circle_filled(xpos, ypos, 6, color, num_segments=12)
            arcade.draw_line_strip(points, color, 2)
            arcade.draw_text(name, points[-1][0] + 0.5 * self.GRAPH_WIDTH / total_x_points + 5, points[-1][1], color=(0, 0, 0), anchor_y="center")

    def reset(self) -> None:
        """Reset the screen."""
        self.timestamp = 0
        self.is_editing = False
        self.manager.disable()
        self.is_saving = False
        self.file_manager.disable()

        # Visual calculations
        self.DRAW_PANEL = self.SCREEN_WIDTH - self.SIDEBAR_WIDTH
        self.GRID_SQ_WIDTH = self.DRAW_PANEL / self.GRID_SIZE_X
        self.GRID_SQ_HEIGHT = self.SCREEN_HEIGHT / self.GRID_SIZE_Y
        self.LAYER_BUTTON_SIZE = self.SIDEBAR_WIDTH / 2
        # Action button sprites
        self.action_buttons = arcade.SpriteList()
        for i, (path, button_type, tracker) in enumerate(self.ACTIONS):
            button = arcade.Sprite(path, scale=50/48)
            button.center_x = self.DRAW_PANEL + self.LAYER_BUTTON_SIZE / 2 + self.LAYER_BUTTON_SIZE * (i % 2 == 1)
            button.center_y = self.LAYER_BUTTON_SIZE / 2 + self.LAYER_BUTTON_SIZE * (i // 2)
            if button_type == "toggle":
                setattr(self, tracker, False)
            elif button_type == "mode":
                setattr(self, tracker, False)
            self.action_buttons.append(button)

        # Other constants
        self.showing_graph = False

        self.on_edit_mode()

    def setup(self) -> None:
        """Set up the game and initialize the variables."""
        self.reset()
        self.mountain_manager = MountainManager()
        self.cur_filename = sys.argv[1] if len(sys.argv) > 1 else "basic.json"
        with open(f"stores/{self.cur_filename}", "r") as f:
            t = deserialize(json.loads(f.read()))
        try:
            # Try to add all existing mountains
            for mountain in t.collect_all_mountains():
                self.mountain_manager.add_mountain(mountain)
        except NotImplementedError:
            pass
        self.mountain = TrailDraw(t)
        self.draw_box = None

    def on_draw(self) -> None:
        """Draw everything"""
        self.clear()
        self.mountain.draw_in_box(self.SCREEN_HEIGHT, self.DRAW_PANEL, 0, 0)
        if self.draw_box is not None and not (self.showing_graph or self.is_editing or self.is_saving):
            arcade.draw_rectangle_filled(self.draw_box.x + self.draw_box.w/2, self.draw_box.y + self.draw_box.h/2, self.draw_box.w, self.draw_box.h, (0, 255, 0, 100))
        # UI - Draw Modes / Action buttons
        self.action_buttons.draw()
        for i, ((path, button_type, tracker), button) in enumerate(zip(self.ACTIONS, self.action_buttons)):
            if button_type == "toggle" or button_type == "mode":
                if getattr(self, tracker):
                    arcade.draw_rectangle_filled(button.center_x, button.center_y, self.LAYER_BUTTON_SIZE, self.LAYER_BUTTON_SIZE, (0, 255, 0, 100))
        if self.is_editing:
            self.manager.draw()
        elif self.showing_graph:
            self.graph.draw()
            self.draw_graph_elems()
        elif self.is_saving:
            self.file_manager.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the mouse buttons are pressed."""
        if button == 1:
            if self.showing_graph:
                self.showing_graph = False
                return
            if x > self.DRAW_PANEL:
                for i, (path, button_type, tracker) in enumerate(self.ACTIONS):
                    sx = self.DRAW_PANEL + self.LAYER_BUTTON_SIZE * (i % 2 == 1)
                    ex = self.DRAW_PANEL + self.LAYER_BUTTON_SIZE * (1+(i % 2 == 1))
                    sy = self.LAYER_BUTTON_SIZE * (i // 2)
                    ey = self.LAYER_BUTTON_SIZE * (i // 2 + 1)
                    if sx <= x < ex and sy <= y < ey:
                        if button_type == "toggle":
                            setattr(self, tracker, not getattr(self, tracker))
                            if hasattr(self, "on_"+tracker):
                                getattr(self, "on_"+tracker)()
                        elif button_type == "mode":
                            setattr(self, tracker, True)
                            if hasattr(self, "on_"+tracker):
                                getattr(self, "on_"+tracker)()
                        elif button_type == "click":
                            getattr(self, tracker)()
            else:
                if self.box_action and not (self.is_editing or self.is_saving or self.showing_graph):
                    if self.cur_draw_mode == DrawMode.ADD_MOUNTAIN:
                        key = secrets.token_hex(2)
                        mountain = Mountain(f"default-{key}", 0, 0)
                        self.box_action(mountain)
                        try:
                            self.mountain_manager.add_mountain(mountain)
                        except NotImplementedError:
                            pass
                    elif self.cur_draw_mode == DrawMode.ADD_BRANCH:
                        self.box_action()
                    elif self.cur_draw_mode == DrawMode.REMOVE:
                        if isinstance(self.cur_trail, TrailSeries):
                            try:
                                self.mountain_manager.remove_mountain(self.cur_trail.mountain)
                            except NotImplementedError:
                                pass
                        self.box_action()
                    elif self.cur_draw_mode == DrawMode.EDIT:
                        self.cur_editing_mountain = self.box_action()
                        self.input_mountain_name.text = self.cur_editing_mountain.name
                        self.input_difficulty_level.text = str(self.cur_editing_mountain.difficulty_level)
                        self.input_length.text = str(self.cur_editing_mountain.length)
                        self.is_editing = True
                        self.manager.enable()
                    self.box_action = None
                    self.cur_trail = None

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """Called when the mouse buttons are released."""
        pass

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        """Called when the mouse moves."""
        self.draw_box, self.box_action, self.cur_trail = self.mountain.box_and_action((x, y), self.cur_draw_mode)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Called when a keyboard key is pressed."""
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Called when a keyboard key is released."""
        pass

    def on_update(self, delta_time) -> None:
        """Movement and game logic."""
        self.timestamp += delta_time

    def on_graph_clicked(self):
        self.showing_graph = True
        import colorsys
        def get_col(index, total):
            return [
                int(255*x)
                for x in colorsys.hls_to_rgb(index/total, 0.6, 0.6)
            ]
        groups = self.mountain_manager.group_by_difficulty()
        to = MountainOrganiser()
        positions = DoubleKeyTable()
        positions.hash1 = lambda k: (k % positions.table_size)
        all_mountains = []
        for i, group in enumerate(groups):
            to.add_mountains(group)
            for mountain in group:
                positions[mountain.difficulty_level, mountain.name] = []
            all_mountains.extend(group)
            for mountain in all_mountains:
                positions[mountain.difficulty_level, mountain.name].append(to.cur_position(mountain))
        self.graph_data = [
            [
                get_col(i, len(all_mountains)),
                len(groups) - len(positions[mountain.difficulty_level, mountain.name]),
                mountain.name,
                positions[mountain.difficulty_level, mountain.name]
            ]
            for i, mountain in enumerate(all_mountains)
        ]

    def on_save_file_clicked(self):
        self.is_saving = True
        self.file_manager.enable()
        self.input_file_name.text = self.cur_filename

    def on_add_mode_mountain(self):
        self.cur_draw_mode = DrawMode.ADD_MOUNTAIN
        self.add_mode_mountain = True
        self.remove_mode = False
        self.edit_mode = False
        self.add_mode_branch = False

    def on_remove_mode(self):
        self.cur_draw_mode = DrawMode.REMOVE
        self.remove_mode = True
        self.add_mode_mountain = False
        self.edit_mode = False
        self.add_mode_branch = False

    def on_edit_mode(self):
        self.cur_draw_mode = DrawMode.EDIT
        self.edit_mode = True
        self.add_mode_mountain = False
        self.remove_mode = False
        self.add_mode_branch = False

    def on_add_mode_branch(self):
        self.cur_draw_mode = DrawMode.ADD_BRANCH
        self.add_mode_branch = True
        self.add_mode_mountain = False
        self.remove_mode = False
        self.edit_mode = False

    def on_save_clicked(self, event):
        old_mountain = copy(self.cur_editing_mountain)
        self.cur_editing_mountain.name = self.input_mountain_name.text
        self.cur_editing_mountain.difficulty_level = int(self.input_difficulty_level.text)
        self.cur_editing_mountain.length = int(self.input_length.text)
        try:
            self.mountain_manager.edit_mountain(old_mountain, self.cur_editing_mountain)
        except NotImplementedError:
            pass
        # Close the window.
        self.on_close_clicked(event)

    def on_close_clicked(self, event):
        self.is_editing = False
        self.manager.disable()
        self.cur_editing_mountain = None

    def on_file_save_clicked(self, event):
        new_path = str(self.input_file_name.text)
        with open(f"stores/{new_path}", "w") as f:
            f.write(serialize(self.mountain.trail))
        # Close the window.
        self.on_file_close_clicked(event)

    def on_file_close_clicked(self, event):
        self.is_saving = False
        self.file_manager.disable()

def main():
    """ Main function """
    window = MyWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
