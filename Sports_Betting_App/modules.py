from shiny import ui
from typing import List
from shiny.types import NavSetArg
import getters
import js_scripts

def nav_controls(prefix: str) -> List[NavSetArg]:
    return [
        ui.nav_panel("Main", main_tab()),
        ui.nav_panel("Intro", intro()),
        ui.nav_panel("Rules", rules()),
            ]
    
def rules():
    return [
        ui.HTML("""<p>Welcome to the thrilling world of sports betting! 
                Let’s dive into some fun terms and how they work. First up, we have the "Spread" or "Line." 
                This is your magic number that tells you which team is favored and by how many points. 
                You might see it written as "Team A -X" or "Team B +X".</p> 
                <p>Here’s the scoop: Team A is the Favorite, and they’re expected to win by X points. 
                Meanwhile, Team B is the Underdog, and they're expected to lose by X points.</p> 
                <p>So, to pick against the spread, the Favorite needs to win by X points or more, 
                while the Underdog needs to either win outright or lose by less than X points. 
                Think of it this way: if you subtract the spread from the Favorite's final score, 
                who would come out on top?</p> <p>Let’s look at a real-world example. 
                Suppose the Vikings are favored by 3 points against the Eagles. 
                This would be shown as Vikings -3 or Eagles +3.</p> <ul> <li>If the game ends Vikings 27 - Eagles 23, 
                and we adjust the Vikings' score by the spread (27 - 3 = 24), the Vikings still win. 
                Since they beat the Eagles by more than 3 points, they covered the spread. 
                So, picking the Vikings would have earned you +1 point!</li> 
                <li>However, if the game ended Vikings 27 - Eagles 25, 
                and we adjust the Vikings' score by the spread (27 - 3 = 24), the Vikings now lose. 
                Even though the Eagles lost the game, they covered the spread, 
                making them the winners in this betting scenario. 
                Thus, picking the Eagles would have earned you +1 point!</li> </ul> 
                <p>Now, let's add some spice with Over/Under betting! 
                Here, you’re betting on whether the total score of both teams combined will be over or under a specific
                number, known as the “Over/Under” line.</p> <ul> 
                <li>If you bet on the Over and the combined score of the Vikings and Eagles is 51 or more, 
                you win +1 point!</li> <li>If the total score is 50 or less and you bet on the Under, 
                you also win +1 point!</li> <li>But, if the total score doesn’t match your bet—either over or 
                under—you don’t win that round.</li> </ul> <p>So whether you’re betting on the spread or the over/under,
                remember: It’s all about the numbers and who can best predict them. 
                Enjoy the game and may the odds be ever in your favor!</p>""")
    ]
    
def intro():
    return [
        ui.HTML("""
<body>
    <h1>🏈 <span class="highlight">Nick's Epic Pickem: Year 1 – The Game Begins!</span> 🏈</h1>

    <p>Hold onto your jerseys, folks! It’s that time of year again, and we’re kicking off <span class="highlight">Nick's Epic Pickem: Year 1</span> with all the pizzazz and pizzazz that a sports betting league can muster—plus a generous sprinkling of terrible football puns!</p>

    <p>If you thought supply chain issues would keep us from delivering a heaping helping of gridiron fun, think again! We’re back with a whole new season of nail-biting picks, questionable predictions, and puns that’ll make you groan louder than a missed field goal.</p>

    <p>Just in case you missed our previous epic sagas (and let’s be honest, who could forget?), here’s a quick look back at our “illustrious” history:</p>

    <ul>
        <li><span class="highlight">HA JK THIS IS YEAR 1!!</span></li>
    </ul>

    <p>And now, drumroll please… <span class="highlight">Nick's Epic Pickem: Year 1</span> is here to make its grand debut!</p>

    <p>So, what’s the game plan? It’s simple:</p>

    <ol>
        <li><strong>Weekly Spreads</strong> – I’ll post the spreads for all NFL games. No, that’s not a typo—spreads, not bread spreads. 🍞 Plus, we’ve got the over/under for each game—think of it as a bet on whether the scoreboard’s about to throw a party or take a nap! 🎉💤</li>
        <li><strong>Make Your Picks</strong> – Choose the favorite, the underdog, or just sit on the sidelines if you’re feeling a bit shy. And don’t forget the over/under—it’s like predicting if the teams will binge or diet on points! 🏈🍔🥗</li>
        <li><strong>Double Down</strong> – Got a spread you’re super confident about? Go ahead, double down on it! If you’re right, it’s double the points—if you’re wrong, well, let’s just say you’ll be wishing you’d bet on the coin toss instead. 🤷‍♂️🪙</li>
        <li><strong>Score Big</strong> – Each right pick nets you +1 point, each wrong one drops you -1 point. Non-answers and ties? They’re worth zero points—just like that last-minute Hail Mary that fell short! 🚫 As for the over/under, nail it and add a bonus point, but miss and you’ll be crying over spilled nachos. 😢🧀</li>
    </ol>

    <p>The stakes are high and the payouts are hot:</p>

    <ul>
        <li><strong>1st Place</strong>: 60% of the pot—because who doesn’t love the sweet taste of victory?</li>
        <li><strong>2nd Place</strong>: 25%—because being the runner-up isn’t so bad when you’ve got a little cash to cushion the fall.</li>
        <li><strong>Last Place</strong>: 15%—yes, even the person who picks every game wrong gets a little something. Hey, we’ve all had those seasons!</li>
    </ul>

    <p>Entry fee is still just a crisp $20. Let’s aim for a pot so big it makes the Super Bowl look like a backyard scrimmage!</p>

    <p>Pay up via cash, mail, or Venmo me at <a href="https://venmo.com/Nicholas-Eglin">@Nicholas-Eglin</a>. Don’t forget to include your name and email so I know who’s in the game.</p>

    <p>Invite everyone you know—friends, family, neighbors, that guy who sells hot dogs outside the stadium—let’s make this league as packed as a playoff game!</p>

    <p>Ready to dive into the action? <span class="highlight">GOTTA PICK EM ALL!!!</span></p>
</body>
                """)
    ]
    
    
def main_tab():
    week_number = getters.get_week()
    return [
        ui.card(
            ui.card_header(ui.HTML(f"""
                <div style="text-align: center;">
                    <h2>🏈Week {week_number}🏈</h2>
                    <ol style="display: inline-block; text-align: left;">
                        <li>Enter your name (use the same one each week)</li>
                        <li>Enter your email (use the same one each week)</li>
                        <li><strong>CLICK</strong> Load Picks</li>
                        <li>Choose the teams you think will beat the spread</li>
                        <li><strong>CLICK</strong> Submit Picks</li>
                        <li>Make sure you receive a confirmation email</li>
                        <li>Come back to edit any picks up until that game starts</li>
                    </ol>
                </div>
            """)),
            ui.p(ui.row(
                    ui.column(12, ui.input_text('name', 'Name', '', width=12)),
                    ui.column(12, ui.input_text('email', 'Email', '', width=12)),
                    style="text-align: center;"
                )),
                ui.card_footer(
                ui.input_action_button('load_picks', 'Load Picks', class_="btn-success", style="display: block; margin: 0 auto;", disabled=True),
                ui.tags.script(js_scripts.form_completion()),

            ),
            full_screen=True,
        ),
        ui.card(
            ui.p(
                ui.output_ui("table_ui"),
            ),
            ui.card_footer(
                ui.input_action_button('submit_picks', 'Submit Picks', class_="btn-success", style="display: block; margin: 0 auto;")
            ),
            full_screen=True,
        )
    ]