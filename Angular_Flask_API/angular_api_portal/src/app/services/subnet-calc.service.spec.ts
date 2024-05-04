import { TestBed } from '@angular/core/testing';

import { SubnetCalcService } from './subnet-calc.service';

describe('SubnetCalcService', () => {
  let service: SubnetCalcService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SubnetCalcService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
