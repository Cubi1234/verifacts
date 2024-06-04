import { Component } from '@angular/core';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { HeadlineService } from './headline.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  animations: [
    trigger('fadeIn', [
      state('void', style({
        opacity: 0,
      })),
      transition(':enter', [
        animate('0.5s ease-in')
      ])
    ])
  ]
})
export class AppComponent {
  title = 'Headline Predictor';
  headline = '';
  prediction: string | null = null;
  certainty: number | null = null;
  entries: any[] = [];

  constructor(private headlineService: HeadlineService) {}

  predictHeadline() {
    this.prediction = null; 
    this.certainty = null; 

    this.headlineService.getPrediction(this.headline).subscribe(response => {
      this.prediction = response.result;
      this.certainty = response.certainty;
    }, error => {
      console.error('Error:', error);
    });

    this.headlineService.getAllEntries().subscribe(entries => {
      this.entries = entries;
      console.log(this.entries[0][2])
    }, error => {
      console.error('Error retrieving entries:', error);
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    date.setHours(date.getHours() - 2);
    return date.toISOString().split('T')[0] + ' ' + date.toTimeString().split(' ')[0];
  }
}
