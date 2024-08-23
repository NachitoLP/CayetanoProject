-- TODAS LAS ATENCIONES REGISTRADAS
SELECT 
    s.service_id [ID de atención],
    r.service_reason [Motivo de atención],
	p.person_dni [Persona atendida],
	service_description [Descripción],
	o.organism_name [Organismo interviniente],
    s.service_status [Seguimiento],
    s.service_date AT TIME ZONE 'UTC' AT TIME ZONE 'Argentina Standard Time' [Fecha de atención],
    s.service_modified_date AT TIME ZONE 'UTC' AT TIME ZONE 'Argentina Standard Time' [Fecha de modificación]
FROM 
    atenciones_service s
JOIN 
    atenciones_reason r ON s.service_reason_id_id = r.service_reason_id
JOIN 
	personas_person p ON s.person_id_id = p.person_dni
LEFT JOIN
	organismos_organism o ON s.organism_id_id = o.organism_id

-- TODAS LAS PERSONAS REGISTRADAS
SELECT
	p.person_dni [DNI],
	p.person_name [Nombre],
	p.person_surname [Apellido],
	p.person_birthdate [Fecha Nac],
	p.person_phone [Teléfono],
	p.person_address [Dirección],
	l.locality_name [Localidad],
	p.person_observations [Observaciones],
	p.person_bg_center [¿Centro de abuelos?]
FROM
	personas_person p
JOIN
	personas_locality l ON locality_id_id = locality_id


-- LISTA DE PERSONAS Y SUS ID DE ATENCIONES -> Si es NULL, no tiene atenciones
SELECT
	p.person_dni [DNI],
	p.person_name [Nombre],
	p.person_surname [Apellido],
	a.service_id [ID de atención]
FROM
	personas_person p
LEFT JOIN
	atenciones_service a ON person_id_id = person_dni