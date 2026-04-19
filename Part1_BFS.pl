% Student 1 : Bassant Tarek (20231037)
%   - find_robot()
%   - get_cell()
%   - within_bounds()
%   - valid_cell()
%   - move()

% Student 2 : Mariam Ehab (20231160)
%   - initial_state()
%   - update_state()
%   - expand()

% Student 3 : Rawda Raafat Ramadan (20231067)
%   - add_to_open()
%   - heuristic()
%   - greedy_sort()
%   - get_score()

% Student 4 : Rahma Bahgat (20231056)
%   - run_bfs()
%   - run_greedy()
%   - print_result()


% =========================================================
% Purpose:
%   Represents the environment where the robot moves
% Symbols:
%   r → robot start position
%   e → empty cell
%   d → debris (blocked)
%   f → fire (blocked)
%   s → survivor (goal)
% =========================================================
grid([
    [r, e, d, e, e],
    [e, e, f, e, s],
    [d, e, e, e, e],
    [e, s, e, f, e]
]).


% print_path(+Path)
% Purpose:
%   Prints the path step-by-step in readable format
% =========================================================
print_path([]) :- nl.

print_path([H]) :-
    H = (R,C),
    format('(~w,~w)', [R,C]), nl.

print_path([H|T]) :-
    H = (R,C),
    format('(~w,~w) -> ', [R,C]),
    print_path(T).


% print_result(+Path, +Steps, +Battery)
% Purpose:
%   Displays final search result including:
%       - Path
%       - Number of steps
%       - Remaining battery
% =========================================================
print_result(Path, Steps, Battery) :-
    write('Path found: '),
    print_path(Path), nl,
    write('Number of steps: '), write(Steps), nl,
    write('Remaining Battery: '), write(Battery), write('%'), nl.


% find_robot(+Grid, -Row, -Col)
% Purpose:
%   Finds the position of the robot (r)
% =========================================================
find_robot(Grid, R, C) :-
    nth1(R, Grid, Row),
    nth1(C, Row, r).


% get_cell(+Grid, +Row, +Col, -Value)
% Purpose:
%   Returns the value stored at a given position
% =========================================================
get_cell(Grid, R, C, Value) :-
    nth1(R, Grid, Row),
    nth1(C, Row, Value).


% within_bounds(+Grid, +Row, +Col)
% Purpose:
%   Checks if position is inside grid limits
% =========================================================
within_bounds(Grid, R, C) :-
    length(Grid, Rows),
    nth1(1, Grid, FirstRow),
    length(FirstRow, Cols),
    R >= 1, R =< Rows,
    C >= 1, C =< Cols.


% valid_cell(+Grid, +Row, +Col)
% Purpose:
%   Checks if a cell is safe to enter
% Rules:
%   - Not debris (d)
%   - Not fire (f)
% =========================================================
valid_cell(Grid, R, C) :-
    get_cell(Grid, R, C, Value),
    Value \= d,
    Value \= f.


% move(+CurrentPos, -NextPos)
% Purpose:
%   Generates all possible movements (4 directions)
% =========================================================
move((R,C), (R1,C)) :- R1 is R - 1. % Up
move((R,C), (R1,C)) :- R1 is R + 1. % Down
move((R,C), (R,C1)) :- C1 is C - 1. % Left
move((R,C), (R,C1)) :- C1 is C + 1. % Right


% valid_move(+Grid, +CurrentPos, -NextPos)
% Purpose:
%   Filters moves to keep only valid ones
% =========================================================
valid_move(Grid, (R,C), (R1,C1)) :-
    move((R,C), (R1,C1)),
    within_bounds(Grid, R1, C1),
    valid_cell(Grid, R1, C1).


% initial_state(+Grid, -State)
% Purpose:
%   Builds the initial state:
%       Position, Path, Battery, Survivors count
% =========================================================
initial_state(Grid, state((R,C), [(R,C)], 100, Survivors)) :-
    find_robot(Grid, R, C),
    get_cell(Grid, R, C, Value),
    ( Value = s -> Survivors is 1 ; Survivors is 0 ).


% update_state(+State, +NewPos, +Grid, -NewState)
% Purpose:
%   Updates state after movement:
%       - Extends path
%       - Decreases battery
%       - Updates survivors count
% =========================================================
update_state(state(_, Path, Battery, S), NewPos, Grid,
             state(NewPos, NewPath, NewBattery, NewS)) :-

    append(Path, [NewPos], NewPath),
    NewBattery is Battery - 10,

    NewPos = (R,C),
    get_cell(Grid, R, C, Value),
    ( Value = s -> NewS is S + 1 ; NewS is S ).


% expand(+State, +Grid, -Children)
% Purpose:
%   Generates all valid next states
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


% goal(+State, +Grid)
% Purpose:
%   Checks if robot reached a survivor
% =========================================================
goal(state((R,C), _, _, _), Grid) :-
    get_cell(Grid, R, C, s).


% add_to_open(+Strategy, +Children, +Open, -NewOpen)
% Purpose:
%   Adds new states depending on strategy
%   BFS → FIFO queue
% =========================================================
add_to_open(bfs, Children, Open, NewOpen) :-
    append(Open, Children, NewOpen).


% Case 1: No solution
search([], _, _, _, _) :-
    write('No path found'), nl, fail.


% Case 2: Goal reached
search([Current | _], _, bfs, Grid, Current) :-
    goal(Current, Grid), !.


% Case 3: Skip visited nodes
search([Current | RestOpen], Closed, Strategy, Grid, Solution) :-
    Current = state(Pos, _, _, _),
    member(Pos, Closed),
    search(RestOpen, Closed, Strategy, Grid, Solution).


% Case 4: Expand and continue search
search([Current | RestOpen], Closed, Strategy, Grid, Solution) :-
    Current = state(Pos, _, _, _),
    \+ member(Pos, Closed),

    expand(Current, Grid, Children),
    add_to_open(Strategy, Children, RestOpen, NewOpen),

    search(NewOpen, [Pos | Closed], Strategy, Grid, Solution).


% run_bfs(-Path, -Steps)
% Purpose:
%   Executes BFS and prints result
% =========================================================
run_bfs(ResultPath, Steps) :-
    grid(Grid),
    initial_state(Grid, S),

    search([S], [], bfs, Grid, state(_, Path, Battery, _)),

    length(Path, Len),
    Steps is Len - 1,
    ResultPath = Path,

    print_result(Path, Steps, Battery), !.
