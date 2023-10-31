### Autor: Pablo Valverde Soriano

Cliente básico para el servicio [APDI-BLOBS](https://github.com/pavalso/APDI)

### Instrucciones de uso

1- Clonar el repositorio

2- Instalar el repositorio con ```pip install .```

3- Instalar las dependencias con ```pip install -r requirements.txt```

4- Ejecutar el cliente con ```blobs_cli <url_servicio_autenticación> <url_servicio_blobs>```

# Manual de Instrucciones

## Comandos Disponibles

### Comandos Generales
- `login <user> <password>`: Inicia sesión en el sistema de autenticación con un nombre de usuario y una contraseña.
- `logout`: Cierra la sesión actual.
- `exit`: Sale de la CLI.

### Gestión de Blobs
- `new <file>`: Crea un nuevo blob a partir de un archivo local.
- `blobs`: Lista todos los blobs disponibles en el sistema.
- `download <blob_id>`: Descarga un blob especificado por su ID.
- `upload <blob_id> <file>`: Sube un archivo local a un blob existente.
- `md5 <blob_id>`: Obtiene el valor MD5 de un blob.
- `sha256 <blob_id>`: Obtiene el valor SHA256 de un blob.
- `visibility <blob_id> <visibility>`: Cambia la visibilidad de un blob a público o privado.
- `allow <username> <blob_id>`: Permite que un usuario acceda a un blob.
- `revoke <username> <blob_id>`: Revoca el acceso de un usuario a un blob.
- `delete <blob_id>`: Elimina un blob.
- `property <blob_id> <property>`: Obtiene una propiedad específica de un blob (accessURL, allowedUsers o isPrivate).

### Consideraciones
- En caso de errores, la CLI proporcionará un mensaje de error informativo.
- Si la sesión expira, deberás iniciar sesión nuevamente.

## Ejemplos de Uso
1. Iniciar sesión en el sistema:
   ```bash
   login <user> <password>
   ```

2. Crear un nuevo blob:
   ```bash
   new <file>
   ```

3. Listar todos los blobs:
   ```bash
   blobs
   ```

4. Descargar un blob:
   ```bash
   download <blob_id>
   ```

5. Subir un archivo a un blob existente:
   ```bash
   upload <blob_id> <file>
   ```

6. Cambiar la visibilidad de un blob a público:
   ```bash
   visibility <blob_id> public
   ```

7. Permitir que un usuario acceda a un blob:
   ```bash
   allow <username> <blob_id>
   ```

8. Revocar el acceso de un usuario a un blob:
   ```bash
   revoke <username> <blob_id>
   ```

9. Eliminar un blob:
   ```bash
   delete <blob_id>
   ```

10. Obtener una propiedad específica de un blob:
    ```bash
    property <blob_id> <property>
    ```
