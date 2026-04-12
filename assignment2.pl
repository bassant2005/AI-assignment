% Student 1 : Bassant tarek , ID : 20231037 
%	work (functions) : find_robot() ,get_cell() ,within_bounds() 
%	,valid_cell() ,move()

%  Student 2 :  , ID :  
%	work (functions) : 

% Student 3 :  , ID :  
%	work (functions) : 

% Student 4 :  , ID :  
%	work (functions) : 
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
print_path([]).
print_path([H|T]) :-
    write(H), write(' -> '),
    print_path(T).

print_result(Path, Steps) :-
    write('Path found: '),
    print_path(Path), nl,
    write('Number of steps: '), write(Steps), nl.


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


%%%%%%%%%%%%%%%%%%%
%REMAINING WORK 
%%%%%%%%%%%%%%%%%%%


%  RUN FUNCTIONS (play with it as you want to test your work)
% =========================================================
% PART 1 (BFS - nearest survivor)
run_bfs(ResultPath, Steps) :-
    grid(Grid),
    initial_state(Grid, S),
    search([S], [], bfs, Grid, state(_, Path, _)),
    length(Path, Len),
    Steps is Len - 1,
    ResultPath = Path.

% PART 2 (GREEDY - max survivors)
run_greedy(ResultPath, Steps, Score) :-
    grid(Grid),
    initial_state(Grid, S),
    search([S], [], greedy, Grid, state(_, Path, _)),
    length(Path, Len),
    Steps is Len - 1,
    heuristic(state(_, Path, []), Grid, Score),
    ResultPath = Path.