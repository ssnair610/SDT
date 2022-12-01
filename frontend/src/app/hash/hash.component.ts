import { Component, OnInit } from '@angular/core';
import { DataService } from './../data.service';

import { of } from 'rxjs';
import{delay} from 'rxjs/operators'

@Component({
  selector: 'app-hash',
  templateUrl: './hash.component.html',
  styleUrls: ['./hash.component.css']
})
export class HashComponent implements OnInit {
   endata;
   dedata;
   tddata;
   ovdata;

   
  constructor() { }

  ngOnInit() {
    // TODO: Get output textarea elements by id and subsume benchmark values
    const edata=of(1);
    edata.pipe(delay(2000)).subscribe(value=>{
      console.log(value);
      this.endata=value;
    })

    const ddata=of(2);
    ddata.pipe(delay(2000)).subscribe(value=>{
      console.log(value);
      this.dedata=value;
    })

    const tdata=of(3);
    tdata.pipe(delay(2000)).subscribe(value=>{
      console.log(value);
      this.tddata=value;
    })

    const odata=of(4);
    odata.pipe(delay(2000)).subscribe(value=>{
      console.log(value);
      this.ovdata=value;
    })
  }

  
}
  
