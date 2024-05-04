import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'onTheMorrowTravel';
  @ViewChild('sidenav') sidenav: MatSidenav | undefined;
  isExpanded = false;
  showSubmenu: boolean = false;
  isShowing = false;
  showSubSubMenu: boolean = false;


  submenu1: boolean = false;
  isMenuOpen = false;
  buttonMenuOpen = false;
  mobile: boolean = false;



  ngOnInit(): void {
    if (window.screen.width <= 605) {
      this.mobile = true;
    }
  }

  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen
  }

  toggleButtonMenu() {
    this.buttonMenuOpen = !this.buttonMenuOpen
    this.isExpanded = !this.isExpanded
    if (window.screen.width <= 605) {
      this.mobile = !this.mobile;
    }
  }


  mouseenter() {
    if (!this.isExpanded) {
      this.isShowing = true;
      this.submenu1 = true;
    }
  }

  mouseleave() {
    if (!this.isExpanded) {
      this.isShowing = false;
      this.submenu1 = false;
    }
  }
}
