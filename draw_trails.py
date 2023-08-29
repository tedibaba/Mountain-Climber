"""
Class used to determine location and size of trail objects in `main.py`

A bit of a mess, you 100% don't need to look at this for your assignment!
"""

from __future__ import annotations
from dataclasses import dataclass, field
from mountain import Mountain
from utils import av, bezier
from constants import DrawMode
from trail import Trail, TrailSeries, TrailSplit

@dataclass
class Box:

    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0

    def __contains__(self, p: tuple[float, float]):
        if self.x <= p[0] <= self.x + self.w:
            if self.y <= p[1] <= self.y + self.h:
                return True
        return False

# These inheritance models are just for hinting that we are injection
# the box attributes into the existing trail classes.

@dataclass
class TrailSplitBox(TrailSplit):

    branch_start_box: Box = field(default_factory=Box)
    branch_end_box: Box = field(default_factory=Box)

@dataclass
class TrailSeriesBox(TrailSeries):

    before_box: Box = field(default_factory=Box)
    mountain_box: Box = field(default_factory=Box)
    after_box: Box = field(default_factory=Box)

@dataclass
class TrailBox(Trail):

    trail_box: Box = field(default_factory=Box)

class TrailDraw:

    ### Visual constants
    # - Vertical
    BRANCH_SEPARATION = 10
    MOUNTAIN_HEIGHT = 30
    EMPTY_HEIGHT = 10
    # - Horizontal
    MIN_MOUNTAIN_WIDTH = 30
    MOUNTAIN_SEP = 10
    TOTAL_MOUNTAIN_WIDTH = MOUNTAIN_SEP + MIN_MOUNTAIN_WIDTH + MOUNTAIN_SEP
    BRANCH_WIDTH = 30
    MIN_BRANCH_CONTENT_WIDTH = 20
    MAX_MOUNTAIN_WIDTH = 120

    ### Click constants
    LINE_VERTICAL_BOX = MOUNTAIN_HEIGHT / 2

    def __init__(self, trail: TrailBox) -> None:
        self.trail = trail

    # VISUAL CALCULATIONS

    def required_height(self, cur_trail: TrailBox|None=None) -> int:
        if cur_trail is None:
            cur_trail = self.trail.store
        else:
            cur_trail = cur_trail.store
        if cur_trail is None:
            return self.EMPTY_HEIGHT
        elif isinstance(cur_trail, TrailSeries):
            return max(self.MOUNTAIN_HEIGHT, self.required_height(cur_trail.following))
        else:
            return max(
                self.required_height(cur_trail.top) + self.BRANCH_SEPARATION + self.required_height(cur_trail.bottom),
                self.required_height(cur_trail.following)
            )

    def required_width(self, cur_trail: TrailBox|None=None) -> int:
        if cur_trail is None:
            cur_trail = self.trail.store
        else:
            cur_trail = cur_trail.store
        if cur_trail is None:
            return 0
        elif isinstance(cur_trail, TrailSeries):
            return self.TOTAL_MOUNTAIN_WIDTH + self.required_width(cur_trail.following)
        else:
            return 2 * self.BRANCH_WIDTH + max(
                self.required_width(cur_trail.top),
                self.required_width(cur_trail.bottom),
                self.MIN_BRANCH_CONTENT_WIDTH,
            ) + self.required_width(cur_trail.following)

    def draw_in_box(self, height, width, minx, miny, cur_trail: TrailBox|None=None) -> None:
        if cur_trail is None:
            ref_trail = self.trail
            cur_trail = self.trail.store
        else:
            ref_trail = cur_trail
            cur_trail = cur_trail.store
        if cur_trail is None:
            self.draw_line(minx, miny + height/2, minx + width, miny + height/2)
            ref_trail.trail_box = Box(minx, miny + height/2-self.LINE_VERTICAL_BOX, width, 2*self.LINE_VERTICAL_BOX)
        elif isinstance(cur_trail, TrailSeries):
            ref_trail.trail_box = Box(minx, miny, width, height)
            p1 = self.TOTAL_MOUNTAIN_WIDTH
            p2 = self.required_width(cur_trail.following)
            total = p1 + p2
            # Draw mountain
            p1_total_dist = (p1 / total) * width
            start_mountain_trail_x = minx
            mountain_width = (self.MIN_MOUNTAIN_WIDTH / self.TOTAL_MOUNTAIN_WIDTH) * p1_total_dist
            mountain_width = max(mountain_width, self.MIN_MOUNTAIN_WIDTH)
            mountain_width = min(mountain_width, self.MAX_MOUNTAIN_WIDTH)
            start_mountain_x = minx + p1_total_dist/2 - mountain_width/2
            end_mountain_x = start_mountain_x + mountain_width
            end_mountain_trail_x = minx + p1_total_dist
            mid = miny + height/2
            self.draw_mountain(av(start_mountain_x, end_mountain_x), mid, (end_mountain_x - start_mountain_x) / self.MIN_MOUNTAIN_WIDTH, cur_trail.mountain)
            self.draw_line(start_mountain_trail_x, mid, start_mountain_x, mid)
            self.draw_line(end_mountain_x, mid, end_mountain_trail_x, mid)
            mountain_actual_height = self.MOUNTAIN_HEIGHT * (end_mountain_x - start_mountain_x) / self.MIN_MOUNTAIN_WIDTH
            cur_trail.before_box = Box(start_mountain_trail_x, mid - mountain_actual_height/2, start_mountain_x - start_mountain_trail_x, mountain_actual_height)
            cur_trail.mountain_box = Box(start_mountain_x, mid - mountain_actual_height/2, end_mountain_x - start_mountain_x, mountain_actual_height)
            cur_trail.after_box = Box(end_mountain_x, mid - mountain_actual_height/2, end_mountain_trail_x - end_mountain_x, mountain_actual_height)
            # Draw rest
            self.draw_in_box(height, p2/total*width, minx+p1_total_dist, miny, cur_trail.following)
        else:
            ref_trail.trail_box = Box(minx, miny, width, height)
            b1 = self.required_width(cur_trail.top)
            b2 = self.required_width(cur_trail.bottom)
            b3 = self.required_width(cur_trail.following)
            total = b3 + max(b1, b2)
            mid = miny + height/2
            pth = self.required_height(cur_trail.top)
            pbh = self.required_height(cur_trail.bottom)
            total_height = pth + pbh
            top_section = pth / total_height * (height - self.BRANCH_SEPARATION)
            bot_section = pbh / total_height * (height - self.BRANCH_SEPARATION)
            if total > 0:
                branch_dist = max(
                    max(b1, b2)/total*(width - 2*self.BRANCH_WIDTH),
                    self.MIN_BRANCH_CONTENT_WIDTH
                )
            else:
                branch_dist = self.MIN_BRANCH_CONTENT_WIDTH
            b3_dist = (width - 2*self.BRANCH_WIDTH) - branch_dist
            # Draw branches
            self.draw_branch(minx, mid, minx+self.BRANCH_WIDTH, miny + bot_section + self.BRANCH_SEPARATION + top_section / 2, miny + bot_section / 2)
            self.draw_branch(minx + width - b3_dist, mid, minx + width - self.BRANCH_WIDTH - b3_dist, miny + bot_section + self.BRANCH_SEPARATION + top_section / 2, miny + bot_section / 2)
            cur_trail.branch_start_box = Box(minx, mid - self.BRANCH_SEPARATION/2 - top_section/2, self.BRANCH_WIDTH, bot_section/2 + top_section/2 + self.BRANCH_SEPARATION)
            cur_trail.branch_end_box = Box(minx+width-b3_dist-self.BRANCH_WIDTH, mid - self.BRANCH_SEPARATION/2 - top_section/2, self.BRANCH_WIDTH, bot_section/2 + top_section/2 + self.BRANCH_SEPARATION)
            # Draw top & bottom
            self.draw_in_box(top_section, branch_dist, minx+self.BRANCH_WIDTH, miny+bot_section+self.BRANCH_SEPARATION, cur_trail.top)
            self.draw_in_box(bot_section, branch_dist, minx+self.BRANCH_WIDTH, miny, cur_trail.bottom)
            # Draw following
            self.draw_in_box(height, b3_dist, minx + width - b3_dist, miny, cur_trail.following)

    def draw_line(self, sx, sy, ex, ey):
        import arcade
        arcade.draw_line(sx, sy, ex, ey, (0, 0, 0), 1)

    def draw_mountain(self, x, y, scale, obj: Mountain):
        import arcade
        sprite_list = arcade.SpriteList()
        mountain = arcade.Sprite("img/hike.png", scale=self.MIN_MOUNTAIN_WIDTH/512 * scale)
        mountain.center_x = x
        mountain.center_y = y
        sprite_list.append(mountain)
        sprite_list.draw()
        arcade.draw_text(
            obj.difficulty_level,
            x - self.MIN_MOUNTAIN_WIDTH * scale / 2,
            y + self.MOUNTAIN_HEIGHT * scale / 2,
            (237, 17, 68),
            font_size=24,
            font_name=("Montserrat", "calibri", "arial"),
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            obj.length,
            x + self.MIN_MOUNTAIN_WIDTH * scale / 2,
            y + self.MOUNTAIN_HEIGHT * scale / 2,
            (17, 127, 245),
            font_size=24,
            font_name=("Montserrat", "calibri", "arial"),
            anchor_x="center",
            anchor_y="center"
        )


    def draw_branch(self, sx, sy, ex, ety, eby):
        import arcade
        bez_top = bezier((sx, sy), (av(sx, ex), sy), (av(sx, ex), ety), (ex, ety))
        arcade.draw_line_strip([
            bez_top(t/100)
            for t in range(101)
        ], (0, 0, 0), 1)
        bez_bot = bezier((sx, sy), (av(sx, ex), sy), (av(sx, ex), eby), (ex, eby))
        arcade.draw_line_strip([
            bez_bot(t/100)
            for t in range(101)
        ], (0, 0, 0), 1)

    def box_and_action(self, mouse_pos: tuple[float, float], mode=DrawMode, cur_trail: Trail|None=None, parent_sets: tuple[Trail, str]|None=None) -> tuple[Box|None, function|None, Trail|None]:
        if cur_trail is None:
            ref_trail = self.trail
            cur_trail = self.trail.store
            parent_sets = (self, "trail")
        else:
            ref_trail = cur_trail
            cur_trail = cur_trail.store
        if mouse_pos not in ref_trail.trail_box:
            return None, None, None
        def set_m(ref, cur_method):
            def func(*m):
                ref.store = cur_method(*m)
            return func
        def set_parent(parent_set, cur_method):
            parent, attribute = parent_set
            def func(*m):
                setattr(parent, attribute, cur_method(*m))
            return func
        if cur_trail is None:
            if mode in [DrawMode.ADD_MOUNTAIN, DrawMode.ADD_BRANCH]:
                return ref_trail.trail_box, set_parent(parent_sets, ref_trail.add_mountain_before if mode == DrawMode.ADD_MOUNTAIN else ref_trail.add_empty_branch_before), cur_trail
        elif isinstance(cur_trail, TrailSeries):
            if mouse_pos in cur_trail.before_box and mode in [DrawMode.ADD_MOUNTAIN, DrawMode.ADD_BRANCH]:
                return cur_trail.before_box, set_m(ref_trail, cur_trail.add_mountain_before if mode == DrawMode.ADD_MOUNTAIN else cur_trail.add_empty_branch_before), cur_trail
            if mouse_pos in cur_trail.mountain_box and mode in [DrawMode.REMOVE, DrawMode.EDIT]:
                return cur_trail.mountain_box, (set_m(ref_trail, cur_trail.remove_mountain) if mode == DrawMode.REMOVE else lambda: cur_trail.mountain), cur_trail
            if mouse_pos in cur_trail.after_box and mode in [DrawMode.ADD_MOUNTAIN, DrawMode.ADD_BRANCH]:
                return cur_trail.after_box, set_m(ref_trail, cur_trail.add_mountain_after if mode == DrawMode.ADD_MOUNTAIN else cur_trail.add_empty_branch_after), cur_trail
            return self.box_and_action(mouse_pos, mode, cur_trail.following, (cur_trail, 'following'))
        else:
            if mouse_pos in cur_trail.branch_start_box and mode == DrawMode.REMOVE:
                return cur_trail.branch_start_box, set_m(ref_trail, cur_trail.remove_branch), cur_trail
            if mouse_pos in cur_trail.branch_end_box and mode == DrawMode.REMOVE:
                return cur_trail.branch_end_box, set_m(ref_trail, cur_trail.remove_branch), cur_trail
            if mouse_pos in cur_trail.bottom.trail_box:
                return self.box_and_action(mouse_pos, mode, cur_trail.bottom, (cur_trail, 'bottom'))
            if mouse_pos in cur_trail.top.trail_box:
                return self.box_and_action(mouse_pos, mode, cur_trail.top, (cur_trail, 'top'))
            return self.box_and_action(mouse_pos, mode, cur_trail.following, (cur_trail, 'following'))
        return None, None, None
