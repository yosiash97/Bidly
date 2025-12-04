import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors({
    origin: [
      'https://bidly-front-end.vercel.app', 
      'https://bidly-front-end-dev.vercel.app',
      'http://localhost:3000' // Allow localhost:3000 for local development
    ],
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true, // Allow credentials (cookies, authorization headers, etc.)
  });

  const PORT = process.env.NODE_ENV === 'production'
  ? 3000
  : 3001;
  const HOST = '0.0.0.0';
  await app.listen(PORT, HOST);
}
bootstrap();
