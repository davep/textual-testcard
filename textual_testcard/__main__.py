"""Simple application to try and make a Textual display break."""

from dataclasses import dataclass
from itertools import cycle

from rich.segment import Segment
from rich.style import Style

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Click
from textual.message import Message
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Footer, Log, Tree

class TestCard(Widget, can_focus=True):

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("space", "lines", "Cycle Lines")
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.line_choices = cycle(Tree.LINES.values())
        self.lines = next(self.line_choices)

    @dataclass
    class CellPicked(Message):
        offset: int

    def on_click(self, event: Click) -> None:
        self.post_message(self.CellPicked(event.style.meta["offset"]))

    def render_line(self, y: int) -> Strip:
        lines = cycle(self.lines)
        return Strip(
            Segment(
                next(lines),
                style=Style(color=self.styles.color.rich_color, meta={"offset": (y * self.size.width) + char}),
            ) for char in range(self.size.width)
        )

    def action_lines(self) -> None:
        self.lines = next(self.line_choices)
        self.refresh()

    def action_refresh(self) -> None:
        self.refresh()

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
