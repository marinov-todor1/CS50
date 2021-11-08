SELECT name
FROM people
JOIN stars, movies
ON people.id = stars.person_id AND movies.id = stars.movie_id
WHERE people.id IN (SELECT person_id FROM stars) AND year = 2004
ORDER BY birth;