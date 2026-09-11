--
-- PostgreSQL database dump
--

\restrict bnGauzKSQPIyrkf9SEHw5FKDhL0rMdMsyKBBPjd7boXXSSYfVJ4SWN0RzAh22nx

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-09-12 04:29:47

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 234 (class 1259 OID 17240)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(100) NOT NULL,
    type character varying(30) NOT NULL,
    balance numeric(12,2) NOT NULL,
    currency character varying(8) NOT NULL,
    enabled boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 17239)
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_id_seq OWNER TO postgres;

--
-- TOC entry 5043 (class 0 OID 0)
-- Dependencies: 233
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- TOC entry 224 (class 1259 OID 17141)
-- Name: budgets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.budgets (
    id integer NOT NULL,
    user_id integer NOT NULL,
    category character varying NOT NULL,
    amount numeric(12,2) NOT NULL,
    month character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.budgets OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17140)
-- Name: budgets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.budgets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.budgets_id_seq OWNER TO postgres;

--
-- TOC entry 5044 (class 0 OID 0)
-- Dependencies: 223
-- Name: budgets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.budgets_id_seq OWNED BY public.budgets.id;


--
-- TOC entry 226 (class 1259 OID 17162)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17161)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- TOC entry 5045 (class 0 OID 0)
-- Dependencies: 225
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 228 (class 1259 OID 17178)
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.password_reset_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token_hash character varying(64) NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.password_reset_tokens OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17177)
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.password_reset_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.password_reset_tokens_id_seq OWNER TO postgres;

--
-- TOC entry 5046 (class 0 OID 0)
-- Dependencies: 227
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.password_reset_tokens_id_seq OWNED BY public.password_reset_tokens.id;


--
-- TOC entry 236 (class 1259 OID 17262)
-- Name: recurring_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recurring_transactions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    type character varying(20) NOT NULL,
    category character varying(80) NOT NULL,
    subcategory character varying(80),
    description character varying,
    frequency character varying(20) NOT NULL,
    next_date timestamp with time zone NOT NULL,
    enabled boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.recurring_transactions OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 17261)
-- Name: recurring_transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recurring_transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recurring_transactions_id_seq OWNER TO postgres;

--
-- TOC entry 5047 (class 0 OID 0)
-- Dependencies: 235
-- Name: recurring_transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recurring_transactions_id_seq OWNED BY public.recurring_transactions.id;


--
-- TOC entry 232 (class 1259 OID 17220)
-- Name: savings_goals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.savings_goals (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(100) NOT NULL,
    target_amount numeric(12,2) NOT NULL,
    saved_amount numeric(12,2) NOT NULL,
    target_date timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.savings_goals OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 17219)
-- Name: savings_goals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.savings_goals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.savings_goals_id_seq OWNER TO postgres;

--
-- TOC entry 5048 (class 0 OID 0)
-- Dependencies: 231
-- Name: savings_goals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.savings_goals_id_seq OWNED BY public.savings_goals.id;


--
-- TOC entry 230 (class 1259 OID 17197)
-- Name: subcategories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subcategories (
    id integer NOT NULL,
    category_id integer NOT NULL,
    name character varying NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.subcategories OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17196)
-- Name: subcategories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subcategories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subcategories_id_seq OWNER TO postgres;

--
-- TOC entry 5049 (class 0 OID 0)
-- Dependencies: 229
-- Name: subcategories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subcategories_id_seq OWNED BY public.subcategories.id;


--
-- TOC entry 222 (class 1259 OID 17120)
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    type character varying NOT NULL,
    category character varying NOT NULL,
    description character varying,
    transaction_date timestamp with time zone DEFAULT now(),
    subcategory character varying,
    category_id integer,
    subcategory_id integer
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17119)
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transactions_id_seq OWNER TO postgres;

--
-- TOC entry 5050 (class 0 OID 0)
-- Dependencies: 221
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- TOC entry 238 (class 1259 OID 17287)
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_sessions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token_hash character varying(64) NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    last_seen_at timestamp with time zone DEFAULT now(),
    revoked_at timestamp with time zone
);


ALTER TABLE public.user_sessions OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 17286)
-- Name: user_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_sessions_id_seq OWNER TO postgres;

--
-- TOC entry 5051 (class 0 OID 0)
-- Dependencies: 237
-- Name: user_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_sessions_id_seq OWNED BY public.user_sessions.id;


--
-- TOC entry 220 (class 1259 OID 17105)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    role character varying(20) DEFAULT 'user'::character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17104)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5052 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4817 (class 2604 OID 17243)
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- TOC entry 4805 (class 2604 OID 17144)
-- Name: budgets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.budgets ALTER COLUMN id SET DEFAULT nextval('public.budgets_id_seq'::regclass);


