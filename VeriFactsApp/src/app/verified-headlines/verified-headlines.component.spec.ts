import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VerifiedHeadlinesComponent } from './verified-headlines.component';

describe('VerifiedHeadlinesComponent', () => {
  let component: VerifiedHeadlinesComponent;
  let fixture: ComponentFixture<VerifiedHeadlinesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VerifiedHeadlinesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VerifiedHeadlinesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
