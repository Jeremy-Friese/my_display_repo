import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { CalendlyService } from '../services/calendly.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  animations: [
    trigger('fadeIn', [
      state('out', style({ opacity: 0 })),
      state('in', style({ opacity: 1 })),
      transition('out <=> in', animate('1800ms ease-out'))
    ])
  ]
})

export class HomeComponent implements OnInit, AfterViewInit {
  @ViewChild('imageElement') imageElement!: ElementRef;
  // Define Pictures that will be used on the page.
  mobile: boolean = false;
  wide: boolean = false;
  topPic = "assets/OTM/Logo.jpg"
  img1 = "assets/Disney/Disney-Park.webp"
  img2 = "assets/Disney-Cruise/Disney-Cruise-Ship-OTM.jpg"
  video = "assets/Disney/otmtravels.mp4"
  family = "assets/Disney/family.jpg"

  spacer = ""

  images: any[] = [
    {
      previewImageSrc:
        'assets/carousel/pirate-night.jpeg',
      thumbnailImageSrc:
        'assets/carousel/pirate-night.jpeg',
      alt: 'Disney Cruise Lines Pirate Night at Sea',
      title: 'Disney Cruise Lines Pirate Night at Sea'
    },
    {
      previewImageSrc:
        'assets/carousel/marvel-at-sea.jpeg',
      thumbnailImageSrc:
        'assets/carousel/marvel-at-sea.jpeg',
      alt: 'Disney Cruise Lines Marvel at Sea',
      title: 'Disney Cruise Lines Marvel at Sea'
    },
    {
      previewImageSrc:
        'assets/carousel/halloween-at-sea.jpeg',
      thumbnailImageSrc:
        'assets/carousel/halloween-at-sea.jpeg',
      alt: 'Dinsey Cruise Lines Halloween at Sea',
      title: 'Dinsey Cruise Lines Halloween at Sea'
    },
    {
      previewImageSrc:
        'assets/carousel/merrytime-cruise.jpeg',
      thumbnailImageSrc:
        'assets/carousel/merrytime-cruise.jpeg',
      alt: 'Disney Cruise Lines Merrytime Cruise',
      title: 'Disney Cruise Lines Merrytime Cruise'
    },
  ];

  // Variable for fadeIn
  isVisible = false;
  // Message that will be loaded to Calendly
  message  = ""


  constructor(public calendly: CalendlyService) {}

  ngOnInit() {
    this.message = "Hi Gennie, I am interested in speaking about your Disney Packages."
    if (window.screen.width <= 605) {
      this.mobile = true;
    }
    if (window.screen.width >= 1900) {
      this.wide = true;
      this.spacer = '<br><br><br><br><br><br><br><br>'
    }
    this.calendly.loadCalendlyScript(this.message)
  }

  onIntersect(entries: IntersectionObserverEntry[]) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        console.log(this.isVisible)
        this.isVisible = true;
      }
    });
  }

  ngAfterViewInit(): void {
    const observer = new IntersectionObserver(this.onIntersect.bind(this), {
      threshold: 0.8  // Trigger when 50% of the image is in view
    });

    observer.observe(this.imageElement.nativeElement);
  }

}
