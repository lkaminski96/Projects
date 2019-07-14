using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using DziennikCszarp.Models;
using Oracle.DataAccess.Client;

namespace DziennikCszarp.Biblioteka
{
    /// <summary>
    /// Klasa generujaca listy
    /// </summary>
    public class DBList
    {
        /// <summary>
        /// Metoda generujaca liste na podstawie podanego zapytania z bazy
        /// </summary>
        /// <param name="query"> zapytanie bazodanowe</param>
        /// <returns></returns>
        public IEnumerable<SelectListItem> GetSelectListItems(string query)
        {
            var elements = new List<Dblist>();

            // Otwieram połączenie.
            OracleConnection conn = new OracleConnection();
            conn.ConnectionString = "Data Source=(DESCRIPTION="
                                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                                    + "(CONNECT_DATA=(SID=xe)));"
                                    + "User Id=hr; Password=hr;";

            conn.Open();

            // Czytam dane i zapisuję w liście.
            OracleCommand cmd = new OracleCommand(query, conn);
            cmd.CommandType = CommandType.Text;
            OracleDataReader dr = cmd.ExecuteReader();
            while (dr.Read())
            {
                elements.Add(new Dblist
                {
                    Key = dr.GetValue(0).ToString(),
                    Value = dr.GetValue(1).ToString()
                });
            }


            // Zamykam połączenie.
            conn.Close();

            // Tworzę listę typu SelectListItem na podstawie danych z bazy.
            var selectList = new List<SelectListItem>();

            foreach (var element in elements)
            {
                selectList.Add(new SelectListItem
                {
                    Value = element.Key,
                    Text = element.Value
                });
            }

            return selectList;
        }

        /// <summary>
        /// Metoda tworzaca elementy listy
        /// </summary>
        /// <returns> zwraca model rodzaji ocen</returns>
        public IEnumerable<string> GetTyp()
        {
            // Lista pozycji rodzaji oceny.
            List<string> list = new List<string>()
            {
                "Sprawdzian",
                "Kartkowka",
                "PracaDomowa",
                "Odpowiedz"
            };

            return list;
        }

        /// <summary>
        /// Metoda generujaca liste do DropDownlist
        /// </summary>
        /// <param name="elements"> elementy listy wysłane do spakowania</param>
        /// <returns> zwraca liste rodzaji ocen</returns>
        public IEnumerable<SelectListItem> GetTypeList(IEnumerable<string> elements)
        {
            var selectList = new List<SelectListItem>();

            // Dodaję kolejne elementy typu string do SelectListItem nadając wartość oraz wyświetlany tekst.
            foreach (var element in elements)
            {
                selectList.Add(new SelectListItem
                {
                    Value = element,
                    Text = element
                });
            }

            return selectList;
        }

        /// <summary>
        /// Metoda tworzaca elementy listy
        /// </summary>
        /// <returns> zwraca model ocen</returns>
        public IEnumerable<double> GetGrade()
        {
            // Lista pozycji ocen.
            List<double> list = new List<double>()
            {
                1,
                1.5,
                1.75,
                2,
                2.5,
                2.75,
                3,
                3.5,
                3.75,
                4,
                4.5,
                4.75,
                5,
                5.5,
                5.75,
                6
            };
            return list;
        }

        /// <summary>
        /// Metoda generujaca liste do DropDownlist
        /// </summary>
        /// <param name="elements"> elementy listy wysłane do spakowania</param>
        /// <returns> zwraca liste ocen</returns>
        public IEnumerable<SelectListItem> GetGradeList(IEnumerable<double> elements)
        {
            var selectList = new List<SelectListItem>();

            // Dodaję kolejne elementy typu string do SelectListItem nadając wartość oraz wyświetlany tekst.
            foreach (var element in elements)
            {
                selectList.Add(new SelectListItem
                {
                    Value = element.ToString(),
                    Text = element.ToString()
                });
            }

            return selectList;
        }


        /// <summary>
        /// Metoda tworzaca elementy listy
        /// </summary>
        /// <returns>zwraca model wykazania ze uczen jest obecny</returns>
        public IEnumerable<string> GetPresent()
        {
            // Lista pozycji obecnosci TAK/NIE.
            List<string> list = new List<string>()
            {
                "TAK",
                "NIE",
                
            };
            return list;
        }

        /// <summary>
        /// Metoda generujaca liste do DropDownlist
        /// </summary>
        /// <param name="elements"> elementy listy wysłane do spakowania</param>
        /// <returns> zwraca liste obecnosci</returns>
        public IEnumerable<SelectListItem> GetPresentsList(IEnumerable<string> elements)
        {
            var selectList = new List<SelectListItem>();

            // Dodaję kolejne elementy typu string do SelectListItem nadając wartość oraz wyświetlany tekst.
            foreach (var element in elements)
            {
                selectList.Add(new SelectListItem
                {
                    Value = element,
                    Text = element
                });
            }

            return selectList;
        }

        /// <summary>
        /// Metoda tworzaca elementy listy
        /// </summary>
        /// <returns> zwraca model godzin w szkole</returns>
        public IEnumerable<int> GetHour()
        {
            // Lista pozycji godzin w szkole.
            List<int> list = new List<int>()
            {
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9
            };
            return list;
        }

        /// <summary>
        /// Metoda generujaca liste do DropDownlist
        /// </summary>
        /// <param name="elements"> elementy listy wysłane do spakowania</param>
        /// <returns> zwraca liste godzin w szkole</returns>
        public IEnumerable<SelectListItem> GetHoursList(IEnumerable<int> elements)
        {
            var selectList = new List<SelectListItem>();
            // Dodaję kolejne elementy typu string do SelectListItem nadając wartość oraz wyświetlany tekst.
            foreach (var element in elements)
            {
                selectList.Add(new SelectListItem
                {
                    Value = element.ToString(),
                    Text = element.ToString()
                });
            }
            return selectList;
        }
    }
}