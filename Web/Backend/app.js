const express=require('express');
const axios=require('axios').default;
const cors=require('cors');

const app=express();

app.use(cors());

app.use(express.json({ limit: "10mb", extended: true }));
app.use(express.urlencoded({ extended: true }));

// Some formatting in the incoming b64 string and also look for type


//vars for temporary storing of response data of encrypt data from the api since db is not used
let encimg,kr,kc,iter_max;

const port=process.env.PORT || 8080;

app.get('/',(req,res)=>{
  res.send("hello");
})

app.post('/encrypt',async (req,res)=>{
  try{    
    const img=req.body.img.toString().slice(22,req.body.img.toString().length);
    const response=await axios.post('http://127.0.0.1:5000/encrypt',{img:img});
    res.send({
      status: 200,
      success: true,
      result: response.data,
      message:"Api is running fine1"
    });
  }catch(err){
    res.send({
      status: 400,
      success: false,
      message:err.message,
      result: null
    });
  }
})

app.post('/decrypt',async(req,res)=>{
  try{
    req.body.img=req.body.img.toString().slice(22,req.body.img.toString().length);
    req.body.kr = Array.from(req.body.kr.split(','),(n) => Number(n));
    req.body.kc = Array.from(req.body.kc.split(','),(n) => Number(n));
    req.body.iter_max=1
    const response=await axios.post('http://127.0.0.1:5000/decrypt',req.body);
    res.send({
      status: 200,
      success: true,
      result: response.data,
      message:"Api is running fine1"
    });
  }catch(err){
    console.log(err.message);
    res.send({
      status: 400,
      success: false,
      message:err.message,
      result: null
    });
  }
})

app.listen(port,(req,res)=>{
  console.log(`Server started @ ${port}`);
})