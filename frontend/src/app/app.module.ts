import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { FileUploadComponent } from './file-upload/file-upload.component';

import { AngularFileUploaderModule } from 'angular-file-uploader';
import { HttpClientModule } from '@angular/common/http';
import { NavComponent } from './nav/nav.component';

import { MatToolbarModule } from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import { HashComponent } from './hash/hash.component';

import { RouteRoutingModule } from './route/route-routing.module';
import { HomeComponent } from './home/home.component';

import {MatButtonModule} from '@angular/material/button';
import { ReviewComponent } from './review/review.component';

import {MatGridListModule} from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatStepperModule } from '@angular/material/stepper';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import { FormsModule } from '@angular/forms';
@NgModule({
  declarations: [
    AppComponent,
    FileUploadComponent,
    NavComponent,
    HashComponent,
    HomeComponent,
    ReviewComponent
  ],
  imports: [
    BrowserModule,
    AngularFileUploaderModule,
    HttpClientModule,
    MatToolbarModule,
    MatIconModule,
    RouteRoutingModule,
    MatButtonModule,
    MatCardModule,
    MatGridListModule,
    MatStepperModule,
    BrowserAnimationsModule,
    FormsModule

    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
