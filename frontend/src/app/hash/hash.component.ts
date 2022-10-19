import { Component, OnInit } from '@angular/core';
import { DataService } from './../data.service';



@Component({
  selector: 'app-hash',
  templateUrl: './hash.component.html',
  styleUrls: ['./hash.component.css']
})
export class HashComponent implements OnInit {
   hashing="Hashing Algorithm";
   crypto1="Encryption Algorithm 1";
   crypto2="Encryption Algorithm 2";
   h=false;
   c1=false;
   c2=false;
   arrow1=false;
   arrow2=false;
   arrow3=false;
   senddata=["ss","dd"]
  combine:string;

   
  constructor(private ds: DataService) { }

  ngOnInit() {
   
  }

  send1(){
  let list=[]
   

    if(this.crypto1!="Encryption Algorithm 1"){
      list.push(this.crypto1);
    }

    if(this.crypto2!="Encryption Algorithm 2"){
      list.push(this.crypto2);
    }

    if(this.hashing!="Hashing Algorithm"){
      list.push(this.hashing)
  }
    let combine;
    combine=list.join(",");
    this.ds.sendData(combine);
   
  
   
  }

 

  hash(x){
    if(x=='a'){
      this.hashing="SHA-1"
      this.h=false
    }
    else if(x=='b'){
      this.hashing="SHA-256"
      this.h=false
    }
    else if(x=='c'){
      this.hashing="MD5"
      this.h=false
    }
    else if(x=='d'){
      this.hashing="SNEFRU"
      this.h=false
    }
    else if(x=='e'){
      this.hashing="HAVAL"
      this.h=false
    }
  }

  onhash(){
    if(this.h==false){
    this.h=true
    }
    else{
      this.h=false
    }

    if(this.arrow1==false){
      this.arrow1=true
    }
    else{
      this.arrow1=false
    }
  }

  crypt1(x){
    if(x=='a'){
      this.crypto1="RSA"
    }
    else if(x=='b'){
      this.crypto1="DES"
    }
    else if(x=='c'){
      this.crypto1="AES"
    }
    else if(x=='d'){
      this.crypto1="ElGamal"
    }
    else if(x=='e'){
      this.crypto1="Rabin"

  }
  else if(x=='f'){
    this.crypto1="Elliptic Curve Cryptosystems"

}
  }

  oncrypto1(){
    if(this.c1==false){
    this.c1=true
    }
    else{
      this.c1=false
    }

    if(this.arrow2==false){
      this.arrow2=true
    }
    else{
      this.arrow2=false
    }
  }


  crypt2(x){
    if(x=='a'){
      this.crypto2="RSA"
    }
    else if(x=='b'){
      this.crypto2="DES"
    }
    else if(x=='c'){
      this.crypto2="AES"
    }
    else if(x=='d'){
      this.crypto2="ElGamal"
    }
    else if(x=='e'){
      this.crypto2="Rabin"

  }
  else if(x=='f'){
    this.crypto2="Elliptic Curve Cryptosystems"

}
  }


  oncrypto2(){
    if(this.c2==false){
    this.c2=true
    }
    else{
      this.c2=false
    }

    if(this.arrow3==false){
      this.arrow3=true
    }
    else{
      this.arrow3=false
    }
  }
}
  
