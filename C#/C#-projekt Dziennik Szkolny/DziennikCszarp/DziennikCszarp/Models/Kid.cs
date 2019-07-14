using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace DziennikCszarp.Models
{
    /// <summary>
    /// Model oceny dla dziecka/ucznia
    /// </summary>
    public class Oceny
    {
        [DisplayName("Imię")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Imie { get; set; }

        [DisplayName("Nazwisko")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Nazwisko { get; set; }

        [DisplayName("Ocena")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public double Ocena { get; set; }

        [DisplayName("Przedmiot")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Przedmiot { get; set; }

        [DisplayName("Typ")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Typ { get; set; }

        [DisplayName("Numer w Dzienniku")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int NrWDzienniku { get; set; }

        [DisplayName("IDUcznia")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int IDUcznia { get; set; }

        [DisplayName("IDPrzedmiotu")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int IDPrzedmiotu { get; set; }

        [DisplayName("IDOceny")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int IDOceny { get; set; }

        [DisplayName("Ocena")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public IEnumerable<SelectListItem> Grades { get; set; }

        [DisplayName("Typ")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public IEnumerable<SelectListItem> Types { get; set; }

        [DisplayName("Uczeń")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public IEnumerable<SelectListItem> FullName { get; set; }
    }

    /// <summary>
    /// Model obecnosci dla dziecka/ucznia
    /// </summary>
    public class Obecnosci
    {
        [DisplayName("IDUcznia")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int IDUcznia { get; set; }

        [DisplayName("Imię")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Imie { get; set; }

        [DisplayName("Nazwisko")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Nazwisko { get; set; }

        [DisplayName("Data")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [DataType(DataType.Date)]
        [DisplayFormat(ApplyFormatInEditMode = true, DataFormatString = "{0:yyyy/MM/dd}")]
        public DateTime Date { get; set; } = DateTime.Now;

        [DisplayName("Godzina Zajęć")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int GodzinaZajec { get; set; }

        [DisplayName("Obecny")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public string CzyObecny { get; set; }

        [DisplayName("IDObecnosci")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int IDObecnosci { get; set; }

        [DisplayName("Przedmiot")]
        [Required(ErrorMessage = "* pole wymagane.")]
        [StringLength(20, MinimumLength = 1)]
        public string Przedmiot { get; set; }

        [DisplayName("IDPrzedmiotu")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public int IDPrzedmiotu { get; set; }

        [DisplayName("Godzina Zajęć")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public IEnumerable<SelectListItem> Hours { get; set; }

        [DisplayName("Uczeń")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public IEnumerable<SelectListItem> FullName { get; set; }

        [DisplayName("Obecny")]
        [Required(ErrorMessage = "* pole wymagane.")]
        public IEnumerable<SelectListItem> Obecny { get; set; }

    }
}