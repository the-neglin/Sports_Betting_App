from shiny import App, render, ui
from shinyswatch import theme
import getters
import modules
import pandas as pd
# import putters

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
        ),
    ui.HTML("""<h1><strong>Nick's Massive Pickem</strong></h1>"""),
    ui.navset_tab(*modules.nav_controls("navset_tab()"), selected='Main')
    )
)

def server(input, output, session):
    df = getters.get_odds()
    @render.table
    def scores():
        return getters.get_leaderboard()
    
    
    #NEED TO UPDATE
    # @reactive.effect
    # @reactive.event(input.name)
    # def set_button_state():
    #     if input.name():
    #         ui.update_action_button("greet", disabled=False)
    #     else:
    #         ui.update_action_button("greet", disabled=True)

    # @render.ui
    # @reactive.event(input.greet)
    # def hello():
    #     return ui.p(f"Hello, {input.name()}!", class_="fs-1 text-primary mt-3")
    
    
    @output
    @render.ui
    def table_ui():
        # Create the UI for each row of the table
        table_rows = []
        for i, row in df.iterrows():
            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(row["Time"]),
                    ui.tags.td(row["Favorite"]),
                    ui.tags.td(row["Spread"]),
                    ui.tags.td(row["Underdog"]),
                    ui.tags.td(
                        ui.input_select(
                            f"spread_pick_{i}",
                            label="",  # Add an empty label or provide a specific label
                            choices=["None", "Favorite", "Underdog"],
                            selected=row["Spread Pick"]
                        )
                    ),
                    ui.tags.td(
                        ui.input_checkbox(
                            f"double_down_{i}",
                            label="Double?", 
                            value=row["Double Down?"]
                        )
                    ),
                                        ui.tags.td(
                        ui.input_select(
                            f"over_under_pick_{i}",
                            label="",  # Add an empty label or provide a specific label
                            choices=["None", "Over", "Under"],
                            selected=row["Over/Under Pick"]
                        )
                    )
                )
            )
        
        # Create the table with header and rows
        table = ui.tags.table(
            ui.tags.thead(
                ui.tags.tr(
                    ui.tags.th("Time"),
                    ui.tags.th("Favorite"),
                    ui.tags.th("Spread"),
                    ui.tags.th("Underdog"),
                    ui.tags.th("Spread Pick"),
                    ui.tags.th("Double Down?"),
                    ui.tags.th("Over/Under Pick"),
                )
            ),
            ui.tags.tbody(*table_rows)
        )
        
        return table
    
    @output
    @render.text
    def table_data():
        # Capture the data from the inputs
        updated_data = []
        for i in range(len(df)):
            updated_data.append({
                "Time": df.at[i, "Time"],
                "Favorite": df.at[i, "Favorite"],
                "Spread": df.at[i, "Spread"],
                "Underdog": df.at[i, "Underdog"],
                "Spread Pick": input[f"spread_pick_{i}"](),
                "Double Down?": input[f"double_down_{i}"](),
                "Over/Under Pick": input[f"over_under_pick_{i}"](),
            })
        return pd.DataFrame(updated_data).to_string(index=False)



app = App(app_ui, server)

