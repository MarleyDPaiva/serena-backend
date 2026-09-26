--
-- PostgreSQL database dump
--

\restrict C1FuY5e6uzd9tdEhczLBDXgEwZC6daQqxkmPn4DBbQBt7ApKq8NAoaDmqvymgpP

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-09-25 22:31:41

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
-- TOC entry 230 (class 1255 OID 16973)
-- Name: atualizar_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.atualizar_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.atualizar_timestamp() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 229 (class 1259 OID 16940)
-- Name: consultas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.consultas (
    id integer NOT NULL,
    paciente_id integer NOT NULL,
    profissional_id integer NOT NULL,
    data_hora timestamp without time zone NOT NULL,
    duracao_minutos integer DEFAULT 50,
    status character varying(20) DEFAULT 'agendada'::character varying NOT NULL,
    valor numeric(10,2),
    observacoes text,
    anotacoes_privadas text,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    atualizado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT consultas_status_check CHECK (((status)::text = ANY ((ARRAY['agendada'::character varying, 'confirmada'::character varying, 'realizada'::character varying, 'cancelada'::character varying, 'faltou'::character varying])::text[])))
);


ALTER TABLE public.consultas OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16939)
-- Name: consultas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.consultas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.consultas_id_seq OWNER TO postgres;

--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 228
-- Name: consultas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.consultas_id_seq OWNED BY public.consultas.id;


--
-- TOC entry 222 (class 1259 OID 16864)
-- Name: especialidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.especialidades (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text
);


ALTER TABLE public.especialidades OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16863)
-- Name: especialidades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.especialidades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.especialidades_id_seq OWNER TO postgres;

--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 221
-- Name: especialidades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.especialidades_id_seq OWNED BY public.especialidades.id;


--
-- TOC entry 224 (class 1259 OID 16877)
-- Name: pacientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pacientes (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    nome_completo character varying(150) NOT NULL,
    cpf character varying(14),
    data_nascimento date,
    telefone character varying(20),
    genero character varying(20),
    endereco text,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.pacientes OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16876)
-- Name: pacientes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pacientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pacientes_id_seq OWNER TO postgres;

--
-- TOC entry 5098 (class 0 OID 0)
-- Dependencies: 223
-- Name: pacientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pacientes_id_seq OWNED BY public.pacientes.id;


--
-- TOC entry 226 (class 1259 OID 16899)
-- Name: profissionais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profissionais (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    nome_completo character varying(150) NOT NULL,
    crp character varying(20) NOT NULL,
    telefone character varying(20),
    bio text,
    valor_consulta numeric(10,2),
    ativo boolean DEFAULT true,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.profissionais OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16898)
-- Name: profissionais_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.profissionais_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.profissionais_id_seq OWNER TO postgres;

--
-- TOC entry 5101 (class 0 OID 0)
-- Dependencies: 225
-- Name: profissionais_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.profissionais_id_seq OWNED BY public.profissionais.id;


--
-- TOC entry 227 (class 1259 OID 16922)
-- Name: profissional_especialidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profissional_especialidades (
    profissional_id integer NOT NULL,
    especialidade_id integer NOT NULL
);


ALTER TABLE public.profissional_especialidades OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16845)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    senha_hash character varying(255) NOT NULL,
    tipo character varying(20) NOT NULL,
    ativo boolean DEFAULT true,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    atualizado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usuarios_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['paciente'::character varying, 'profissional'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16844)
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
-- TOC entry 5105 (class 0 OID 0)
-- Dependencies: 219
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4893 (class 2604 OID 16943)
-- Name: consultas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultas ALTER COLUMN id SET DEFAULT nextval('public.consultas_id_seq'::regclass);


--
-- TOC entry 4887 (class 2604 OID 16867)
-- Name: especialidades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.especialidades ALTER COLUMN id SET DEFAULT nextval('public.especialidades_id_seq'::regclass);


--
-- TOC entry 4888 (class 2604 OID 16880)
-- Name: pacientes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes ALTER COLUMN id SET DEFAULT nextval('public.pacientes_id_seq'::regclass);


--
-- TOC entry 4890 (class 2604 OID 16902)
-- Name: profissionais id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissionais ALTER COLUMN id SET DEFAULT nextval('public.profissionais_id_seq'::regclass);


--
-- TOC entry 4883 (class 2604 OID 16848)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 4925 (class 2606 OID 16957)
-- Name: consultas consultas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_pkey PRIMARY KEY (id);


--
-- TOC entry 4906 (class 2606 OID 16875)
-- Name: especialidades especialidades_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_nome_key UNIQUE (nome);


--
-- TOC entry 4908 (class 2606 OID 16873)
-- Name: especialidades especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_pkey PRIMARY KEY (id);


--
-- TOC entry 4910 (class 2606 OID 16892)
-- Name: pacientes pacientes_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_cpf_key UNIQUE (cpf);


--
-- TOC entry 4912 (class 2606 OID 16888)
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id);


--
-- TOC entry 4914 (class 2606 OID 16890)
-- Name: pacientes pacientes_usuario_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_usuario_id_key UNIQUE (usuario_id);


--
-- TOC entry 4916 (class 2606 OID 16916)
-- Name: profissionais profissionais_crp_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissionais
    ADD CONSTRAINT profissionais_crp_key UNIQUE (crp);


