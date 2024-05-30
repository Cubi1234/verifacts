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
  isLoading = false;

  constructor(private headlineService: HeadlineService) {}

  predictHeadline() {
    this.isLoading = true;
    this.prediction = null; 

    this.headlineService.getPrediction(this.headline).subscribe(response => {
      setTimeout(() => {
        this.prediction = response.prediction;
        this.isLoading = false;
      }, 1000);
    }, error => {
      console.error('Error:', error);
      this.isLoading = false;
    });
  }
}