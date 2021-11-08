SELECT DISTINCT(name) FROM people
JOIN movies, stars
ON movies.id = stars.movie_id AND people.id = stars.person_id
WHERE title IN (SELECT title
FROM movies
JOIN people, stars
ON movies.id = stars.movie_id AND people.id = stars.person_id
WHERE name = "Kevin Bacon" AND birth = 1958)
EXCEPT SELECT name FROM people WHERE name = "Kevin Bacon";