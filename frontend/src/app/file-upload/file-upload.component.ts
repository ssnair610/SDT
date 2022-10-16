import { Component, OnInit } from '@angular/core';
import { forEach } from '@angular/router/src/utils/collection';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit {
  files1="No file chosen";
  files2;
  
  constructor(private http:HttpClient) { }

  ngOnInit() {
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
    
  }
}

onSubmit(){
  const formdata=new FormData();
  formdata.append('f',this.files2);
 
  this.http.post<any>("http://localhost:3000/file",formdata).subscribe(response=>{
    console.log(response);
  })
}

}
