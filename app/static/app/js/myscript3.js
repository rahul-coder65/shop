$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
  //  console.log(id);
    $.ajax({
       type:"GET",
       url: "/pluscart",
       data: {
          prod_id : id
       },
       success: function(data){
           eml.innerText = data.quantity
            document.getElementById("cart-no").innerHTML = data.tt
           document.getElementById("amount").innerText = data.amount
           document.getElementById("totalamount").innerText = data.totalamount
       }
    })
  })
  $('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    
    var eml = this.parentNode.children[2]
   
  //  console.log(id);
    $.ajax({
       type:"GET",
       url: "/minuscart",
       data: {
          prod_id : id
         
         
       },
       success: function(data){
      
       
            eml.innerText = data.quantity
            document.getElementById("cart-no").innerHTML = data.tt
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            if(data.tt === 0){
                location.href = "/cart"
            }
            else if(data.quantity === 0){
                document.getElementById("remove-this").remove()
                location.reload(true);
            }
       }
    })
  })
  
  
  $('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
       type:"GET",
       url: "/removecart",
       data: {
          prod_id : id
       },
       success: function(data){
           document.getElementById("amount").innerText = data.amount
           document.getElementById("totalamount").innerText = data.totalamount
  
           document.getElementById("remove-this").remove()

           document.getElementById("cart-no").innerText = data.tt

           if(data.tt === 0){
              location.href = "/cart"
           }
          
        
       }
    })
  })
  
  $('#slider1, #slider2, #slider3, #slider4').owlCarousel({
      loop: true,
      margin: 20,
      responsiveClass: true,
      responsive: {
          0: {
              items: 1,
              nav: false,
              autoplay: true,
          },
          600: {
              items: 3,
              nav: true,
              autoplay: true,
          },
          1000: {
              items: 5,
              nav: true,
              loop: true,
              autoplay: true,
          }
      }
  })
  
  $('#slider1, #slider2, #slider3, #slider4').owlCarousel({
      loop: true,
      margin: 20,
      responsiveClass: true,
      responsive: {
          0: {
              items: 1,
              nav: false,
              autoplay: true,
          },
          600: {
              items: 3,
              nav: true,
              autoplay: true,
          },
          1000: {
              items: 5,
              nav: true,
              loop: true,
              autoplay: true,
          }
      }
  })

  var availableTags = [];
  $.ajax({
   method : "GET",
   url : "/search",
   success : function(response){
    console.log(response)
    searchAjax(response)
   }
  });
  function searchAjax(availableTags){
    $( "#searchproduct" ).autocomplete({
        source: availableTags
      });
  }
  let input = document.getElementById("searchproduct");

  // Execute a function when the user presses a key on the keyboard
  input.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.getElementById("mybtn").click();
    }
  });
  