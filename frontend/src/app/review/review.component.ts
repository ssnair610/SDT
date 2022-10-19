import { Component, OnDestroy, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from './../data.service';


@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit,OnDestroy {
  data;
  dataPassed:any;
 
  constructor(private http: HttpClient,private ds: DataService) {
 

}

  ngOnInit() {
    this.http.get('./server/uploads/w1.txt', { responseType: 'text' })
    .subscribe(data => {
      console.log(data);
      this.data=data;
    }); 

  this.ds.getData().subscribe(dataPassed => { 
    
    sessionStorage.setItem('name', dataPassed);
    
     
     
  });
  this.dataPassed=sessionStorage.getItem('name');
    console.log(this.dataPassed)
  
  //sessionStorage.clear();
  
  }

  ngOnDestroy(){
    //sessionStorage.clear();
  }

}
