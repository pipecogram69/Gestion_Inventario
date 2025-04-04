
# 📦 Gestión de Inventario - Proyecto con PostgreSQL en Docker

Este proyecto utiliza Docker para levantar una base de datos PostgreSQL con una estructura y datos iniciales ya cargados.

---

## ✅ Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 ¿Cómo levantar el proyecto?

1. **Clona este repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/Gestion_Inventario.git
   cd Gestion_Inventario
   ```

2. **Levanta los servicios con Docker Compose:**

   ```bash
   docker-compose up -d
   ```

   Esto creará un contenedor con PostgreSQL en el puerto `5433` y ejecutará automáticamente el script `inventarios.sql` para crear la base y cargar datos.

3. **Conéctate a la base de datos:**

   ```bash
   docker exec -it inventarios-db psql -U postgres -d inventarios
   ```

---

## 🛠️ Configuración

- Puerto local expuesto: **5433**
- Usuario: `postgres`
- Contraseña: `123456`
- Base de datos: `inventarios`

---

## 🗃️ Estructura de carpetas

```
Gestion_Inventario/
├── docker-compose.yml
├── init/
│   └── inventarios.sql  <-- script de inicialización
└── README.md
```

---

## 🧽 ¿Necesitas reiniciar todo desde cero?

Si necesitas borrar todo (contenedor + volumen + base de datos):

```bash
docker-compose down -v
docker-compose up -d
```
