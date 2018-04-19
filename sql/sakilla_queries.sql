use sakila;

-- 1a. Display the first and last names of all actors from the table actor. 
select first_name, last_name from actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name
select CONCAT(first_name, " " , last_name) AS Actor_Name  from actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select actor_id, first_name, last_name from actor where (last_name = NULL or last_name = ' ' ) ;

-- 2b. Find all actors whose last name contain the letters GEN:
select * from actor where last_name like '%GEN%' ;

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
select * from actor where last_name like '%LI%' 
order by last_name, first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country from country where country in ('Afghanistan', 'Bangladesh', 'China');

-- 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.
ALTER TABLE actor
ADD COLUMN `middle_name` VARCHAR(1) NULL AFTER `first_name`;

-- 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.
ALTER TABLE actor
CHANGE COLUMN `middle_name` `middle_name` BLOB NULL ;

-- 3c. Now delete the middle_name column.
ALTER TABLE actor
DROP COLUMN `middle_name`;


-- 4a. List the last names of actors, as well as how many actors have that last name.
select last_name,  count(*)
from actor
where last_name <> ' ' 
group by last_name ;


-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select last_name,  count(*)
from actor
where last_name <> ' ' 
group by last_name having count(*) >= 2;

-- 4c Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record
select * from actor
where last_name = 'WILLIAMS'
and first_name = 'GROUCHO' ;

Update actor
set first_name = 'HARPO'
where last_name = 'WILLIAMS'
and first_name = 'GROUCHO' ;

select * from actor
where last_name = 'WILLIAMS'
and first_name = 'HARPO' ;

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. 
-- It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. 
-- Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. 
-- BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)

update actor
set first_name = 'MUCHO GROUCHO'
where actor_id = 172 ;

select * from actor
where actor_id = 172 ;

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it? 
-- Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html
show CREATE TABLE address; 

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
select a.first_name, a.last_name, b.address
from 
staff a, address b
where a.address_id = b.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment. 
select a.first_name, a.last_name, a.staff_id, sum(b.amount) as amount_rung
from 
staff a, payment b
where a.staff_id = b.staff_id
and b.payment_date >= '2005-08-01 00:00:00' 
and b.payment_date >= '2005-08-31 11:59:59' 
group by staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
select a.film_id, a.title, count(b.film_id) as nbr_of_actors
from
film a, film_actor b
where
a.film_id = b.film_id
group by b.film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
select a.film_id, a.title, count(b.film_id) as nbr_of_copies
from film a, inventory b
where a.title = 'Hunchback Impossible' 
and a.film_id = b.film_id
group by b.film_id;

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
select a.customer_id, a.first_name, a.last_name, sum(b.amount) as total_amount_paid
from customer a
left join payment b
on
a.customer_id = b.customer_id
group by b.customer_id
order by a.last_name
;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, 
-- films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English. 
select a.title
from film a
where (a.title like 'K%' or a.title like 'Q%')
and a.language_id in
	(select b.language_id
	from language b
	where
	b.name= 'English');


-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
select a.first_name, a.last_name
from actor a
where
a.actor_id in
	(select b.actor_id
     from
     film_actor b
     where b.film_id in
		(select c.film_id
         from film c
         where
         c.title = 'Alone Trip'
		)
    ) ;

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
select a.customer_id, a.first_name, a.last_name, a.email 
FROM 
	customer a,
	address b,
	city c,
	country d
where
	a.address_id = b.address_id
and b.city_id = c.city_id
and c.country_id = d.country_id
and d.country = 'Canada' ;

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as famiy films.
select a.film_id, a.title
from
	film a,
    film_category b,
	category c
where
	a.film_id = b.film_id
and b.category_id = c.category_id
and c.name = 'Family'; 


-- 7e. Display the most frequently rented movies in descending order.
select a.film_id, a.title, a.rental_duration
from film a
order by a.rental_duration desc;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
select store_id a, sum(b.amount) as business_value
FROM 
store a,
payment b
where
	a.manager_staff_id = b.staff_id
group by a.manager_staff_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
select store_id a, c.city, d.country
FROM 
store a,
address b,
city c,
country d
where
	a.address_id = b.address_id
and b.city_id = c.city_id
and c.country_id = d.country_id
group by a.manager_staff_id;


-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
select a.name, sum(e.amount) as gross_revenue
from 
category a,
film_category b,
inventory c,
rental d,
payment e
where 
	a.category_id = b.category_id
and b.film_id = c.film_id
and c.inventory_id = d.inventory_id
and d.rental_id = e.rental_id
group by e.rental_id
order by gross_revenue desc, a.name
limit 5 ;


-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.

create view top_genres as
select a.name, sum(e.amount) as gross_revenue
from 
category a,
film_category b,
inventory c,
rental d,
payment e
where 
	a.category_id = b.category_id
and b.film_id = c.film_id
and c.inventory_id = d.inventory_id
and d.rental_id = e.rental_id
group by e.rental_id
order by gross_revenue desc, a.name 
limit 5;

-- 8b. How would you display the view that you created in 8a?
select name from top_genres;


-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view top_genres;