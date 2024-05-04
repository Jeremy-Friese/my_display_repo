import { Component, OnInit } from '@angular/core';
import { CalendlyService } from '../services/calendly.service';

@Component({
  selector: 'app-disney',
  templateUrl: './disney.component.html',
  styleUrls: ['./disney.component.scss']
})
export class DisneyComponent implements OnInit {
  constructor(public calendly: CalendlyService) { }
  mobile: boolean = false;
  // topPic = "assets/Disney-Park/otmtravels.png"
  // topPic = "assets/OTM/otmtravels.png";
  topPic = "assets/OTM/Logo.jpg"
  epcot = "assets/Disney-Park/Epcot.jpg";
  disneyWish = "assets/Disney-Cruise/Disney-Cruise-Wish-OTM.jpg";
  parallaxImage1 = "assets/Disney-Park/otm-disney-castle.jpg";
  parallaxImage2 = "assets/Disney-Park/disney-castle-group.jpg";
  parallaxImage3 = "assets/Disney-Cruise/Disney-cruise-OTM.jpg";
  parallaxImage4 = "assets/Star-Wars/Disney-Star-Wars-Malinium-Falcon-OTM.jpg";
  img2 = "assets/Disney-Park/disney-friends-otm.jpg";
  img1 = "assets/Disney-Park/disney-castle-group.jpg";
  img3 = "assets/Disney-Cruise/disney-cruise-hall.jpg";
  img4 = "assets/Star-Wars/Disney-Storm-Trooper-OTM.jpg";
  toggelOn = false;
  styleBackground = "lightblue";
  textColor = "blue";
  tabColor = "white";
  tabText = "Experience The Force!";
  cardText = "A Force Experience Like No Other!";
  cardBackground = "rgb(226, 220, 220)"
  message = "Hi Gennie, I am interested in a Walt Disney Vacation Package. Test"

  ngOnInit(): void {
    if (window.screen.width <= 605) {
      this.mobile = true;
    }
    this.calendly.loadCalendlyScript(this.message)
    if (window.screen.width <= 605) {
      this.parallaxImage1 = "assets/Disney-Park/otm-disney-castle-mobile.jpg";
      this.parallaxImage2 = "assets/Disney-Park/disney-castle-group-mobile.jpg";
      this.parallaxImage3 = "assets/Disney-Cruise/Disney-cruise-OTM-mobile.jpg";
      this.parallaxImage4 = "assets/Star-Wars/Disney-Star-Wars-Malinium-Falcon-OTM-mobile.jpg";
      this.disneyWish = "assets/Disney-Cruise/mobile-Disney-Cruise-Wish-OTM-mobile.jpg";
      this.img4 = "assets/Star-Wars/rey-chewie-otm.jpg";
    }
  }


  onToggle(): void {
    console.log(this.toggelOn)
    this.toggelOn = !this.toggelOn
    if (this.toggelOn) {
      this.styleBackground = "red"
      this.tabColor = "darkred"
      this.textColor = "darkred"
      this.parallaxImage4 = "assets/Star-Wars/Disney-Kylo-Ren-OTM.jpg"
      this.img4 = "assets/Star-Wars/vader-kylo.jpg"
      this.tabText = "Where the First Order Rules the Galaxy!"
      this.cardText = "Your First Steps To Becoming A Powerful Sith!"
      this.cardBackground = "red"
      if (window.screen.width <= 605) {
        this.parallaxImage4 = "assets/Star-Wars/Disney-Kylo-Ren-OTM-mobile.jpg"
        this.img4 = "assets/Star-Wars/vader-kylo-mobile.jpg"
      }
    }
    else {
      this.styleBackground = "lightblue"
      this.textColor = "blue"
      this.tabColor = "white"
      this.parallaxImage4 = "assets/Star-Wars/Disney-Star-Wars-Malinium-Falcon-OTM.jpg"
      this.img4 = "assets/Star-Wars/Disney-Storm-Trooper-OTM.jpg"
      this.tabText = "Experience The Force!"
      this.cardText = "A Force Experience Like No Other!"
      this.cardBackground = "rgb(226, 220, 220)"
      if (window.screen.width <= 650) {
        this.img4 = "assets/Star-Wars/rey-chewie-otm.jpg";
      }
    }
  }
}
