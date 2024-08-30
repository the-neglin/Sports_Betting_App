from shiny import App, render, ui, reactive
from shinyswatch import theme
import getters
import putters
import modules
import pandas as pd

app_ui = ui.page_fluid(
    theme.superhero(),
    ui.tags.style(
        """
        table.dataframe {
            text-align: center;
        }
        table.dataframe th {
            text-align: center;
        }
        """
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h4('Leaderboard'),
            ui.p(f'Latest Score: {getters.get_last_score()} CT'),
            ui.output_table("scores"),
            open='always',
            position='right',
            width=325
        ),
    ui.HTML("""<h1><strong>Nick's Massive Pickem</strong></h1>"""),
    ui.navset_tab(*modules.nav_controls("navset_tab()"), selected='Main')
    )
)

def server(input, output, session):

    @render.table
    def scores():
        return getters.get_leaderboard()

    @reactive.Calc
    def name():
        return input.name().strip()

    @reactive.Calc
    def email():
        return input.email().strip()

    loaded_data = reactive.Value(None)

    @reactive.Effect
    @reactive.event(input.load_picks, ignore_none=True)
    def _():
        print("Getting odds data...")
        data = getters.get_odds(name=name(), email=email())
        loaded_data.set(data)
        print("Loaded odds data:", data)

    @output
    @render.ui
    @reactive.event(loaded_data)
    def table_ui():
        df = loaded_data.get()

        if df.empty:
            return ui.HTML("<p>No data available. Please press 'Load Picks'.</p>")

        table_rows = []
        for i, row in df.iterrows():
            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(row["Time"]),
                    ui.tags.td(row["Favorite"]),
                    ui.tags.td(row["Spread"]),
                    ui.tags.td(row["Underdog"]),
                    ui.tags.td(row["Over/Under"]),
                    ui.tags.td(
                        ui.input_select(
                            f"spread_pick_{i}",
                            label="",
                            choices=["None", "Favorite", "Underdog"],
                            selected=row.get("Spread Pick", "None"), selectize=True, width='93%'
                        )
                    ),
                    ui.tags.td(
                        ui.input_checkbox(
                            f"double_down_{i}",
                            label="Double?",
                            value=row.get("Double Down?", False), width='50%'
                        )
                    ),
                    ui.tags.td(
                        ui.input_select(
                            f"over_under_pick_{i}",
                            label="",
                            choices=["None", "Over", "Under"],
                            selected=row.get("Over/Under Pick", "None"), selectize=True, width='80%'
                        )
                    )
                )
            )

        table = ui.tags.table(
            ui.tags.thead(
                ui.tags.tr(
                    ui.tags.th("Time"),
                    ui.tags.th("Favorite"),
                    ui.tags.th("Spread"),
                    ui.tags.th("Underdog"),
                    ui.tags.th("Over/Under"),
                    ui.tags.th("Spread Pick"),
                    ui.tags.th("Double Down?"),
                    ui.tags.th("Over/Under Pick"),
                )
            ),
            ui.tags.tbody(*table_rows)
        )

        return table

    @reactive.Effect
    @reactive.event(input.submit_picks)
    def update_data():
        df = loaded_data.get()
        updated_data = []
        for i in range(len(df)):
            updated_data.append({
                "Time": df.at[i, "Time"],
                "Favorite": df.at[i, "Favorite"],
                "Spread": df.at[i, "Spread"],
                "Underdog": df.at[i, "Underdog"],
                "Over/Under": df.at[i, "Over/Under"],
                "Spread Pick": input[f"spread_pick_{i}"](),
                "Double Down?": input[f"double_down_{i}"](),
                "Over/Under Pick": input[f"over_under_pick_{i}"](),
                "user_id": df.at[i, "user_id"],
                "game_id": df.at[i, "game_id"],
            })

        updated_df = pd.DataFrame(updated_data)

        loaded_data.set(updated_df)
        putters.put_picks(updated_df)
        print("Updated picks:", updated_df)

    @output
    @render.text
    @reactive.event(loaded_data)
    def table_data():
        df = loaded_data.get()
        return df.to_string(index=False)


app = App(app_ui, server)