import { Component, Input, OnInit } from '@angular/core';
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  selector: 'app-verified-headlines',
  templateUrl: './verified-headlines.component.html',
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
export class VerifiedHeadlinesComponent implements OnInit {
  @Input() entries: any[] = [];
  @Input() showVerifiedHeadlines = false;
  currentPage = 0;
  entriesPerPage = 9;

  constructor() {}

  ngOnInit(): void {}

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

  get paginatedEntries() {
    const startIndex = this.currentPage * this.entriesPerPage;
    return this.entries.slice(startIndex, startIndex + this.entriesPerPage);
  }

  nextPage() {
    if ((this.currentPage + 1) * this.entriesPerPage < this.entries.length) {
      this.currentPage++;
    }
  }

  previousPage() {
    if (this.currentPage > 0) {
      this.currentPage--;
    }
  }
}
