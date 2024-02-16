import json
from pathlib import Path

from reactpy import component, hooks, html, run

HERE = Path(__file__)
DATA_PATH = HERE.parent / "data.json"
food_data = json.loads(DATA_PATH.read_text())
sculpture_data = json.loads(DATA_PATH.read_text())


@component
def Search(value, set_value):
    def handle_change(event):
        set_value(event["target"]["value"])

    return html.label(
        "Search by Sculpture Name: ",
        html.input({"value": value, "on_change": handle_change}),
    )



@component
def Table(value, set_value):
    rows = []
    for row in food_data:
        name = html.td(row["name"])
        descr = html.td(row["description"])
        tr = html.tr(name, descr, value)
        if not value:
            rows.append(tr)
        elif value.lower() in row["name"].lower():
            rows.append(tr)
        headers = html.tr(html.td(html.b("name")), html.td(html.b("description")))
    table = html.table(html.thead(headers), html.tbody(rows))
    return table

@component
def FilterableList(value, set_value ):
    
    return html.aside({"class_name": "filtre","id":"filtre"},Search(value, set_value), 
                  html.hr(), 
                  Table(value, set_value),
                
                
            
            )



@component
def hello_world(recipient: str):
    return html.h1(f"Hello {recipient}!")

@component
def PrintButton(display_text, message_text):
    index, set_index = hooks.use_state(0)
    def handle_event(event):
        set_index(index + 1)

    return html.div({"style": {"width":"100%"}},
        html.button({"on_click": handle_event}, display_text),
        *([html.p(message_text) for _ in range(index)] if index != 0 else "")
        )

@component
def Gallery():
    index, set_index = hooks.use_state(0)
    show_more, set_show_more = hooks.use_state(False)

    def handle_next_click(event):
        set_index(index + 1)

    def handle_more_click(event):
        set_show_more(not show_more)

    bounded_index = index % len(sculpture_data)
    sculpture = sculpture_data[bounded_index]
    alt = sculpture["alt"]
    artist = sculpture["artist"]
    description = sculpture["description"]
    name = sculpture["name"]

    return html.div(
        html.button({"on_click": handle_next_click}, "Next"),
        html.h2(name, " by ", artist),
        html.img({ "alt": alt, "style": {"height": "200px"}}),
        html.p(f"({bounded_index + 1} or {len(sculpture_data)})"),
        html.div(
            html.button(
                {"on_click": handle_more_click},
                f"{('Show' if show_more else 'Hide')} details",
            ),
            (html.p(description) if show_more else ""),
        ),
    )

@component
def App():
    return html.div(
        html.section({"style": {"width": "50%", "float": "left"}}, Gallery()),
        html.section({"style": {"width": "50%", "float": "left"}}, Gallery()),
    )
@component
def PresentationApp():
    index, set_index = hooks.use_state(0)
    value, set_value = hooks.use_state("")
    def handle_next_click(event):
        set_index((index + 1)% 3)
    
    liste_comp = [html.div({"style": {"display": "flex","width":"100%"}},PrintButton("Play", "Playing"),PrintButton("Pause", "Pause")),
                  App(),
                  FilterableList(value, set_value)
     ]
    return html.div({"style": {"display": "flex","flex_flow":"column","gap":"30px"}},
                    html.button({"on_click": handle_next_click},"Next component" ),liste_comp[index])
