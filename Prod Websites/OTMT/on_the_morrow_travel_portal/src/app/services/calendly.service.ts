import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CalendlyService {

  constructor() { }

  loadCalendlyScript(message: string) {
    const script = document.createElement('script');
    script.src = 'https://assets.calendly.com/assets/external/widget.js';
    script.async = true;
    script.onload = () => {
      this.initCalendlyWidget(message);
    };
    document.head.appendChild(script);
  }

  initCalendlyWidget(message: string) {
    // Safe check to see if Calendly is loaded
    if ('Calendly' in window) {
      (window as any).Calendly.initBadgeWidget({
        url: 'https://calendly.com/jeremy-utzn/Book-Your-Trip',
        parentElement: document.getElementById('calendly-widget-container'),
        text: 'Book a Call For Information',
        color: '#0069ff',
        textColor: '#ffffff',
        branding: undefined,
        prefill: {
          customAnswers: {
            a1: message
          }
        },
        utm: {}
      });
    } else {
      console.error('Calendly has not been loaded correctly.');
    }
  }
}