--
-- TOC entry 4918 (class 2606 OID 16912)
-- Name: profissionais profissionais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissionais
    ADD CONSTRAINT profissionais_pkey PRIMARY KEY (id);


--
-- TOC entry 4920 (class 2606 OID 16914)
-- Name: profissionais profissionais_usuario_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissionais
    ADD CONSTRAINT profissionais_usuario_id_key UNIQUE (usuario_id);


--
-- TOC entry 4923 (class 2606 OID 16928)
-- Name: profissional_especialidades profissional_especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissional_especialidades
    ADD CONSTRAINT profissional_especialidades_pkey PRIMARY KEY (profissional_id, especialidade_id);


--
-- TOC entry 4902 (class 2606 OID 16862)
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- TOC entry 4904 (class 2606 OID 16860)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4926 (class 1259 OID 16968)
-- Name: idx_consultas_data_hora; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_consultas_data_hora ON public.consultas USING btree (data_hora);


--
-- TOC entry 4927 (class 1259 OID 16969)
-- Name: idx_consultas_paciente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_consultas_paciente ON public.consultas USING btree (paciente_id);


--
-- TOC entry 4928 (class 1259 OID 16970)
-- Name: idx_consultas_profissional; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_consultas_profissional ON public.consultas USING btree (profissional_id);


--
-- TOC entry 4929 (class 1259 OID 16971)
-- Name: idx_consultas_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_consultas_status ON public.consultas USING btree (status);


--
-- TOC entry 4921 (class 1259 OID 16976)
-- Name: idx_prof_esp_especialidade; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_prof_esp_especialidade ON public.profissional_especialidades USING btree (especialidade_id);


--
-- TOC entry 4900 (class 1259 OID 16972)
-- Name: idx_usuarios_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_usuarios_email ON public.usuarios USING btree (email);


--
-- TOC entry 4937 (class 2620 OID 16975)
-- Name: consultas trg_consultas_atualizado; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_consultas_atualizado BEFORE UPDATE ON public.consultas FOR EACH ROW EXECUTE FUNCTION public.atualizar_timestamp();


--
-- TOC entry 4936 (class 2620 OID 16974)
-- Name: usuarios trg_usuarios_atualizado; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_usuarios_atualizado BEFORE UPDATE ON public.usuarios FOR EACH ROW EXECUTE FUNCTION public.atualizar_timestamp();


--
-- TOC entry 4934 (class 2606 OID 16958)
-- Name: consultas consultas_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id) ON DELETE CASCADE;


--
-- TOC entry 4935 (class 2606 OID 16963)
-- Name: consultas consultas_profissional_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultas
    ADD CONSTRAINT consultas_profissional_id_fkey FOREIGN KEY (profissional_id) REFERENCES public.profissionais(id) ON DELETE CASCADE;


--
-- TOC entry 4930 (class 2606 OID 16893)
-- Name: pacientes pacientes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4931 (class 2606 OID 16917)
-- Name: profissionais profissionais_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissionais
    ADD CONSTRAINT profissionais_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4932 (class 2606 OID 16934)
-- Name: profissional_especialidades profissional_especialidades_especialidade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissional_especialidades
    ADD CONSTRAINT profissional_especialidades_especialidade_id_fkey FOREIGN KEY (especialidade_id) REFERENCES public.especialidades(id) ON DELETE CASCADE;


--
-- TOC entry 4933 (class 2606 OID 16929)
-- Name: profissional_especialidades profissional_especialidades_profissional_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profissional_especialidades
    ADD CONSTRAINT profissional_especialidades_profissional_id_fkey FOREIGN KEY (profissional_id) REFERENCES public.profissionais(id) ON DELETE CASCADE;


--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO serena_admin;


--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE consultas; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.consultas TO serena_admin;


--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 228
-- Name: SEQUENCE consultas_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.consultas_id_seq TO serena_admin;


--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE especialidades; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.especialidades TO serena_admin;


--
-- TOC entry 5096 (class 0 OID 0)
-- Dependencies: 221
-- Name: SEQUENCE especialidades_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.especialidades_id_seq TO serena_admin;


--
-- TOC entry 5097 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE pacientes; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pacientes TO serena_admin;


--
-- TOC entry 5099 (class 0 OID 0)
-- Dependencies: 223
-- Name: SEQUENCE pacientes_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pacientes_id_seq TO serena_admin;


--
-- TOC entry 5100 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE profissionais; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.profissionais TO serena_admin;


--
-- TOC entry 5102 (class 0 OID 0)
-- Dependencies: 225
-- Name: SEQUENCE profissionais_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.profissionais_id_seq TO serena_admin;


--
-- TOC entry 5103 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE profissional_especialidades; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.profissional_especialidades TO serena_admin;


--
-- TOC entry 5104 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE usuarios; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.usuarios TO serena_admin;


--
-- TOC entry 5106 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE usuarios_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.usuarios_id_seq TO serena_admin;


--
-- TOC entry 2078 (class 826 OID 16843)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO serena_admin;


--
-- TOC entry 2077 (class 826 OID 16842)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO serena_admin;


-- Completed on 2026-09-25 22:31:42

--
-- PostgreSQL database dump complete
--

\unrestrict C1FuY5e6uzd9tdEhczLBDXgEwZC6daQqxkmPn4DBbQBt7ApKq8NAoaDmqvymgpP

