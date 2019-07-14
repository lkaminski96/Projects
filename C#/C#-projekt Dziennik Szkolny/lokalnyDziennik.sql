select u.imie, u.nazwisko from uczen u 
join uczen_rodzic ur on u.IDUCZNIA = ur.UCZEN_IDUCZNIA 
join rodzic r on r.IDRODZICA = ur.RODZIC_IDRODZICA
where r.IDRODZICA = 1;

select u.iducznia, u.imie || ' ' || u.nazwisko as imieNazwisko from uczen u 
                          join Uczen_rodzic ur on ur.uczen_iducznia = u.iducznia 
                          join Rodzic r on r.IDRODZICA = ur.RODZIC_IDRODZICA where r.idrodzica = 1
                          order by imieNazwisko;

select u.imie, u.nazwisko, o.data, g.IDGODZ, o.obecny, p.nazwa, u.iducznia from uczen u
join obecnosci o on o.uczen_iducznia = u.IDUCZNIA
join godziny g on g.IDGODZ = o.GODZINY_IDGODZ
join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM
join UCZEN_RODZIC ur on ur.uczen_iducznia = u.IDUCZNIA
join RODZIC r on r.idrodzica = ur.RODZIC_IDRODZICA
where ur.RODZIC_IDRODZICA = 1 and o.data=TO_DATE('2018/08/24', 'yyyy/mm/dd') and  u.iducznia = 1 
Order by u.nazwisko, o.data, g.IDGODZ;




select u.imie, u.nazwisko, o.Ocena, p.nazwa, o.typ from uczen u 
                          join oceny o on u.IDUCZNIA = o.UCZEN_IDUCZNIA
                          join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM 
                          join klasa k on k.IDKLASY = p.KLASA_IDKLASY 
                          join Uczen_rodzic ur on ur.uczen_IDUCZNIA = u.IDUCZNIA 
                          join Rodzic r on r.IDRODZICA = ur.RODZIC_IDRODZICA 
                          where ur.RODZIC_IDRODZICA = 1 and u.IDUCZNIA= 26
                         Order by u.nazwisko, p.nazwa, o.ocena;
                         
-- Nauczyciel
select k.nazwa, p.nazwa, p.idprzedm from Przedmiot p 
join nauczyciel n on p.NAUCZYCIEL_IDNAUCZ = n.idNaucz 
join klasa k on k.IDKLASY = p.KLASA_IDKLASY 
where p.NAUCZYCIEL_IDNAUCZ = 4;

-- Ocen uczniow
select distinct(u.iducznia), u.imie || ' ' || u.nazwisko from uczen u 
join oceny o on u.iducznia = o.UCZEN_iducznia 
join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM
join klasa k on k.IDKLASY = p.KLASA_IDKLASY 
join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ
where p.NAUCZYCIEL_IDNAUCZ = 4 and k.nazwa = '4J' and p.nazwa ='J.Angielski';


-- Obecnosci uczniow

select u.IDUCZNIA, u.imie, u.nazwisko, o.data, g.IDGODZ, o.obecny, o.IdObec from uczen u 
join obecnosci o on o.UCZEN_iducznia = u.iducznia
join godziny g on g.IDGODZ = o.GODZINY_IDGODZ
join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM
join klasa k on k.IDKLASY = p.KLASA_IDKLASY 
join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ 
where p.NAUCZYCIEL_IDNAUCZ = 4 and o.data = '2018/08/24' and p.NAZWA = 'J.Angielski' and k.NAZWA = '4J'
Order by u.iducznia, o.data, g.IDGODZ;

