const express=require('express');
const bodyParser=require('body-parser');
const multer=require('multer');

const app=express();

const storage = multer.diskStorage({
    destination: (req,file,callBack)=>{
        callBack(null,"uploads")
    },
    filename: (req,file,callBack)=>{
        callBack(null,`${file.originalname}`)
    }
})

var upload = multer({storage:storage})

app.post('/file',upload.single('f'),(req,res,next)=>{
    const file=req.file;
    console.log(file.filename);
    res.send(file)
})

app.listen(3000,()=>{
    console.log("Server started on port 3000");
});

module.exports = app;