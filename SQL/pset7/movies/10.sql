SELECT name
FROM people
JOIN directors, ratings, movies
ON people.id = directors.person_id AND directors.movie_id = movies.id AND movies.id = ratings.movie_id
WHERE people.id IN (SELECT person_id FROM directors) AND rating >= 9.0;