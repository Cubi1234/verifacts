import { Component, Input, OnInit } from '@angular/core';
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  selector: 'app-related-searches',
  templateUrl: './related-searches.component.html',
  styleUrls: ['./related-searches.component.css'],
  animations: [
    trigger('fadeIn', [
      state('void', style({
        opacity: 0,
      })),
      transition(':enter', [
        animate('0.5s ease-in', style({ opacity: 1 }))
      ])
    ]),
  ]
})
export class RelatedSearchesComponent implements OnInit {
  @Input() factCheckResults: any[] = [];
  currentPageFacts = 0;
  itemsPerPageFacts = 6;

  constructor() {}

  ngOnInit(): void {}

  getPaginatedResults() {
    const startIndex = this.currentPageFacts * this.itemsPerPageFacts;
    return this.factCheckResults.slice(startIndex, startIndex + this.itemsPerPageFacts);
  }

  nextPageFacts() {
    const totalPages = Math.ceil(this.factCheckResults.length / this.itemsPerPageFacts);
    if (this.currentPageFacts < totalPages - 1) {
      this.currentPageFacts++;
    }
  }

  previousPageFacts() {
    if (this.currentPageFacts > 0) {
      this.currentPageFacts--;
    }
  }

  getTotalFactPages(): number {
    return Math.ceil(this.factCheckResults.length / this.itemsPerPageFacts);
  }

  formatDate(dateString: string | null): string {
    if (!dateString) {
      return 'No date available';
    }
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return 'No date available';
    }
    date.setHours(date.getHours() - 2);
    return date.toISOString().split('T')[0] + ' ' + date.toTimeString().split(' ')[0];
  }
}
