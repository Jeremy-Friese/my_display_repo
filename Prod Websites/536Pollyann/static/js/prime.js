
var headOne = document.querySelector("#one")
var headTwo = document.querySelector("#two")


var i = 0;
var txt = 'Check out this perfect sized, low maintenance adorable 3 bedroom, 2 bathroom, home.  Excellent usage of space and an abundance of natural light.  Neutral paint colors, art niches, crown mouldings, and other custom touches make this a beautiful retirement or starter home.  Kitchen features gas cooking, large pantry, and breakfast bar.  Pride of ownership shows in this single-owner home.  Master suite features separate tub and shower, dual vanities, and roomy walk-in closet.';
var speed = 15; /* The speed/duration of the effect in milliseconds */


function typeWriter() {
  if (i < txt.length) {
    document.getElementById("demo").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}
