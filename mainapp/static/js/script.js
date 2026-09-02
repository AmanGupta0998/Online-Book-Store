var typed = new Typed(".text1", {
  strings: ["Email: vidyaprakashanmandir@gmail.com", "Contact-no: +919889824690", "Created By: Aman Gupta"],
  typeSpeed: 100,
  backSpeed: 100,
  backDelay: 1500,
  loop: true
});

        
        
 function price() {
            //window.alert("hii");
            var pp = document.getElementById("pp").innerHTML;
            var qty = document.getElementById("qty").value;
            var tp = pp * qty;
            document.getElementById("tp").innerHTML = tp;
        }