--
-- TOC entry 4807 (class 2604 OID 17165)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 4810 (class 2604 OID 17181)
-- Name: password_reset_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id SET DEFAULT nextval('public.password_reset_tokens_id_seq'::regclass);


--
-- TOC entry 4819 (class 2604 OID 17265)
-- Name: recurring_transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recurring_transactions ALTER COLUMN id SET DEFAULT nextval('public.recurring_transactions_id_seq'::regclass);


--
-- TOC entry 4815 (class 2604 OID 17223)
-- Name: savings_goals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings_goals ALTER COLUMN id SET DEFAULT nextval('public.savings_goals_id_seq'::regclass);


--
-- TOC entry 4812 (class 2604 OID 17200)
-- Name: subcategories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories ALTER COLUMN id SET DEFAULT nextval('public.subcategories_id_seq'::regclass);


--
-- TOC entry 4803 (class 2604 OID 17123)
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- TOC entry 4821 (class 2604 OID 17290)
-- Name: user_sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions ALTER COLUMN id SET DEFAULT nextval('public.user_sessions_id_seq'::regclass);


--
-- TOC entry 4800 (class 2604 OID 17108)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5033 (class 0 OID 17240)
-- Dependencies: 234
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (id, user_id, name, type, balance, currency, enabled, created_at) FROM stdin;
1	2	Rutuja	Expense	500.00	INR	t	2026-09-12 02:49:31.960737+05:30
\.


--
-- TOC entry 5023 (class 0 OID 17141)
-- Dependencies: 224
-- Data for Name: budgets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.budgets (id, user_id, category, amount, month, created_at) FROM stdin;
1	1	string	1.00	string	2026-09-11 03:35:48.8176+05:30
2	1	Food	5000.00	2026-09	2026-09-11 03:36:42.858393+05:30
3	1	Rent	5500.00	2026-09	2026-09-11 19:38:48.128694+05:30
5	2	Food	3500.00	2026-09	2026-09-11 21:19:31.677404+05:30
6	2	Healthcare	6000.00	2026-09	2026-09-12 03:44:21.633954+05:30
\.


--
-- TOC entry 5025 (class 0 OID 17162)
-- Dependencies: 226
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, enabled, created_at) FROM stdin;
1	Home	t	2026-09-11 21:51:13.427384+05:30
2	Food	t	2026-09-11 21:51:13.427384+05:30
3	Transport	t	2026-09-11 21:51:13.427384+05:30
4	Shopping	t	2026-09-11 21:51:13.427384+05:30
5	Healthcare	t	2026-09-11 21:51:13.427384+05:30
6	Entertainment	t	2026-09-11 21:51:13.427384+05:30
7	Salary	t	2026-09-11 21:51:13.427384+05:30
8	Other	t	2026-09-11 21:51:13.427384+05:30
\.


--
-- TOC entry 5027 (class 0 OID 17178)
-- Dependencies: 228
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.password_reset_tokens (id, user_id, token_hash, expires_at, used_at, created_at) FROM stdin;
\.


--
-- TOC entry 5035 (class 0 OID 17262)
-- Dependencies: 236
-- Data for Name: recurring_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recurring_transactions (id, user_id, amount, type, category, subcategory, description, frequency, next_date, enabled, created_at) FROM stdin;
1	2	5000.00	income	Gold	Share market	NA	daily	2026-09-12 02:50:00+05:30	t	2026-09-12 02:50:44.199772+05:30
\.


--
-- TOC entry 5031 (class 0 OID 17220)
-- Dependencies: 232
-- Data for Name: savings_goals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.savings_goals (id, user_id, name, target_amount, saved_amount, target_date, created_at) FROM stdin;
1	2	Ea do eos quidem dol	50.00	32.00	2025-03-26 05:30:00+05:30	2026-09-12 02:24:38.667593+05:30
\.


