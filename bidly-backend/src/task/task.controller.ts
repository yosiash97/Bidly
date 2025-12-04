import { Controller, Get, Post, Body, Patch, Param, Delete, Query } from '@nestjs/common';
import { TaskService } from './task.service';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';
import { BidsService } from 'src/bids/bids.service';

@Controller('task')
export class TaskController {
  constructor(
    private readonly taskService: TaskService,
    private readonly bidService: BidsService
    ) {}
  @Get()
  findAll() {
    return this.taskService.executeGptScraper();
  }

  @Get('distance')
  async dummy(@Query('sliderValue') sliderValue: number) {
    console.log("Head to Delilah2")
    let records = await this.bidService.findAll();
    const homeDistance = `POINT 37.3387 121.8853`;
    let homeLat = 37.3387
    let homeLong = -121.8853

    let filtered_records = await this.bidService.findBidsWithinDistance(homeLat, homeLong, sliderValue)
    console.log("Filtered Records -> ", filtered_records)
    await new Promise(resolve => setTimeout(resolve, 2000));

    return filtered_records
  }
}
