import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { BidsModule } from './bids/bids.module';
import { ScheduleModule } from '@nestjs/schedule';
import { TaskModule } from './task/task.module';
@Module({
  imports: [BidsModule, ScheduleModule.forRoot(), TaskModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