--
-- TOC entry 5029 (class 0 OID 17197)
-- Dependencies: 230
-- Data for Name: subcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subcategories (id, category_id, name, enabled, created_at) FROM stdin;
1	1	Rent	t	2026-09-11 21:51:13.427384+05:30
2	1	Electricity	t	2026-09-11 21:51:13.427384+05:30
3	1	Water	t	2026-09-11 21:51:13.427384+05:30
4	1	Internet	t	2026-09-11 21:51:13.427384+05:30
5	1	Maintenance	t	2026-09-11 21:51:13.427384+05:30
6	2	Groceries	t	2026-09-11 21:51:13.427384+05:30
7	2	Dining	t	2026-09-11 21:51:13.427384+05:30
8	2	Coffee	t	2026-09-11 21:51:13.427384+05:30
9	3	Fuel	t	2026-09-11 21:51:13.427384+05:30
10	3	Public transport	t	2026-09-11 21:51:13.427384+05:30
11	3	Taxi	t	2026-09-11 21:51:13.427384+05:30
12	4	Clothing	t	2026-09-11 21:51:13.427384+05:30
13	4	Electronics	t	2026-09-11 21:51:13.427384+05:30
14	4	Household	t	2026-09-11 21:51:13.427384+05:30
15	5	Doctor	t	2026-09-11 21:51:13.427384+05:30
16	5	Medicine	t	2026-09-11 21:51:13.427384+05:30
17	6	Movies	t	2026-09-11 21:51:13.427384+05:30
18	6	Games	t	2026-09-11 21:51:13.427384+05:30
19	6	Subscriptions	t	2026-09-11 21:51:13.427384+05:30
\.


--
-- TOC entry 5021 (class 0 OID 17120)
-- Dependencies: 222
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transactions (id, user_id, amount, type, category, description, transaction_date, subcategory, category_id, subcategory_id) FROM stdin;
2	1	50000.00	income	Salary	Monthly salary	2026-09-10 22:01:00.044505+05:30	\N	\N	\N
1	1	700.00	expense	Food	Dinner updated	2026-09-10 22:00:05.616033+05:30	\N	\N	\N
4	1	900.00	expense	Home	NA	2026-09-10 11:54:00+05:30	\N	\N	\N
5	1	3000.00	expense	Rent	NA	2026-09-11 19:40:00+05:30	\N	\N	\N
7	2	35000.00	expense	Bricks	We send Money Phonepay through to Vikas.	2026-09-11 12:00:00+05:30	\N	\N	\N
8	2	25000.00	income	Salary	Created Salary	2026-09-11 12:00:00+05:30	\N	\N	\N
9	2	90.00	expense	Food	Pay online	2026-09-11 12:00:00+05:30	\N	\N	\N
10	2	350.00	expense	Food	Cash	2026-09-11 12:00:00+05:30	\N	\N	\N
11	2	100045.00	income	Other	Collect From Bill	2026-09-11 12:00:00+05:30	\N	8	\N
12	2	2600.00	income	Home	NA	2026-09-11 12:00:00+05:30	Bhisi	1	\N
13	2	6000.00	expense	Party	NA	2026-09-11 12:00:00+05:30	Group Party	\N	\N
14	2	2500.00	expense	Food	NA	2026-09-11 12:00:00+05:30	Dining	2	7
\.


--
-- TOC entry 5037 (class 0 OID 17287)
-- Dependencies: 238
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_sessions (id, user_id, token_hash, created_at, last_seen_at, revoked_at) FROM stdin;
\.


--
-- TOC entry 5019 (class 0 OID 17105)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password_hash, created_at, role) FROM stdin;
1	test@example.com	$2b$12$kP7KtasdpHYqLWXHN2IXO.3TtymEc6TAzhSrs46.BfyhQV7Alj4eC	2026-09-09 21:43:43.060001+05:30	user
3	New@gmail.com	$2b$12$1n6BEQhTXeHHDsNAA3TgWuwaqYrRwlKNjMDix50YPrrnkoAQWx5I2	2026-09-11 21:13:25.97976+05:30	user
2	Krushna2@gmail.com	$2b$12$ydg1YtXvRQjrV8xeei0Z5.9HLU79sA0ThUcf4QbHxQXOoCpfpgyC2	2026-09-11 21:11:32.3055+05:30	user
\.


--
-- TOC entry 5053 (class 0 OID 0)
-- Dependencies: 233
-- Name: accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_id_seq', 1, true);


--
-- TOC entry 5054 (class 0 OID 0)
-- Dependencies: 223
-- Name: budgets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.budgets_id_seq', 6, true);


--
-- TOC entry 5055 (class 0 OID 0)
-- Dependencies: 225
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 8, true);


--
-- TOC entry 5056 (class 0 OID 0)
-- Dependencies: 227
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 1, false);


--
-- TOC entry 5057 (class 0 OID 0)
-- Dependencies: 235
-- Name: recurring_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.recurring_transactions_id_seq', 1, true);


--
-- TOC entry 5058 (class 0 OID 0)
-- Dependencies: 231
-- Name: savings_goals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.savings_goals_id_seq', 1, true);


--
-- TOC entry 5059 (class 0 OID 0)
-- Dependencies: 229
-- Name: subcategories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subcategories_id_seq', 19, true);


--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 221
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transactions_id_seq', 14, true);


--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 237
-- Name: user_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_sessions_id_seq', 1, false);


--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- TOC entry 4851 (class 2606 OID 17253)
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 4832 (class 2606 OID 17154)
-- Name: budgets budgets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_pkey PRIMARY KEY (id);


