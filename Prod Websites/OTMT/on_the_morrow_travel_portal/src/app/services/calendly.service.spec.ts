import { TestBed } from '@angular/core/testing';

import { CalendlyService } from './calendly.service';

describe('CalendlyService', () => {
  let service: CalendlyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CalendlyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
