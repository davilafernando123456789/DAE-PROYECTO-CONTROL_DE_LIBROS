CREATE DATABASE biblioteca
USE biblioteca
DROP TRIGGER despues_insertar_prestamo
DELIMITER //

CREATE TRIGGER despues_insertar_prestamo
AFTER INSERT ON biblioteca_prestamo
FOR EACH ROW
BEGIN
    DECLARE estudiante_existente INT;
    
    -- Verificar si el estudiante ya existe en Penalizacion
    SELECT COUNT(*) INTO estudiante_existente
    FROM biblioteca_penalizacion
    WHERE IdEstudiante_id = NEW.IdEstudiante_id;
    
    IF estudiante_existente = 0 THEN
        -- Insertar nuevo registro en Penalizacion si el estudiante no existe
        INSERT INTO biblioteca_penalizacion (IdEstudiante_id, Estado)
        VALUES (NEW.IdEstudiante_id, 'Apto');
    ELSE
        -- Actualizar fecha de entrega y estado en Devolucion
        UPDATE biblioteca_devolucion
        SET Fecha_entrega = NULL, Estado = 'No entregado'
        WHERE IdPrestamo = NEW.IdPrestamo;
    END IF;
END;
//

DELIMITER ;