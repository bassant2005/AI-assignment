% Student 1 : Bassant Tarek, ID : 20231037 
%	work (functions) : find_robot() , get_cell() , within_bounds() 
%	, valid_cell() , move()

%  Student 2 : Mariam Ehab, ID : 20231160 
%	work (functions) : initial_state() , update_state() , expand()

% Student 3 : Rawda Raafat Ramadan, ID : 20231067
%	work (functions) : add_to_open() , heuristic() , greedy_sort()
%	, get_score()

% Student 4 : Rahma Bahgat , ID : 20231056
%	work (functions) : run_greedy() , print_result()
% ---------------------------------------------------------

% Example grid (change for testing)
% there is a solution
%grid([
 %   [r, e, s],
%	[d, f, e],
%[e, s, e]
%]).

% grid([
% 	[r, e, d, e, e],
%	[e, e, f, e, s],
%	[d, e, e, e, d],
%	[e, s, e, f, s]
%]).

% battery test
 grid([
     [r, e, e, e, e],
     [e, d, d, d, e],
     [e, d, s, d, e],
     [e, d, d, d, e],
     [e, e, e, e, e]
 ]).


% displaying the final output of the search in a readable format.
% It prints the path step-by-step and shows the total number of 
% steps taken by the robot.
% =========================================================
print_path([]) :- nl.
print_path([H]) :-
    H = (R,C),
    format('(~w,~w)', [R,C]), nl.
print_path([H|T]) :-
    H = (R,C),
    format('(~w,~w) -> ', [R,C]),
    print_path(T).

print_result(Path, Steps, Score, survivors) :-
    write('Path found: '),
    print_path(Path),
    write('Survivors rescued: '), write(Score), nl,
    write('Number of steps: '), write(Steps), nl.


% Purpose:
%   Finds the position of the robot 'r' in the grid.
% =========================================================
find_robot(Grid, R, C) :-
    nth1(R, Grid, Row),
    nth1(C, Row, r).


% Purpose:
%   Retrieves the value of a specific cell in the grid.
% =========================================================
get_cell(Grid, R, C, Value) :-
    nth1(R, Grid, Row),
    nth1(C, Row, Value).


% Purpose:
%   Ensures that a position is inside the grid boundaries.
% =========================================================
within_bounds(Grid, R, C) :-
    length(Grid, Rows),
    nth1(1, Grid, FirstRow),
    length(FirstRow, Cols),
    R >= 1, R =< Rows,
    C >= 1, C =< Cols.


% Purpose:
%   Checks if a cell is safe for the robot to enter.
% =========================================================
valid_cell(Grid, R, C) :-
    get_cell(Grid, R, C, Value),
    Value \= d,
    Value \= f.


% Purpose:
%   Generates all possible movements from a position.
% =========================================================
move((R,C), (R1,C)) :- R1 is R - 1.
move((R,C), (R1,C)) :- R1 is R + 1.
move((R,C), (R,C1)) :- C1 is C - 1.
move((R,C), (R,C1)) :- C1 is C + 1.


% Purpose:
%   Produces ONLY valid moves for the robot.
% =========================================================
valid_move(Grid, (R,C), (R1,C1)) :-
    move((R,C), (R1,C1)),
    within_bounds(Grid, R1, C1),
    valid_cell(Grid, R1, C1).


% Purpose:
%   Builds the initial state
% =========================================================
initial_state(Grid, state((R,C), [(R,C)], 100, Survivors)) :-
    find_robot(Grid, R, C),
    get_cell(Grid, R, C, Value),
    ( Value = s -> Survivors is 1 ; Survivors is 0 ).


% Purpose:
%   Updates state after movement
% =========================================================
update_state(state(_, Path, Battery, S), NewPos, Grid,
             state(NewPos, NewPath, NewBattery, NewS)) :-

    append(Path, [NewPos], NewPath),
    NewBattery is Battery - 10,

    NewPos = (R,C),
    get_cell(Grid, R, C, Value),
    ( Value = s -> NewS is S + 1 ; NewS is S ).


% Purpose:
%   Generates all valid successor states
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

expand(state(_, _, 0, _), _, []).


% Purpose:
%   Adds states to OPEN (Greedy)
% =========================================================
add_to_open(greedy, Children, Open, NewOpen) :-
    append(Open, Children, TempOpen),
    greedy_sort(TempOpen, NewOpen).


% Purpose:
%   Heuristic = number of survivors collected
% =========================================================
heuristic(state(_, _, _, Survivors), _, Score) :-
    Score is Survivors.


% Purpose:
%   Sort OPEN descending by heuristic
% =========================================================
greedy_sort(Open, Sorted) :-
    map_list_to_pairs(get_score, Open, Pairs),
    keysort(Pairs, SortedAsc),
    reverse(SortedAsc, SortedDesc),
    pairs_values(SortedDesc, Sorted).


% Purpose:
%   Extract heuristic score
% =========================================================
get_score(State, Score) :-
    heuristic(State, _, Score).


% GREEDY SEARCH (OPEN + CLOSED EXPLICIT)
% =========================================================

% Case 1:
%   If OPEN list is empty → return best solution found
search([], _, _, _, Best, Best).

% Case 2:
%   Skip states with no battery
search([Current | RestOpen], Closed, Strategy, Grid, BestSoFar, Solution) :-
    Current = state(_, _, Battery, _),
    Battery =< 0,
    search(RestOpen, Closed, Strategy, Grid, BestSoFar, Solution).

% Case 3:
%   Skip already visited positions
search([Current | RestOpen], Closed, Strategy, Grid, BestSoFar, Solution) :-
    Current = state(Pos, _, _, _),
    member(Pos, Closed),
    search(RestOpen, Closed, Strategy, Grid, BestSoFar, Solution).

% Case 4:
%   Update BEST solution if current is better
search([Current | RestOpen], Closed, Strategy, Grid, BestSoFar, Solution) :-
    Current = state(Pos, _, Battery, S1),
    BestSoFar = state(_, _, _, S2),

    ( S1 > S2 -> NewBest = Current ; NewBest = BestSoFar ),

    Battery > 0,
    \+ member(Pos, Closed),

    expand(Current, Grid, Children),
    add_to_open(Strategy, Children, RestOpen, NewOpen),

    search(NewOpen, [Pos | Closed], Strategy, Grid, NewBest, Solution).


% PART 2 (GREEDY - max survivors)
run_greedy(Steps, Score) :-
    grid(Grid),
    initial_state(Grid, Initial),

    % initial best = initial state
    search([Initial], [], greedy, Grid, Initial, state(_, Path, _, Score)),

    length(Path, Len),
    Steps is Len - 1,
    print_result(Path, Steps, Score, survivors), !.
