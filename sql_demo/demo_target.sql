--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: senior_course; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.senior_course (
    course_id integer NOT NULL,
    teacher_id integer NOT NULL,
    course_name character varying(100) NOT NULL,
    course_start_time date,
    course_end_time date,
    teacher_name character varying(100),
    teacher_photo character varying(100),
    teacher_introduction character varying(100)
);


ALTER TABLE public.senior_course OWNER TO postgres;

--
-- Data for Name: senior_course; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.senior_course (course_id, teacher_id, course_name, course_start_time, course_end_time, teacher_name, teacher_photo, teacher_introduction) FROM stdin;
1	1	Math	2015-09-05	2022-01-30	Mary	https://image.com/1.jpg	She has taught senior students for 10 years.
5	2	English	2021-09-01	2022-01-30	Andrew	https://image.com/2.jpg	He graduated from CMU.
4	3	Computer Science	2021-09-01	2022-01-30	YI MEI	https://image.com/3.jpg	He is young and creative.
6	3	Computer Science	2021-09-01	2022-01-30	YI MEI	https://image.com/3.jpg	He is young and creative.
7	3	Computer Science	2022-09-01	2023-01-30	YI MEI	https://image.com/3.jpg	He is young and creative.
3	2	English	2023-09-06	2022-01-30	Andrew	https://image.com/2.jpg	He graduated from CMU.
2	1	Physic	2035-09-06	2022-01-30	Mary	https://image.com/1.jpg	She has taught senior students for 10 years.
\.


--
-- Name: senior_course senior_course_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.senior_course
    ADD CONSTRAINT senior_course_pkey PRIMARY KEY (course_id);


--
-- PostgreSQL database dump complete
--

