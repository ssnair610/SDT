import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import * as CryptoJS from 'crypto-js' // Public encryptions

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit {
  files1="No file chosen";
  files2;
  selectE1="";
  selectE2="";
  selectH="";
  text="";
  disable=true;
  disable2=true;
  s1=false;
  s2=false;
  data;


  // Find another library to fill the vacant ones up. [Vivek]
  // Generate Public-Private Key pairs. [Together]
  // Server side (all of this operation) [Ganith]

  encryptData = (data:string, algorithm:string) => {
    // Generate a Public-Private Key generation
    let key = "secret"
    switch (algorithm) {
      case "RSA":
        // TODO: python mli script to transform data to rsa-encrypted
        break;
      case "AES":
        CryptoJS.AES.encrypt(data, key)
        // TODO: python mli script to transform data to aes-encrypted
        break;
      case "DES":
        CryptoJS.DES.encrypt(data, key)
        // TODO: python mli script to transform data to des-encrypted
        break;
    
      case "ElGamal":
        // TODO: python mli script to transform data to elGamal-encrypted
        break;

      case "Rabin":
        // TODO: python mli script to transform data to rabin-encrypted
        break;
    
      default:
        break;
    }

    return data
  }

  hashData = (data:string, algorithm:string) => {
    switch (algorithm) {
      case "SHA-1":
        CryptoJS.SHA1(data)
        // TODO: python mli script to transform data to sha-1-hashed
        break;
    
      case "SHA-256":
        CryptoJS.SHA256(data)
        // TODO: python mli script to transform data to sha-1-hashed
        break;
    
      case "MD5":
        CryptoJS.MD5(data)
        // TODO: python mli script to transform data to sha-1-hashed
        break;
    
      case "SNEFRU":
        
        // TODO: python mli script to transform data to sha-1-hashed
        break;
    
      case "HAVAL":
        
        // TODO: python mli script to transform data to sha-1-hashed
        break;
    
      default:
        break;
    }
  }

  constructor(private http:HttpClient,private router: Router) { }

  ngOnInit() {
    
    if((this.selectE1=="" || this.selectE1=="Encryption Algorithm 1")||(this.selectH=="" || this.selectH=="Hashing Algorithm")){
      this.disable=true
    }
    else {
      this.encryptData(this.data, this.selectE1) //Encrypting based on first alg
      this.encryptData(this.data, this.selectE2) //Encrypting based on second alg
      this.hashData(this.data, this.selectH) //Hashing wrt alg

      this.disable=false
    }
  }


  afuConfig = {
    formatsAllowed: ".pdf,.jpg,.png",
    maxSize: "1",
    uploadAPI: {
      url:"http://localhost:3000/file"
    }
};

selectFile(event){
  if(event.target.files.length>0){
    const file = event.target.files[0];
    this.files1=file.name;
    this.files2=file;
    if(this.text!="" || this.files1!="No file chosen"){
      this.disable2=false
      this.s1=true
    }
    else{
      this.disable2=true
      this.s1=false
    }
    
  }
}

onSubmit(){
  if(this.files1!="No file chosen"){
  const formdata=new FormData();
  formdata.append('f',this.files2);
 
  this.http.post<any>("http://localhost:3000/file",formdata).subscribe(response=>{
    console.log(response);
  })
}
 // this.router.navigateByUrl('/hash');
}

onselect(){
  if((this.selectE1=="" || this.selectE1=="Encryption Algorithm 1")||(this.selectH=="" || this.selectH=="Hashing Algorithm")){
    this.disable=true
    this.s2=false

  }
  else{
    this.disable=false
    this.s2=true
  }
}

textarea(){
  if(this.text!="" || this.files1!="No file chosen"){
    this.disable2=false
    this.s1=true
  }
  else{
    this.disable2=true
    this.s1=false
  }
}

review(){
  if(this.files1!="No file chosen"){
  this.http.get('./server/uploads/w1.txt', { responseType: 'text' })
    .subscribe(data => {
      console.log(data);
      this.data=data;
    });
  }
  else if(this.text!=''){
    this.data=this.text;
  } 
}

}


