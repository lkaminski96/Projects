-- Generated by Oracle SQL Developer Data Modeler 17.4.0.355.2121
--   at:        2018-08-23 15:30:21 CEST
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



CREATE TABLE godziny (
    idgodz        INTEGER NOT NULL,
    rozpoczecie   VARCHAR2(10) NOT NULL,
    zakonczenie   VARCHAR2(10) NOT NULL
);

COMMENT ON TABLE godziny IS
    'tabela zawierajaca godziny zajec w szkole';

ALTER TABLE godziny ADD CONSTRAINT godziny_pk PRIMARY KEY ( idgodz );

CREATE TABLE klasa (
    idklasy              INTEGER
        CONSTRAINT nnc_klasa_idklasy NOT NULL,
    nazwa                VARCHAR2(10)
        CONSTRAINT nnc_klasa_nazwa NOT NULL,
    profil               VARCHAR2(256)
        CONSTRAINT nnc_klasa_profil NOT NULL,
    rocznik              INTEGER
        CONSTRAINT nnc_klasa_rocznik NOT NULL,
    nauczyciel_idnaucz   INTEGER NOT NULL
);

COMMENT ON TABLE klasa IS
    'tabela zawierajaca klasy w szkole';

ALTER TABLE klasa ADD CONSTRAINT klasa_pk PRIMARY KEY ( idklasy );

CREATE TABLE nauczyciel (
    idnaucz      INTEGER NOT NULL,
    imie         VARCHAR2(256) NOT NULL,
    nazwisko     VARCHAR2(256) NOT NULL,
    pesel        VARCHAR2(11) NOT NULL,
    nrtelefonu   VARCHAR2(20) NOT NULL,
    email        VARCHAR2(256) NOT NULL,
    login        VARCHAR2(256) NOT NULL,
    haslo        VARCHAR2(256) NOT NULL,
    sol          VARCHAR2(256) NOT NULL
);

COMMENT ON TABLE nauczyciel IS
    'tabela zawierajaca informacje o nauczycielu  w szkole';

ALTER TABLE nauczyciel ADD CONSTRAINT nauczyciel_pk PRIMARY KEY ( idnaucz );

CREATE TABLE obecnosci (
    idobec               INTEGER NOT NULL,
    data                 DATE NOT NULL,
    obecny               VARCHAR2(1) NOT NULL,
    uczen_iducznia       INTEGER NOT NULL,
    przedmiot_idprzedm   INTEGER NOT NULL,
    godziny_idgodz       INTEGER NOT NULL
);

COMMENT ON TABLE obecnosci IS
    'Tabela zawierajaca obecnosci uczniow na zajeciach';

ALTER TABLE obecnosci ADD CONSTRAINT obecnosci_pk PRIMARY KEY ( idobec );

CREATE TABLE oceny (
    idoceny              INTEGER NOT NULL,
    ocena                FLOAT(3) NOT NULL,
    typ                  VARCHAR2(256) NOT NULL,
    uczen_iducznia       INTEGER NOT NULL,
    przedmiot_idprzedm   INTEGER NOT NULL
);

COMMENT ON TABLE oceny IS
    'Tabela zawierajaca oceny  uczniow na zajeciach';

ALTER TABLE oceny ADD CONSTRAINT oceny_pk PRIMARY KEY ( idoceny );

CREATE TABLE profesja (
    idprof               INTEGER NOT NULL,
    nazwa                VARCHAR2(256) NOT NULL,
    nauczyciel_idnaucz   INTEGER NOT NULL
);

COMMENT ON TABLE profesja IS
    'tabela zawierajaca zawody wykonywane przez nauczycieli';

ALTER TABLE profesja ADD CONSTRAINT profesja_pk PRIMARY KEY ( idprof );

CREATE TABLE przedmiot (
    idprzedm             INTEGER NOT NULL,
    nazwa                VARCHAR2(256) NOT NULL,
    nauczyciel_idnaucz   INTEGER NOT NULL,
    klasa_idklasy        INTEGER NOT NULL
);

COMMENT ON TABLE przedmiot IS
    'Tabela zawierajaca przedmioty przedmioty szkolne';

ALTER TABLE przedmiot ADD CONSTRAINT przedmiot_pk PRIMARY KEY ( idprzedm );

