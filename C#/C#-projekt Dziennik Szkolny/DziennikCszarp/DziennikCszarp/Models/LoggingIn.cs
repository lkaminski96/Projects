using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Mvc.Html;
using DziennikCszarp.ViewModels;

namespace DziennikCszarp.Models
{
    /// <summary>
    /// Model Logowania do dziennika
    /// </summary>
    public class LoggingIn
    {
        [Required(ErrorMessage = "Uzupełnij pole")]
        [Display(Name = "Login")]
        [DataType(DataType.Text)]
        public string Username { get; set; }

        [Required(ErrorMessage = "Uzupełnij pole")]
        [Display(Name = "Hasło")]
        [DataType(DataType.Text)]
        public string Password { get; set; }

        [Display(Name = "Zaloguj jako")]
        [DataType(DataType.Text)]
        public Person kto { get; set; }

        public int IDOsoby { get; set; }
    }
    
    /// <summary>
    /// Lista osob mozliwych do zalogowania
    /// </summary>
    public enum Person
    {
        Nauczyciel,
        Rodzic
    }
}