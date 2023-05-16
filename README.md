# Trabajo Práctico 1 - Sistemas Distribuidos
- [Link al set de datos](https://www.kaggle.com/datasets/jeanmidev/public-bike-sharing-in-north-america).
- [Link a notebook de muestra de comandos](https://www.kaggle.com/code/pablodroca/bike-rides-analyzer).

# Ejecución
**Servidor:**
* Para ejecutar el servidor y buildear la imagen
```bash
make server-up
```

* Para ejecutar ver los logs del servidor
```bash
make server-logs
```

* Build, ejecución y logs todos juntos
```bash
make server-run
```

* Para dar de baja al servidor
```bash
make server-down
```

**Cliente:**
* Para ejecutar el cliente y buildear la imagen
```bash
make client-up
```

* Para ejecutar ver los logs del cliente
```bash
make client-logs
```

* Build, ejecución y logs todos juntos
```bash
make client-run
```

* Para dar de baja al cliente
```bash
make client-down
```