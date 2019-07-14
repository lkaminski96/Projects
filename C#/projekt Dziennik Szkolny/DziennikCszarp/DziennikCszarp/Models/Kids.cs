using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace DziennikCszarp.Models
{
    /// <summary>
    /// Model przedstawiajacy dzieci zalogowanego rodzica
    /// </summary>
    public class Kids
    {
        public int IDDziecka { get; set; }

        [DataType(DataType.Date)]
        [DisplayFormat(ApplyFormatInEditMode = true, DataFormatString = "{0:yyyy/MM/dd}")]
        public DateTime Date { get; set; } = DateTime.Now;

        [Required(ErrorMessage = "Pole jest wymagane!")]
        public IEnumerable<SelectListItem> Dzieci { get; set; }
    }
}