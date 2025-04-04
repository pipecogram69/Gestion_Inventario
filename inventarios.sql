--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

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

--
-- Name: inventario; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA inventario;


ALTER SCHEMA inventario OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: producto; Type: TABLE; Schema: public; Owner: arquitectura
--

CREATE TABLE public.producto (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    stock integer NOT NULL,
    precio integer NOT NULL
);


ALTER TABLE public.producto OWNER TO arquitectura;

--
-- Name: producto_id_seq; Type: SEQUENCE; Schema: public; Owner: arquitectura
--

CREATE SEQUENCE public.producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.producto_id_seq OWNER TO arquitectura;

--
-- Name: producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: arquitectura
--

ALTER SEQUENCE public.producto_id_seq OWNED BY public.producto.id;


--
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion character varying(200),
    categoria character varying(50) NOT NULL,
    precio numeric(10,2) NOT NULL,
    stock integer NOT NULL
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- Name: productos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.productos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.productos_id_seq OWNER TO postgres;

--
-- Name: productos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.productos_id_seq OWNED BY public.productos.id;


--
-- Name: transacciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transacciones (
    id integer NOT NULL,
    tipo character varying(10) NOT NULL,
    fecha timestamp without time zone NOT NULL,
    producto_id integer NOT NULL,
    cantidad integer NOT NULL
);


ALTER TABLE public.transacciones OWNER TO postgres;

--
-- Name: transacciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transacciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transacciones_id_seq OWNER TO postgres;

--
-- Name: transacciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transacciones_id_seq OWNED BY public.transacciones.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    rol character varying(50) NOT NULL,
    contrasena character varying(100) NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: producto id; Type: DEFAULT; Schema: public; Owner: arquitectura
--

ALTER TABLE ONLY public.producto ALTER COLUMN id SET DEFAULT nextval('public.producto_id_seq'::regclass);


--
-- Name: productos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos ALTER COLUMN id SET DEFAULT nextval('public.productos_id_seq'::regclass);


--
-- Name: transacciones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacciones ALTER COLUMN id SET DEFAULT nextval('public.transacciones_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: arquitectura
--

COPY public.producto (id, nombre, stock, precio) FROM stdin;
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (id, nombre, descripcion, categoria, precio, stock) FROM stdin;
1	Laptop HP	Laptop de 15 pulgadas, 8GB RAM, 256GB SSD	Electr¢nica	1200.00	10
2	Smartphone Samsung	Tel‚fono inteligente con 128GB de almacenamiento	Electr¢nica	800.00	15
3	Teclado mec nico	Teclado mec nico RGB, switches azules	Accesorios	100.00	20
5	Monitor 24"	Monitor Full HD de 24 pulgadas	Electr¢nica	200.00	12
6	Impresora l ser	Impresora l ser monocrom tica	Oficina	150.00	8
9	Disco duro externo	Disco duro de 1TB, USB 3.0	Almacenamiento	60.00	22
10	Router Wi-Fi	Router de doble banda, 1200Mbps	Redes	80.00	14
11	Alexa	asistente virtual controlado por voz	tecnologia	200.00	20
13	Laptop Dell XPS 13	Laptop ultradelgada, 16GB RAM, 512GB SSD\t	electronica 	1200000.00	40
12	enchufes inteligentes 	Los enchufes inteligentes son dispositivos versátiles que nos permiten controlar cualquier aparato que conectamos a ellos: un router	tecnologia	100000.00	60
4	Mouse inal mbrico	Mouse ergon¢mico con conexi¢n Bluetooth	Accesorios	100000.00	30
14	iPhone 14 Pro	 iPhone 14 Pro\tTeléfono inteligente con 256GB de almacenamiento	Celulares	120.00	50
8	Disco Duro SSD 1TB	Disco de estado sólido ultra rápido USB 3.1	Almacenamiento	180.00	20
7	Cargador port til	Bater¡a externa de 20000mAh	Accesorios	1000.00	40
\.


--
-- Data for Name: transacciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transacciones (id, tipo, fecha, producto_id, cantidad) FROM stdin;
1	entrada	2025-03-18 19:53:13.044197	11	20
2	salida	2025-03-23 20:17:45.87877	11	0
3	salida	2025-03-23 20:18:12.97701	11	0
4	salida	2025-03-23 20:20:17.160035	11	0
5	salida	2025-03-23 20:26:19.191593	11	0
6	salida	2025-03-23 20:28:48.925154	11	0
7	entrada	2025-03-23 20:33:05.627099	12	50
8	salida	2025-03-23 20:33:26.957196	11	0
9	salida	2025-03-23 20:35:23.225907	12	10
10	entrada	2025-03-23 20:36:00.482772	12	20
11	entrada	2025-03-23 20:39:59.616346	13	40
12	salida	2025-03-23 21:56:37.84976	4	0
13	salida	2025-03-23 21:57:42.153663	4	0
14	entrada	2025-03-23 22:14:25.764543	14	50
15	entrada	2025-03-23 22:19:46.53424	7	15
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, rol, contrasena) FROM stdin;
1	julian felipe cortes moreno	empleado	123456
2	Maria	superadmin	Arquitectura
\.


--
-- Name: producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: arquitectura
--

SELECT pg_catalog.setval('public.producto_id_seq', 1, false);


--
-- Name: productos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_id_seq', 14, true);


--
-- Name: transacciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transacciones_id_seq', 15, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 2, true);


--
-- Name: producto producto_pkey; Type: CONSTRAINT; Schema: public; Owner: arquitectura
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (id);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id);


--
-- Name: transacciones transacciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacciones
    ADD CONSTRAINT transacciones_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: transacciones transacciones_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacciones
    ADD CONSTRAINT transacciones_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: SCHEMA inventario; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA inventario TO arquitectura;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO arquitectura;


--
-- Name: TABLE productos; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.productos TO arquitectura;


--
-- Name: SEQUENCE productos_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.productos_id_seq TO arquitectura;


--
-- Name: TABLE transacciones; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.transacciones TO arquitectura;


--
-- Name: SEQUENCE transacciones_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.transacciones_id_seq TO arquitectura;


--
-- Name: TABLE usuarios; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.usuarios TO arquitectura;


--
-- Name: SEQUENCE usuarios_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.usuarios_id_seq TO arquitectura;


--
-- PostgreSQL database dump complete
--

