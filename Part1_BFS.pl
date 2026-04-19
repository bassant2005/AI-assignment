% Student 1 : Bassant Tarek, ID : 20231037 
%	work (functions) : find_robot() , get_cell() , within_bounds() 
%	, valid_cell() , move()

%  Student 2 : Mariam Ehab, ID : 20231160 
%	work (functions) : initial_state() , update_state() , expand()

% Student 3 : Rawda Raafat Ramadan, ID : 20231067
%	work (functions) : add_to_open() , heuristic() , greedy_sort(), get_score()

% Student 4 : Rahma Bahgat , ID : 20231056
%	work (functions) : run_bfs() , run_greedy() , print_result()
% ---------------------------------------------------------

% Example grid (change for testing)
grid([
    [r, e, d, e, e],
    [e, e, f, e, s],
    [d, e, e, e, e],
    [e, s, e, f, e]
]).

% displaying the final output of the search in a readable format.
% It prints the path step-by-step and shows the total number of steps taken by the robot.
% =========================================================

print_path([]) :- nl.
print_path([H]) :-
    H = (R,C),
    format('(~w,~w)', [R,C]), nl.
print_path([H|T]) :-
    H = (R,C),
    format('(~w,~w) -> ', [R,C]),
    print_path(T).

print_result(Path, Steps, Battery) :-
    write('Path found: '),
    print_path(Path), nl,
    write('Number of steps: '), write(Steps), nl,
    write('Remaining Battery: '), write(Battery), write('%'), nl.


% Purpose:
%   Finds the position of the robot 'r' in the grid.
% How it works:
%   - nth1(R, Grid, Row): tries each row
%   - nth1(C, Row, r): finds column where value = r
%   - Prolog automatically searches using backtracking
% =========================================================
find_robot(Grid, R, C) :-
    nth1(R, Grid, Row),
    nth1(C, Row, r).


% Purpose:
%   Retrieves the value of a specific cell in the grid.
% How it works:
%   - Gets row R using nth1
%   - Gets column C from that row
% =========================================================
get_cell(Grid, R, C, Value) :-
    nth1(R, Grid, Row),
    nth1(C, Row, Value).


% Purpose:
%   Ensures that a position is inside the grid boundaries.
% How it works:
%   - Finds total number of rows
%   - Finds total number of columns
%   - Checks:
%       1 <= R <= Rows
%       1 <= C <= Cols
% =========================================================
within_bounds(Grid, R, C) :-
    length(Grid, Rows),
    nth1(1, Grid, FirstRow),
    length(FirstRow, Cols),
    R >= 1, R =< Rows,
    C >= 1, C =< Cols.


% Purpose:
%   Checks if a cell is safe for the robot to enter.
% Rules:
%   - Cannot enter:
%       d → debris
%       f → fire
%   - Can enter:
%       e → empty
%       s → survivor
%       r → starting position
% How it works:
%   - Gets the value of the cell
%   - Ensures it is NOT d and NOT f
% =========================================================
valid_cell(Grid, R, C) :-
    get_cell(Grid, R, C, Value),
    Value \= d,
    Value \= f.


% Purpose:
%   Generates all possible movements from a position.
% Allowed movements:
%   - Up    → (R-1, C)
%   - Down  → (R+1, C)
%   - Left  → (R, C-1)
%   - Right → (R, C+1)
% =========================================================
move((R,C), (R1,C)) :- R1 is R - 1. % Up
move((R,C), (R1,C)) :- R1 is R + 1. % Down
move((R,C), (R,C1)) :- C1 is C - 1. % Left
move((R,C), (R,C1)) :- C1 is C + 1. % Right


% Purpose:
%   Produces ONLY valid moves for the robot.
% Flow:
%   move → filter by bounds → filter by obstacles
% =========================================================
valid_move(Grid, (R,C), (R1,C1)) :-
    move((R,C), (R1,C1)),
    within_bounds(Grid, R1, C1),
    valid_cell(Grid, R1, C1).


% initial_state(+Grid, -State)
% Purpose: Builds the initial state before search starts
% =========================================================
initial_state(Grid, state((R,C), [(R,C)], 100, Survivors)) :-
    find_robot(Grid, R, C),
    get_cell(Grid, R, C, Value),
    ( Value = s -> Survivors is 1 ; Survivors is 0 ).


