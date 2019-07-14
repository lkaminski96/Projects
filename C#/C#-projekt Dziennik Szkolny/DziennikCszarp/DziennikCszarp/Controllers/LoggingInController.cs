using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Web;
using System.Web.Mvc;
using System.Web.UI.WebControls;
using Oracle.DataAccess.Client;
using DziennikCszarp.Models;
using DziennikCszarp.ViewModels;


namespace DziennikCszarp.Controllers
{
    public class LoggingInController : Controller
    {

        /// <summary>
            /// Metoda służąca do wyświetlenia panelu logowania do serwisu
            /// </summary>
            /// <returns>Zwracane jest przekierowanie do funkcji sprawdzającej czy osoba została poprawnie zalogowana</returns>
            // GET: Login
            public ActionResult Index()
        {
            return View();
        }
        /// <summary>
        /// Metoda służąca do logowania użytkownika
        /// </summary>
        /// <param name="user">Dane logowania podane przez użytkownika</param>
        /// <returns>Jeśli osoba została poprawnie zalogowana to zostanie przekierowana do strony głównej serwisu</returns>
        [HttpPost]
        public ActionResult Login(AccountViewModel user)
        {
            if (ModelState.IsValid)
            {
                //dane chwilowe do połączenia na sztywno
                OracleConnection conn = new OracleConnection();
                conn.ConnectionString = "Data Source=(DESCRIPTION="
                    + "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))"
                    + "(CONNECT_DATA=(SID=xe)));"
                    + "User Id=hr; Password=hr;";

                conn.Open();
                string sql = "";
                // zapisanie zapytania w zaleznosci od tego kto probuje sie zalogowac
                if (user.account.kto == Person.Nauczyciel)
                    sql = "select idnaucz, login, haslo, sol from nauczyciel";

                else if (user.account.kto == Person.Rodzic)
                    sql = "select idrodzica, login, haslo, sol from rodzic";


                // wykonanie zapytania SQL
                OracleCommand cmd = new OracleCommand(sql, conn);
                cmd.CommandType = CommandType.Text;
                bool czypoprawne = false;
                OracleDataReader dr = cmd.ExecuteReader();
                while (dr.Read())
                {
                    // sprawdzenie czy podany login i haslo sa poprawne
                    if ((user.account.Username.ToLower() == dr.GetString(1).ToLower()) && ( GetMD5(user.account.Password + dr.GetString(3)) == dr.GetString(2)))
                    {
                        czypoprawne = true;
                        user.account.IDOsoby = Convert.ToInt16(dr.GetValue(0));
                    }      
                }
                if (czypoprawne)
                {
                    // zapisanie odpowiednich danych i przeniesienie na odpowiednia strone
                    Session["Username"] = user.account.Username;
                    Session["IDZalogowanego"] = user.account.IDOsoby;
                    conn.Close();
                    if (user.account.kto == Person.Rodzic)
                        return RedirectToAction("Index", "Kids");

                    if (user.account.kto == Person.Nauczyciel)
                        return RedirectToAction("Index", "Pupils");

                    return View("Index");
                }
                ViewBag.Error = "Niepoprawne dane logowania";
                conn.Close();
                return View("Index");
            }
            return View("Index");
        }
        /// <summary>
        /// Metoda służąca do wylogowania użytkownika z serwisu
        /// </summary>
        /// <returns>Usuwana jest sesja oraz osoba zostaje przekierowana do strony głównej serwisu</returns>

        public ActionResult Logout()
        {
            Session["Username"] = null;
            Session["IDZalogowanego"] = null;
            return RedirectToAction("Index", "LoggingIn");
        }
        /// <summary>
        /// Metoda zwracajaca zhaszowane haslo uzytkownika
        /// </summary>
        /// <param name="password"> przechowuje haslo podane od uzytkownika wraz z sola z bazy</param>
        /// <returns> zwraca hash hasla uzytkownika</returns>
        public string GetMD5(string password)
        {
            using (MD5 md5Hash = MD5.Create())
            {
                string hash = GetMd5Hash(md5Hash, password);
                return hash;
            }
        }

        /// <summary>
        /// Metoda hashująca hasło
        /// </summary>
        /// <param name="md5Hash">zmienna typu MD5</param>
        /// <param name="haslo">hasło podane przez użytkownika</param>
        /// <returns> zwraca zhaszowane haslo</returns>
        static string GetMd5Hash(MD5 md5Hash, string haslo)
        {
            byte[] data = md5Hash.ComputeHash(Encoding.UTF8.GetBytes(haslo));

            StringBuilder sBuilder = new StringBuilder();

            for (int i = 0; i < data.Length; i++)
            {
                sBuilder.Append(data[i].ToString("x2"));
            }

            return sBuilder.ToString();
        }

    }
}