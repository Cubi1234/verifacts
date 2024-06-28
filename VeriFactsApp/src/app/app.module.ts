import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { VerifiedHeadlinesComponent } from './verified-headlines/verified-headlines.component';
import { RelatedSearchesComponent } from './related-searches/related-searches.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    VerifiedHeadlinesComponent,
    RelatedSearchesComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    HttpClientModule,
    FontAwesomeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