CREATE TABLE rodzic (
    idrodzica    INTEGER NOT NULL,
    imie         VARCHAR2(256) NOT NULL,
    nazwisko     VARCHAR2(256) NOT NULL,
    nrtelefonu   VARCHAR2(20) NOT NULL,
    email        VARCHAR2(256) NOT NULL,
    login        VARCHAR2(256) NOT NULL,
    haslo        VARCHAR2(256) NOT NULL,
    sol          VARCHAR2(256) NOT NULL,
    pesel        VARCHAR2(11) NOT NULL
);

COMMENT ON TABLE rodzic IS
    'Tabela zawierajaca informacje o rodzicach';

ALTER TABLE rodzic ADD CONSTRAINT rodzic_pk PRIMARY KEY ( idrodzica );

CREATE TABLE uczen (
    iducznia        INTEGER NOT NULL,
    imie            VARCHAR2(256) NOT NULL,
    nazwisko        VARCHAR2(256) NOT NULL,
    pesel           VARCHAR2(11) NOT NULL,
    nrtelefonu      VARCHAR2(20) NOT NULL,
    email           VARCHAR2(256) NOT NULL,
    klasa_idklasy   INTEGER NOT NULL
);

COMMENT ON TABLE uczen IS
    'Tabela zawierajaca informacje o uczniach';

ALTER TABLE uczen ADD CONSTRAINT uczen_pk PRIMARY KEY ( iducznia );

CREATE TABLE uczen_rodzic (
    uczen_iducznia     INTEGER NOT NULL,
    rodzic_idrodzica   INTEGER NOT NULL
);

COMMENT ON TABLE uczen_rodzic IS
    'Tabela zawierajaca informacje o powiazaniach miedzy uczniem a rodzicem';

ALTER TABLE uczen_rodzic ADD CONSTRAINT uczen_rodzic_pk PRIMARY KEY ( uczen_iducznia,
rodzic_idrodzica );

ALTER TABLE klasa
    ADD CONSTRAINT klasa_nauczyciel_fk FOREIGN KEY ( nauczyciel_idnaucz )
        REFERENCES nauczyciel ( idnaucz );

ALTER TABLE obecnosci
    ADD CONSTRAINT obecnosci_godziny_fk FOREIGN KEY ( godziny_idgodz )
        REFERENCES godziny ( idgodz );

ALTER TABLE obecnosci
    ADD CONSTRAINT obecnosci_przedmiot_fk FOREIGN KEY ( przedmiot_idprzedm )
        REFERENCES przedmiot ( idprzedm );

ALTER TABLE obecnosci
    ADD CONSTRAINT obecnosci_uczen_fk FOREIGN KEY ( uczen_iducznia )
        REFERENCES uczen ( iducznia );

ALTER TABLE oceny
    ADD CONSTRAINT oceny_przedmiot_fk FOREIGN KEY ( przedmiot_idprzedm )
        REFERENCES przedmiot ( idprzedm );

ALTER TABLE oceny
    ADD CONSTRAINT oceny_uczen_fk FOREIGN KEY ( uczen_iducznia )
        REFERENCES uczen ( iducznia );

ALTER TABLE profesja
    ADD CONSTRAINT profesja_nauczyciel_fk FOREIGN KEY ( nauczyciel_idnaucz )
        REFERENCES nauczyciel ( idnaucz );

ALTER TABLE przedmiot
    ADD CONSTRAINT przedmiot_klasa_fk FOREIGN KEY ( klasa_idklasy )
        REFERENCES klasa ( idklasy );

ALTER TABLE przedmiot
    ADD CONSTRAINT przedmiot_nauczyciel_fk FOREIGN KEY ( nauczyciel_idnaucz )
        REFERENCES nauczyciel ( idnaucz );

ALTER TABLE uczen
    ADD CONSTRAINT uczen_klasa_fk FOREIGN KEY ( klasa_idklasy )
        REFERENCES klasa ( idklasy );

ALTER TABLE uczen_rodzic
    ADD CONSTRAINT uczen_rodzic_rodzic_fk FOREIGN KEY ( rodzic_idrodzica )
        REFERENCES rodzic ( idrodzica );

ALTER TABLE uczen_rodzic
    ADD CONSTRAINT uczen_rodzic_uczen_fk FOREIGN KEY ( uczen_iducznia )
        REFERENCES uczen ( iducznia );



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                            10
-- CREATE INDEX                             0
-- ALTER TABLE                             22
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
