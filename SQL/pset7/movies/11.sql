SELECT DISTINCT(title)
FROM movies
JOIN stars, ratings, people
ON movies.id = stars.movie_id AND movies.id = ratings.movie_id AND people.id = stars.person_id
WHERE name LIKE "%Chadwick Boseman%"
ORDER BY rating DESC
LIMIT 5;