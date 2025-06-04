import 'dotenv/config';
import express from 'express';
import mongoose from 'mongoose';
import {router as apiRouter} from './routes/api.js';

(async()=>{
  await mongoose.connect(process.env.MONGO_URI!);
  console.log('MongoDB connected');

  const app=express();
  app.use(express.json());
  app.use('/v1',apiRouter);

  const port=process.env.PORT||4000;
  app.listen(port,()=>console.log(`API listening on :${port}`));
})();
