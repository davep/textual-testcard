"""Simple application to try and make a Textual display break."""

from dataclasses import dataclass
from itertools import cycle
from typing import ClassVar

from rich.segment import Segment
from rich.style import Style

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Click
from textual.message import Message
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Footer, Log, Tree

class TestCard(Widget, can_focus=True):

    COMPONENT_CLASSES: ClassVar[set[str]] = {
        "test-card--cursor",
    }

    DEFAULT_CSS = """
    TestCard > .test-card--cursor {
        background: red;
    }
    """

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("space", "lines", "Cycle Lines"),
        Binding("up", "move(0,-1)"),
        Binding("down", "move(0,1)"),
        Binding("left", "move(-1,0)"),
        Binding("right", "move(1,0)"),
        Binding("enter", "report")
    ]

    row: reactive[int] = reactive(0)
    col: reactive[int] = reactive(0)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.line_choices = cycle(Tree.LINES.values())
        self.lines = next(self.line_choices)

    @dataclass
    class CellPicked(Message):
        offset: int

    def on_click(self, event: Click) -> None:
        self.post_message(self.CellPicked(event.style.meta["offset"]))
        self.row = event.style.meta["offset"] // self.size.width
        self.col = event.style.meta["offset"] % self.size.width

    def action_report(self) -> None:
        self.post_message(self.CellPicked((self.row * self.size.width) + self.col))

    def render_line(self, y: int) -> Strip:
        lines = cycle(self.lines)
        cursor_style = self.get_component_rich_style("test-card--cursor")
        return Strip(
            Segment(
                next(lines),
                style=(
                    (cursor_style if y == self.row and char == self.col else Style(color=self.styles.color.rich_color)) +
                    Style(meta={"offset": (y * self.size.width) + char})
                ),
            ) for char in range(self.size.width)
        )

    def action_lines(self) -> None:
        self.lines = next(self.line_choices)
        self.refresh()

    def action_refresh(self) -> None:
        self.refresh()

    def action_move(self, colwise: int, rowwise: int) -> None:
        if rowwise:
            self.row += rowwise
        if colwise:
            self.col += colwise

class TestCardApp(App[None]):

    CSS = """
    TestCard {
        height: 8fr;
        color: cornflowerblue;
    }

    .io {
        background: $surface;
    }

    .io:focus {
        background: $surface-lighten-1;
    }
    """

    def compose(self) -> ComposeResult:
        yield TestCard(classes="io")
        yield Log(classes="io")
        yield Footer()

    @on(TestCard.CellPicked)
    def log_cell(self, event: TestCard.CellPicked) -> None:
        self.query_one(Log).write_line(f"{event!r}")

def run():
    TestCardApp().run()

if __name__ == "__main__":
    run()

### __main__.py ends here
