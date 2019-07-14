using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Web;

namespace DziennikCszarp.Models
{
    /// <summary>
    /// Model do generowania List
    /// </summary>
    public class Dblist
    {
        [DisplayName("Klucz")]
        public string Key { get; set; }

        [DisplayName("Wartość")]
        public string Value { get; set; }
    }
}