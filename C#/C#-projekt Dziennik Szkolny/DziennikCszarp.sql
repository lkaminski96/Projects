delete from uczen_rodzic
where UCZEN_RODZIC.UCZEN_IDUCZNIA = 1 ;

create or replace trigger Test_trig
before delete on  uczen_rodzic
for each row
begin
    
end;

create or replace TRIGGER rodzic_trigg
BEFORE INSERT ON rodzic
FOR EACH ROW

BEGIN
  SELECT rodzic_seq.NEXTVAL
  INTO   :new.idrodzica
  FROM   dual;
END;