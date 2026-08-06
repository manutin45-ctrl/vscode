a.
SELECT  name, gr.genre
FROM imdb.movies mv
inner join imdb.genres gr on (mv.id = gr.movie_id)
4.png


b.  
SELECT  name, gr.genre
FROM imdb.movies mv
left join imdb.genres gr on (mv.id = gr.movie_id)
where genre =''
5.png

c.  
SELECT id, name, `year`, `rank`, movie_id, genre
FROM imdb.movies 
cross join imdb.genres

3.png

d. 
SELECT  name, gr.genre
FROM imdb.movies mv
left join imdb.genres gr on (mv.id = gr.movie_id)

1.png

e.  

SELECT distinct ( first_name, last_name, year )
FROM imdb.actors ac
inner  join  imdb.roles r on (ac.id = r.actor_id)
right semi join imdb.movies mv on (r.movie_id = mv.id)
where year = 2001

6.png


f.
SELECT  name, gr.genre
FROM imdb.movies mv
left anti join imdb.genres gr on (mv.id = gr.movie_id)

2.png