%%%%%%%%%%%%%%%%%%%%%%%%%%%% team members %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name : Bassant Tarek , ID : 20231037 , Work : Tasks (1,4)
% Name : Rahma Bahgat  , ID : 20231056 , Work : Task (6)
% Name : Mariam Ehab   , ID : 20231160 , Work : Tasks (2,5)
% Name : Rawda Raafat  , ID : 20231067 , Work : Task (3)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



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



%%%%%%%%%%%%%%%%%%%%%%% Helpers %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Manual member function : cheack if the element is a member 
% in the list 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Base case: X is the head of the list
my_member(X, [X|_]).

% Recursive case: check in the tail
my_member(X, [_|T]) :-
    my_member(X, T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% reverse_list(L, Reversed)
% Purpose:
%   Reverses a list L and returns it as Reversed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
reverse_list(L, Reversed) :-
    reverse_helper(L, [], Reversed).   

% Base case: empty list, accumulator becomes the reversed list
reverse_helper([], Acc, Acc).

% Recursive case: move head H to accumulator and process tail
reverse_helper([H|T], Acc, Reversed) :-
    reverse_helper(T, [H|Acc], Reversed).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Task 1 : books_borrowed_by_student(Student, L)
% Purpose:
%   Collects all books borrowed by a specific student (Student)
%   and returns them in a list L.
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
% Task 2 : borrowers_count(Book, N)
% Purpose:
%   Counts how many students borrowed a specific book
%   Controls backtracking so only one answer is returned.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
borrowers_count(Book, N) :-
    collect_borrowers(Book, [], L),
    list_length(L, N),
    !.   % no backtracking

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% collect_borrowers(Book, Acc, L)
% Purpose:
%   Traverse all borrowed facts to find students who
%   borrowed the given book and put them in a list.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Case 1: Found a student who borrowed the book but not already in Acc
collect_borrowers(Book, Acc, L) :-
    borrowed(Student, Book),
    \+ my_member(Student, Acc),
    collect_borrowers(Book, [Student|Acc], L).

% Case 2: No more students to collect
collect_borrowers(_, Acc, Acc).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% list_length(List, N)
% Purpose:
%   Counts the number of elements in a list
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Base case: empty list has length 0
list_length([], 0).

% Recursive case: length of list = 1 + length of tail
list_length([_|T], N) :-
    list_length(T, N1),
    N is N1 + 1.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Rawda put ur work here plz
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task 4 : ratings_of_book(Book, L)
% Purpose:
%   Collects all ratings for a specific book and returns them
%   as a list of tuples (Student, Score).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ratings_of_book(Book, L) :-
    collect_ratings(Book, [], L), % cut: stop after the first solution (no backtracking)
    !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% collect_ratings(Book, Acc, L)
% Purpose:
%   Traverse all rating facts and accumulate ratings for
%   the given book.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Case 1: found a rating for the book
collect_ratings(Book, Acc, L) :-
    rating(Student, Book, Score),
    \+ my_member((Student,Score), Acc),
    collect_ratings(Book, [(Student,Score)|Acc], L).

% Case 2: no more ratings
collect_ratings(_, Acc, L) :-
    reverse_list(Acc, L).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task 5 : top_reviewer(Student)
% Purpose:
%   Finds the student who gave the highest single rating
%   in the whole system.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
top_reviewer(Student) :-
    find_top(Student, _),
    !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% find_top(Student, Score)
% Purpose:
%   Finds a student whose rating Score has no higher
%   rating anywhere else in the system.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
find_top(Student, Score) :-
    rating(Student, _, Score), % get a rating from any student
    \+ higher_exists(Score).   % make sure no higher rating exists

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% higher_exists(Score)
% Purpose:
%   Succeeds if there is any rating in the system
%   that is strictly higher than Score.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
higher_exists(Score) :-
    rating(_, _, Other),
    Other > Score.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task 6 : most_common_topic_for_student(Student, Topic)
% Purpose:
%   Finds the most common topic in books borrowed by a specific student
%   Controls backtracking so only one answer is returned.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% append_topics(L1, L2, Result)
% Purpose:
%   Concatenates two lists into Result
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
append_topics([], L, L) :- !.
append_topics([H|T], L2, [H|R]) :-
    append_topics(T, L2, R),
    !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% collect_topics_from_books(Books, Acc, TopicsList)
% Purpose:
%   Collects all topics from a list of books into one big list
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
collect_topics_from_books([], Acc, Acc) :- !.
collect_topics_from_books([Book|T], Acc, TopicsList) :-
    topics(Book, Topics),
    append_topics(Topics, Acc, NewAcc),
    collect_topics_from_books(T, NewAcc, TopicsList),
    !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% count_topic(Topic, List, Count)
% Purpose:
%   Counts how many times Topic appears in List
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
count_topic(_, [], 0) :- !.
count_topic(Topic, [Topic|T], Count) :-
    count_topic(Topic, T, C1),
    Count is C1 + 1,
    !.
count_topic(Topic, [H|T], Count) :-
    Topic \= H,
    count_topic(Topic, T, Count),
    !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% find_most_common(List, CurrentMaxTopic, CurrentMaxCount, Topic)
% Purpose:
%   Finds the topic with the highest frequency in the list
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
find_most_common([], Topic, _, Topic) :- !.

find_most_common([H|T], CurrentTopic, CurrentCount, Topic) :-
    count_topic(H, [H|T], Count),
    Count > CurrentCount,
    find_most_common(T, H, Count, Topic),
    !.

find_most_common([H|T], CurrentTopic, CurrentCount, Topic) :-
    count_topic(H, [H|T], Count),
    Count =< CurrentCount,
    find_most_common(T, CurrentTopic, CurrentCount, Topic),
    !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% most_common_topic_for_student(Student, Topic)
% Purpose:
%   Main predicate that returns the most common topic for a student
%   Uses cut to control unnecessary backtracking
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
most_common_topic_for_student(Student, Topic) :-
    books_borrowed_by_student(Student, Books),
    collect_topics_from_books(Books, [], AllTopics),
    find_most_common(AllTopics, none, 0, Topic),
    !.   % <-- cut to prevent extra answers