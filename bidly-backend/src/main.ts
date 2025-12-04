import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors({
    origin: true,
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
  });

  const PORT = process.env.PORT || 3001;
  const HOST = '0.0.0.0';
  await app.listen(PORT, HOST);
}
bootstrap();
