# CMSC 14200 Course Project

Team members:
- QA: Kendra Kim (yejikim)
- Bot: Matthew Liew (mliew)
- TUI: Jaimny Ramos Ruballos (jramosruballos)
- GUI: Riley Yuan (ryyuan)

Enhancements
1. GUI-TITLE, click on "Start Game" button to switch interfaces and start
2. GUI-ANIMATION, animates cards being removed and added back in
3. TUI-LETTERS-X, run TUI as follows:
    'python3 src/tui.py --extended'
    This will display a tableau with the extended deck. You should be able to call fits with a size of 4.

Improvements

Game Logic
Issue with constructor. See code comment(s).
We completed the constructor by adding the correct Value Erros as needed as well
as initializing more attributes like active_players.

Issue with active_players. See code comment(s).
We changed the active players method so it just returns the active players,
and they are initialized in the constructor allowing us to edit the set when
eliminating players.

Issue with tableau. See code comment(s).
We corrected the mismatch so the return type is now correct.

Issue with non_empty_positions. See code comment(s).
The non_empty_positions property now returns a set of positions that contain cards, 
using the Tableau class.

Issue with done. See code comment(s).
The done property now reflects game completion status and is properly set in all 
game ending scenarios including lightning mode victories and eliminations. 
The property is now consistent throughout the implementation.

Issue with outcome. See code comment(s).
The outcome property now returns an empty set when the game is not done and 
calculates winners based on maximum scores when the game ends. 
It now properly tracks the outcome in various scenarios including lightning mode 
and handles ties by returning a set of tied players.

Issue with card_at. See code comment(s).
The card_at method now performs bounds checking on the position and raises a 
ValueError for out-of-bounds positions. It properly handles the null case when a
position contains no card and now returns just the features dictionary 
rather than the Card object.

Issue with call_fit. See code comment(s).
The call_fit method now has validation for player eligibility, 
position count, duplicate positions, and empty positions, 
by raising ValueError exceptions. It also correctly handles card 
replacement from the deck after successful fits and appropriately updates 
scores based on success or failure.

Issue with moonshot_start and/or moonshot_end. See code comment(s).
The moonshot methods now properly validate game state and player eligibility, 
and board fullness before allowing a moonshot. The moonshot_end method now 
calculates results based on whether the moonshot was countered and 
uses dynamic board size instead of hardcoded fit values for score adjustments.

No function header comments at all
Added function headers to all the methods under the tableau class in letters.py
as well as all of the Letters game methods

GUI
This component received two S's in Milestone 2

TUI
This component recieved two S's in Milestone 2.

Bot

Rubric Comment:
[Major] The greedy and smart strategies do not win 100% (or close to 100%) of the time against the random strategy.

I restructured the decision-making process for moonshot and end-game moves, 
ensuring they are handled within the suggest_move() function rather than the 
simulation loop. Now, both smart and  greedy bots independently analyze the 
tableau to determine optimal moments for executing these strategies. 
Additionally, I corrected the overlap calculation for the SmartBot by replacing 
the logical AND (and) with set intersection (&) accurately identifying 
overlapping fits. I also fixed the logic in my break statements to make 
sure the simulation was working correctly. These refinements correct the 
simulation and now the smart and greedy bots consistently outperform
random bots, as expected.

Rubric Comment:
The majority of the functions have a complete function header comment (but some are incomplete or missing)

Added and described each function

QA
This component received two S's in Milestone 2
