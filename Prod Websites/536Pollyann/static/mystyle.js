
var headOne = document.querySelector("#one")
var headTwo = document.querySelector("#two")

headOne.addEventListener("mouseover", function(){
  headOne.textContent = "What Good Finds";
  headOne.style.color = "Blue";
  })

headOne.addEventListener("mouseout", function(){
  headOne.textContent = "What Good Finds";
  headOne.style.color = "Green";
  })
