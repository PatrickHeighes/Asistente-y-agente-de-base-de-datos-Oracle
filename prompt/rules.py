DATABASE_RULES = """
1. Estás interactuando con una base de datos Oracle.
2. Utiliza siempre la sintaxis SQL compatible con Oracle.
3. No uses funciones específicas de MySQL, PostgreSQL o SQL Server (como LIMIT en lugar de FETCH FIRST n ROWS ONLY si es necesario, aunque LangChain maneja parte de esto).
4. Respeta estrictamente los nombres de las tablas y columnas del esquema Chinook (Artist, Album, Track, Invoice, Customer, etc.).
5. Devuelve únicamente consultas SQL limpias y legibles cuando se te solicite.
"""