
# Guía para usar la base de datos PostgreSQL con Docker en otra máquina

## 🖥️ PASOS PARA USARLO EN OTRA MÁQUINA

### 1. Instalar Docker

Asegúrate de tener Docker instalado en la otra máquina.
Puedes descargarlo desde:
👉 [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

---

### 2. Obtener el proyecto

Puedes copiar el proyecto completo (por ejemplo, como un archivo `.zip`) o clonarlo desde GitHub:

```bash
git clone https://github.com/tu-usuario/Gestion_Inventario_Docker.git
cd Gestion_Inventario_Docker
```

---

### 3. Levantar el contenedor con Docker Compose

Desde la terminal, ubicado en la carpeta del proyecto:

```bash
docker-compose up -d
```

✅ Esto iniciará el contenedor con PostgreSQL en el **puerto 5433**, con tu base de datos ya montada desde `inventarios.sql`.

---

### 4. Verificar que todo esté corriendo correctamente

Ejecuta:

```bash
docker ps
```

---

### 5. Acceder a la base de datos desde el contenedor

```bash
docker exec -it inventarios-db psql -U postgres -d inventarios
```

---

Con esto, la base de datos estará disponible y funcional sin necesidad de volver a crearla.