% update_state(+State, +NewPos, +Grid, -NewState)
% Purpose: Updates state after moving to a new position
% =========================================================
update_state(state(_, Path, Battery, S), NewPos, Grid,
             state(NewPos, NewPath, NewBattery, NewS)) :-

    % Update path
    append(Path, [NewPos], NewPath),

    % Decrease battery
    NewBattery is Battery - 10,

    % Check if new cell has a survivor
    NewPos = (R,C),
    get_cell(Grid, R, C, Value),

    ( Value = s -> NewS is S + 1 ; NewS is S ).


% expand(+State, +Grid, -Children)
% Purpose: Generates all valid successor states
% =========================================================
expand(state(Pos, Path, Battery, S), Grid, Children) :-
    Battery > 0,
    findall(
        Child,
        (
            valid_move(Grid, Pos, NewPos),
            \+ member(NewPos, Path),
            update_state(state(Pos, Path, Battery, S), NewPos, Grid, Child)
        ),
        Children
    ).


% No expansion if battery is empty
expand(state(_, _, 0, _), _, []).


% Goal for BFS: reach a survivor
goal(state((R,C), _, _, _), Grid) :-
    get_cell(Grid, R, C, s).


% Purpose:
%   Manages how states are added to the OPEN list.
% Behavior:
%   - BFS → acts like a queue (FIFO)
% =========================================================
add_to_open(bfs, Children, Open, NewOpen) :-
    append(Open, Children, NewOpen).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%REMAINING WORK :
% Member x
%% BFS SEARCH (OPEN + CLOSED EXPLICIT)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Purpose:
%   Main search engine for BFS.
%   It uses:
%       - OPEN list → states to be explored
%       - CLOSED list → visited positions (to avoid loops)
% How it works:
%   - Repeatedly takes the first state from OPEN
%   - Checks if it is the goal
%   - Otherwise expands it and continues searching
% =========================================================

% Case 1:
%   If OPEN list is empty → no solution exists
search([], _, _, _, _) :-
    write('No path found'), nl, fail.


% Case 2:
%   If the current state is the goal → stop search
% How it works:
%   - Takes the first element in OPEN
%   - Checks goal condition
%   - Returns it as the solution
% =========================================================
search([Current | _], _, bfs, Grid, Current) :-
    goal(Current, Grid), !.


% Case 3:
%   Skip already visited positions
% Why:
%   - Prevents infinite loops
%   - Avoids revisiting same cell
% How it works:
%   - Extract position from state
%   - If already in CLOSED → ignore it
%   - Continue with rest of OPEN
% =========================================================
search([Current | RestOpen], Closed, Strategy, Grid, Solution) :-
    Current = state(Pos, _, _, _),
    member(Pos, Closed),
    search(RestOpen, Closed, Strategy, Grid, Solution).


% Case 4:
%   Expand current state and continue search
% How it works:
%   1. Extract current position
%   2. Ensure it is not visited before
%   3. Generate children using expand/3
%   4. Add children to OPEN (FIFO for BFS)
%   5. Add current position to CLOSED
%   6. Continue searching recursively
% =========================================================
search([Current | RestOpen], Closed, Strategy, Grid, Solution) :-
    Current = state(Pos, _, _, _),
    \+ member(Pos, Closed),

    % Generate next possible states
    expand(Current, Grid, Children),

    % Add children to OPEN list based on strategy
    add_to_open(Strategy, Children, RestOpen, NewOpen),

    % Continue search with updated OPEN and CLOSED
    search(NewOpen, [Pos | Closed], Strategy, Grid, Solution).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%  RUN FUNCTIONS (play with it as you want to test your work)
% =========================================================
% PART 1 (BFS - nearest survivor)
% Fixed: extracts Battery from final state and passes it to print_result
run_bfs(ResultPath, Steps) :-
    grid(Grid),
    initial_state(Grid, S),
    search([S], [], bfs, Grid, state(_, Path, Battery, _)),
    length(Path, Len),
    Steps is Len - 1,
    ResultPath = Path,
    print_result(Path, Steps, Battery), !.
