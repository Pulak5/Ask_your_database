"""Training data preparation for text-to-SQL fine-tuning.

Usage:
    python -m src.training.prepare_data \
        --output-dir data/train \
        --eval-file data/eval/demo_eval.jsonl

Generates 100 synthetic question/SQL pairs for the Pagila schema,
applies a leakage guard, then saves train.jsonl (90%) and val.jsonl (10%).
"""
from __future__ import annotations

import argparse
import json
import random
from difflib import SequenceMatcher
from pathlib import Path

# ---------------------------------------------------------------------------
# 100 hardcoded synthetic Q/A pairs (Pagila schema, no LLM required)
# ---------------------------------------------------------------------------
SYNTHETIC_PAIRS: list[dict] = [
    # --- Easy: single-table selects ---
    {
        "question": "List all film titles.",
        "sql": "SELECT title FROM film ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film"],
    },
    {
        "question": "Show all actor first and last names.",
        "sql": "SELECT first_name, last_name FROM actor ORDER BY last_name;",
        "difficulty": "easy",
        "tags": ["actor"],
    },
    {
        "question": "List all categories.",
        "sql": "SELECT name FROM category ORDER BY name;",
        "difficulty": "easy",
        "tags": ["category"],
    },
    {
        "question": "Show all language names.",
        "sql": "SELECT name FROM language;",
        "difficulty": "easy",
        "tags": ["language"],
    },
    {
        "question": "List all country names.",
        "sql": "SELECT country FROM country ORDER BY country;",
        "difficulty": "easy",
        "tags": ["country"],
    },
    {
        "question": "Show all city names.",
        "sql": "SELECT city FROM city ORDER BY city;",
        "difficulty": "easy",
        "tags": ["city"],
    },
    {
        "question": "List all customer first and last names.",
        "sql": "SELECT first_name, last_name FROM customer ORDER BY last_name;",
        "difficulty": "easy",
        "tags": ["customer"],
    },
    {
        "question": "How many films are in the database?",
        "sql": "SELECT COUNT(*) AS total_films FROM film;",
        "difficulty": "easy",
        "tags": ["film", "aggregate"],
    },
    {
        "question": "How many actors are there?",
        "sql": "SELECT COUNT(*) AS total_actors FROM actor;",
        "difficulty": "easy",
        "tags": ["actor", "aggregate"],
    },
    {
        "question": "How many customers are active?",
        "sql": "SELECT COUNT(*) AS active_customers FROM customer WHERE active = TRUE;",
        "difficulty": "easy",
        "tags": ["customer", "filter"],
    },
    # --- Easy: filters ---
    {
        "question": "Show films rated PG.",
        "sql": "SELECT title FROM film WHERE rating = 'PG' ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show films rated R.",
        "sql": "SELECT title FROM film WHERE rating = 'R' ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show films released after 2010.",
        "sql": "SELECT title, release_year FROM film WHERE release_year > 2010 ORDER BY release_year;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Find films with a rental rate greater than 4.99.",
        "sql": "SELECT title, rental_rate FROM film WHERE rental_rate > 4.99 ORDER BY rental_rate DESC;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "List films longer than 120 minutes.",
        "sql": "SELECT title, length FROM film WHERE length > 120 ORDER BY length DESC;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show customers who are inactive.",
        "sql": "SELECT first_name, last_name FROM customer WHERE active = FALSE;",
        "difficulty": "easy",
        "tags": ["customer", "filter"],
    },
    {
        "question": "Find staff members by store 1.",
        "sql": "SELECT first_name, last_name FROM staff WHERE store_id = 1;",
        "difficulty": "easy",
        "tags": ["staff", "filter"],
    },
    {
        "question": "Show the 10 most expensive films by rental rate.",
        "sql": "SELECT title, rental_rate FROM film ORDER BY rental_rate DESC LIMIT 10;",
        "difficulty": "easy",
        "tags": ["film", "order", "limit"],
    },
    {
        "question": "Show the 5 shortest films.",
        "sql": "SELECT title, length FROM film ORDER BY length ASC LIMIT 5;",
        "difficulty": "easy",
        "tags": ["film", "order", "limit"],
    },
    {
        "question": "What is the average rental rate of all films?",
        "sql": "SELECT ROUND(AVG(rental_rate), 2) AS avg_rental_rate FROM film;",
        "difficulty": "easy",
        "tags": ["film", "aggregate"],
    },
    # --- Medium: joins ---
    {
        "question": "List all films in the Action category.",
        "sql": (
            "SELECT f.title FROM film f "
            "JOIN film_category fc ON f.film_id = fc.film_id "
            "JOIN category c ON fc.category_id = c.category_id "
            "WHERE c.name = 'Action' ORDER BY f.title;"
        ),
        "difficulty": "medium",
        "tags": ["film", "category", "join"],
    },
    {
        "question": "List all films in the Comedy category.",
        "sql": (
            "SELECT f.title FROM film f "
            "JOIN film_category fc ON f.film_id = fc.film_id "
            "JOIN category c ON fc.category_id = c.category_id "
            "WHERE c.name = 'Comedy' ORDER BY f.title;"
        ),
        "difficulty": "medium",
        "tags": ["film", "category", "join"],
    },
    {
        "question": "Show all films and their categories.",
        "sql": (
            "SELECT f.title, c.name AS category FROM film f "
            "JOIN film_category fc ON f.film_id = fc.film_id "
            "JOIN category c ON fc.category_id = c.category_id "
            "ORDER BY f.title;"
        ),
        "difficulty": "medium",
        "tags": ["film", "category", "join"],
    },
    {
        "question": "Show all actors in the film with title 'ACADEMY DINOSAUR'.",
        "sql": (
            "SELECT a.first_name, a.last_name FROM actor a "
            "JOIN film_actor fa ON a.actor_id = fa.actor_id "
            "JOIN film f ON fa.film_id = f.film_id "
            "WHERE f.title = 'ACADEMY DINOSAUR';"
        ),
        "difficulty": "medium",
        "tags": ["actor", "film", "join"],
    },
    {
        "question": "List customers and their city of residence.",
        "sql": (
            "SELECT c.first_name, c.last_name, ci.city FROM customer c "
            "JOIN address a ON c.address_id = a.address_id "
            "JOIN city ci ON a.city_id = ci.city_id "
            "ORDER BY c.last_name;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "address", "join"],
    },
    {
        "question": "Show the number of films per category.",
        "sql": (
            "SELECT c.name AS category, COUNT(fc.film_id) AS film_count "
            "FROM category c "
            "JOIN film_category fc ON c.category_id = fc.category_id "
            "GROUP BY c.name ORDER BY film_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["film", "category", "aggregate", "join"],
    },
    {
        "question": "Show each film and the number of actors in it.",
        "sql": (
            "SELECT f.title, COUNT(fa.actor_id) AS actor_count FROM film f "
            "JOIN film_actor fa ON f.film_id = fa.film_id "
            "GROUP BY f.title ORDER BY actor_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["film", "actor", "aggregate", "join"],
    },
    {
        "question": "Show each actor and the number of films they appear in.",
        "sql": (
            "SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS film_count "
            "FROM actor a "
            "JOIN film_actor fa ON a.actor_id = fa.actor_id "
            "GROUP BY a.actor_id, a.first_name, a.last_name "
            "ORDER BY film_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["actor", "film", "aggregate", "join"],
    },
    {
        "question": "Which actors have appeared in more than 10 films?",
        "sql": (
            "SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS film_count "
            "FROM actor a "
            "JOIN film_actor fa ON a.actor_id = fa.actor_id "
            "GROUP BY a.actor_id, a.first_name, a.last_name "
            "HAVING COUNT(fa.film_id) > 10 "
            "ORDER BY film_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["actor", "film", "aggregate", "having"],
    },
    {
        "question": "Show the total number of rentals per customer.",
        "sql": (
            "SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS rental_count "
            "FROM customer c "
            "JOIN rental r ON c.customer_id = r.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "ORDER BY rental_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "rental", "aggregate", "join"],
    },
    # --- Medium: more joins & aggregates ---
    {
        "question": "Who are the top 5 customers by total spending?",
        "sql": (
            "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_spent "
            "FROM customer c "
            "JOIN payment p ON c.customer_id = p.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "ORDER BY total_spent DESC LIMIT 5;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "payment", "aggregate", "join"],
    },
    {
        "question": "What is the total revenue per store?",
        "sql": (
            "SELECT s.store_id, SUM(p.amount) AS total_revenue "
            "FROM store s "
            "JOIN staff st ON s.store_id = st.store_id "
            "JOIN payment p ON st.staff_id = p.staff_id "
            "GROUP BY s.store_id ORDER BY total_revenue DESC;"
        ),
        "difficulty": "medium",
        "tags": ["store", "payment", "aggregate", "join"],
    },
    {
        "question": "List the 10 most rented films.",
        "sql": (
            "SELECT f.title, COUNT(r.rental_id) AS rental_count "
            "FROM film f "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "GROUP BY f.film_id, f.title "
            "ORDER BY rental_count DESC LIMIT 10;"
        ),
        "difficulty": "medium",
        "tags": ["film", "rental", "aggregate", "join"],
    },
    {
        "question": "How many rentals occurred each month?",
        "sql": (
            "SELECT DATE_TRUNC('month', rental_date) AS month, COUNT(*) AS rental_count "
            "FROM rental "
            "GROUP BY month ORDER BY month;"
        ),
        "difficulty": "medium",
        "tags": ["rental", "aggregate", "date"],
    },
    {
        "question": "What is the average rental duration by film category?",
        "sql": (
            "SELECT c.name AS category, "
            "ROUND(AVG(EXTRACT(EPOCH FROM (r.return_date - r.rental_date))/86400), 2) AS avg_days "
            "FROM rental r "
            "JOIN inventory i ON r.inventory_id = i.inventory_id "
            "JOIN film f ON i.film_id = f.film_id "
            "JOIN film_category fc ON f.film_id = fc.film_id "
            "JOIN category c ON fc.category_id = c.category_id "
            "WHERE r.return_date IS NOT NULL "
            "GROUP BY c.name ORDER BY avg_days DESC;"
        ),
        "difficulty": "hard",
        "tags": ["rental", "film", "category", "aggregate", "date"],
    },
    {
        "question": "Show the average payment amount per customer.",
        "sql": (
            "SELECT c.first_name, c.last_name, ROUND(AVG(p.amount), 2) AS avg_payment "
            "FROM customer c "
            "JOIN payment p ON c.customer_id = p.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "ORDER BY avg_payment DESC;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "payment", "aggregate"],
    },
    {
        "question": "Show the number of inventory items per store.",
        "sql": (
            "SELECT store_id, COUNT(*) AS inventory_count "
            "FROM inventory GROUP BY store_id ORDER BY store_id;"
        ),
        "difficulty": "easy",
        "tags": ["inventory", "aggregate"],
    },
    {
        "question": "List stores with their manager names.",
        "sql": (
            "SELECT s.store_id, st.first_name, st.last_name "
            "FROM store s "
            "JOIN staff st ON s.manager_staff_id = st.staff_id;"
        ),
        "difficulty": "medium",
        "tags": ["store", "staff", "join"],
    },
    {
        "question": "Show cities and their countries.",
        "sql": (
            "SELECT ci.city, co.country FROM city ci "
            "JOIN country co ON ci.country_id = co.country_id "
            "ORDER BY co.country, ci.city;"
        ),
        "difficulty": "easy",
        "tags": ["city", "country", "join"],
    },
    {
        "question": "Show addresses and their cities.",
        "sql": (
            "SELECT a.address, ci.city FROM address a "
            "JOIN city ci ON a.city_id = ci.city_id "
            "ORDER BY ci.city;"
        ),
        "difficulty": "easy",
        "tags": ["address", "city", "join"],
    },
    # --- Hard: subqueries / complex aggregates ---
    {
        "question": "Which films have never been rented?",
        "sql": (
            "SELECT f.title FROM film f "
            "WHERE f.film_id NOT IN ("
            "  SELECT i.film_id FROM inventory i "
            "  JOIN rental r ON i.inventory_id = r.inventory_id"
            ") ORDER BY f.title;"
        ),
        "difficulty": "hard",
        "tags": ["film", "rental", "subquery"],
    },
    {
        "question": "Find customers who have never made a payment.",
        "sql": (
            "SELECT c.first_name, c.last_name FROM customer c "
            "WHERE c.customer_id NOT IN (SELECT customer_id FROM payment) "
            "ORDER BY c.last_name;"
        ),
        "difficulty": "hard",
        "tags": ["customer", "payment", "subquery"],
    },
    {
        "question": "Show the most popular film in each category.",
        "sql": (
            "SELECT c.name AS category, f.title, COUNT(r.rental_id) AS rental_count "
            "FROM category c "
            "JOIN film_category fc ON c.category_id = fc.category_id "
            "JOIN film f ON fc.film_id = f.film_id "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "GROUP BY c.name, f.title "
            "ORDER BY c.name, rental_count DESC;"
        ),
        "difficulty": "hard",
        "tags": ["film", "category", "rental", "aggregate"],
    },
    {
        "question": "What is the total revenue generated by each film?",
        "sql": (
            "SELECT f.title, SUM(p.amount) AS total_revenue "
            "FROM film f "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "JOIN payment p ON r.rental_id = p.rental_id "
            "GROUP BY f.film_id, f.title "
            "ORDER BY total_revenue DESC;"
        ),
        "difficulty": "hard",
        "tags": ["film", "payment", "aggregate", "join"],
    },
    {
        "question": "Show the top 3 actors by total revenue generated from their films.",
        "sql": (
            "SELECT a.first_name, a.last_name, SUM(p.amount) AS total_revenue "
            "FROM actor a "
            "JOIN film_actor fa ON a.actor_id = fa.actor_id "
            "JOIN film f ON fa.film_id = f.film_id "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "JOIN payment p ON r.rental_id = p.rental_id "
            "GROUP BY a.actor_id, a.first_name, a.last_name "
            "ORDER BY total_revenue DESC LIMIT 3;"
        ),
        "difficulty": "hard",
        "tags": ["actor", "payment", "aggregate", "join"],
    },
    {
        "question": "Find customers who rented more than 20 films.",
        "sql": (
            "SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS rental_count "
            "FROM customer c "
            "JOIN rental r ON c.customer_id = r.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "HAVING COUNT(r.rental_id) > 20 "
            "ORDER BY rental_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "rental", "having"],
    },
    {
        "question": "Show the number of rentals by day of week.",
        "sql": (
            "SELECT TO_CHAR(rental_date, 'Day') AS day_of_week, COUNT(*) AS rental_count "
            "FROM rental GROUP BY day_of_week ORDER BY rental_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["rental", "aggregate", "date"],
    },
    {
        "question": "What percentage of rentals have been returned?",
        "sql": (
            "SELECT ROUND(100.0 * COUNT(return_date) / COUNT(*), 2) AS return_pct "
            "FROM rental;"
        ),
        "difficulty": "medium",
        "tags": ["rental", "aggregate"],
    },
    {
        "question": "Show films with more than 5 copies in inventory.",
        "sql": (
            "SELECT f.title, COUNT(i.inventory_id) AS copy_count "
            "FROM film f "
            "JOIN inventory i ON f.film_id = i.film_id "
            "GROUP BY f.film_id, f.title "
            "HAVING COUNT(i.inventory_id) > 5 "
            "ORDER BY copy_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["film", "inventory", "having"],
    },
    {
        "question": "What is the longest film in the database?",
        "sql": "SELECT title, length FROM film ORDER BY length DESC LIMIT 1;",
        "difficulty": "easy",
        "tags": ["film", "aggregate"],
    },
    {
        "question": "What is the shortest film in the database?",
        "sql": "SELECT title, length FROM film ORDER BY length ASC LIMIT 1;",
        "difficulty": "easy",
        "tags": ["film", "aggregate"],
    },
    # --- More medium/hard ---
    {
        "question": "Show the monthly revenue for the year 2005.",
        "sql": (
            "SELECT DATE_TRUNC('month', payment_date) AS month, SUM(amount) AS revenue "
            "FROM payment "
            "WHERE payment_date >= '2005-01-01' AND payment_date < '2006-01-01' "
            "GROUP BY month ORDER BY month;"
        ),
        "difficulty": "medium",
        "tags": ["payment", "aggregate", "date"],
    },
    {
        "question": "Find all films that feature both 'PENELOPE GUINESS' and 'NICK WAHLBERG'.",
        "sql": (
            "SELECT f.title FROM film f "
            "JOIN film_actor fa1 ON f.film_id = fa1.film_id "
            "JOIN actor a1 ON fa1.actor_id = a1.actor_id "
            "JOIN film_actor fa2 ON f.film_id = fa2.film_id "
            "JOIN actor a2 ON fa2.actor_id = a2.actor_id "
            "WHERE a1.first_name = 'PENELOPE' AND a1.last_name = 'GUINESS' "
            "AND a2.first_name = 'NICK' AND a2.last_name = 'WAHLBERG';"
        ),
        "difficulty": "hard",
        "tags": ["film", "actor", "join"],
    },
    {
        "question": "Show customers who have rented Action films.",
        "sql": (
            "SELECT DISTINCT c.first_name, c.last_name "
            "FROM customer c "
            "JOIN rental r ON c.customer_id = r.customer_id "
            "JOIN inventory i ON r.inventory_id = i.inventory_id "
            "JOIN film f ON i.film_id = f.film_id "
            "JOIN film_category fc ON f.film_id = fc.film_id "
            "JOIN category cat ON fc.category_id = cat.category_id "
            "WHERE cat.name = 'Action' "
            "ORDER BY c.last_name;"
        ),
        "difficulty": "hard",
        "tags": ["customer", "rental", "category", "join"],
    },
    {
        "question": "What is the average number of rentals per customer?",
        "sql": (
            "SELECT ROUND(AVG(rental_count), 2) AS avg_rentals_per_customer "
            "FROM (SELECT customer_id, COUNT(*) AS rental_count FROM rental GROUP BY customer_id) sub;"
        ),
        "difficulty": "hard",
        "tags": ["customer", "rental", "aggregate", "subquery"],
    },
    {
        "question": "List all NC-17 films.",
        "sql": "SELECT title FROM film WHERE rating = 'NC-17' ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show the number of films per rating.",
        "sql": (
            "SELECT rating, COUNT(*) AS film_count "
            "FROM film GROUP BY rating ORDER BY film_count DESC;"
        ),
        "difficulty": "easy",
        "tags": ["film", "aggregate"],
    },
    {
        "question": "Show customers from the USA.",
        "sql": (
            "SELECT c.first_name, c.last_name, ci.city "
            "FROM customer c "
            "JOIN address a ON c.address_id = a.address_id "
            "JOIN city ci ON a.city_id = ci.city_id "
            "JOIN country co ON ci.country_id = co.country_id "
            "WHERE co.country = 'United States' "
            "ORDER BY c.last_name;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "address", "country", "join"],
    },
    {
        "question": "Find films that have been rented more than 5 times.",
        "sql": (
            "SELECT f.title, COUNT(r.rental_id) AS rental_count "
            "FROM film f "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "GROUP BY f.film_id, f.title "
            "HAVING COUNT(r.rental_id) > 5 "
            "ORDER BY rental_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["film", "rental", "having"],
    },
    {
        "question": "Show the total amount paid by each customer.",
        "sql": (
            "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_paid "
            "FROM customer c "
            "JOIN payment p ON c.customer_id = p.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "ORDER BY total_paid DESC;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "payment", "aggregate"],
    },
    {
        "question": "List all G-rated films longer than 90 minutes.",
        "sql": (
            "SELECT title, length FROM film "
            "WHERE rating = 'G' AND length > 90 ORDER BY length DESC;"
        ),
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show the number of customers per store.",
        "sql": (
            "SELECT store_id, COUNT(*) AS customer_count "
            "FROM customer GROUP BY store_id ORDER BY store_id;"
        ),
        "difficulty": "easy",
        "tags": ["customer", "aggregate"],
    },
    {
        "question": "Show films that are available in both stores.",
        "sql": (
            "SELECT DISTINCT f.title FROM film f "
            "JOIN inventory i1 ON f.film_id = i1.film_id AND i1.store_id = 1 "
            "JOIN inventory i2 ON f.film_id = i2.film_id AND i2.store_id = 2 "
            "ORDER BY f.title;"
        ),
        "difficulty": "hard",
        "tags": ["film", "inventory", "join"],
    },
    {
        "question": "What was the highest single payment amount?",
        "sql": "SELECT MAX(amount) AS max_payment FROM payment;",
        "difficulty": "easy",
        "tags": ["payment", "aggregate"],
    },
    {
        "question": "What was the lowest single payment amount?",
        "sql": "SELECT MIN(amount) AS min_payment FROM payment;",
        "difficulty": "easy",
        "tags": ["payment", "aggregate"],
    },
    {
        "question": "Show the total revenue.",
        "sql": "SELECT SUM(amount) AS total_revenue FROM payment;",
        "difficulty": "easy",
        "tags": ["payment", "aggregate"],
    },
    {
        "question": "Show rentals that have not been returned yet.",
        "sql": (
            "SELECT r.rental_id, c.first_name, c.last_name, f.title, r.rental_date "
            "FROM rental r "
            "JOIN customer c ON r.customer_id = c.customer_id "
            "JOIN inventory i ON r.inventory_id = i.inventory_id "
            "JOIN film f ON i.film_id = f.film_id "
            "WHERE r.return_date IS NULL "
            "ORDER BY r.rental_date;"
        ),
        "difficulty": "medium",
        "tags": ["rental", "filter", "join"],
    },
    {
        "question": "Show rentals made in January 2006.",
        "sql": (
            "SELECT rental_id, customer_id, rental_date FROM rental "
            "WHERE rental_date >= '2006-01-01' AND rental_date < '2006-02-01' "
            "ORDER BY rental_date;"
        ),
        "difficulty": "easy",
        "tags": ["rental", "filter", "date"],
    },
    {
        "question": "Find the actor who appears in the most films.",
        "sql": (
            "SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS film_count "
            "FROM actor a "
            "JOIN film_actor fa ON a.actor_id = fa.actor_id "
            "GROUP BY a.actor_id, a.first_name, a.last_name "
            "ORDER BY film_count DESC LIMIT 1;"
        ),
        "difficulty": "medium",
        "tags": ["actor", "film", "aggregate"],
    },
    {
        "question": "Show the most common film rating.",
        "sql": (
            "SELECT rating, COUNT(*) AS cnt FROM film "
            "GROUP BY rating ORDER BY cnt DESC LIMIT 1;"
        ),
        "difficulty": "easy",
        "tags": ["film", "aggregate"],
    },
    {
        "question": "List films with their rental rates and lengths.",
        "sql": "SELECT title, rental_rate, length FROM film ORDER BY rental_rate DESC, length DESC;",
        "difficulty": "easy",
        "tags": ["film"],
    },
    {
        "question": "How many distinct customers have rented films?",
        "sql": "SELECT COUNT(DISTINCT customer_id) AS distinct_customers FROM rental;",
        "difficulty": "easy",
        "tags": ["rental", "aggregate"],
    },
    {
        "question": "Show the top 10 grossing categories.",
        "sql": (
            "SELECT c.name AS category, SUM(p.amount) AS revenue "
            "FROM category c "
            "JOIN film_category fc ON c.category_id = fc.category_id "
            "JOIN film f ON fc.film_id = f.film_id "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "JOIN payment p ON r.rental_id = p.rental_id "
            "GROUP BY c.name ORDER BY revenue DESC LIMIT 10;"
        ),
        "difficulty": "hard",
        "tags": ["category", "payment", "aggregate", "join"],
    },
    {
        "question": "Show the average film length per category.",
        "sql": (
            "SELECT c.name AS category, ROUND(AVG(f.length), 2) AS avg_length "
            "FROM category c "
            "JOIN film_category fc ON c.category_id = fc.category_id "
            "JOIN film f ON fc.film_id = f.film_id "
            "GROUP BY c.name ORDER BY avg_length DESC;"
        ),
        "difficulty": "medium",
        "tags": ["category", "film", "aggregate", "join"],
    },
    {
        "question": "Find all films with 'LOVE' in the title.",
        "sql": "SELECT title FROM film WHERE title ILIKE '%LOVE%' ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Find all actors with the first name 'JOHN'.",
        "sql": (
            "SELECT first_name, last_name FROM actor "
            "WHERE first_name = 'JOHN' ORDER BY last_name;"
        ),
        "difficulty": "easy",
        "tags": ["actor", "filter"],
    },
    {
        "question": "Show customers who have spent more than $100 total.",
        "sql": (
            "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_spent "
            "FROM customer c "
            "JOIN payment p ON c.customer_id = p.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "HAVING SUM(p.amount) > 100 "
            "ORDER BY total_spent DESC;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "payment", "having"],
    },
    {
        "question": "Show the number of rentals per staff member.",
        "sql": (
            "SELECT s.first_name, s.last_name, COUNT(r.rental_id) AS rental_count "
            "FROM staff s "
            "JOIN rental r ON s.staff_id = r.staff_id "
            "GROUP BY s.staff_id, s.first_name, s.last_name "
            "ORDER BY rental_count DESC;"
        ),
        "difficulty": "medium",
        "tags": ["staff", "rental", "aggregate"],
    },
    {
        "question": "Show the daily revenue for all time.",
        "sql": (
            "SELECT DATE(payment_date) AS day, SUM(amount) AS revenue "
            "FROM payment GROUP BY day ORDER BY day;"
        ),
        "difficulty": "medium",
        "tags": ["payment", "aggregate", "date"],
    },
    {
        "question": "What is the average rental rate by category?",
        "sql": (
            "SELECT c.name AS category, ROUND(AVG(f.rental_rate), 2) AS avg_rate "
            "FROM category c "
            "JOIN film_category fc ON c.category_id = fc.category_id "
            "JOIN film f ON fc.film_id = f.film_id "
            "GROUP BY c.name ORDER BY avg_rate DESC;"
        ),
        "difficulty": "medium",
        "tags": ["category", "film", "aggregate", "join"],
    },
    {
        "question": "Show customers who rented from both stores.",
        "sql": (
            "SELECT c.first_name, c.last_name "
            "FROM customer c "
            "WHERE c.customer_id IN ("
            "  SELECT r.customer_id FROM rental r "
            "  JOIN inventory i ON r.inventory_id = i.inventory_id "
            "  WHERE i.store_id = 1"
            ") AND c.customer_id IN ("
            "  SELECT r.customer_id FROM rental r "
            "  JOIN inventory i ON r.inventory_id = i.inventory_id "
            "  WHERE i.store_id = 2"
            ") ORDER BY c.last_name;"
        ),
        "difficulty": "hard",
        "tags": ["customer", "rental", "subquery"],
    },
    {
        "question": "Show films that were released in 2006.",
        "sql": "SELECT title FROM film WHERE release_year = 2006 ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show the top 5 cities by number of customers.",
        "sql": (
            "SELECT ci.city, COUNT(c.customer_id) AS customer_count "
            "FROM city ci "
            "JOIN address a ON ci.city_id = a.city_id "
            "JOIN customer c ON a.address_id = c.address_id "
            "GROUP BY ci.city ORDER BY customer_count DESC LIMIT 5;"
        ),
        "difficulty": "medium",
        "tags": ["city", "customer", "aggregate", "join"],
    },
    {
        "question": "Show the number of films per language.",
        "sql": (
            "SELECT l.name AS language, COUNT(f.film_id) AS film_count "
            "FROM language l "
            "LEFT JOIN film f ON l.language_id = f.language_id "
            "GROUP BY l.name ORDER BY film_count DESC;"
        ),
        "difficulty": "easy",
        "tags": ["film", "language", "aggregate"],
    },
    {
        "question": "Show PG-13 films with a rental rate under $3.",
        "sql": (
            "SELECT title, rental_rate FROM film "
            "WHERE rating = 'PG-13' AND rental_rate < 3.00 ORDER BY rental_rate;"
        ),
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Find all payments made by customer with ID 1.",
        "sql": (
            "SELECT payment_id, amount, payment_date FROM payment "
            "WHERE customer_id = 1 ORDER BY payment_date;"
        ),
        "difficulty": "easy",
        "tags": ["payment", "filter"],
    },
    {
        "question": "Show all inventory items for store 2.",
        "sql": (
            "SELECT i.inventory_id, f.title FROM inventory i "
            "JOIN film f ON i.film_id = f.film_id "
            "WHERE i.store_id = 2 ORDER BY f.title;"
        ),
        "difficulty": "easy",
        "tags": ["inventory", "film", "join"],
    },
    {
        "question": "What is the total number of inventory items?",
        "sql": "SELECT COUNT(*) AS total_inventory FROM inventory;",
        "difficulty": "easy",
        "tags": ["inventory", "aggregate"],
    },
    {
        "question": "Show the most recent rental date.",
        "sql": "SELECT MAX(rental_date) AS latest_rental FROM rental;",
        "difficulty": "easy",
        "tags": ["rental", "aggregate"],
    },
    {
        "question": "Show the earliest payment date.",
        "sql": "SELECT MIN(payment_date) AS earliest_payment FROM payment;",
        "difficulty": "easy",
        "tags": ["payment", "aggregate"],
    },
    {
        "question": "Find customers whose last name starts with 'S'.",
        "sql": (
            "SELECT first_name, last_name FROM customer "
            "WHERE last_name ILIKE 'S%' ORDER BY last_name;"
        ),
        "difficulty": "easy",
        "tags": ["customer", "filter"],
    },
    {
        "question": "Show the second most rented film.",
        "sql": (
            "SELECT f.title, COUNT(r.rental_id) AS rental_count "
            "FROM film f "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "GROUP BY f.film_id, f.title "
            "ORDER BY rental_count DESC "
            "LIMIT 1 OFFSET 1;"
        ),
        "difficulty": "medium",
        "tags": ["film", "rental", "aggregate"],
    },
    {
        "question": "Show films that have been rented in the last 30 days (from max rental date).",
        "sql": (
            "SELECT DISTINCT f.title FROM film f "
            "JOIN inventory i ON f.film_id = i.film_id "
            "JOIN rental r ON i.inventory_id = r.inventory_id "
            "WHERE r.rental_date >= (SELECT MAX(rental_date) - INTERVAL '30 days' FROM rental) "
            "ORDER BY f.title;"
        ),
        "difficulty": "hard",
        "tags": ["film", "rental", "subquery", "date"],
    },
    {
        "question": "Show customers with no rentals in the last 90 days.",
        "sql": (
            "SELECT c.first_name, c.last_name FROM customer c "
            "WHERE c.customer_id NOT IN ("
            "  SELECT DISTINCT r.customer_id FROM rental r "
            "  WHERE r.rental_date >= (SELECT MAX(rental_date) - INTERVAL '90 days' FROM rental)"
            ") ORDER BY c.last_name;"
        ),
        "difficulty": "hard",
        "tags": ["customer", "rental", "subquery", "date"],
    },
    {
        "question": "What is the median payment amount?",
        "sql": "SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_payment FROM payment;",
        "difficulty": "hard",
        "tags": ["payment", "aggregate"],
    },
    {
        "question": "Show the category with the highest average rental rate.",
        "sql": (
            "SELECT c.name AS category, ROUND(AVG(f.rental_rate), 2) AS avg_rate "
            "FROM category c "
            "JOIN film_category fc ON c.category_id = fc.category_id "
            "JOIN film f ON fc.film_id = f.film_id "
            "GROUP BY c.name ORDER BY avg_rate DESC LIMIT 1;"
        ),
        "difficulty": "medium",
        "tags": ["category", "film", "aggregate"],
    },
    {
        "question": "List all films with a description containing 'epic'.",
        "sql": "SELECT title, description FROM film WHERE description ILIKE '%epic%' ORDER BY title;",
        "difficulty": "easy",
        "tags": ["film", "filter"],
    },
    {
        "question": "Show the number of payments per month.",
        "sql": (
            "SELECT DATE_TRUNC('month', payment_date) AS month, COUNT(*) AS payment_count "
            "FROM payment GROUP BY month ORDER BY month;"
        ),
        "difficulty": "medium",
        "tags": ["payment", "aggregate", "date"],
    },
    {
        "question": "Show actor pairs who have appeared in the same film.",
        "sql": (
            "SELECT a1.first_name || ' ' || a1.last_name AS actor1, "
            "a2.first_name || ' ' || a2.last_name AS actor2, "
            "COUNT(fa1.film_id) AS shared_films "
            "FROM film_actor fa1 "
            "JOIN film_actor fa2 ON fa1.film_id = fa2.film_id AND fa1.actor_id < fa2.actor_id "
            "JOIN actor a1 ON fa1.actor_id = a1.actor_id "
            "JOIN actor a2 ON fa2.actor_id = a2.actor_id "
            "GROUP BY a1.actor_id, a1.first_name, a1.last_name, "
            "a2.actor_id, a2.first_name, a2.last_name "
            "ORDER BY shared_films DESC LIMIT 10;"
        ),
        "difficulty": "hard",
        "tags": ["actor", "film", "join", "aggregate"],
    },
    {
        "question": "Show the customer with the highest number of rentals.",
        "sql": (
            "SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS rental_count "
            "FROM customer c "
            "JOIN rental r ON c.customer_id = r.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name "
            "ORDER BY rental_count DESC LIMIT 1;"
        ),
        "difficulty": "medium",
        "tags": ["customer", "rental", "aggregate"],
    },
]

assert len(SYNTHETIC_PAIRS) == 100, f"Expected 100 pairs, got {len(SYNTHETIC_PAIRS)}"


# ---------------------------------------------------------------------------
# Leakage guard
# ---------------------------------------------------------------------------

def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def filter_leakage(pairs: list[dict], eval_questions: list[str], threshold: float = 0.8) -> list[dict]:
    """Filter out any training example whose question is identical or near-duplicate to an eval question.

    Returns the clean subset of pairs.
    """
    clean: list[dict] = []
    removed: list[tuple[str, str, float]] = []

    for pair in pairs:
        q = pair["question"]
        is_leaking = False
        for eq in eval_questions:
            ratio = _similarity(q, eq)
            if ratio >= threshold:
                is_leaking = True
                removed.append((q, eq, ratio))
                break
        if not is_leaking:
            clean.append(pair)

    if removed:
        print(f"⚠️ Leakage Guard: Removed {len(removed)} examples exceeding similarity threshold {threshold}:")
        for tq, eq, r in removed[:10]:
            print(f"   - Removed '{tq}' (matches eval '{eq}' with ratio {r:.2f})")
        if len(removed) > 10:
            print(f"   - ... and {len(removed) - 10} more.")
    else:
        print("✅ Leakage Guard: 0 leaking examples found. All training questions are clean.")

    # Verification: assert 0 leakage in retained set
    for pair in clean:
        for eq in eval_questions:
            sim = _similarity(pair["question"], eq)
            assert sim < threshold, f"Post-filter leakage violation: {pair['question']} ~ {eq}"

    return clean


# ---------------------------------------------------------------------------
# SFT prompt builder
# ---------------------------------------------------------------------------

def _build_sft_pair(schema_text: str, pair: dict) -> dict:
    """Build SFT-format {prompt, completion} using the app's prompt format."""
    try:
        from src.app.prompts import build_prompt
        prompt = build_prompt(schema_text, pair["question"])
    except ImportError:
        # Fallback if running standalone
        prompt = (
            f"### Schema:\n{schema_text}\n\n"
            f"### Question: {pair['question']}\n\n"
            f"### SQL:\n"
        )
    return {"prompt": prompt, "completion": pair["sql"]}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare SFT training data for text-to-SQL.")
    parser.add_argument("--output-dir", default="data/train")
    parser.add_argument("--eval-file", default="data/eval/demo_eval.jsonl")
    parser.add_argument("--schema-description", default="data/demo_db/schema_description.txt")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    # Load eval questions for leakage check
    eval_questions: list[str] = []
    eval_path = Path(args.eval_file)
    if eval_path.exists():
        for line in eval_path.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    eval_questions.append(obj.get("question", ""))
                except json.JSONDecodeError:
                    pass
        print(f"Loaded {len(eval_questions)} eval questions for leakage check.")
    else:
        print(f"Warning: eval file not found at {eval_path}, skipping leakage check.")

    # Leakage guard
    training_candidate_pairs = SYNTHETIC_PAIRS
    if eval_questions:
        print("Running leakage guard...")
        training_candidate_pairs = filter_leakage(SYNTHETIC_PAIRS, eval_questions)
        print(f"✅ Leakage guard passed. Clean dataset size: {len(training_candidate_pairs)}")

    # Load schema description
    schema_path = Path(args.schema_description)
    if schema_path.exists():
        schema_text = schema_path.read_text()
    else:
        print(f"Warning: schema description not found at {schema_path}, using placeholder.")
        schema_text = "Database: DVD Rental Store (Pagila subset)"

    # Build SFT pairs
    sft_pairs = [_build_sft_pair(schema_text, p) for p in training_candidate_pairs]

    # Shuffle and split
    indices = list(range(len(sft_pairs)))
    random.shuffle(indices)
    split = int(0.9 * len(indices))
    train_indices = indices[:split]
    val_indices = indices[split:]

    train_pairs = [sft_pairs[i] for i in train_indices]
    val_pairs = [sft_pairs[i] for i in val_indices]

    # Write output
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    train_path = out_dir / "train.jsonl"
    val_path = out_dir / "val.jsonl"

    train_path.write_text("\n".join(json.dumps(p) for p in train_pairs) + "\n")
    val_path.write_text("\n".join(json.dumps(p) for p in val_pairs) + "\n")

    print(f"✅ Wrote {len(train_pairs)} train examples to {train_path}")
    print(f"✅ Wrote {len(val_pairs)} val examples to {val_path}")


if __name__ == "__main__":
    main()
