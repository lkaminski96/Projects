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
    public class KidsController : Controller
    {
        // GET: Kids
        public ActionResult Index()
        {
            if(Session["IDZalogowanego"] != null && Session["Username"] != null)
                return View();

             return RedirectToAction("Index", "LoggingIn");
        }

        /// <summary>
        /// Akcja generujaca dzieci dla zalogowanego rodzica
        /// </summary>
        /// <returns> zwraca widok dzieci</returns>
        public ActionResult Dzieciaki()
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";

            conn.Open();
            var model = new Kids();
            string sql = "select u.iducznia, u.imie || ' ' || u.nazwisko as imieNazwisko from uczen u" +
                         " join Uczen_rodzic ur on ur.uczen_iducznia = u.iducznia" +
                         " join Rodzic r on r.IDRODZICA = ur.RODZIC_IDRODZICA where r.idrodzica =" + Convert.ToInt16(Session["IDZalogowanego"]) +
                         " order by imieNazwisko";
            // Lista dzieci.
            DBList Kids = new DBList();
            model.Dzieci = Kids.GetSelectListItems(sql);
            conn.Close();
            return PartialView(model);
        }

        /// <summary>
        /// Akcja generujaca oceny dla wybranego dziecka
        /// </summary>
        /// <param name="model"> Model dziecka</param>
        /// <returns> zwraca oceny dziecka </returns>
        [HttpPost]
        public ActionResult Ocenki(Kids model)
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
            
            string sql = "select u.imie, u.nazwisko, o.Ocena, p.nazwa, o.typ from uczen u " +
                         " join oceny o on u.IDUCZNIA = o.UCZEN_IDUCZNIA " +
                         " join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                         " join klasa k on k.IDKLASY = p.KLASA_IDKLASY " +
                         " join Uczen_rodzic ur on ur.uczen_IDUCZNIA = u.IDUCZNIA " +
                         " join Rodzic r on r.IDRODZICA = ur.RODZIC_IDRODZICA " +
                         " where ur.RODZIC_IDRODZICA =" + Convert.ToInt16(Session["IDZalogowanego"]) + " and u.IDUCZNIA=" + model.IDDziecka +
                         " Order by u.nazwisko, p.nazwa, o.ocena";

            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();
            // wypelnianie danych dla wybranego dziecka
            while (dr.Read())
            {
                grades.Add
                (
                    new Oceny { Imie = dr.GetString(0), Nazwisko = dr.GetString(1), Ocena = Convert.ToDouble(dr.GetValue(2)), Przedmiot = dr.GetString(3), Typ = dr.GetString(4) }
                );
            }
            conn.Close();
            return PartialView(grades);
        }

        /// <summary>
        /// Akcja generujaca dzieci dla rodzica
        /// </summary>
        /// <returns> zwraca liste dzieci powiazanych z rodzicem</returns>
        public ActionResult Dziecioki()
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";

            conn.Open();
            var model = new Kids();
            string sql = "select u.iducznia, u.imie || ' ' || u.nazwisko as imieNazwisko from uczen u" +
                         " join Uczen_rodzic ur on ur.uczen_iducznia = u.iducznia" +
                         " join Rodzic r on r.IDRODZICA = ur.RODZIC_IDRODZICA where r.idrodzica =" + Convert.ToInt16(Session["IDZalogowanego"]) +
                         " order by imieNazwisko";
            // Lista dzieci.
            DBList Kids = new DBList();
            model.Dzieci = Kids.GetSelectListItems(sql);
            conn.Close();
            return PartialView(model);
        }

        /// <summary>
        /// Akcja generujaca obecnosci dla wybranego dziecka
        /// </summary>
        /// <param name="model"> Model dziecka dla obecnosci</param>
        /// <returns> zwraca widok obecnosci dla wybranego dziecka</returns>
        [HttpPost]
        public ActionResult Presents(Kids model)
        {
            // polaczenie
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";
            conn.Open();
            string sql = "select u.imie, u.nazwisko, o.data, g.IDGODZ, o.obecny, p.nazwa, u.iducznia from uczen u " +
                          " join obecnosci o on o.uczen_iducznia = u.IDUCZNIA " +
                          " join godziny g on g.IDGODZ = o.GODZINY_IDGODZ " +
                          " join przedmiot p on p.IDPRZEDM = o.PRZEDMIOT_IDPRZEDM " +
                          " join UCZEN_RODZIC ur on ur.uczen_iducznia = u.IDUCZNIA " +
                          " join RODZIC r on r.idrodzica = ur.RODZIC_IDRODZICA " +
                          " where ur.RODZIC_IDRODZICA = " + Convert.ToInt16(Session["IDZalogowanego"]) + "and o.data = TO_DATE('" + model.Date.ToString("yyyy/MM/dd") + "', 'yyyy/mm/dd') and u.iducznia =" + model.IDDziecka +
                          " Order by u.nazwisko, o.data, g.IDGODZ";
            // lista obecnosci
            var obecnosci = new List<Obecnosci>();
            OracleCommand cmd = new OracleCommand(sql, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();

            // wypelnianie modelu danymi z bazy
            while (dr.Read())
            {
                obecnosci.Add
                (
                    new Obecnosci
                    {
                        Imie = dr.GetString(0),
                        Nazwisko = dr.GetString(1),
                        Date = DateTime.Parse(dr.GetOracleDate(2).ToString()),
                        GodzinaZajec = Convert.ToInt16(dr.GetValue(3)),
                        CzyObecny = dr.GetString(4),
                        Przedmiot = dr.GetString(5)
                    }
               );
            }
            conn.Close();
            return PartialView(obecnosci);
        }
    }
    
}
