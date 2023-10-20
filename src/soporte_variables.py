lista_paises = ['United States', 'Canada' , 'Argentina']

dicc_estados = {
    'NV' : 'Nevada',
    'TX' : 'Texas',
    'IN' : 'Indianapolis',
    'CA' : 'California',
    'VA' : 'Virginia',
    'NY' : 'New York',
    'MI' : 'Michigan', 
    'GA' : 'Georgia', 
    'ND' : 'North Dakota', 
    'New York, NY' : 'New York', 
    'Ciudad Autónoma de Buenos Aires' : 'Buenos Aires'}

tabla_paises = '''
CREATE TABLE IF NOT EXISTS `Universidades`.`paises` (
    `id_estado` INT NOT NULL AUTO_INCREMENT,
    `nombre_pais` VARCHAR(45) NOT NULL,
    `nombre_provincia` VARCHAR(45),
    `latitud` FLOAT,
    `longitud`FLOAT,
    PRIMARY KEY (`id_estado`));
'''

tabla_universidades = '''
CREATE TABLE IF NOT EXISTS `Universidades`.`universidades` (
    `id_universidades` INT NOT NULL AUTO_INCREMENT,
    `nombre_universidad` VARCHAR(100) NOT NULL,
    `pagina_web` VARCHAR(100),
    `paises_id_estado` INT NOT NULL,
    PRIMARY KEY (`id_universidades`),
    CONSTRAINT `fk_universidades_paises`
        FOREIGN KEY (`paises_id_estado`)
        REFERENCES `Universidades`.`paises` (`id_estado`));
ENGINE = InnoDB;
'''