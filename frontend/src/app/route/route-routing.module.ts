import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { FileUploadComponent } from '../file-upload/file-upload.component';
import { HashComponent } from '../hash/hash.component';
import { HomeComponent } from '../home/home.component';
import { ReviewComponent } from '../review/review.component';

const routes: Routes = [
  {path:'home',component:HomeComponent},
  {path:'file',component:FileUploadComponent},
    {path:'hash',component:HashComponent},
    {path:'review',component:ReviewComponent},
   { path:'',redirectTo:'/home',pathMatch:"full"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class RouteRoutingModule { }
