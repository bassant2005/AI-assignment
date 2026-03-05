%%%%%%%%%%%%%%%%%%%%%%%%%%%% team members Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name : Bassant Tarek , ID : 20231037 , Work : Tasks(1,4)
% 
% 
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%% Students Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% student(Name, Year)

student(ali, first).
student(sara, second).
student(omar, third).
student(mona, second).
student(yousef, first).
student(nour, fourth).
student(karim, third).

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Books Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% book(Title, Author)

book(prolog_fundamentals, dr_hassan).
book(recursion_in_depth, dr_sara).
book(list_programming, dr_ahmed).
book(ai_intro, dr_mona).

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Borrow Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% borrowed(Student, Book)

borrowed(ali, prolog_fundamentals).
borrowed(ali, list_programming).

borrowed(sara, recursion_in_depth).
borrowed(sara, ai_intro).

borrowed(omar, recursion_in_depth).

borrowed(mona, prolog_fundamentals).
borrowed(mona, recursion_in_depth).
borrowed(mona, list_programming).

borrowed(yousef, list_programming).

borrowed(nour, ai_intro).

borrowed(karim, recursion_in_depth).

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Topics Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% topics(Book, TopicsList)

topics(prolog_fundamentals, [facts, rules, queries, unification]).
topics(recursion_in_depth, [base_case, recursive_case, tracing, termination]).
topics(list_programming, [head_tail, member, append, length, prefix, suffix]).
topics(ai_intro, [search, logic, knowledge_representation]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Ratings Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% rating(Student, Book, Score)

rating(ali, prolog_fundamentals, 85).
rating(ali, list_programming, 90).

rating(sara, recursion_in_depth, 95).
rating(sara, ai_intro, 88).

rating(omar, recursion_in_depth, 80).

rating(mona, prolog_fundamentals, 92).
rating(mona, recursion_in_depth, 89).
rating(mona, list_programming, 91).

rating(yousef, list_programming, 60).

rating(nour, ai_intro, 78).

rating(karim, recursion_in_depth, 83).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Manual member function : cheack if the element is a member 
% in the list 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Base case: X is the head of the list
my_member(X, [X|_]).

% Recursive case: check in the tail
my_member(X, [_|T]) :-
    my_member(X, T).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Task 1 : books_borrowed_by_student(Student, L)
% Purpose:
%   Collects all books borrowed by a specific student (Student)
%   and returns them in a list L.
% How it works:
%   1. Calls `collect_books` with an empty accumulator to 
%      start collecting books.
%   2. Uses a cut (!) to stop searching after the first solution.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
books_borrowed_by_student(Student, L) :-
    collect_books(Student, [], L),
    !.   % cut: stop after the first solution (no backtracking)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% collect_books(Student, Acc, L)
% Purpose:
%   Traverse all `borrowed` facts to find books borrowed by
%   a student and accumulate them in a list.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Case 1: Student borrowed a book not already in Acc
collect_books(Student, Acc, L) :-
    borrowed(Student, Book),      % find a borrowed book for the student
    \+ my_member(Book, Acc),         % check that it is not already in accumulator
    collect_books(Student, [Book|Acc], L).  % add to accumulator and continue

% Case 2: No more books to collect
collect_books(_, Acc, L) :-
    reverse_list(Acc, L).         % reverse accumulator to preserve original order


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% reverse_list(L, Reversed)
% Purpose:
%   Reverses a list L and returns it as Reversed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
reverse_list(L, Reversed) :-
    reverse_helper(L, [], Reversed).   % use helper predicate with accumulator

% Base case: empty list, accumulator becomes the reversed list
reverse_helper([], Acc, Acc).

% Recursive case: move head H to accumulator and process tail
reverse_helper([H|T], Acc, Reversed) :-
    reverse_helper(T, [H|Acc], Reversed).