import { Component, ElementRef, ViewChild, OnInit } from '@angular/core';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { HeadlineService } from './headline.service';
import { FactCheckService } from './fact-check.service';
import nlp from 'compromise';

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
        animate('0.5s ease-in', style({ opacity: 1 }))
      ])
    ]),
  ]
})
export class AppComponent implements OnInit {
  title = 'Headline Predictor';
  headline = '';
  prediction: string | null = null;
  certainty: number | null = null;
  entries: any[] = [];
  showVerifiedHeadlines = false;
  currentPage = 0;
  entriesPerPage = 9;
  currentPageFacts = 0;
  itemsPerPageFacts = 6;
  isSidebarOpen = false;

  selectedTab: string = 'verified';
  factCheckResults: any[] = [];

  @ViewChild('pageContentWrapper') pageContentWrapper!: ElementRef;

  selectTab(tab: string) {
    this.selectedTab = tab;
    setTimeout(() => {
      this.pageContentWrapper.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  @ViewChild('headlineHistory') headlineHistory!: ElementRef;

  constructor(private headlineService: HeadlineService, private factCheckService: FactCheckService) {}

  ngOnInit(): void {
    this.headlineService.getAllEntries().subscribe(entries => {
      this.entries = entries;
    }, error => {
      console.error('Error retrieving entries:', error);
    });
  }

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
  
  predictHeadline() {
    this.prediction = null;
    this.certainty = null;
    this.currentPage = 0;
    this.currentPageFacts = 0;
    this.factCheckResults = [];
    
    this.headlineService.getPrediction(this.headline).subscribe(response => {
      this.prediction = response.result;
      this.certainty = response.certainty;
      this.showVerifiedHeadlines = true;
      
      setTimeout(() => {
        this.scrollToHistory();
      }, 500);
    }, error => {
      console.error('Error:', error);
    });
    
    this.headlineService.getAllEntries().subscribe(entries => {
      this.entries = entries;
    }, error => {
      console.error('Error retrieving entries:', error);
    });
    
    const keywords = this.extractKeywords(this.headline);
    const firstThreeKeywords = keywords.slice(0, 3);
    const allFactCheckResults: any[] = [];
    
    firstThreeKeywords.forEach(keyword => {
      this.factCheckService.getFactCheck(keyword, 'en-US').subscribe(response => {
        const keywordFactCheckResults = response.claims || [];
        allFactCheckResults.push(...keywordFactCheckResults);
        
        this.shuffleArray(allFactCheckResults);
        
        this.handleFactCheckResponse(allFactCheckResults);
      }, error => {
        console.error(`Error fetching fact check results for keyword "${keyword}":`, error);
      });
    });
  }

  shuffleArray(array: any[]) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }
  
  handleFactCheckResponse(response: any) {
    this.factCheckResults = response;
  }
  
  extractKeywords(headline: string): string[] {
    const words = headline.split(' ');
    const stopwords = ['a', 'an', 'the', 'of', 'in', 'on', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
      'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'to'
    ];

    const doc = nlp(headline);
    const verbs = doc.verbs().out('array');
    console.log(verbs)
    const prepositions = doc.prepositions().out('array');

    // Add verbs and prepositions to stopwords
    stopwords.push(...verbs);
    stopwords.push(...prepositions);
    const keywords = words.filter(word => !stopwords.includes(word.toLowerCase()));

    const combinedKeywords = [...new Set(keywords)];
    return combinedKeywords;
  }

  scrollToHistory() {
    if (this.headlineHistory) {
      this.headlineHistory.nativeElement.scrollIntoView({ behavior: 'smooth' });
    }
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
