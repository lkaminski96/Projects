using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using DziennikCszarp.Biblioteka;
using DziennikCszarp.Models;
using Oracle.DataAccess.Client;

namespace DziennikCszarp.Controllers
{
    public class PupilsController : Controller
    {
        // zmienne potrzebne do zapamietania potrzebnych danych z bazy
        public static string ClassName;
        public static string SubjectName;
        public static DateTime data;

        // GET: Subjects
        public ActionResult Index()
        {
            if (Session["IDZalogowanego"] != null && Session["Username"] != null)
                return View();

            return RedirectToAction("Index", "LoggingIn");
        }

        /// <summary>
        /// Akcja generujaca liste przedmiotow i klas uczeszczajacych na dane przedmioty
        /// </summary>
        /// <returns> zwraca widok klas i przedmiotow</returns>
        public ActionResult Przedmioty()
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            // model klas i przedmiotow
            var model = new Pupils();
            string sql = "select p.idprzedm, k.nazwa || ' ' || p.nazwa as KlasaPrzedmiot  from Przedmiot p " +
                         "join nauczyciel n on p.NAUCZYCIEL_IDNAUCZ = n.idNaucz " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "where p.NAUCZYCIEL_IDNAUCZ = " + Convert.ToInt16(Session["IDZalogowanego"]);

            // Lista uczniow.
            DBList Pupile = new DBList();
            model.Przedmioty = Pupile.GetSelectListItems(sql);
            conn.Close();
            return PartialView(model);
        }

        /// <summary>
        /// Akcja Generujaca Oceny uczniow dla danego przedmiotu z danej klasy
        /// </summary>
        /// <param name="formcollection"> zawiera wartosc wybrana przez nauczyciela</param>
        /// <returns> zwraca widok ocen uczniow dla danego przedmiotu z danej klasy</returns>
        [HttpPost]
        public ActionResult Ocenki(FormCollection formcollection)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            // lista Ocen
            var grades = new List<Oceny>();

            // zapamietanie wybranego pola przez nauczyciela
            var projectName = formcollection["ProjectName"];
            var NazwaKlasy = projectName.Split(' ');
            PupilsController.ClassName = NazwaKlasy[0];
            PupilsController.SubjectName = NazwaKlasy[1];

