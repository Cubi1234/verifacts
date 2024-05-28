import { Component } from '@angular/core';
import { HeadlineService } from './headline.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Headline Predictor';
  headline = '';
  prediction = '';

  constructor(private headlineService: HeadlineService) {}

  predictHeadline() {
    this.headlineService.getPrediction(this.headline).subscribe(response => {
      this.prediction = response.prediction;
    }, error => {
      console.error('Error:', error);
    });
  }
}
