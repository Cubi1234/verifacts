import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RelatedSearchesComponent } from './related-searches.component';

describe('RelatedSearchesComponent', () => {
  let component: RelatedSearchesComponent;
  let fixture: ComponentFixture<RelatedSearchesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RelatedSearchesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RelatedSearchesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
