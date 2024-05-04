import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisneyShipsComponent } from './disney-ships.component';

describe('DisneyShipsComponent', () => {
  let component: DisneyShipsComponent;
  let fixture: ComponentFixture<DisneyShipsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DisneyShipsComponent]
    });
    fixture = TestBed.createComponent(DisneyShipsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
