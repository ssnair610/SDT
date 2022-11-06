import { Component, OnInit } from '@angular/core';
import { forEach } from '@angular/router/src/utils/collection';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit {
  files1="No file chosen";
  files2;
  selectE1="";
  selectH="";
  text="";
  disable=true;
  disable2=true;
  s1=false;
  s2=false;
  data;



  constructor(private http:HttpClient,private router: Router) { }

  ngOnInit() {
    

    if((this.selectE1=="" || this.selectE1=="Encryption Algorithm 1")||(this.selectH=="" || this.selectH=="Hashing Algorithm")){
      this.disable=true
    }
    else{
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


