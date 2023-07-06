CREATE DATABASE biblioteca
USE biblioteca
-----------------------------
CREATE TRIGGER LIBRO_ACTUALIZAR_AI
AFTER INSERT ON biblioteca_prestamo
FOR EACH ROW
    UPDATE biblioteca_libro
    SET Cantidad = Cantidad - 1
    WHERE IdLibro = NEW.IdLibro_id;
------------------------
CREATE TRIGGER LIBRO_ACTUALIZAR_AD
AFTER DELETE ON biblioteca_prestamo
FOR EACH ROW
    UPDATE biblioteca_libro
    SET Cantidad = Cantidad + 1
    WHERE IdLibro = OLD.IdLibro_id;   
------------------------------------------------

