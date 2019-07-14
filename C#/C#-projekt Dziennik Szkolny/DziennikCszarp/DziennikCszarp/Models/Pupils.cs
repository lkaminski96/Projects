using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace DziennikCszarp.Models
{
    /// <summary>
    /// Model przedstawiajacy Wybor przedmiotu i klasy
    /// </summary>
    public class Pupils
    {
        public int IDPrzedmiotu { get; set; }

        [DataType(DataType.Date)]
        [DisplayFormat(ApplyFormatInEditMode = true, DataFormatString = "{0:yyyy/MM/dd}")]
        public DateTime Date { get; set; } = DateTime.Now;

        public IEnumerable<SelectListItem> Przedmioty { get; set; }
    }

}