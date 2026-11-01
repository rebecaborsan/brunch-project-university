-- Se ruleaza cu un cont PostgreSQL care poate crea utilizatori si baze de date.
-- Exemplu: psql -U nume_administrator -d postgres -f creare_user.sql
\set ON_ERROR_STOP on

CREATE USER brunch_user;
-- Parola se introduce aici si nu ramane scrisa in fisier.
\password brunch_user
CREATE DATABASE brunch_bloom OWNER brunch_user;
