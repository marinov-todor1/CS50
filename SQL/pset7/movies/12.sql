SELECT title
FROM movies
JOIN stars, ratings, people
ON movies.id = stars.movie_id AND movies.id = ratings.movie_id AND people.id = stars.person_id
WHERE name IN ("Johnny Depp", "Helena Bonham Carter")
GROUP BY title
HAVING COUNT(*) = 2;