            string sql = "select u.iducznia, u.imie, u.nazwisko,  o.Ocena, o.TYP, o.IdOceny, p.IDPRZEDM from uczen u " +
                         "join oceny o on u.iducznia = o.UCZEN_iducznia " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where p.NAUCZYCIEL_IDNAUCZ =" + Convert.ToInt16(Session["IDZalogowanego"]) + "and k.nazwa = '" + PupilsController.ClassName + "' and p.nazwa = '" + PupilsController.SubjectName + "' Order by u.iducznia";

            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();
            // wypelnienie danymi z bazy ocen dla uczniow
            while (dr.Read())
            {
                grades.Add
                (
                    new Oceny { NrWDzienniku = Convert.ToInt16(dr.GetValue(0)), Imie = dr.GetString(1), Nazwisko = dr.GetString(2), Ocena = Convert.ToDouble(dr.GetValue(3)), Typ = dr.GetString(4), IDOceny = Convert.ToInt16(dr.GetValue(5)), IDPrzedmiotu = Convert.ToInt16(dr.GetValue(6)) }
                );
            }
            conn.Close();
            return PartialView(grades);
        }

        /// <summary>
        /// Replika strony generujacej widok ocen
        /// </summary>
        /// <returns> zwraca widok ocen dla uncziow z zapamietanym wyborem</returns>
        public ActionResult Ocenki()
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            //lista ocen
            var grades = new List<Oceny>();
            string sql = "select u.iducznia, u.imie, u.nazwisko,  o.Ocena, o.TYP, o.IdOceny, p.IDPRZEDM from uczen u " +
                         "join oceny o on u.iducznia = o.UCZEN_iducznia " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where p.NAUCZYCIEL_IDNAUCZ =" + Convert.ToInt16(Session["IDZalogowanego"]) + "and k.nazwa = '" + PupilsController.ClassName + "' and p.nazwa = '" + PupilsController.SubjectName + "' Order by u.iducznia";

            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();
            // wypelnienie danych z bazy dla ocen uczniow
            while (dr.Read())
            {
                grades.Add
                (
                    new Oceny { NrWDzienniku = Convert.ToInt16(dr.GetValue(0)), Imie = dr.GetString(1), Nazwisko = dr.GetString(2), Ocena = Convert.ToDouble(dr.GetValue(3)), Typ = dr.GetString(4), IDOceny = Convert.ToInt16(dr.GetValue(5)), IDPrzedmiotu = Convert.ToInt16(dr.GetValue(6)) }
                );
            }
            conn.Close();
            return PartialView(grades);
        }

        /// <summary>
        /// Akcja Generujaca formularz edytowania oceny dla ucznia
        /// </summary>
        /// <param name="id"> id oceny wybranej przez nauczyciela</param>
        /// <returns> zwraca forumlarz</returns>
        [HttpGet]
        public ActionResult EditGrade(int id)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";

            conn.Open();
            string sql = "select u.iducznia, u.imie, u.nazwisko,  o.Ocena, o.TYP, o.IdOceny, p.IDPRZEDM from uczen u " +
                         "join oceny o on u.iducznia = o.UCZEN_iducznia " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where o.IDOceny = :id";
            // model ocen
            var grade = new Oceny();

            // Lista ocen
            DBList gradelist = new DBList();
            var ocena = gradelist.GetGrade();
            grade.Grades = gradelist.GetGradeList(ocena);

            // Lista typow
            DBList typelist = new DBList();
            var type = typelist.GetTyp();
            grade.Types = typelist.GetTypeList(type);

            // generowanie danych 
            DataTable data = new DataTable();
            OracleDataAdapter OracleAdapter = new OracleDataAdapter(sql, conn);

            // Dodaję parametry do zapytania.
            OracleAdapter.SelectCommand.Parameters.Add(
                new OracleParameter("id", id)
            );
            OracleAdapter.Fill(data);
            conn.Close();

            if(data.Rows.Count == 1)
            {
                // dodanie danych do modelu ocen
                grade.NrWDzienniku = Convert.ToInt32(data.Rows[0][0].ToString());
                grade.Imie = data.Rows[0][1].ToString();
                grade.Nazwisko = data.Rows[0][2].ToString();
                grade.Ocena = Convert.ToDouble(data.Rows[0][3].ToString());
                grade.Typ = data.Rows[0][4].ToString();
                grade.IDOceny = Convert.ToInt32(data.Rows[0][5].ToString());
                grade.IDPrzedmiotu = Convert.ToInt32(data.Rows[0][6].ToString());

                return View(grade);
            }
            return RedirectToAction("Przedmioty");
        }

        /// <summary>
        /// Akcja zapisujaca dane do bazy
        /// </summary>
        /// <param name="model"> model oceny</param>
        /// <returns> powraca do widoku ocen dla uczniow z edytowana ocena</returns>
        [HttpPost]
        public ActionResult EditGrade(Oceny model)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql = "update oceny set ocena = :ocena, typ = :typ " +
                         "where idoceny = :id";
            // parametryzacji zapytania i wykonanie go
            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.Parameters.Add(
                new OracleParameter("ocena", model.Ocena)
            );
            cmd.Parameters.Add(
                new OracleParameter("typ", model.Typ)
            );
            cmd.Parameters.Add(
                new OracleParameter("idoceny", model.IDOceny)
            );
            cmd.ExecuteNonQuery();
            conn.Close();
            return RedirectToAction("Ocenki");
        }

        /// <summary>
        /// akcja generujaca formularz dodawania oceny uczniom
        /// </summary>
        /// <returns> zwraca formularz z dodawaniem ocen uczniowi</returns>
        [HttpGet]
        public ActionResult AddGrade()
        {

            string sql = "select distinct(u.iducznia), u.imie || ' ' || u.nazwisko from uczen u " +
                         "join oceny o on u.iducznia = o.UCZEN_iducznia " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where p.NAUCZYCIEL_IDNAUCZ =" + Convert.ToInt16(Session["IDZalogowanego"]) + "and k.nazwa = '" + PupilsController.ClassName + "' and p.nazwa = '" + PupilsController.SubjectName + "' Order by u.iducznia";
            // model oceny
            var grade = new Oceny();
            // Lista ocen
            DBList gradelist = new DBList();
            var ocena = gradelist.GetGrade();
            grade.Grades = gradelist.GetGradeList(ocena);

            // Lista typow
            DBList typelist = new DBList();
            var type = typelist.GetTyp();
            grade.Types = typelist.GetTypeList(type);

            DBList Pupile = new DBList();
            grade.FullName = Pupile.GetSelectListItems(sql);

            return View(grade);
        }
        /// <summary>
        /// Akcja dodajace dane do bazy
        /// </summary>
        /// <param name="model"> model oceny</param>
        /// <returns> powraca do widoku ocen dla uczniow</returns>
        [HttpPost]
        public ActionResult AddGrade(Oceny model)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql1 = "select p.idprzedm from przedmiot p " +
                          "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                          "where p.nazwa='" + PupilsController.SubjectName + "' and k.nazwa = '" + PupilsController.ClassName + "'";
            OracleCommand cmd1 = new OracleCommand(sql1, conn);
            cmd1.CommandType = CommandType.Text;
            OracleDataReader dr = cmd1.ExecuteReader();
            while (dr.Read())
            {
                model.IDPrzedmiotu = Convert.ToInt16(dr.GetValue(0));
            }
            string sql = "INSERT INTO Oceny(Ocena, Typ, Uczen_IDUcznia, Przedmiot_IDPrzedm)" +
                         "VALUES(:ocena, :typ, :IDUcznia, :IDPrzedmiotu)";
            // parametryzacja i wykonanie zapytania
            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.Parameters.Add(
                new OracleParameter("ocena", model.Ocena)
            );
            cmd.Parameters.Add(
                new OracleParameter("typ", model.Typ)
            );
            cmd.Parameters.Add(
                new OracleParameter("IDUcznia", model.IDUcznia)
            );
            cmd.Parameters.Add(
                new OracleParameter("IDPrzedmiotu", model.IDPrzedmiotu)
            );
            cmd.ExecuteNonQuery();
            conn.Close();
            return RedirectToAction("Ocenki");
        }
        /// <summary>
        /// Akcja usuwajaca ocene z tabeli
        /// </summary>
        /// <param name="id"> id oceny</param>
        /// <returns> powraca do widoku ocen</returns>
        [HttpGet]
        public ActionResult DelGrade(int id)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql = "Delete from Oceny " +
                         "where IDOceny = :IDOceny";
            // parametryzacja i wykonanie polecenia
            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.Parameters.Add(
                new OracleParameter("IDOceny", id)
            );
            cmd.ExecuteNonQuery();
            conn.Close();
            return RedirectToAction("Ocenki");
        }


        // Obecnosci

        /// <summary>
        /// Akcja generujaca przedmioty i klasy prowadzone przez nauczyciela
        /// </summary>
        /// <returns> zwraca widok przedmiotow i klas</returns>
        public ActionResult Przedmiotyy()
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            // model klas i przedmiotow
            var model = new Pupils();
            string sql = "select p.idprzedm, k.nazwa || ' ' || p.nazwa as KlasaPrzedmiot  from Przedmiot p " +
                         "join nauczyciel n on p.NAUCZYCIEL_IDNAUCZ = n.idNaucz " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "where p.NAUCZYCIEL_IDNAUCZ = " + Convert.ToInt16(Session["IDZalogowanego"]);

            // Lista uczniow.
            DBList Pupile = new DBList();
            model.Przedmioty = Pupile.GetSelectListItems(sql);
            conn.Close();
            return PartialView(model);
        }

        /// <summary>
        /// Akcja generujaca obecnosci dla uczniow na przedmiocie
        /// </summary>
        /// <param name="model"> Model ucznia</param>
        /// <param name="formcollection"> przechowuje informacje o wyborze klasy i przedmiotu przez nauczyciela</param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult Presents(Kids model, FormCollection formcollection)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            // Lista modeli obecnosci
            var obecnosci = new List<Obecnosci>();

            var projectName = formcollection["ProjectName"];
            var NazwaKlasy = projectName.Split(' ');
            PupilsController.ClassName = NazwaKlasy[0];
            PupilsController.SubjectName = NazwaKlasy[1];
            PupilsController.data = model.Date;

            string sql = "select u.IDUCZNIA, u.imie, u.nazwisko, o.data, g.IDGODZ, o.obecny, o.IdObec from uczen u " +
                         "join obecnosci o on o.UCZEN_iducznia = u.iducznia " +
                         "join godziny g on g.IDGODZ = o.GODZINY_IDGODZ " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where p.NAUCZYCIEL_IDNAUCZ =" + Convert.ToInt16(Session["IDZalogowanego"]) + "and o.data = TO_DATE('" + PupilsController.data.ToString("yyyy/MM/dd") + "', 'yyyy/mm/dd') and p.NAZWA ='" + PupilsController.SubjectName + "' and k.NAZWA = '" + PupilsController.ClassName + "'" +
                         "Order by u.iducznia, o.data, g.IDGODZ";

            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();
            // wypelnienie modelu obecnosci danymi z bazy
            while (dr.Read())
            {
                obecnosci.Add
                (
                    new Obecnosci
                    {
                        IDUcznia = Convert.ToInt16(dr.GetValue(0)),
                        Imie = dr.GetString(1),
                        Nazwisko = dr.GetString(2),
                        Date = DateTime.Parse(dr.GetOracleDate(3).ToString()),
                        GodzinaZajec = Convert.ToInt16(dr.GetValue(4)),
                        CzyObecny = dr.GetString(5),
                        IDObecnosci = Convert.ToInt16(dr.GetValue(6))
                    }
               );
            }
            conn.Close();
            return PartialView(obecnosci);
        }
        /// <summary>
        /// Akcja generujaca obecnosci dla uczniow na przedmiocie(Replika)
        /// </summary>
        /// <returns> zwraca widok obecnosci dla uczniow</returns>
        public ActionResult Presents()
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();

            // lista modeli obecnosci
            var obecnosci = new List<Obecnosci>();

            string sql = "select u.IDUCZNIA, u.imie, u.nazwisko, o.data, g.IDGODZ, o.obecny, o.IdObec from uczen u " +
                         "join obecnosci o on o.UCZEN_iducznia = u.iducznia " +
                         "join godziny g on g.IDGODZ = o.GODZINY_IDGODZ " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where p.NAUCZYCIEL_IDNAUCZ =" + Convert.ToInt16(Session["IDZalogowanego"]) + "and o.data = TO_DATE('" + PupilsController.data.ToString("yyyy/MM/dd") + "', 'yyyy/mm/dd') and p.NAZWA ='" + PupilsController.SubjectName + "' and k.NAZWA = '" + PupilsController.ClassName + "'" +
                         "Order by u.iducznia, o.data, g.IDGODZ";

            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();
            // wypelnienie danymi z bazy modelu obecnosci
            while (dr.Read())
            {
                obecnosci.Add
                (
                    new Obecnosci
                    {
                        IDUcznia = Convert.ToInt16(dr.GetValue(0)),
                        Imie = dr.GetString(1),
                        Nazwisko = dr.GetString(2),
                        Date = DateTime.Parse(dr.GetOracleDate(3).ToString()),
                        GodzinaZajec = Convert.ToInt16(dr.GetValue(4)),
                        CzyObecny = dr.GetString(5),
                        IDObecnosci = Convert.ToInt16(dr.GetValue(6))
                    }
               );
            }
            // Lista modeli.
            conn.Close();
            return PartialView(obecnosci);
        }

        /// <summary>
        /// Akcja generujaca formularz dodawania obecnosci
        /// </summary>
        /// <returns> zwraca model obecnosci</returns>
        [HttpGet]
        public ActionResult AddPresent()
        {

            string sql = "select distinct(u.iducznia), u.imie || ' ' || u.nazwisko from uczen u " +
                         "join oceny o on u.iducznia = o.UCZEN_iducznia " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where p.NAUCZYCIEL_IDNAUCZ =" + Convert.ToInt16(Session["IDZalogowanego"]) + "and k.nazwa = '" + PupilsController.ClassName + "' and p.nazwa = '" + PupilsController.SubjectName + "' Order by u.iducznia";

            // model obecnosci
            var present = new Obecnosci();

            // Lista Godzin zajęć
            DBList hourslist = new DBList();
            var hour = hourslist.GetHour();
            present.Hours = hourslist.GetHoursList(hour);

            // Lista obecny TAK/NIE
            DBList presentlist = new DBList();
            var obecnosci = presentlist.GetPresent();
            present.Obecny = presentlist.GetPresentsList(obecnosci);

            // lista uczniow
            DBList Pupile = new DBList();
            present.FullName = Pupile.GetSelectListItems(sql);

            return View(present);
        }

        /// <summary>
        /// Akcja dodajaca obecnosc do bazy
        /// </summary>
        /// <param name="model"> model Obecnosci</param>
        /// <returns> zwraca widok obecnosci uczniow</returns>
        [HttpPost]
        public ActionResult AddPresent(Obecnosci model)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql1 = "select p.idprzedm from przedmiot p " +
                          "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                          "where p.nazwa='" + PupilsController.SubjectName + "' and k.nazwa = '" + PupilsController.ClassName + "'";
            OracleCommand cmd1 = new OracleCommand(sql1, conn);
            cmd1.CommandType = CommandType.Text;
            OracleDataReader dr = cmd1.ExecuteReader();
            // pobranie id przedmiotu dla klasy i nazwy przedmiotu
            while (dr.Read())
            {
                model.IDPrzedmiotu = Convert.ToInt16(dr.GetValue(0));
            }
            string sql = "INSERT INTO Obecnosci(Data, Obecny, Uczen_IDUcznia, Przedmiot_IDPrzedm, Godziny_IDGODZ)" +
                         "VALUES(:data, :obecny, :IDUcznia, :IDPrzedmiotu, :IDGodz)";
            // parametryzacja oraz wykonanie polecenia
            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.Parameters.Add(
                new OracleParameter("data", model.Date)
            );
            cmd.Parameters.Add(
                new OracleParameter("obecny", model.CzyObecny)
            );
            cmd.Parameters.Add(
                new OracleParameter("IDUcznia", model.IDUcznia)
            );
            cmd.Parameters.Add(
                new OracleParameter("IDPrzedmiotu", model.IDPrzedmiotu)
            );
            cmd.Parameters.Add(
                new OracleParameter("IDGodz", model.GodzinaZajec)
            );
            cmd.ExecuteNonQuery();
            conn.Close();
            return RedirectToAction("Presents");
        }

        /// <summary>
        /// Akcja generujaca formularz do edytowania obecnosci
        /// </summary>
        /// <param name="id"> id obecnosci</param>
        /// <returns> zwraca model obecnosci</returns>
        [HttpGet]
        public ActionResult EditPresent(int id)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql = "select u.IDUCZNIA, u.imie, u.nazwisko, o.data, g.IDGODZ, o.obecny from uczen u " +
                         "join obecnosci o on o.UCZEN_iducznia = u.iducznia " +
                         "join godziny g on g.IDGODZ = o.GODZINY_IDGODZ " +
                         "join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         "join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         "join nauczyciel n on n.idnaucz = p.NAUCZYCIEL_IDNAUCZ " +
                         "where o.IdObec = :id";

            // model obecnosci
            var present = new Obecnosci();

            // Lista Godzin zajęć
            DBList hourslist = new DBList();
            var hour = hourslist.GetHour();
            present.Hours = hourslist.GetHoursList(hour);

            // Lista obecny TAK/NIE
            DBList presentlist = new DBList();
            var obecnosci = presentlist.GetPresent();
            present.Obecny = presentlist.GetPresentsList(obecnosci);

            DataTable data = new DataTable();
            OracleDataAdapter OracleAdapter = new OracleDataAdapter(sql, conn);

            // Dodaję parametry do zapytania.
            OracleAdapter.SelectCommand.Parameters.Add(
                new OracleParameter("id", id)
            );
            OracleAdapter.Fill(data);
            conn.Close();
            // wypelnienie danych dla modelu obecnosci
            if (data.Rows.Count == 1)
            {
                present.IDUcznia = Convert.ToInt32(data.Rows[0][0].ToString());
                present.Imie = data.Rows[0][1].ToString();
                present.Nazwisko = data.Rows[0][2].ToString();
                present.Date = Convert.ToDateTime(data.Rows[0][3]);
                present.GodzinaZajec = Convert.ToInt32(data.Rows[0][4].ToString());
                present.CzyObecny = data.Rows[0][5].ToString();
                present.IDObecnosci = id;
                return View(present);
            }
            return RedirectToAction("Przedmioty");
        }

        /// <summary>
        /// Akcja dodajaca naniesione poprawki do bazy
        /// </summary>
        /// <param name="model"> model obecnosci</param>
        /// <returns> zwraca obecnosci uczniow </returns>
        [HttpPost]
        public ActionResult EditPresent(Obecnosci model)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql = "update obecnosci set data = :data, GODZINY_IDGODZ = :IDGodz, obecny = :obecny " +
                         "where idobec = :id";

            OracleCommand cmd = new OracleCommand(sql, conn);
            
            // parametryzacja i wykonanie polecenia
            cmd.Parameters.Add(
                new OracleParameter("data", model.Date)
            );
            cmd.Parameters.Add(
                new OracleParameter("IDGodz", model.GodzinaZajec)
            );
            cmd.Parameters.Add(
                new OracleParameter("obecny", model.CzyObecny)
            );
            cmd.Parameters.Add(
                new OracleParameter("id", model.IDObecnosci)
            );
            cmd.ExecuteNonQuery();
            conn.Close();
            return RedirectToAction("Presents");
        }

        /// <summary>
        /// Akcja usuwajaca obecnosc z bazy
        /// </summary>
        /// <param name="id"> id obecnosci</param>
        /// <returns> zwraca widok obecnosci uczniow</returns>
        [HttpGet]
        public ActionResult DelPresent(int id)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql = "Delete from Obecnosci " +
                         "where IDObec = :IDObec";
            OracleCommand cmd = new OracleCommand(sql, conn);

            // parametryzacja i wykonanie zapytania
            cmd.Parameters.Add(
                new OracleParameter("IDObec", id)
            );
            cmd.ExecuteNonQuery();
            conn.Close();
            return RedirectToAction("Presents");
        }

    }
}