--
-- TOC entry 4835 (class 2606 OID 17174)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 4841 (class 2606 OID 17188)
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 4857 (class 2606 OID 17278)
-- Name: recurring_transactions recurring_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recurring_transactions
    ADD CONSTRAINT recurring_transactions_pkey PRIMARY KEY (id);


--
-- TOC entry 4849 (class 2606 OID 17231)
-- Name: savings_goals savings_goals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings_goals
    ADD CONSTRAINT savings_goals_pkey PRIMARY KEY (id);


--
-- TOC entry 4845 (class 2606 OID 17210)
-- Name: subcategories subcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_pkey PRIMARY KEY (id);


--
-- TOC entry 4830 (class 2606 OID 17133)
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- TOC entry 4862 (class 2606 OID 17297)
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- TOC entry 4827 (class 2606 OID 17116)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4852 (class 1259 OID 17260)
-- Name: ix_accounts_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_accounts_id ON public.accounts USING btree (id);


--
-- TOC entry 4853 (class 1259 OID 17259)
-- Name: ix_accounts_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_accounts_user_id ON public.accounts USING btree (user_id);


--
-- TOC entry 4833 (class 1259 OID 17160)
-- Name: ix_budgets_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_budgets_id ON public.budgets USING btree (id);


--
-- TOC entry 4836 (class 1259 OID 17176)
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- TOC entry 4837 (class 1259 OID 17175)
-- Name: ix_categories_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_categories_name ON public.categories USING btree (name);


--
-- TOC entry 4838 (class 1259 OID 17194)
-- Name: ix_password_reset_tokens_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_password_reset_tokens_token_hash ON public.password_reset_tokens USING btree (token_hash);


--
-- TOC entry 4839 (class 1259 OID 17195)
-- Name: ix_password_reset_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_password_reset_tokens_user_id ON public.password_reset_tokens USING btree (user_id);


--
-- TOC entry 4854 (class 1259 OID 17285)
-- Name: ix_recurring_transactions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_recurring_transactions_id ON public.recurring_transactions USING btree (id);


--
-- TOC entry 4855 (class 1259 OID 17284)
-- Name: ix_recurring_transactions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_recurring_transactions_user_id ON public.recurring_transactions USING btree (user_id);


--
-- TOC entry 4846 (class 1259 OID 17238)
-- Name: ix_savings_goals_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_savings_goals_id ON public.savings_goals USING btree (id);


--
-- TOC entry 4847 (class 1259 OID 17237)
-- Name: ix_savings_goals_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_savings_goals_user_id ON public.savings_goals USING btree (user_id);


--
-- TOC entry 4842 (class 1259 OID 17217)
-- Name: ix_subcategories_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_subcategories_category_id ON public.subcategories USING btree (category_id);


--
-- TOC entry 4843 (class 1259 OID 17216)
-- Name: ix_subcategories_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_subcategories_id ON public.subcategories USING btree (id);


--
-- TOC entry 4828 (class 1259 OID 17139)
-- Name: ix_transactions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_transactions_id ON public.transactions USING btree (id);


--
-- TOC entry 4858 (class 1259 OID 17303)
-- Name: ix_user_sessions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_sessions_id ON public.user_sessions USING btree (id);


--
-- TOC entry 4859 (class 1259 OID 17304)
-- Name: ix_user_sessions_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_sessions_token_hash ON public.user_sessions USING btree (token_hash);


--
-- TOC entry 4860 (class 1259 OID 17305)
-- Name: ix_user_sessions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_sessions_user_id ON public.user_sessions USING btree (user_id);


--
-- TOC entry 4824 (class 1259 OID 17117)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4825 (class 1259 OID 17118)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 4868 (class 2606 OID 17254)
-- Name: accounts accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4864 (class 2606 OID 17155)
-- Name: budgets budgets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4865 (class 2606 OID 17189)
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4869 (class 2606 OID 17279)
-- Name: recurring_transactions recurring_transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recurring_transactions
    ADD CONSTRAINT recurring_transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4867 (class 2606 OID 17232)
-- Name: savings_goals savings_goals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings_goals
    ADD CONSTRAINT savings_goals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4866 (class 2606 OID 17211)
-- Name: subcategories subcategories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- TOC entry 4863 (class 2606 OID 17134)
-- Name: transactions transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4870 (class 2606 OID 17298)
-- Name: user_sessions user_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2026-09-12 04:29:48

--
-- PostgreSQL database dump complete
--

\unrestrict bnGauzKSQPIyrkf9SEHw5FKDhL0rMdMsyKBBPjd7boXXSSYfVJ4SWN0RzAh22nx

